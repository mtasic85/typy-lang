import sys
import types
from typing import TypeVar
from types import FrameType, TracebackType
from typing import Any


def auto_typevar_excepthook(
    exc_type: type[BaseException],
    exc_value: BaseException,
    traceback: TracebackType | None,
) -> None:
    if exc_type is not NameError:
        # Let other exceptions pass through normally
        sys.__excepthook__(exc_type, exc_value, traceback)
        return

    # Extract the NameError message: "name 'XYZ' is not defined"
    error_msg = str(exc_value)
    if not error_msg.startswith("name '") or not error_msg.endswith("' is not defined"):
        sys.__excepthook__(exc_type, exc_value, traceback)
        return

    missing_name = error_msg.split("'")[1]  # Extract XYZ

    # Get the frame where the error occurred
    if traceback is None:
        sys.__excepthook__(exc_type, exc_value, traceback)
        return
    frame = traceback.tb_frame
    lineno = traceback.tb_lineno

    # Create a new TypeVar with the exact missing name
    # We use exec to define it in the local namespace
    typevar_code = f"{missing_name} = TypeVar('{missing_name}')"

    try:
        exec(typevar_code, frame.f_globals, frame.f_locals)
        print(f"[AutoTypeVar] Created: {typevar_code}")

        # Now re-execute the failed line so execution continues
        # Use linecache to get the exact source line
        import linecache

        filename = frame.f_code.co_filename
        line = linecache.getline(filename, lineno).strip()

        # Re-execute the line (now that the variable exists)
        exec(line, frame.f_globals, frame.f_locals)

    except Exception as e:
        print(f"[AutoTypeVar] Failed to auto-create TypeVar: {e}")
        sys.__excepthook__(exc_type, exc_value, traceback)
        return

    # Suppress the exception - execution continues!
    return


# Install the hook
sys.excepthook = auto_typevar_excepthook


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
        class Specialized(cls):
            def __init__(self, *args, **kwargs):
                self.T = types
                self.args = args
                self.kwargs = kwargs

        return Specialized


Point = struct()
Point2 = struct[T](x=T, y=T)

print(Point)
print(Point2)
