from dataclasses import dataclass
from multiprocessing import Pipe, connection, Process


@dataclass
class ParallelRunner:
    _recv_conn: connection.Connection = None
    _send_conn: connection.Connection = None
    _result: object = None
    method: str = 'multiprocessing'

    def __post_init__(self):
        self._recv_conn, self._send_conn = Pipe(duplex=False)

    def _executor(self, conn: connection.Connection, f, args):
        res = f(*args)
        conn.send(res)
        conn.close()

    def start(self, func, args):
        self.p = Process(target=self._executor, args=(self._send_conn, func, args))
        # self.p = Thread(target=self.executor, args=(self.send_conn, func, args))
        self.p.start()

    def _join(self):
        self.p.join()
        self._recv_conn.close()

    def get_result(self):
        if self._result is None:
            self._join()
            self._result = self._recv_conn.recv()
        return self._result


def gorun(func, *args) -> object:
    gparallel = ParallelRunner()
    gparallel.start(func, args)
    return gparallel
