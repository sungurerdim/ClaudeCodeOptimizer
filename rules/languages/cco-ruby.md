# Ruby Rules
*Stack-specific rules for Ruby projects*

**Trigger:** {ruby_manifest}, {ruby_ext}

- **Freeze-Strings**: Use frozen_string_literal pragma
- **Block-Yield**: Prefer yield over block.call
- **Method-Visibility**: Explicit private/protected declarations
- **Type-Check**: Static type checking (Sorbet or RBS) for public APIs
- **Pattern-Match**: Use pattern matching for complex conditionals
- **Ractor-Thread-Safe**: Use Ractor for thread-safe parallelism
- **Data-Class**: Use Data.define for immutable value objects
