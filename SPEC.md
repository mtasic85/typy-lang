# typy

## Imports

Input:

```python
from typy.c import *

cflags('-Wall')
ldflags('-lm')

include('stdio.h')
include('stdint.h')

a: int8_t = 10
printf('%d\n', a)
```

Output:

```c
#include "stdio.h"
#include "stdint.h"

int __MODULE_PATH__main(int argc, char** argv) {
    int8_t a = 10;
    printf('%d\n', a);
    return 0;
}
```

## Integers 1

Input:

```python
a: int8_t = 10
b: int8_t = 20
c: int8_t = a + b
```

Output:

```c
int8_t a = 10;
int8_t b = 20;
int8_t c;
    int8_t __r0;
    bool __r1 = ckd_add(&__r0, a, b);
    assert(!__r1, "panic: OverflowError");
```

## Integers 2

Input:

```python
a: int8_t = 10
b: int8_t = 20
c: uint8_t = a + b # cast(a + b, uint8_t)
```

Output:

```c
int8_t a = 10;
int8_t b = 20;
uint8_t c;
    int8_t __r0;
    bool __r1 = ckd_add(&__r0, a, b);
    assert(!__r1, "panic: OverflowError");
    c = (uint8_t)(__r0);
```
