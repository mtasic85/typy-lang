# Name of this programming language implementation is "pnc" and stands for Python is not C.
# This is subset of Python language that supports C semantics but is compatible with Python syntax/semantics as much as possible.
# Goal is to allow Python developers to write faster code, but not necessarily compiled native. In otherwords, as fast as possible interpreted language.
# This is fast dynamic language with types.
# Not every C code is semantically valld pnc code. Not every Python code is semantically valid pnc code. pnc is more strict and opinionated emphasing on performance, type safety, concurrency, and memory safety.
# Assume that all objects are allocated on heap. In order to improve perfromance, objects are dynamically allocated in the way so allocation, access, and freeing to them is perfromant.
#
# Supported statements/expressions: if, else, elif, while, for, return, break, continue, def, type, import, from/import/as, with/as, match/case, pass, yield.
#
# Unsupported statements/expressions: try, except, finally, raise, class, field from, async, await.
#
# Ternary if/else expression is supported.
#
# Functions are typed, but support `*args` and `**kwargs`.
# Lambda functions are not supported because they cannot be typed with current Python syntax.
#
# List, dict and set and their comprehension is supported.
# Tuples are supported.
# Generators are supported.
#
# Decorators are supported.
#
# Syntax of `match/case` is only supported for object destruction not value matching.
# Use `if/else/elif` for detailed check of object values and conditions.
#
# Error handling is supported using `Result[T, E]`, `Err[E]`, `Ok[T]` inspired by Rust language.
# Optional values are supported using `Option[T]`, None, `Some[T]` inspired by Rust language.

# C-like struct, compatible with C
Point2 = struct[T](x: T, y: T)
Point3 = struct[X, Y, Z](x: X, y: Y, z: Z)

# C-like union, compatible with C
Point = union[T](p1: T, p2: Point2, p3: Point3)

# C-like enum, compatible with C
Color = enum[i32](
    RED=auto(),
    GREEN=auto(),
    BLUE=auto(),
)


# functions are only allowed. functions within functions are also available.
def point2_add[T](a: Point2[T], b: Point2[T]) -> Point2[T]:
    res: Point2[T] = Point2[T](a.x + b.x, a.y + b.y)
    return res


p1 = Point2[f32](1, 2)
p2 = Point2[f32](2, 3)
p3 = point2_add(p1, p2)

point2_add = op.add(point2_add)
p4 = p1 + p2


# `op` is builtin and similar to `operator — Standard operators as functions` module in Python.
@op.add
def point_add[T](self: Point2[T], other: Point2[T]) -> Point2[T]:
    return point2_add(a, b)


p4 = p1 + p2

p1 = Point3[f32, f32, f32](0.0, 0.5, 1.0)

pu1 = Point[f64](p1=1.0)
pu2 = Point[f64](p2=Point2[f64](1.0, 1.0))
pu3 = Point[f64](p3=Point3[f32, f32, f32](0.0, 0.5, 1.0))

match pu1:
    case Point(p1):
        v = p1
    case Point2(x, _):
        print(x)
    case Point3(x, _, _):
        print(x)
    case _:
        pass

# generator/iterator example
def gen(b: int, e: int, s: int=1) -> Iterator[int]:
    i: int = b

    while i < e:
        yield i
        i += s

for i in gen(0, 10, 2):
    print(i)
