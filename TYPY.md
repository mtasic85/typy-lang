# typy

typy (aka typy-lang) is strongly typed Python subset.

typy is implemented in C99/C11.
typy is interpreted language which require compiler and virtual machine.
Virtual machine is register based.
Direct threading is a technique used in typy to improve the efficiency of instruction dispatch in virtual machine.
typy doesn't implement JIT, but doesn't limit future versions to implement it, or to implement Ahead of Time compiler directly to native code for a given platform/architecutre.
typy compiler produces bytecode from source code.
Bytecode can be file by file, or it can be combined bytecode for all compiled typy source files.
Once bootstrapped, typy is used to implement its own builtins/stdlib.
To consider complete bootstrapped version of typy, it means that all low-level (primitive number types), memory management functions, and generics are already implemented.
typy does not use GC, but has well structured/defined set of rules how automatic memory management is handled.


## typy doesn't have/support
- Default CPython builtins
- Default CPython modules/packages included
- `globals` and `locals`, so `global` and `nonlocal` statements are not supported
- `with` and `with ... as ...` statements
- `try`, `except`, `except*`, `raise`, `finally` statements
- `async` and `await` statements, so coroutines are not supported
- list/dict/set comprehension
- generator expression, what looks like a "tuple comprehension", which creates a generator object that produces items lazily
- `yield` statement, so generators are not supported
- an assignment expression operator called walrus operator `:=`


## typy has/supports
- strongly typed (generic) functions
- strongly typed variables / constants
- strongly typed (generic) classes with explicit single inheritance
- static modules inspired by fixed static typed members; similar to how C-based python modules are implemented
- `if`, `elif`, `else` statements
- ternary `if` / `else` expressions
- `while`, `else` statements
- `for`, `else` statements; only for types that satisfy `Iterator` type
- `match` / `case` statements
- `import`, `import ... as ...`, `from ... import ...`, `from ... import ... as ...` statements
- multiple object return in form of statically typed `tuple`
- variable number of arguments `*args` and keyword arguments `**kwargs`; `*args` and `**kwargs` are statically typed


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


## Classes/Types
- Classes (`class` statement) can be used to define custom types/classes.
- Class support only single inheritance.
- Class can inherit only following classes: `struct`, `union`, `variant`, `enum` and `protocol`.
- Class cannot use custom metaclass (aka type of class/type).
- Every class is of instance `type`.
- Class doesn't support multiple inheritance.
- As implementation detail and choice, `struct`, `union`, `variant`, `enum` and `protocol` subclass universal supertype called `object`. `object` cannot be directly inherited. `object` cannot be instantiated.
- If class doesn't inherit other classes it is assumed it inherits `struct`, aka struct type, aka product type.
- Multiple inheritance is not supported.
- Classes can inherit from exactly one of the following base types:
  - `struct` - for data structures with related fields; C-like
  - `union` - for memory-efficient type storage; C-like
  - `variant` - for discriminated unions; Inspired by Mojo programming language
  - `enum` - for type-safe enumerations; C23-like explicitly specified underlying integer type
  - `protocol` - for interface contracts; defines an interface or contract that types must implement


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

# or
class HashablePoint[T: Number, _: Hash](struct):
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


## Naming Conventions
- Functions: `snake_case` (e.g., `point2_add`).
- Classes: `PascalCase` (e.g., `Point2`).
- Variables: `snake_case` (e.g., `result_value`).
- TypeVars: Single capital letters `T`, `U`, `V`, or capital letters with numbers `T1`, `T2`, `U1`, `U2`, `U3`.  Special case is `_` (eg `_: Hash`) used mostly for protocols.


## Pointers
- Pointer type `Ptr[T]` is safe strongly typed generic type, for example: `ByteP: type = Ptr[byte]`.
- Pointer value of type `Ptr[T]` obtained using `ptr(o)` is pointer of an object, for example `v_p: ByteP = ptr(b'H')`.


## Memory Management
- `ptr[T: type=object](o: T) -> Ptr[T]` - gets pointer to object `o`, returns `Ptr[T]`
-  pointer dereferencing is done taking 0-th index value from pointer object `ptr[0]`, example `o1: i32 = 10; p1: Ptr[i32] = ptr(o1); o1 = p1[0]`
- `malloc[T](size_t) -> Ptr[T]` - allocates memory on heap, returns `Ptr[T]`
- `calloc[T](num: size_t, size: size_t) -> Ptr[T]` - allocates memory for an array of num objects of size and initializes all bytes in the allocated storage to zero
- `realloc[T](ptr: Ptr[T], new_size: size_t) -> Ptr[T]` - resizes memory allocation
- `free[T](ptr: Ptr[T])` - frees heap memory


