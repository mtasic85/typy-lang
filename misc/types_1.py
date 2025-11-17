import sys
from typing import TypeVar

class MagicDict(dict):
    def __missing__(self, key):
        # Check if the missing name looks like a generic type param (customize as needed)
        if len(key) == 1 and key.isupper():
            val = TypeVar(key)
            self[key] = val
            return val
        # For non-matching names, raise as usual to avoid masking real errors
        raise KeyError(key)

# Set up the magic globals early in the script
globals_dict = MagicDict(globals())
sys.modules[__name__].__dict__ = globals_dict

# C-like struct, compatible with C
class struct[*T]:
    def __init__(self, *args, **kwargs):
        self.T = T
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *_args, **_kwargs):
        return (self.T, self.args, self.kwargs, _args, _kwargs)

    @classmethod
    def __class_getitem__(cls, *types):
        # Note: *types may include TypeVars or concrete types
        return cls[*types]

# C-like struct, compatible with C
Point = struct()
Point2 = struct[T](x=T, y=T)
Point3 = struct[X, Y, Z](x=X, y=Y, z=Z)

# # C-like union, compatible with C
# union = struct
# AnyPoint = union[T](p1=T, p2=Point2, p3=Point3)

# # C-like enum, compatible with C
# type Color = enum[i32](
#     RED=auto(),
#     GREEN=auto(),
#     BLUE=auto(),
# )

# # functions are only allowed. functions within functions are also available.
# def point2_add[T](a: Point2[T], b: Point2[T]) -> Point2[T]:
#     res: Point2[T] = Point2[T](a.x + b.x, a.y + b.y)
#     return res


# p1 = Point2[f32](1, 2)
# p2 = Point2[f32](2, 3)
# p3 = point2_add(p1, p2)

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
