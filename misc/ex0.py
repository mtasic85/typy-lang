
#
# built-in types
#
class Ok[T]:
    v: T

class Err[E]:
    e: E

class Result[T, E](variant):
    """
    Result type cannot be directly instantiated because it inherits `variant`.

    Examples:
        r0: Result[i32, str] = Ok[i32](10)
        r1: Result[i32, str] = Ok[i32](20)
        r2: Result[i32, str] = r0 + r1 # internally checks if r0 and r1 are of type Ok or Err
        print(r2.unwrap())
    """
    v: Ok[T]
    e: Err[E]

class Some[T]:
    v: T

class Option[T](variant):
    """
    Option type cannot be directly instantiated because it inherits `variant`.

    Examples:
        r0: Option[i32] = Some[i32](10)
        r1: Option[i32] = Some[i32](20)
        r2: Option[i32] = r0 + r1 # internally checks if r0 and r1 are of type Some
        print(r2.unwrap())
    """
    n: NoneType
    v: Some[T]

#
# user-defined
#
class Pos1D:
    x: f64

class Pos2D[T](struct):
    x: T
    y: T

class LuaType[u64](enum):
    I32 = 0u64
    I64 = 1u64
    F32 = 2u64
    F64 = 3u64

class LuaValue(union):
    v_i32: i32
    v_i64: i64
    v_f32: f32
    v_f64: f64

class LuaObject:
    type: LueType
    value: LuaValue

class AnyPoint[X](variant):
    class Point1D:
        x: X

        def __add__(self: Self, o: Self) -> Self:
            r: Self = Point1D(self.x + o.x)
            return r

    class Point2D[Y]:
        x: X
        y: Y

        def __add__(self: Self, o: Self) -> Self:
            r: Self = Point2D[Y](self.x + o.x, self.y + o.y)
            return r

    class Point3D[Y, Z]:
        x: X
        y: Y
        z: Z

        def __add__(self: Self, o: Self) -> Self:
            r: Self = Point3D[Y, Z](self.x + o.x, self.y + o.y, self.z + o.z)
            return r
