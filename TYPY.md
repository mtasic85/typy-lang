# typy

typy (aka typy-lang) is strongly-typed Python subset.

## typy doesn't have/support
- Default CPython builtins
- Default CPython modules/packages included
- `globals` and `locals`, so `global` and `nonlocal` statements are not supported
- `with` and `with ... as ...` statements
- `try`, `except`, `raise` statements
- `async` and `await` statements, so coroutines are not supported
- list/dict/set comprehension
- `yield` statement, so generators are not supported

## typy has/supports
- strongly typed (generic) functions
- strongly typed variables / constants
- strongly typed (generic) classes with explicit single inheritance

## Builtin types, functions, constants
- `NoneType` is type for instance of `None`. It is equivalent of `NULL` in C. Used for pointers and void returning functions.
- Boolean type `bool` (unsigned 8-bit integer, 1 byte, although it only requires 1 bit). It is equivalent of `_Bool` in C. Has to value `True` and `False`.
- Integer types:
  - Signed integers: `i8`, `i16`, `i32`, `i64` (equivalent of `intN_t` in C, where `N` is number of bits).
  - Unsigned integers: `u8`, `u16`, `u32`, `u64` (equivalent of `uintN_t` in C, where `N` is number of bits).
  - Size integers: `ssize_t` (equivalent for signed `ssize_t` in C), `size_t` (equivalent for unsigned `size_t` in C).
  - `ptrdiff_t` (equivalent of `ptrdiff_t` in C). `ptrdiff` is the signed integer type of the result of subtracting two pointers. It is used for pointer arithmetic and array indexing, if negative values are possible.
- Float types: `f32`, `f64` .
- Since numbers constants (integers, floats, etc) don't hold prefix/suffix what is their type, we need to explicitly declare type of variable like `a: i32 = 10` to represent for example signed 32-bit integer of value `10`, and this logic applies for all numerals. It is responsibility of compiler to infer type of values based on declared types of variables and function parameters.
- Byte type `byte` is single C-char encoded as unsigned 8-bit integer, for example: `b0: byte = b'H'`. Byte has always length 1. Byte value is immutable, but new value can be re-assigned to variable.

## Typed function / types
```python

```

## Generics functions / types
- Generic function is defined as:
```python
# `T` has to satisfy `Number` type
def add[T: Number](a: T, b: T) -> T:
    c: T = a + b
    return c

a0: u32 = add[u32](10, 20) # 30 value of u32 type
a1: f64 = add[f64](10.0, 20.0) # 30.0 value of f64 type
```
- Generic class is defined as:
```python
# Struct inheritance - extends data structure
class ColoredPoint[T]:
    x: T
    y: T
    color: str
```

## Single inheritance rules
- As implementation detail and choice, `struct`, `union`, `variant`, `enum` and `protocol` subclass universal supertype called `object`. `object` cannot be directly inherited. `object` cannot be instantiated.
- Multiple inheritance is not supported. Classes that don't inherit any base type default to `struct`.
- Classes can inherit from exactly one of the following base types:
  - `struct` - for data structures with related fields
  - `union` - for memory-efficient type storage
  - `variant` - for discriminated unions
  - `enum` - for type-safe enumerations
  - `protocol` - for interface contracts

Examples:
```python
# Struct inheritance - extends data structure
class ColoredPoint[T](struct):
    x: T
    y: T
    color: str

# Protocol inheritance - implements interface
# `T` has to satisfy both types `Number` and `Hash`
# Depending on implementation, `Number` can be either `variant` or `protocol` class. Same applies to `Hash`.
class HashablePoint[T: (Number, Hash)](struct):
    x: T
    y: T
    
    def __hash__(self) -> ssize:
        return hash(self.x) + hash(self.y)

# Enum inheritance - extends enumeration
# `_` has to satisfy type `UInt` (unsigned integer)
# all members have to satisfy `UInt` variant type
class ExtendedStatus[_: UInt](enum):
    OK = 0
    ERROR = 1
    WARNING = 2
    CRITICAL = 3
```

## Protocol usage in generic functions / types
Examples:
```python
# `Hash` protocol
class Hash(protocol):
    def __hash__(self) -> ssize:
        pass

# `_` is special indicator which is used to enforce that `SomeInt` has to satisfy `Hash` protocol
class SomeInt[T: Int, _: Hash]:
    v: T
    
    def __init__(self, v: T):
        self.v = v
    
    def __hash__(self) -> ssize:
        return self.v

# `Copy` protocol
class Copy(protocol):
    def __copy__(self) -> Self:
        pass

class One[T: Copy]:
    #  since `T` has to satisfy `Copy` type, `__copy__` method has to be implemented
    def __copy__(self) -> Self:
        return One[T]()

class Other[T: Copy]:
    #  since `T` has to satisfy `Copy` type, `__copy__` method has to be implemented
    def __copy__(self) -> Self:
        return Other[T]()

c: Copy
c = One()  # OK
c = Other()  # Also OK
```


## Variant usage in generic functions / types
Examples:
```python
class Int(variant):
    i8
    i16
    i32
    i64
    ssize_t
    ptrdiff_t

class UInt(variant):
    u8
    u16
    u32
    u64
    size_t

class Float(variant):
    f32
    f64

class Number(variant):
    Int
    UInt
    Float

# `T` has to satisfy variant type `Number`
def add[T: Number](a: T, b: T) -> T:
    c: T = a + b
    return c
```


## Bytes and strings
- Bytes type `bytes` which is C-like string. Null characters are allowed anywhere in `bytes`. Example: `data: bytes = b'Hello 123'`. Bytes value has any length, equal or greater from zero. Bytes value is immutable, but new value can be re-assigned to variable.
- String type `str` which is utf-8 encoded unicode. Only utf-8 encoding is supported. Null characters are allowed anywhere in `str`. Example: `text: str = 'Hello world'`. String value has any length, equal or greater from zero. String value is immutable, but new value can be re-assigned to variable.
- Bytes can be decoded to strings. Strings can be encoded to bytes.
