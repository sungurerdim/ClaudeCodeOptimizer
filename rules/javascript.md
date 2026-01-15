# JavaScript Rules
*Stack-specific rules for JavaScript projects*

**Trigger:** {js_manifest}, {js_ext}

- **JSDoc-Types**: Type hints via JSDoc for public APIs
- **ES-Modules**: ESM over CommonJS (import/export)
- **Const-Default**: const > let > never var
- **Async-Handling**: Proper Promise handling, always catch rejections
- **Array-Methods**: Prefer map/filter/reduce over manual loops
- **Optional-Chain**: Use ?. and ?? for safe property access
- **Destructuring**: Destructure objects/arrays for clarity
- **Top-Level-Await**: Use top-level await in modules
- **Private-Fields**: Use # for private class fields
- **Modern-Array**: Use Array.at(), Object.hasOwn(), Array.findLast()
