# typy-lang

Subset of strongly typed Python

## Code Style Guidelines

### Builtin Types
- `NoneType` is type for instance of `None`. It is equivalent of `NULL` in C. Used for pointers and void returning functions.
- For generic types, prefer single capital letters (`T`, `U`, `V`).
- Use proper type annotations for all function parameters and return values.
- Use proper type annotations for all variables.
- Boolean type `bool` (unsigned 8-bit integer, 1 byte, although it only requires 1 bit).
- Integer types: i8, i16, i32, i64, u8, u16, u32, u64, ssize_t, size_t .
- Float types: f32, f64 .
- Byte type `byte` is single C-char encoded as unsigned 8-bit integer, for example: `b0: byte = b'H'`. Byte has always length 1.
- Pointer type `Ptr[T]` is safe strongly typed generic type, for example: `ByteP: type = Ptr[byte]`.
- Pointer value of type `Ptr[T]` obtained using `ptr(o)` is pointer of an object, for example `v_p: ByteP = ptr(b'H')`.
- Bytes type `bytes` which is C-like string. Null characters are allowed anywhere in `bytes`. It is implemented as struct with `len: size_t` and `data: Ptr[byte]`.
- String type `str` which is utf-8 encoded unicode. Null characters are allowed anywhere in `str`. It is implemented as struct with `len: size_t` and `data: Ptr[byte]`.
- List type `list[T]` is strongly typed dynamic array. It is implemented as struct with `cap: size_t` (capacity), `len: size_t` (length), `items: Ptr[T]`.
- Dict type `dict[K, V]` is strongly typed dynamic dictionary/map. When dict is used, the key type `K` must implement the `Hashable` protocol, e.g., `dict[K: Hashable, V]`.
- Protocol type `protocol` defines an interface that types must implement. Protocols specify methods that implementing classes must provide. For example: `class Hashable(protocol): def __hash__(self) -> ssize_t: ...`

### Builtin Functions
- `malloc` from C stdlib. Usage: `ptr = malloc(size)` where size is a `size_t` and ptr is of type `Ptr[T]`.
- `realloc` from C stdlib. Usage: `ptr = realloc(ptr, new_size)` where ptr is of type `Ptr[T]` and new_size is a `size_t`.
- `free` from C stdlib. Usage: `free(ptr)` where ptr is of type `Ptr[T]`.

### Protocol Usage in Generic Types
Generic types can specify protocol constraints using the format `GenericType[T: Protocol]`. This ensures that type parameters implement required methods.

Examples:
- `dict[K: Hashable, V]` - ensures keys are hashable
- `list[T: Serializable]` - ensures items are serializable

### Naming Conventions
- Functions: `snake_case` (e.g., `point2_add`).
- Classes: `PascalCase` (e.g., `Point2`).
- Variables: `snake_case` (e.g., `result_value`).
- TypeVars: Single capital letters `T`, `U`, `V`, or capital letters with numbers `T1`, `T2`, `U1`, `U2`, `U3`.

### Error Handling
- Exception handling doesn't exits like in regular Python.
- Don't use try/except blocks, it is impossible to raise exceptions.
- Use explicit error handling.
- Use `Result[T, E]` (`Ok[T]` and `Err[E]`) and `Option[T]` (`NoneType` and `Some[T]`) patterns inspired by Rust.
- `Result[T, E]` can be instantiated with `Ok[T]` or `Err[E]` values, not directly with the `Result` type itself.
- `Option[T]` can be instantiated with `Some[T]` or `NoneType` values, not directly with the `Option` type itself.
- Return meaningful error instances of `Err[T]` type.
- Use simple match/case statements to handle errors (simple pattern matching with simple value destruction/unpacking).

### General
- Classes can be used only for user-defined types/classes.
- Class cannot use metaclass.
- User-defined class doesn't support multiple inheritance.
- User-defined class should inherit only following classes: `struct`, `union`, `variant` and `enum`.
- If user-defined class doesn't inherit other classes it is assumed it inherits `struct`, aka struct type.
- Struct (`struct`) is a data structure that groups related fields and methods together, allowing you to encapsulate data and functionality.
- Union (`union`) in typy like in C is a user-defined data type that allows you to store different data types in the same memory location, meaning only one member can hold a value at any given time. This makes unions memory-efficient, as they share the same memory space among their members.
- Variant (`variant`) is a discriminated union type, similar to std::variant in C++ or enum in Rust. It can store exactly one value that can be any of the specified types, determined at runtime. Variant type itself cannot be directly instantiated. However, it can be used as a base class for other types, such as `Result[T, E]` and `Option[T]`, which are designed to be instantiated with their constituent types (`Ok[T]`/`Err[E]` and `Some[T]` respectively).
- Enum (`enum`) is a way to define a set of named values in the typy programming language, similar to enums in other languages. They are used to create type-safe enumerations which means that enums can have generic types like number types (signed/unsigned integers, floats).
- Protocol (`protocol`) defines an interface or contract that types must implement. Protocols specify method signatures that implementing classes must provide. Protocols enable structural typing and can be used as constraints in generic types. For example, `dict[K: Hashable, V]` ensures that keys implement the `Hashable` protocol.
- Classes have all fields explicitly defined with their types and optional default values.
- Classes and functions are the primary abstraction.
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
