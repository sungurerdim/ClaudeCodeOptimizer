# Lua Rules
*Stack-specific rules for Lua projects*

**Trigger:** {lua_manifest}, {lua_ext}

- **Local-Variables**: local by default, minimize globals
- **Module-Pattern**: Use module pattern for encapsulation
- **Table-Pool**: Reuse tables to reduce GC pressure
- **Metatables**: Use metatables for OOP patterns
- **Error-Handling-Lua**: pcall/xpcall for error handling
- **LuaJIT-Compat**: Write LuaJIT-compatible code when targeting it
