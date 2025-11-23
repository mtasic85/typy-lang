import builtins
from typing import TypeVar

# Dynamically inject single capital letter TypeVars into builtins
for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    if not hasattr(builtins, letter):
        setattr(builtins, letter, TypeVar(letter))

# NOTE: goal is to produce single capital letter generic types (TypeVar) like:
#   T = TypeVar("T")

if __name__ == "__main__":
    # no T was defined, which means it had to be somehow dynamically returned from current module or __builtins__ module
    print(T)
