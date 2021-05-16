from dataclasses import dataclass
from multiprocessing import Pipe, connection, Process
from threading import Thread
from typing import Union


@dataclass
class ParallelRunner:
    _recv_conn: connection.Connection = None
    _send_conn: connection.Connection = None
    _result: object = None
    _p: Union[Thread, Process] = None
    _method: str = 'multiprocessing'

    def __post_init__(self):
        self._recv_conn, self._send_conn = Pipe(duplex=False)

    def _executor(self, conn: connection.Connection, f, args):
        res = f(*args)
        conn.send(res)
        conn.close()

    def start(self, func, args):
        self._p = Process(target=self._executor, args=(self._send_conn, func, args))
        # self.p = Thread(target=self.executor, args=(self.send_conn, func, args))
        self._p.start()

    def _join(self):
        self._p.join()

    def get_result(self) -> object:
        if self._result is None:
            self._join()
            self._result = self._recv_conn.recv()
            self._recv_conn.close()
        return self._result


def gorun(func, *args) -> ParallelRunner:
    runner = ParallelRunner()
    runner.start(func, args)
    return runner
