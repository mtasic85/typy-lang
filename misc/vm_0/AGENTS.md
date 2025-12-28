# AGENTS.MD

## Project Context
Develop lightweight VMs for **typy-lang** - strict, strongly-typed Python subset. Pure C only (C99/C11), no C++.

## Build/Test Commands
- **Compile**: `clang -std=c11 -Wall -Wextra -Werror -g -fsanitize=address,undefined -o vm vm.c && ./vm`
- **Cross-check**: `gcc -std=c11 -Wall -Wextra -Werror -g -o vm vm.c && ./vm`
- **Single test**: Direct compile + run as above

## Code Style
- **Naming**: snake_case for functions/variables, SCREAMING_CASE for constants/types
- **Headers**: Include all headers used, prefer forward declarations
- **Error handling**: Use assert() for invariants, check all allocations/returns
- **Formatting**: 4-space tabs, 80-char line limit, no trailing whitespace