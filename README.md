# lepy
lepy

## Checking Misc Examples

This only checks if syntax is correct.

```bash
python -B -m py_compile misc/types_4.py
```

## Code Style Guidelines

### Types
- Use TypeVar for generic types, prefer single capital letters (`T`, `U`, `V`)
- Define TypeVars at module level with descriptive names
- Use proper type annotations for all function parameters and return values

### Naming Conventions
- Functions: `snake_case` (e.g., `point2_add`)
- Classes: `PascalCase` (e.g., `Point2`)
- Variables: `snake_case` (e.g., `result_value`)
- TypeVars: Single capital letters `T`, `U`, `V`, or capital letters with numbers `T1`, `T2`, `U1`, `U2`, `U3`.

### Error Handling
- Use Result[T, E] and Option[T] patterns inspired by Rust
- Avoid try/except blocks; prefer explicit error handling
- Return meaningful error types instead of raising exceptions

### General
- No classes allowed (language restriction)
- Functions are the primary abstraction
- Use struct syntax for data structures
- Prefer functional programming patterns
- Keep code concise and focused on performance
