from multiprocessing import Pipe, connection, Process
from threading import Thread
from typing import Callable
from typing import Union

from pydantic import constr
from pydantic.dataclasses import dataclass

from go_parallel.config import ParallelRunnerConfig


class IParallelRunner:
    def get_result(self) -> object:
        pass


@dataclass(config=ParallelRunnerConfig)
class _ParallelRunner(IParallelRunner):
    recv_conn: connection.Connection = None
    send_conn: connection.Connection = None
    result: object = None
    p: Union[Thread, Process] = None
    method: constr(regex=r"\b((multiprocessing|multithreading))\b") = "multiprocessing"

    def __post_init__(self):
        self.recv_conn, self.send_conn = Pipe(duplex=False)

    def _executor(self, conn: connection.Connection, f, args):
        res = f(*args)
        conn.send(res)
        conn.close()

    def start(self, func, args):
        self.p = Process(target=self._executor, args=(self.send_conn, func, args))
        # self.p = Thread(target=self.executor, args=(self.send_conn, func, args))
        self.p.start()

    def _join(self):
        self.p.join()

    def get_result(self) -> object:
        if self.result is None:
            self._join()
            self.result = self.recv_conn.recv()
            self.recv_conn.close()
        return self.result


def gorun(func: Callable, *args) -> _ParallelRunner:
    """
    Run the function 'func' asynchronously with the parameters '*args'.
    This function returns immediately.
    Example :

        runner = gorun(f, 5)
        result = runner.get_result()

    :param func: the function that needs to be executed asynchronously.
    :param args: arguments that need to be passed to `func`
    :return: Executes `func` asynchronously and returns an object of ParallelRunner.
    """
    runner: _ParallelRunner = _ParallelRunner(method="multiprocessing")
    runner.start(func, args)
    return runner
