# TypeScript Rules
*Modern patterns and strict configurations*

**Trigger:** {ts_config}, {ts_ext}

## Strict Config [CRITICAL]

```json
{
  "strict": true,
  "noUncheckedIndexedAccess": true
}
```

## Modern Syntax (ES2024+)

- **satisfies**: Type validation without widening: `const x = {...} satisfies Config`
- **using**: Resource management: `using file = await openFile()`
- **Import attributes**: `import data from './data.json' with { type: 'json' }`

## Type Patterns

- **Branded types**: `type UserId = string & { __brand: 'UserId' }`
- **Type guards**: `function isUser(x: unknown): x is User`
- **Template literals**: `type Route = \`/api/${string}\``
- **const type params**: `function f<const T>(x: T)` for literal inference

## Runtime Validation

Use zod at API boundaries - never trust external data.