## bytes, str, list, tuple, dict, set
Core principles how they are implemented:
```python

class bytes:
    # bytes `data` are raw `byte` (`u8`) values 
    len: size_t
    data: Ptr[byte]

class str:
    # str data is encoded in UTF-8
    data_len: size_t # raw length of `data`; `str.__len__` is called to get utf-8 string length
    data: Ptr[byte]

class list[T]:
    len: size_t
    cap: size_t
    items: Ptr[T] # C-array of type `T`

class tuple[T]:
    len: size_t
    items: Ptr[T] # C-array of type `T`

class _dict_entry[K: Hash, V]:
    hash: ssize_t
    key: K
    value: V

class dict[K: Hash, V]:
    # Number of active and dummy entries. If you delete a key, the entry will become
    # a dummy entry and fill remains the same, if you add a new key and the new
    # key doesn't occupy a dummy entry, this is increased by 1
    fill: size_t
    # Number of active entries. If you add a new key, it is increased by 1, if you
    # delete a key, it is decreased by 1.
    used: size_t
    # Bitmask of the hash table, the table contains `mask + 1` slots. We store the
    # mask instead of the size because when we are looking up the entry for a key,
    # `slot = key_hash & mask` is used to get the slot index. "capacity" of dict is `mask + 1`
    mask: size_t
    # Array `entries` contains the key object,
    # the value object, and the key's hash, the key's hash is stored as a cache, for
    # example, when we are searching for a key, we can use the cached hash to perform
    # a fast comparison.
    entries: Ptr[_dict_entry[K, V]] # C-array of type struct `_dict_entry`

class _set_entry[V: Hash]:
    hash: ssize_t
    key: V

class set[V: Hash]:
    # Number of active and dummy entries. If you delete a key, the entry will become
    # a dummy entry and fill remains the same, if you add a new key and the new
    # key doesn't occupy a dummy entry, this is increased by 1
    fill: size_t
    # Number of active entries. If you add a new key, it is increased by 1, if you
    # delete a key, it is decreased by 1.
    used: size_t
    # Bitmask of the hash table, the table contains `mask + 1` slots. We store the
    # mask instead of the size because when we are looking up the entry for a key,
    # `slot = key_hash & mask` is used to get the slot index. "capacity" of dict is `mask + 1`
    mask: size_t
    # Array `entries` contains
    # the value object, and the key's hash, the key's hash is stored as a cache, for
    # example, when we are searching for a key, we can use the cached hash to perform
    # a fast comparison.
    entries: Ptr[_set_entry[V]] # C-array of type struct `_set_entry`
```
Each type has almost the same methods like Python, just strongly typed.


## Error Handling
- Exception handling doesn't exits like in regular Python.
- Don't use `try`, `except`, `except*`, `raise`, `finally` statements, it is impossible to raise exceptions.
- Use explicit error handling.
- `Result[T, E]` is variant type holding values of types `Ok[T]` or `Err[E]`.
- `Option[T]` is variant type holding values of type `Some[T]` or `NoneType` (`None` value).
- `Result[T, E]` and `Option[T]` cannot be directly instantiated because it is subclass of `variant`.
- Use `Result[T, E]` (`Ok[T]` and `Err[E]`) and `Option[T]` (`NoneType` and `Some[T]`) patterns inspired by Rust.
- Functions that can return potential error should use `Result[T, E]` as return type. They return meaningful error instances of `Err[T]` type, or value of type `Ok[T]` in case of success.
- Functions that don't return errors, but might return optional values, should use `Option[T]` as return type.
- Use simple match/case statements to handle errors (simple pattern matching with simple value destruction/unpacking).


## Error Propagation

Functions can propagate `Result` errors up the call chain without modification.

## Automatic memory management (AMM)

typy doesn't have and doesn't use GC. Instead, typy has semantically structured memory management.

Examples:
```python
x: i32 = 10
y: i32 = 20

def f(x: i32, y: i32) -> i32:
    z: i32 = x + y
    return z

z: i32 = f(x, y) # x, y are moved inside of f1; f1 is responsible for their lifetime
# w: i32 = x + y # panics because x, y are moved to f1
```

```python
x: i32 = 10
y: i32 = 20

def f(x: i32, y: i32) -> (i32, i32):
    x += 1 # local x got new value
    y += 1 # local x got new value
    return x, y # returns new objects/values

x, y = f(x, y) # it is ok because x, y get reassigned, but kept their type
```

```python
x: i32 = 10
y: i32 = 20

def f(x: i32, y: i32) -> (i32, i32):
    return x, y

x1: i32
y1: i32
x1, y1 = f2(x, y)
```

```python
x: i32 = 10
y: i32 = 20
z: i32 = 30

def f(x: i32, y: i32) -> (i32, i32):
    return x, y

x, y = f(x, y)
```
