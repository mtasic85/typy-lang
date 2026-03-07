# TYPY

## Overview

TYPY (also known as typy-lang) is a strongly typed Python subset starting from C semantics and Python syntax.

## Core Concepts

- **Strongly Typed**: All values have explicit types
- **C Semantics**: Runtime behavior based on C-like semantics
- **Python Syntax**: Familiar Python-like syntax
- **Fresh Builtins**: New built-in functions and capabilities
- **std Module**: Core module with C primitives (int types, float definitions, etc.)
- **ffi Module**: Foreign Function Interface for interacting with C libraries

## Language Specification

### Type System

- All values have explicit types
- Type checking is enforced at compile-time and runtime
- Type inference is supported where applicable

### Syntax

- Python-like syntax with restrictions
- New syntax constructs as defined
- Clear separation between syntax and semantics

### Semantics

- C-like runtime semantics
- Behavior defined through C standards where applicable
- Memory management follows C-like patterns

## Builtins

New built-in functions and types specific to TYPY.

## Standard Library

### std Module

The `std` module provides C primitives, similar to libc (muslc, glibc):

- **Primitive Types**: int types (int8_t, int16_t, int32_t, int64_t, etc.)
- **Floating-point Types**: float definitions (float, double, long double)
- **Other C Types**: char, bool, size_t, pointers, etc.
- **C Standard Library**: Standard C functions and utilities

### ffi Module

The `ffi` module provides Foreign Function Interface capabilities:

- **C Library Interaction**: Call functions from external C libraries
- **Memory Management**: Allocate and manage C memory
- **Data Types**: Convert between TYPY types and C types
- **Pointer Operations**: Work with C pointers and references

## Development

This specification is defined incrementally as the language evolves. New features, restrictions, and semantics will be added as the implementation progresses.

## Notes

- No assumptions made about the language at this stage
- Everything is being defined from scratch
- Starting point: C semantics + Python syntax
