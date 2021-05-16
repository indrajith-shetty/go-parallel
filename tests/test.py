import time

from go_parallel import gorun

a = "sdfsdfsfsdfsdfsds"


def f(name):
    global a
    print(name)
    print(a)
    a = "empty f"
    return name + " is appended"


def sleeper(seconds):
    global a
    time.sleep(seconds)
    # print(a)
    a = "empty sleeper"

    return a


if __name__ == "__main__":
    runner = gorun(sleeper, 5)
    runner2 = gorun(f, "indra")
    print(runner2.get_result())
    print(runner.get_result())
