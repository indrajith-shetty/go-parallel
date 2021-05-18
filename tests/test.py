import time

from go_parallel.go_parallel import gorun, IParallelRunner


def f(name):
    print(name)
    return name + " is appended"


def sleeper(seconds):
    time.sleep(seconds)
    a = "empty sleeper"

    return a


if __name__ == "__main__":
    runner: IParallelRunner = gorun(sleeper, 5)
    runner2: IParallelRunner = gorun(f, "i")
    print(runner2.get_result())
    print(runner.get_result())
