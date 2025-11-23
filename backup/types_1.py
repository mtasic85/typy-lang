from typing import TypeVar

T = TypeVar("T")
X = TypeVar("X")
Y = TypeVar("Y")
Z = TypeVar("Z")


class struct:
    def __init__(self, *T):
        self.T = T

    def __call__(self, **kwargs):
        attrs = {}

        def __init__(self, *args):
            if len(args) != len(kwargs):
                raise TypeError(f"Expected {len(kwargs)} arguments, got {len(args)}")
            for i, name in enumerate(kwargs):
                setattr(self, name, args[i])

        attrs["__init__"] = __init__
        attrs["__annotations__"] = kwargs
        if self.T:

            def __class_getitem__(cls, item):
                typ = item
                new_annotations = {
                    k: typ if v == self.T[0] else v
                    for k, v in cls.__annotations__.items()
                }
                return type(
                    cls.__name__,
                    (),
                    {
                        "__init__": attrs["__init__"],
                        "__annotations__": new_annotations,
                    },
                )

            attrs["__class_getitem__"] = __class_getitem__
        cls = type("Struct", (), attrs)
        return cls

    @classmethod
    def __class_getitem__(cls, *types):
        return cls(*types)


f32 = float
i32 = int

# # Predefine common TypeVars
# T = TypeVar("T")
# X = TypeVar("X")
# Y = TypeVar("Y")
# Z = TypeVar("Z")


# # C-like struct, compatible with C
# class struct[*T]:
#     def __init__(self, *args, **kwargs):
#         self.T = T
#         self.args = args
#         self.kwargs = kwargs

#     def __call__(self, *_args, **_kwargs):
#         return (self.T, self.args, self.kwargs, _args, _kwargs)

#     @classmethod
#     def __class_getitem__(cls, *types):
#         # Note: *types may include TypeVars or concrete types
#         class Specialized(cls):
#             def __init__(self, *args, **kwargs):
#                 self.T = types
#                 self.args = args
#                 self.kwargs = kwargs

#         return Specialized


# # C-like struct, compatible with C
# Point = struct()
Point2 = struct[T](x=T, y=T)
# Point3 = struct[X, Y, Z](x=X, y=Y, z=Z)

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

if __name__ == "__main__":
    p1 = Point2[f32](1.0, 2.0)
    p2 = Point2[f32](2.0, 3.0)
    print(f"p1: x={p1.x}, y={p1.y}")
    print(f"p2: x={p2.x}, y={p2.y}")
