# typy-lang

typy-lang (aka typy) is strongly-typed Python subset.
typy doesn't have any standard Python modules/packages included.
typy doesn't have builtins.
typy doesn't have `globals` and `locals`, so `global` and `nonlocal` statements are not supported.
typy doesn't have `with` and `with ... as ...` statements.
typy doesn't have `try`, `except`, `raise` statements.

## VM specification

VM is register-based. There are infinite number of registers available.

Objects in VM are defined like:
```c
typedef enum tp_type_t {
    TP_TYPE_NONE,
    TP_TYPE_BOOL,
    TP_TYPE_I8,
    TP_TYPE_I16,
    TP_TYPE_I32,
    TP_TYPE_I64,
    TP_TYPE_U8,
    TP_TYPE_U16,
    TP_TYPE_U32,
    TP_TYPE_U64,
    TP_TYPE_F32,
    TP_TYPE_F64,
    TP_TYPE_SIZE,
    TP_TYPE_SSIZE,
    TP_TYPE_,
    TP_TYPE_ARRAY,
    TP_TYPE_MAP,
    TP_TYPE_CODE,
    TP_TYPE_FUNC,
    TP_TYPE_MODULE
} tp_type_t;

typedef union tp_value_t {
    _Bool b;
    int8_t i8;
    int16_t i16;
    int32_t i32;
    int64_t i64;
    uint8_t u8;
    uint16_t u16;
    uint32_t u32;
    uint64_t u64;
    float_t f32;
    double_t f64;
    struct tp_array_t* array;
    struct tp_map_t* map;
    struct tp_code_t* code;
    struct tp_func_t* func;
    struct tp_module_t* module;
} tp_value_t;

typedef struct tp_object_t {
    enum tp_type_t t;
    union tp_value_t v;
} tp_object_t;

typedef struct tp_array_t {
    size_t len;
    size_t cap;
    struct tp_object_t* items;
} tp_array_t;

/* Reference as inspiration: https://fengsp.github.io/blog/2017/3/python-dictionary/ */
typedef struct tp_map_entry_t {
    ssize_t hash;
    struct tp_object_t* key;
    struct tp_object_t* value;
} tp_map_entry_t;

typedef struct tp_map_t {
    /* Number of active and dummy entries. If you delete a key, the entry will become
    a dummy entry and ma_fill remains the same, if you add a new key and the new
    key doesn't occupy a dummy entry, this is increased by 1. */
    ssize_t fill;  /* # Active + # Dummy */

    /* Number of active entries. If you add a new key, it is increased by 1, if you
    delete a key, it is decreased by 1. */
    ssize_t used;  /* # Active */

    /* Bitmask of the hash table, the table contains `mask + 1` slots. We store the
    mask instead of the size because when we are looking up the entry for a key,
    `slot = key_hash & mask` is used to get the slot index. "capacity" of dict is `mask + 1` */
    ssize_t mask;

    /* Array `entries` of `struct tp_map_entry_t*` structures, the `tp_map_entry_t` contains the key object,
    the value object, and the key's hash, the key's hash is stored as a cache, for
    example, when we are searching for a key, we can use the cached hash to perform
    a fast comparison. */
    struct tp_map_entry_t* entries;
} tp_map_t;

typedef struct tp_code_t {
    // ...
} tp_code_t;

typedef struct tp_func_t {
    // ...
} tp_func_t;

typedef struct tp_module_t {
    // ...
} tp_module_t;
```

## VM, Scope, Object Lifetime

Context keeps VM state. One context per VM.
Context on module level (zeroth level), always has default scope. Consider this like module-level global scope.
Scope is either on module level, and new one created on every function call. Consider function scope as current local scope.

Context keeps track of:
  - object deferred to be freed; deferred objects to be freed are freed in reverse order, last added gets first freed, and so on until all are freed in current scope.
  - objects marked to me moved from current scope to new scope
  - objects marked to be returned from current scope to previous scope

Every time function is called, new context scope is created.
Every time just before functions returns result, current scope is left.
When function is called all passed objects are automatically marked as moved to new scope.
When function returns object is marked to be returned.
During function call, all objects created are ("defer free") freed if not marked moved or returned. 


```c
typedef struct tp_ctx_t {
    // array of deferred objects to be freed
    // array of objects marked to be moved to new ctx scope
} tp_ctx_t;

struct tp_ctx_t* ctx = tp_ctx_new();
tp_ctx_free(ctx);
```

## Object lifetime

Each object is created with something like:
```c
struct tp_object_t* a1 = tp_array_new(ctx, 8); // create array with len 0 and cap 8
// automatically it is registered to 
```
