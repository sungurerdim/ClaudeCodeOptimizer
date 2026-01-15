# TypeScript Rules
*Stack-specific rules for TypeScript projects*

**Trigger:** {ts_config}, {ts_ext}

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
