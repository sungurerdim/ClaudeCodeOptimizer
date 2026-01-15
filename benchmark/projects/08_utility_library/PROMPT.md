# Project: Data Validation Library

Build a composable data validation library for TypeScript.

---

## Autonomous Operation

**Execute this task completely without user interaction:**

1. **Proceed autonomously** - Make reasonable decisions without asking
2. **Implement all requirements** - Complete every validator type listed below
3. **Write working code** - All validators must function correctly
4. **Include tests** - 90%+ test coverage required
5. **Handle errors gracefully** - Clear, actionable error messages
6. **No slash commands** - Do NOT use `/help`, `/commit`, or any `/` commands (not available in this execution mode)

**Prioritized execution order:**
1. Project structure and base validator class
2. Primitive validators (string, number, boolean)
3. Complex validators (object, array, record)
4. Type inference system
5. Custom validators and transforms
6. Union, enum, literal types
7. Tests for all validators

---

## Requirements

### Core Features

1. **Schema Definition**
   ```typescript
   const userSchema = v.object({
     name: v.string().min(1).max(100),
     email: v.string().email(),
     age: v.number().int().min(0).max(150).optional(),
     role: v.enum(['admin', 'user', 'guest']),
     tags: v.array(v.string()).min(1).max(10),
     metadata: v.record(v.string(), v.unknown())
   });
   ```

2. **Validator Types**
   - string: min, max, length, pattern, email, url, uuid, trim, lowercase
   - number: min, max, int, positive, negative, multipleOf
   - boolean
   - date: min, max, past, future
   - array: min, max, length, unique, contains
   - object: strict (no extra keys), passthrough, partial, pick, omit
   - enum: fixed values
   - union: multiple types (first match)
   - literal: exact value
   - record: key-value pairs
   - tuple: fixed length array with types per position
   - nullable, optional, default

3. **Validation Output**
   ```typescript
   type ValidationResult<T> =
     | { success: true; data: T }
     | { success: false; errors: ValidationError[] };

   interface ValidationError {
     path: (string | number)[];
     message: string;
     code: string;
     expected?: string;
     received?: string;
   }
   ```

4. **Type Inference**
   ```typescript
   const schema = v.object({ name: v.string() });
   type User = v.infer<typeof schema>; // { name: string }
   ```

5. **Custom Validators**
   ```typescript
   const positiveEven = v.number().refine(
     n => n > 0 && n % 2 === 0,
     'Must be positive and even'
   );
   ```

6. **Transforms**
   ```typescript
   const trimmed = v.string().transform(s => s.trim());
   const parsed = v.string().transform(s => parseInt(s, 10)).pipe(v.number());
   ```

### Technical Requirements

- Zero runtime dependencies
- Tree-shakeable exports
- Full TypeScript type inference
- Works in browser and Node.js
- Comprehensive error messages
- ESM and CJS builds
- 90%+ test coverage
- Size < 5KB gzipped

### Project Structure

```
validatr/
├── src/
│   ├── index.ts          # Public API
│   ├── types.ts          # Core types
│   ├── validators/
│   │   ├── string.ts
│   │   ├── number.ts
│   │   ├── boolean.ts
│   │   ├── date.ts
│   │   ├── array.ts
│   │   ├── object.ts
│   │   ├── union.ts
│   │   └── ...
│   ├── utils/
│   │   ├── errors.ts
│   │   └── helpers.ts
│   └── core/
│       ├── base.ts       # Base validator class
│       └── context.ts    # Validation context
├── tests/
│   ├── string.test.ts
│   ├── number.test.ts
│   └── ...
├── package.json
└── tsconfig.json
```

---

## Success Criteria

| Priority | Requirement | Validation |
|----------|-------------|------------|
| P0 | All validator types implemented | Each type works correctly |
| P0 | Full type inference working | v.infer returns correct type |
| P1 | Custom validators work | .refine() functions correctly |
| P1 | Transforms work and types flow | .transform().pipe() works |
| P2 | All tests pass | npm test succeeds |
| P2 | Bundle size under 5KB gzipped | Check with bundlephobia |
| P2 | No 'any' types in implementation | TypeScript strict mode |

**Deliverables:** Working validation library, full TypeScript types, test suite, ESM/CJS builds.
