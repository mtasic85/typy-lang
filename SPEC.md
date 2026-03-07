# SPEC.md

## Primitive Types

All primitive types from the C standard library are fully supported in typy-lang.

## Variable Declaration and Definition

### Syntax

```python
variable_name: type = value # value is of type `type` and it's found at compile-time
```

### Examples

```python
a: int8_t = 10 # value is of type int8_t and it's found at compile-time
b: uint16_t = 11 # here value is of type uint16_t
```

## Function Definitions

### Syntax

```python
def function_name(param: type, param2: type) -> return_type:
    # function body
    return value
```

### Examples

```python
def mul_nums(x: int8_t, y: int8_t) -> int8_t:
    z: int8_t = x + y # possible overflow works like in C
    return z
```

Similar functions are fully supported with the same syntax and semantics.

## Pointer Types

Pointer types are defined as `Ptr[T]` where `T` is the pointed-to type.

### Syntax

```python
a: int8_t = 10
p0: Ptr[int8_t] = ptr(a) # type-safe pointer, works like `int8_t * p0 = &a`
p1: Ptr[void] = ptr[void](a) # type unsafe pointer, works like `void * p1 = (void*)(&a)` . this exists only for low-level programming. most of users should not use this.
b: int8_t = p0[0] # safe dereference pointer
c: int8_t = cast(p1, int8_t)[0] # unsafe pointer dereferencing 
```

### Pointer Operations

- `ptr(value)` - Creates a type-safe pointer to the value
- `ptr[T](value)` - Creates a type-unsafe pointer to the value
- `cast(value, target_type)` - Casts a value to a target type, useful for unsafe pointer dereferencing
- Pointer dereferencing is performed using `[0]` on pointer objects
- Type-safe pointers are recommended for most use cases
- Type-unsafe pointers (`Ptr[void]`) are provided for low-level programming and should be used with caution
