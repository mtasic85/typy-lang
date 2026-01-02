# typy-lang

Subset of strongly typed Python

## Code Style Guidelines

### Builtin Types
- `NoneType` is type for instance of `None`. It is equivalent of `NULL` in C. Used for pointers and void returning functions.
- For generic types, prefer single capital letters (`T`, `U`, `V`).
- Boolean type `bool` (unsigned 8-bit integer, 1 byte, although it only requires 1 bit). It is equivalent of `_Bool` in C. Has to value `True` and `False`.
- Integer types:
  - Signed integers: `i8`, `i16`, `i32`, `i64` (equivalent of `intN_t` in C, where `N` is number of bits).
  - Unsigned integers: `u8`, `u16`, `u32`, `u64` (equivalent of `uintN_t` in C, where `N` is number of bits).
  - Size integers: `ssize` (equivalent for signed `ssize_t` in C), `usize` (equivalent for unsigned `size_t` in C).
  - `ptrdiff` (equivalent of `ptrdiff_t` in C). `ptrdiff` is the signed integer type of the result of subtracting two pointers. It is used for pointer arithmetic and array indexing, if negative values are possible.
- Float types: `f32`, `f64` .
- Since numbers constants (integers, floats, etc) don't hold prefix/suffix what is their type, we need to explicitly encapsulate numbers like `a: i32 = i32(10)` to represent for example signed 32-bit integer of value `10`, and this logic applies for all numerals.
- Byte type `byte` is single C-char encoded as unsigned 8-bit integer, for example: `b0: byte = b'H'`. Byte has always length 1.
- Pointer type `Ptr[T]` is safe strongly typed generic type, for example: `ByteP: type = Ptr[byte]`.
- Pointer value of type `Ptr[T]` obtained using `ptr(o)` is pointer of an object, for example `v_p: ByteP = ptr(b'H')`.
- Bytes type `bytes` which is C-like string. Null characters are allowed anywhere in `bytes`. It is implemented as struct with `len: size_t` and `data: Ptr[byte]`.
- String type `str` which is utf-8 encoded unicode. Null characters are allowed anywhere in `str`. It is implemented as struct with `len: size_t` and `data: Ptr[byte]`.
- List type `list[T]` is strongly typed dynamic array. It is implemented as struct with `cap: size_t` (capacity), `len: size_t` (length), `items: Ptr[T]`.
- Dict type `dict[K, V]` is strongly typed dynamic dictionary/map. When dict is used, the key type `K` must implement the `HashProtocol` protocol, e.g., `dict[K: HashProtocol, V]`.

### Builtin Functions
- `malloc` from C stdlib. Usage: `ptr = malloc(size)` where size is a `size_t` and ptr is of type `Ptr[T]`.
- `realloc` from C stdlib. Usage: `ptr = realloc(ptr, new_size)` where ptr is of type `Ptr[T]` and new_size is a `size_t`.
- `free` from C stdlib. Usage: `free(ptr)` where ptr is of type `Ptr[T]`.

### Memory Management
- `ptr(o)` - gets pointer to object `o`, returns `Ptr[T]`
- `malloc[T](size)` - allocates memory on heap, returns `Ptr[T]`
- `realloc[T](ptr, new_size)` - resizes memory allocation
- `free(ptr)` - frees heap memory

Examples:
```python
# Stack pointer
p: Point = Point()
ptr_p: Ptr[Point] = ptr(p)

# Heap allocation with proper sizing
size: usize = 10 * sizeof(i32)
data: Ptr[i32] = malloc[i32](size)
# Use data...
free(data)  # Type-safe from variable

# Dynamic resizing example
capacity: usize = 8
data_size: usize = capacity * sizeof(f64)
data: Ptr[f64] = malloc[f64](data_size)
length: usize = 0

# Resize when needed
if length >= capacity:
    new_capacity: usize = capacity * 2
    new_size: usize = new_capacity * sizeof(f64)
    data = realloc[f64](data, new_size)
    capacity = new_capacity
```

### Classes/Types
- Classes (`class` statement) can be used to define custom types/classes.
- Class can inherit only following classes: `struct`, `union`, `variant`, `enum` and `protocol`.
- Class cannot use custom metaclass (aka type of class/type).
- Every class is of instance `type`.
- Class doesn't support multiple inheritance.
- If class doesn't inherit other classes it is assumed it inherits `struct`, aka struct type, aka product type.
- Struct (`struct`) is a data structure that groups related fields and methods together, allowing you to encapsulate data and functionality.
- Union (`union`) in typy like in C is a user-defined data type that allows you to store different data types in the same memory location, meaning only one member can hold a value at any given time. This makes unions memory-efficient, as they share the same memory space among their members.
- Variant (`variant`) is a discriminated union type, similar to std::variant in C++, enum in Rust, Variant in Mojo programming language. It can store exactly one value that can be any of the specified types, determined at runtime. Variant type itself cannot be directly instantiated. However, it can be used as a base class for other types, such as `Result[T, E]` and `Option[T]`, which are designed to be instantiated with their constituent types (`Ok[T]`/`Err[E]` and `Some[T]` respectively). Variant is more like declaration since it cannot be instantiated directly.
- Enum (`enum`) is a way to define a set of named values in the typy programming language, similar to enums in other languages. They are used to create type-safe enumerations which means that enums can have generic types like number types (signed/unsigned integers, floats). They work like enums in C/C++.
- Protocol (`protocol`) defines an interface or contract that types must implement. Protocols specify method signatures that implementing classes must provide. Protocols enable structural typing and can be used as constraints in generic types. For example, `dict[K: HashProtocol, V]` ensures that keys implement the `HashProtocol` protocol. Single class can satisfy multiple protocols at once. Protocol type `protocol` defines an interface that types must implement. Protocols specify methods that implementing classes must provide. For example: `class HashProtocol(protocol): def __hash__(self) -> ssize: pass`. Protocol methods definitions can be empty and use `pass` statement.
- As implementation detail and choice, `struct`, `union`, `variant`, `enum` and `protocol` subclass universal supertype called `object`. `object` cannot be directly inherited. `object` cannot be instantiated.

