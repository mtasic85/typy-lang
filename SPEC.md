# SPEC.md

## Primitive Types

All primitive types from the C standard library are fully supported in typy-lang. This includes integer types (int8_t, int16_t, int32_t, int64_t, etc.), floating-point types (float, double, long double), and other C types (char, bool, size_t, pointers, etc.).

## Variable Declaration and Definition

### Syntax

```python
variable_name: type = value  # value is of type `type` and it's found at compile-time
```

### Examples

```python
a: int8_t = 10  # value is of type int8_t and it's found at compile-time
b: uint16_t = 11  # here value is of type uint16_t
c: float32_t = 3.14  # floating-point value
d: bool = True  # boolean value
```

## Function Definitions

Function definitions in TYPY follow strict typing rules. All parameters and return values must have explicit types declared.

### Syntax

```python
def function_name(param: type, param2: type) -> return_type:
    # function body
    return value
```

### Examples

```python
def mul_ints(x: int8_t, y: int8_t) -> int8_t:
    z: int8_t = x + y  # possible overflow works like in C
    return z

def add_floats(a: float32_t, b: float32_t) -> float32_t:
    c: float32_t = a + b
    return c

class Point(struct):
    x: int32_t
    y: int32_t

def process_point(p: Point) -> int32_t:
    return p.x + p.y
```

Similar functions are fully supported with the same syntax and semantics.

```python
def function_name(param: type, param2: type) -> return_type:
    # function body
    return value
```

### Examples

```python
def add_ints(x: int8_t, y: int8_t) -> int8_t:
    z: int8_t = x + y  # possible overflow works like in C
    return z
```

Similar functions are fully supported with the same syntax and semantics.

## Structs

Structs are defined using the `struct` base class. typy does not support multiple inheritance. Classes inherit from a single base class.

### Allocation Strategy

The allocation strategy for structs is determined by the return type of the `__new__` method:

- Returns `T` (the struct type itself) -> **Stack allocation** (default implementation)
- Returns `Ptr[T]` -> pointer or **Heap allocation** (manual implementation)

### Syntax

```python
class Point(struct):
    x: float32_t
    y: float32_t

    def add(self, other: Point) -> Point:
        result: Point = Point(0.0, 0.0)
        result.x = self.x + other.x
        result.y = self.y + other.y
        return result


p0: Point = Point(10.0, 20.0)
p1: Point = Point(20.0, 30.0)
p2: Point = p0.add(p1)
```

### Generic Functions

Generic functions follow a similar pattern:

```python
def mul_nums[U, V, Z](x: U, y: V) -> Z:
    z: Z = cast(x, Z) * cast(y, V)
    return z
```

### Generic Structs

Classes support generics, allowing structs to work with different types. The allocation strategy works the same way for generic structs:

```python
class Point[T](struct):
    x: T
    y: T

    def add(self, other: Point[T]) -> Point[T]:
        result: Point[T] = Point[T](0, 0)
        result.x = self.x + other.x
        result.y = self.y + other.y
        return result

# all three statements below are the same
p0: Point[int32_t] = Point[int32_t](10, 20)
p0: Point = Point[int32_t](10, 20)
p0 = Point[int32_t](10, 20)

# all three statements below are the same
p1: Point[float32_t] = Point[float32_t](10.0, 20.0)
p1: Point = Point[float32_t](10.0, 20.0)
p1 = Point[float32_t](10.0, 20.0)
```

### Heap-Allocated Generic Structs

For heap allocation, the same pattern applies:

```python
class Point1[T](struct):
    x: T
    y: T

    def __new__(cls, x: T, y: T) -> Ptr[Point1[T]]:
        self: Ptr[Point1[T]] = cast(malloc(sizeof(Point1[T])), Ptr[Point1[T]])
        self.x = x
        self.y = y
        return self
    
    def __del__(self):
        free(self)

p1: Ptr[Point1[int32_t]] = Point1[int32_t](10, 20)
del p1
```

## Pointer Types

Pointer types are defined as `Ptr[T]` where `T` is the pointed-to type.

### Stack vs Heap Allocation

**Stack Allocation (Default)**:
```python
p: Point = Point(10.0, 20.0)
# Returns Point (not a pointer)
# Stack-allocated
# Lifetime tied to current scope
# No manual free() needed
```

**Heap Allocation (Manual)**:
```python
p: Ptr[Point1] = Point1(10.0, 20.0)
# Requires custom __new__ that returns Ptr[Point1]
# Heap-allocated via malloc()
# Must manually free() when done; or `del p` which will trigger `Point1.__del__`
```

### Syntax

```python
a: int8_t = 10
p0: Ptr[int8_t] = ptr(a) # type-safe pointer, works like `int8_t * p0 = &a`
p1: Ptr[void] = ptr[void](a) # type-unsafe pointer, works like `void * p1 = (void*)(&a)`; this exists only for low-level programming. most users should not use this.
b: int8_t = p0[0] # safe dereference pointer
c: int8_t = cast(p1, Ptr[int8_t])[0] # unsafe pointer dereferencing 
```

### Pointer Operations

- `ptr(value)` - creates a type-safe pointer to the value
- `ptr[T](value)` - creates a type-unsafe pointer to the value
- `cast(value, target_type)` - casts a value to a target type, useful for unsafe pointer dereferencing
- pointer dereferencing is performed using `[0]` on pointer objects
- type-safe pointers are recommended for most use cases
- type-unsafe pointers (`Ptr[void]`) are provided for low-level programming and should be used with caution

### Memory Management

- **No garbage collection**: Users are responsible for manually freeing heap-allocated memory
- **Manual cleanup**: Use `free(pointer)` when done with heap-allocated structs
- **Stack lifetime**: Stack-allocated structs are automatically cleaned up when they go out of scope
- **No automatic destructors**: Since there's no garbage collection, explicit cleanup is required for heap-allocated resources

### Memory Management

- **No garbage collection**: Users are responsible for manually freeing heap-allocated memory
- **Manual cleanup**: Use `free(pointer)` when done with heap-allocated structs
- **Stack lifetime**: Stack-allocated structs are automatically cleaned up when they go out of scope
- **No automatic destructors**: Since there's no garbage collection, explicit cleanup is required for heap-allocated resources
