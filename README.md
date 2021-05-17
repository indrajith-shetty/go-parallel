# go-parallel
Utility function for running functions asynchronously.

Install:

* pip install go-parallel

Usage:
```python

import time
from go_parallel.go_parallel import gorun


def f(name):
    time.sleep(5)
    return name + " has changed"

if __name__ == "__main__":
    runner1 = gorun(f, "indra")
    runner2 = gorun(f, "test")

    print(runner1.get_result())

```
