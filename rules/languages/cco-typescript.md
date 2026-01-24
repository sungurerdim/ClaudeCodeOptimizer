# TypeScript Rules
*Stack-specific rules for TypeScript/JavaScript projects*

**Trigger:** {ts_config}, {ts_ext}, {js_manifest}, {js_ext}

## JavaScript Patterns

- **JSDoc-Types**: Type hints via JSDoc for public APIs (when not using TypeScript)
- **ES-Modules**: ESM over CommonJS (import/export)
- **Const-Default**: const > let > never var
- **Async-Handling**: Proper Promise handling, always catch rejections
- **Array-Methods**: Prefer map/filter/reduce over manual loops
- **Optional-Chain**: Use ?. and ?? for safe property access
- **Destructuring**: Destructure objects/arrays for clarity
- **Top-Level-Await**: Use top-level await in modules
- **Private-Fields**: Use # for private class fields
- **Modern-Array**: Use Array.at(), Object.hasOwn(), Array.findLast()

## Type Safety

- **Strict-Mode**: Enable `strict: true` in tsconfig.json
- **Null-Safety**: Enable strict null checks in tsconfig.json
- **Index-Access**: Enable `noUncheckedIndexedAccess` for array/object safety
- **No-Any**: Use `unknown` instead of `any` for truly unknown types
- **Explicit-Return**: Add return types on public functions
- **Null-Check**: Always check for null/undefined before accessing properties
- **Utility-Types**: Use `Partial<T>`, `Pick<T>`, `Omit<T>`, `Required<T>` for type transformations
- **Discriminated-Unions**: Use discriminated unions with a `type` or `kind` field for state management

## Modern Syntax

- **Satisfies-Operator**: Use `satisfies` for type validation without widening: `const x = {...} satisfies Config`
- **Const-Type-Params**: Use `const` type parameters for literal inference: `function f<const T>(x: T)`
- **Using-Keyword**: Use `using` for resource management: `using file = await openFile()`
- **Import-Attributes**: Use import attributes: `import data from './data.json' with { type: 'json' }`

## Type Patterns

- **Branded-Types**: Use branded types for validated primitives: `type UserId = string & { __brand: 'UserId' }`
- **Type-Guards**: Use type predicates for narrowing: `function isUser(x: unknown): x is User`
- **Infer-Keyword**: Use `infer` in conditional types: `type ElementOf<T> = T extends (infer E)[] ? E : never`
- **Template-Literal-Types**: Use template literal types: `type Route = \`/api/${string}\``

## Runtime Validation

- **Zod-Schemas**: Use zod for runtime validation at API boundaries
- **Validate-External**: Always validate data from external sources (API responses, user input)
