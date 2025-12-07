struct Pos1D:
    x: f64

struct Pos2D[T]:
    x: T
    y: T

enum LuaType[u64]:
    I32
    I64
    F32
    F64

union LuaValue:
    v_i32: i32
    v_i64: i64
    v_f32: f32
    v_f64: f64

struct LuaObject:
    type: LueType
    value: LuaValue

variant AnyPoint[X]:
    struct Point1D:
        x: X

        fn __add__(self: Self, o: Self) -> Self:
            r: Self = Point1D(self.x + o.x)
            return r

    struct Point2D[Y]:
        x: X
        y: Y

        fn __add__(self: Self, o: Self) -> Self:
            r: Self = Point2D[Y](self.x + o.x, self.y + o.y)
            return r

    struct Point3D[Y, Z]:
        x: X
        y: Y
        z: Z

        fn __add__(self: Self, o: Self) -> Self:
            r: Self = Point3D[Y, Z](self.x + o.x, self.y + o.y, self.z + o.z)
            return r
