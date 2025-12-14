#
# built-in types
#
class struct: pass # noqa
class union: pass # noqa
class variant: pass # noqa
class enum: pass # noqa
class protocol: pass # noqa

class i8: pass # noqa
class i16: pass # noqa
class i32: pass # noqa
class i64: pass # noqa
class u8: pass # noqa
class u16: pass # noqa
class u32: pass # noqa
class u64: pass # noqa
class ssize: pass # noqa
class usize: pass # noqa
class ptrdiff: pass # noqa
class f32: pass # noqa
class f64: pass # noqa


class Hashable(protocol):
    def __hash__(self) -> ssize: # type: ignore
        pass

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

        r0: Result[f64, str] = Err('Bad value')
        print(r0)
    """
    v: Ok[T]
    e: Err[E]

class NoneType: pass # noqa

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

        r0: Option[f64] = None
        print(r0)
    """
    n: NoneType
    v: Some[T]


#
# built-in functions
#
def hash[T: Hashable](o: T) -> ssize:
    """Generic hash function"""
    return o.__hash__()
