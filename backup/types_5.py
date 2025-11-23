import builtins
from typing import TypeVar


# # Dynamically inject single capital letter TypeVars into builtins
# for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
#     if not hasattr(builtins, letter):
#         setattr(builtins, letter, TypeVar(letter))


# i8 = int
# i16 = int
# i32 = int
# i64 = int
# u8 = int
# u16 = int
# u32 = int
# u64 = int
# f16 = float
# f32 = float
# f64 = float


# # C-like struct, compatible with C
# class _generic_type[*T]:
#     def __init__(self, types, *args, **kwargs):
#         self.types = types
#         self.args = args
#         self.kwargs = kwargs

#     def __call__(self, *_args, **_kwargs):
#         return _generic_type(self.types, *_args, **_kwargs)

#     def __getattr__(self, attr: str) -> Any:
#         return self.kwargs[attr]

#     def __setattr__(self, attr: str, value: Any):
#         self.kwargs[attr] = value

#     @classmethod
#     def __class_getitem__(cls, *types):
#         return _generic_type(types)

# class struct[*T]:
#     def __init__(self, *args, **kwargs):
#         self.struct = _generic_type(T)

#     def __call__(self, *_args, **_kwargs):
#         return self.struct(*_args, **_kwargs)

#     @classmethod
#     def __class_getitem__(cls, *types):
#         return _generic_type(types)




# C-like struct, compatible with C
Point = struct()
Point2 = struct[T](x=T, y=T)
Point3 = struct[X, Y, Z](x=X, y=Y, z=Z)

p1 = Point2[f32](1.0, 2.0)
p2 = Point2[f32](2.0, 3.0)
print(f"p1: x={p1.x}, y={p1.y}")
print(f"p2: x={p2.x}, y={p2.y}")


# C-like union, compatible with C
AnyPoint = union[T](p1=T, p2=Point2, p3=Point3)


# C-like enum, compatible with C
type Color = enum[i32](
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

#
#
#
with union[T] as AnyPoint:
    with struct as Point:
        pass

    with struct[T] as Point2:
        x: T
        y: T

        def __add__[T](a: Point2[T], b: Point2[T]) -> Point2[T]:
            res: Point2[T] = Point2[T](a.x + b.x, a.y + b.y)
            return res

    with struct[X, Y, Z] as Point3:
        x: X
        y: Y
        z: Z

        def __add__[X, Y, Z](a: Point3[X, Y, Z], b: Point3[X, Y, Z]) -> Point3[X, Y, Z]:
            res: Point3[X, Y, Z] = Point3[X, Y, Z](a.x + b.x, a.y + b.y, a.z + b.z)
            return res





# # op.add
# point2_add = op.add(point2_add)
# p4 = p1 + p2

# # `op` is builtin and similar to `operator — Standard operators as functions` module in Python.
# @op.add
# def point_add[T](self: Point2[T], other: Point2[T]) -> Point2[T]:
#     return point2_add(a, b)


# p4 = p1 + p2

# #
# # 1
# #
# Point2 = struct[T](x: T, y: T)

# def point2_add[T](a: Point2[T], b: Point2[T]) -> Point2[T]:
#     res: Point2[T] = Point2[T](a.x + b.x, a.y + b.y)
#     return res

# def point2_sub[T](a: Point2[T], b: Point2[T]) -> Point2[T]:
#     res: Point2[T] = Point2[T](a.x - b.x, a.y - b.y)
#     return res

# #
# # 2
# #
# with struct() as Point2Trait:
#     def __add__[T](a: Point2[T], b: Point2[T]) -> Point2[T]:
#         res: Point2[T] = Point2[T](a.x + b.x, a.y + b.y)
#         return res

#     def __sub__[T](a: Point2[T], b: Point2[T]) -> Point2[T]:
#         res: Point2[T] = Point2[T](a.x - b.x, a.y - b.y)
#         return res

#     add = __add__
#     sub = __sub__


# with struct[T] as Point2:
#     x: T
#     y: T