### Single Inheritance Rules
Classes can inherit from exactly one of the following base types:
- `struct` - for data structures with related fields  
- `union` - for memory-efficient type storage
- `variant` - for discriminated unions
- `enum` - for type-safe enumerations
- `protocol` - for interface contracts

Multiple inheritance is not supported. Classes that don't inherit any base type default to `struct`.

Examples:
```python
# Struct inheritance - extends data structure
class ColoredPoint[T](struct):
    x: T
    y: T
    color: str

# Protocol inheritance - implements interface
class HashablePoint[T](struct):
    x: T
    y: T
    
    def __hash__(self) -> ssize:
        return hash(self.x) + hash(self.y)

# Enum inheritance - extends enumeration
class ExtendedStatus(enum):
    OK = 0
    ERROR = 1
    WARNING = 2
    CRITICAL = 3
```

### Protocol Usage in Generic Types
Generic types can specify protocol constraints using the format `GenericType[T: Protocol]`. This ensures that type parameters implement required methods.

Examples:
- `dict[K: HashProtocol, V]` - ensures keys are hashable
- `list[T: SerializeProtocol]` - ensures items are serializable
- `HashProtocol` implementation:
  ```python
  class HashProtocol(protocol):
      def __hash__(self) -> ssize:
          pass
  
  class SomeInt[T: Integer]:
      v: T
      
      def __init__(self, v: T):
          self.v = v
      
      def __hash__(self) -> ssize:
          return self.v
  ```
- `CopyProtocol` implementation:
  ```python
  class CopyProtocol(protocol):
      def __copy__(self) -> Self:
          pass
  
  class One:
      def __copy__(self) -> One:
          pass
  
  class Other:
      def __copy__[T: Other](self: T) -> T:
          pass
  
  c: CopyProtocol
  c = One()  # OK
  c = Other()  # Also OK
  ```

### Naming Conventions
- Functions: `snake_case` (e.g., `point2_add`).
- Classes: `PascalCase` (e.g., `Point2`).
- Variables: `snake_case` (e.g., `result_value`).
- TypeVars: Single capital letters `T`, `U`, `V`, or capital letters with numbers `T1`, `T2`, `U1`, `U2`, `U3`.

### Error Handling
- Exception handling doesn't exits like in regular Python.
- Don't use try/except blocks, it is impossible to raise exceptions.
- Use explicit error handling.
- `Result[T, E]` is variant type holding values of types `Ok[T]` or `Err[E]`.
- `Option[T]` is variant type holding values of type `Some[T]` or `NoneType` (`None` value).
- `Result[T, E]` and `Option[T]` cannot be directly instantiated because it is subclass of `variant`.
- Use `Result[T, E]` (`Ok[T]` and `Err[E]`) and `Option[T]` (`NoneType` and `Some[T]`) patterns inspired by Rust.
- Functions that can return potential error should use `Result[T, E]` as return type. They return meaningful error instances of `Err[T]` type, or value of type `Ok[T]` in case of success.
- Functions that don't return errors, but might return optional values, should use `Option[T]` as return type.
- Use simple match/case statements to handle errors (simple pattern matching with simple value destruction/unpacking).

### Error Propagation

Functions can propagate `Result` errors up the call chain without modification.

### General
- Use proper type annotations for all function parameters and return values.
- Use proper type annotations for all variables.
- Classes and functions are the primary abstraction.
- Classes have all fields explicitly defined with their types and optional default values.
- Prefer functional programming patterns.

## Development

Ignore files from local `misc` and `backup` directories if they exist, unless otherwise specified.

### Checking Misc Examples

You cannot use `python` command to run `typy` programs because `typy` requires special compiler/interpreter to be developed which is goal here.

This only checks if syntax is correct:

```bash
python -B -m py_compile example.py
```

Keep code concise and focused on performance.
Assume that standard Python library (stdlib) and builtins don't exist.
Only `typy` (locally) defined functions, types and modules/packages exist.
Never update `README.md` file, except if otherwise specified. It is ground truth and official specification of `typy`.
