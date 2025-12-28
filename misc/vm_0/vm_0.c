#include <math.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include <float.h>

enum tp_type_t;
union tp_value_t;
struct tp_object_t;
struct tp_array_t;
struct tp_map_entry_t;
struct tp_map_t;
struct tp_ctx_t;

typedef enum tp_type_t {
    TP_TYPE_NONE,
    TP_TYPE_BOOL,
    TP_TYPE_I32,
    TP_TYPE_I64,
    TP_TYPE_U32,
    TP_TYPE_U64,
    TP_TYPE_F32,
    TP_TYPE_F64,
    TP_TYPE_ARRAY,
    TP_TYPE_MAP
} tp_type_t;

typedef union tp_value_t {
    _Bool b;
    int32_t i32;
    int64_t i64;
    uint32_t u32;
    uint64_t u64;
    float_t f32;
    double_t f64;
    struct tp_array_t* array;
    struct tp_array_t* map;
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

typedef struct tp_map_entry_t {
    ssize_t hash;
    struct tp_object_t* key;
    struct tp_object_t* value;
} tp_map_entry_t;

/* Reference as inspiration: https://fengsp.github.io/blog/2017/3/python-dictionary/ */
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

    /* Array `entries` of `struct tp_object_t*` structures, the `tp_map_entry_t` contains the key object,
    the value object, and the key's hash, the key's hash is stored as a cache, for
    example, when we are searching for a key, we can use the cached hash to perform
    a fast comparison. */
    struct tp_object_t* entries;
} tp_map_t;

typedef struct tp_ctx_t {
    /* ctx object should also trace scopes somehow, so it can check it objects can be moved from outer scopes into new/current one.
    ctx should also check if object can be returned from current scope. */
    struct tp_object_t* defer_free_objects; // array, we need to register which objects should be freed when (function) scope ends
    struct tp_object_t* mark_return_objects; // array, we need to register which objects should be returned when (function) scope ends
    struct tp_object_t* mark_move_objects; // array, we need to register which objects should be moved from current (function) scope
} tp_ctx_t;

struct tp_object_t* custom_user_function_2(struct tp_ctx_t* ctx, tp_object_t* args, tp_object_t* kwagrs) {
    co_ctx_begin_scope(ctx); // start new scope, which will become current scope; checks if objects can be moved
    struct tp_object_t* res = tp_object_none_new(ctx);
    tp_object_mark_return(ctx, res);

cleanup:
    tp_ctx_free_defer_objects(ctx);
    co_ctx_end_scope(ctx); // end current scope; checks if objects can be returned
    return tp_object_return(res);
}

struct tp_object_t* custom_user_function(struct tp_ctx_t* ctx, tp_object_t* args, tp_object_t* kwagrs) {
    co_ctx_begin_scope(ctx); // start new scope, which will become current scope; checks if objects can be moved

    struct tp_object_t* a1 = tp_array_new(ctx, 8); // create array with len 0 and cap 8
    tp_object_defer_free(ctx, a1); // registered to be freed when scope ends, just before current function exists.

    struct tp_object_t* a2 = tp_array_new(ctx, 8); // create array with len 0 and cap 8
    tp_object_free(ctx, a2); // immediately free; check if a2 is not in `defer_free_objects`; check if a3 is not in

    struct tp_object_t* a3 = tp_array_new(ctx, 8); // create array with len 0 and cap 8
    tp_object_mark_return(ctx, a3); // a3 survives, escapes current (function) scope, since it is marked to be returned

    struct tp_object_t* a4 = tp_i32_new(ctx, 1);
    struct tp_object_t* a5 = tp_i32_new(ctx, 2);
    struct tp_object_t* args1 = tp_array_new(ctx, 8);
    tp_array_append(ctx, a4);
    tp_array_append(ctx, a5);
    struct tp_object_t* kwargs1 = tp_map_new(ctx, 8); // create map with "capacity" 8; actually `capacity == mask + 1`
    tp_object_mark_move(ctx, args1); // mark object to be moved to new scope; should not be used in current scope past this point
    tp_object_mark_move(ctx, kwargs1); // mark object to be moved to new scope; should not be used in current scope past this point
    struct tp_object_t* res1 = custom_user_function_2(ctx, args1, kwargs1);
    tp_object_defer_free(ctx, res1);

cleanup:
    tp_ctx_free_defer_objects(ctx);
    co_ctx_end_scope(ctx); // end current scope; checks if objects can be returned
    return tp_object_return(a3);
}

int main(int argc, char** argv) {
    printf("vm_0\n");
    struct tp_ctx_t* ctx = tp_ctx_new();
    tp_object_t* r = custom_user_function(ctx, NULL, NULL);
    tp_ctx_free(ctx);
    return 0;
}
