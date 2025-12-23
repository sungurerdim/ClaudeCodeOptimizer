# Project: Data Validation Library

Build a composable data validation library for TypeScript.

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

## Success Criteria
- All validator types implemented
- Full type inference working
- Custom validators work
- Transforms work and types flow through
- All tests pass
- Bundle size under target
- No any types in implementation
