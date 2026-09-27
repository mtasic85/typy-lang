# TYPY

## Overview

`typy` (also known as `typy-lang`) is a strongly typed Python subset starting from C semantics and Python syntax.

## Core Concepts

- **Strongly Typed**: All values have explicit types
- **C Semantics**: Runtime behavior based on C-like semantics
- **Python Syntax**: Familiar Python syntax
- **Fresh Builtins**: New independent built-in functions, types and capabilities
- **std Module**: Core module with C primitives (int types, float definitions, etc.)
- **ffi Module**: Foreign Function Interface for interacting with C libraries

## Language Specification

### Type System

- All values have explicit types
- Type checking is enforced at compile-time and runtime
- Type inference is supported where applicable

### Syntax

- Subset of Python syntax with restrictions
- Clear separation between syntax and semantics

### Semantics

- C-like runtime semantics
- Behavior defined through C standards where applicable
- Memory management follows C-like patterns

## Builtins

New built-in functions and types specific to `typy`.

## Standard Library

### std Module

The `std` module provides C primitives, similar to libc (`muslc`, `glibc`):

- **Primitive Types**: `int` types (`int8_t`, `uint16_t`, `int32_t`, `uint64_t`, etc.)
- **Floating-point Types**: `float` definitions (`float`, `double`, `long double`)
- **Other C Types**: `char`, `bool`, `size_t`, pointers, etc.
- **C Standard Library**: Standard C functions and utilities
- **Memory Management**: `malloc` and `free` for manual heap allocation and deallocation
- **Type Operations**: `sizeof` for getting the size of types and structs

### ffi Module

The `ffi` module provides Foreign Function Interface capabilities (based on `libffi`).

**Note**: This is not a priority focus at this stage.

- **C Library Interaction**: Call functions from external C libraries
- **Memory Management**: Allocate and manage C memory
- **Data Types**: Convert between typy types and C types
- **Pointer Operations**: Work with C pointers and references

## Development

This specification is defined incrementally as the language evolves.
New features, restrictions, and semantics will be added as the implementation progresses.

## Notes

- Everything is being defined from scratch
- Starting point: C semantics + Python syntax

For detailed language specifications, see [SPEC.md](./SPEC.md).
