# go-parallel

Utility function for running functions asynchronously.

Install:

* `pip install go-parallel`

Usage:

```python

import time
from go_parallel.go_parallel import gorun, IParallelRunner


def f(name):
    time.sleep(5)
    return name + " has changed"


if __name__ == "__main__":
    runner1: IParallelRunner = gorun(f, "in")  # runs function `f` asynchronously. Returns immediately.
    runner2: IParallelRunner = gorun(f, "test")

    result = runner1.get_result()  # waits until the function call `f("in")` returns. 
    print(result)

```
