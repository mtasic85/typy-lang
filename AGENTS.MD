# AGENTS.MD

## Project Context
Develop **typy-lang** compiler and light runtime which is strict, strongly-typed Python subset that compiles to native code.
Implemented in pure C only (C99/C11), no C++.
Once minimal typy compiler/runtime is implemented, rest of code can be implemented directly in typy for simplicity.
Multi-platform and multi-architecture.

## Build/Test Commands
- **Compile**: `clang -std=c11 -Wall -Wextra -Werror -g -fsanitize=address,undefined -o typy typy.c && ./typy`
- **Test**: Not implemented at the moment, but planned in pure typy.
- Ignore directories: `misc/`

## Code Style
- **Naming**: snake_case for functions/variables, SCREAMING_CASE for constants/types
- **Headers**: Include all headers used, prefer forward declarations
- **Error handling**: Use assert() for invariants, check all allocations/returns
- **Formatting**: 4-space tabs, 80-char line limit, no trailing whitespace
