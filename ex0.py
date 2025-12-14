from typy import * # noqa

#
# user-defined
#
class Pos1D:
    x: f64

class Pos2D[T](struct):
    x: T
    y: T

class LuaType[u64](enum):
    I32 = u64(0)
    I64 = u64(1)
    F32 = u64(2)
    F64 = u64(3)

class LuaValue(union):
    v_i32: i32
    v_i64: i64
    v_f32: f32
    v_f64: f64

class LuaObject:
    type: LuaType
    value: LuaValue

# Define struct types separately for proper variant usage
class Point1D[T](struct):
    x: T

class Point2D[T, U](struct):
    x: T
    y: U

class Point3D[T, U, V](struct):
    x: T
    y: U
    z: V

# Proper variant usage
class AnyPoint[T](variant):
    point1d: Point1D[T]
    point2d: Point2D[T, T]
    point3d: Point3D[T, T, T]

#
# single inheritance examples
#
# Struct inheritance - extends data structure
class ColoredPoint[T](struct):
    x: T
    y: T
    color: str

# Enum inheritance - extends enumeration
class ExtendedStatus[i32](enum):
    OK = i32(0)
    ERROR = i32(1)
    WARNING = i32(2)
    CRITICAL = i32(3)

#
# protocol usage examples
#
class StringHashable:
    value: str

    def __hash__(self) -> ssize:
        return hash(self.value)

class IntHashable:
    value: i32

    def __hash__(self) -> ssize:
        return hash(self.value)

# Example usage with protocol constraint
string_dict: dict[StringHashable, str] = dict[StringHashable, str]()
int_dict: dict[IntHashable, i32] = dict[IntHashable, i32]()

#
# memory management examples
#
# Basic pointer examples
i: i32 = i32(42)
ptr_i: Ptr[i32] = ptr(i)

class Point:
    x: f64
    y: f64

p: Point = Point()
ptr_p: Ptr[Point] = ptr(p)

# Heap allocation with proper sizing
size: usize = usize(10) * sizeof(i32)
arr: Ptr[i32] = malloc[i32](size)

# Use allocated memory
i: u64

for i in range[u64](u64(10)):
    arr[i] = i * u64(2)

# Free memory - type-safe from ptr variable
free(arr)

# Dynamic resizing example
capacity: usize = usize(8)
data_size: usize = capacity * sizeof(f64)
data: Ptr[f64] = malloc[f64](data_size)
length: usize = usize(0)

# Resize when needed
if length >= capacity:
    new_capacity: usize = capacity * usize(2)
    new_size: usize = new_capacity * sizeof(f64)
    data = realloc[f64](data, new_size)
    capacity = new_capacity

#
# error propagation examples
#
class FileError:
    message: str

def read_file(path: str) -> Result[str, FileError]:
    if not file_exists(path):
        return Err[FileError](FileError("File not found"))

    content: str = file_read(path)
    return Ok[str](content)

def process_file(path: str) -> Result[str, FileError]:
    # Simple error propagation
    result: Result[str, FileError] = read_file(path)

    match result:
        case Ok(content):
            return Ok[str](content.upper())
        case Err(e):
            return Err[FileError](e)  # Propagate error

def validate_content(content: str) -> Result[str, FileError]:
    if len(content) == usize(0):
        return Err[FileError](FileError("Empty file"))

    return Ok[str](content)

def process_and_validate(path: str) -> Result[str, FileError]:
    # Chain operations with error propagation
    read_result: Result[str, FileError] = read_file(path)

    match read_result:
        case Ok(content):
            return validate_content(content)
        case Err(e):
            return Err[FileError](e)

#
# pattern matching enhancements
#
def divide(a: f64, b: f64) -> Result[f64, str]:
    if b == f64(0.0):
        return Err[str]("Division by zero")

    return Ok[f64](a / b)

def safe_divide(numbers: list[f64]) -> Result[f64, str]:
    if len(numbers) < usize(2):
        return Err[str]("Need at least 2 numbers")

    result: f64 = numbers[0]
    i: u64

    for i in range[u64](u64(1), len(numbers)):
        div_result: Result[f64, str] = divide(result, numbers[i])

        match div_result:
            case Ok(v):
                result = v
            case Err(e):
                return Err[str](e)

    return Ok[f64](result)

def find_item(items: list[i32], target: i32) -> Option[i32]:
    item: i32

    for item in items:
        if item == target:
            return Ok[i32](item)

    return Err[i32]("Item not found")

def process_items(items: list[i32]) -> list[i32]:
    result: list[i32] = list[i32]()
    item: i32

    for item in items:
        find_result: Option[i32] = find_item(items, item + i32(1))

        match find_result:
            case Ok(next_item):
                result.append(item + next_item)
            case Err(_):
                result.append(item)

    return result
