---
metadata:
  name: "Advanced TypeScript Types"
  activation_keywords: ["type", "conditional", "mapped", "utility", "template"]
  category: "language-typescript"
principles: ['P_TYPE_SAFETY', 'P_LINTING_SAST', 'U_DRY', 'U_NO_OVERENGINEERING']
---

# Advanced TypeScript Types

Master advanced TypeScript type system features for type-safe and expressive code.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Advanced Type Features:**
- Conditional types: `T extends U ? X : Y` for type branching
- Mapped types: Transform object properties systematically
- Template literal types: Type-safe string manipulation
- Utility types: Built-in transformations (Partial, Pick, Omit, etc.)
- Type inference: `infer` keyword for extracting types

**Key Patterns:**
1. Use conditional types for type-level logic
2. Create custom utility types with mapped types
3. Extract types from existing values with `typeof` and `ReturnType`
4. Use template literals for type-safe string patterns
5. Leverage distributive conditional types for unions

**Common Use Cases:**
- API response types with conditional fields
- Form validation types
- Event handler type extraction
- Route parameter parsing

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**Conditional Types:**
```typescript
// Basic conditional type
type IsString<T> = T extends string ? true : false;

type A = IsString<string>;  // true
type B = IsString<number>;  // false

// Extract array element type
type ElementType<T> = T extends (infer U)[] ? U : never;

type C = ElementType<string[]>;  // string
type D = ElementType<number>;    // never

// Non-nullable type
type NonNullable<T> = T extends null | undefined ? never : T;

type E = NonNullable<string | null>;  // string
```

**Mapped Types:**
```typescript
// Make all properties optional
type Partial<T> = {
  [P in keyof T]?: T[P];
};

// Make all properties readonly
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};

// Pick specific properties
type Pick<T, K extends keyof T> = {
  [P in K]: T[P];
};

// Omit specific properties
type Omit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;

// Custom: Make specific keys required
type RequireKeys<T, K extends keyof T> = T & {
  [P in K]-?: T[P];
};

interface User {
  id: number;
  name?: string;
  email?: string;
}

type RequiredUser = RequireKeys<User, 'name' | 'email'>;
// { id: number; name: string; email: string }
```

**Template Literal Types:**
```typescript
// Type-safe event names
type EventName = 'click' | 'focus' | 'blur';
type EventHandler = `on${Capitalize<EventName>}`;
// 'onClick' | 'onFocus' | 'onBlur'

// API endpoint types
type HTTPMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type Endpoint = `/api/${string}`;
type APICall = `${HTTPMethod} ${Endpoint}`;
// 'GET /api/...' | 'POST /api/...' | etc.

// CSS properties
type CSSUnit = 'px' | 'em' | 'rem' | '%';
type Size = `${number}${CSSUnit}`;
// '10px' | '1.5em' | '100%' | etc.

// Route parameters
type Route = '/user/:id' | '/post/:slug/comment/:commentId';
type ExtractParams<T extends string> =
  T extends `${infer _Start}:${infer Param}/${infer Rest}`
    ? Param | ExtractParams<`/${Rest}`>
    : T extends `${infer _Start}:${infer Param}`
    ? Param
    : never;

type UserParams = ExtractParams<'/user/:id'>;  // 'id'
type PostParams = ExtractParams<'/post/:slug/comment/:commentId'>;  // 'slug' | 'commentId'
```

**Utility Types:**
```typescript
interface Todo {
  id: number;
  title: string;
  completed: boolean;
  createdAt: Date;
}

// Partial - all properties optional
type TodoUpdate = Partial<Todo>;

// Required - all properties required
type TodoCreate = Required<Pick<Todo, 'title'>>;

// Pick - select properties
type TodoPreview = Pick<Todo, 'id' | 'title'>;

// Omit - exclude properties
type TodoWithoutDates = Omit<Todo, 'createdAt'>;

// Record - create object type
type TodosByStatus = Record<'pending' | 'done', Todo[]>;

// ReturnType - extract function return type
function getTodo() { return { id: 1, title: 'Test' }; }
type TodoReturn = ReturnType<typeof getTodo>;

// Parameters - extract function parameters
function updateTodo(id: number, data: Partial<Todo>) {}
type UpdateParams = Parameters<typeof updateTodo>;  // [number, Partial<Todo>]
```

**Advanced Type Inference:**
```typescript
// Infer function return type
type InferReturn<T> = T extends (...args: any[]) => infer R ? R : never;

// Infer array element type
type InferElement<T> = T extends (infer E)[] ? E : never;

// Infer Promise resolved type
type InferPromise<T> = T extends Promise<infer U> ? U : never;

// Deep property access
type DeepValue<T, K extends string> =
  K extends `${infer First}.${infer Rest}`
    ? First extends keyof T
      ? DeepValue<T[First], Rest>
      : never
    : K extends keyof T
    ? T[K]
    : never;

interface User {
  profile: {
    address: {
      city: string;
    }
  }
}

type City = DeepValue<User, 'profile.address.city'>;  // string
```

**Discriminated Unions:**
```typescript
type Success<T> = {
  status: 'success';
  data: T;
};

type Error = {
  status: 'error';
  error: string;
};

type Result<T> = Success<T> | Error;

function handleResult<T>(result: Result<T>) {
  if (result.status === 'success') {
    // TypeScript knows result is Success<T>
    console.log(result.data);
  } else {
    // TypeScript knows result is Error
    console.log(result.error);
  }
}
```

**Builder Pattern with Types:**
```typescript
type Builder<T, K extends keyof T = never> = {
  [P in keyof T]-?: P extends K
    ? T[P]
    : never extends T[P]
    ? (value: T[P]) => Builder<T, K | P>
    : (value: T[P]) => Builder<T, K | P>;
} & (K extends keyof T ? { build(): Pick<T, K> } : {});

interface User {
  name: string;
  age: number;
  email?: string;
}

// Usage provides type-safe builder
const user = UserBuilder()
  .name('Alice')
  .age(30)
  .build();  // ✓ Type-safe
```

**Type Guards with Custom Types:**
```typescript
// Type predicate
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

// Assertion function
function assertIsDefined<T>(value: T): asserts value is NonNullable<T> {
  if (value === undefined || value === null) {
    throw new Error('Value is not defined');
  }
}

// Usage
function process(value: string | undefined) {
  assertIsDefined(value);
  // TypeScript knows value is string here
  console.log(value.toUpperCase());
}
```

**Recursive Types:**
```typescript
// JSON type
type JSONValue =
  | string
  | number
  | boolean
  | null
  | JSONValue[]
  | { [key: string]: JSONValue };

// Tree structure
interface TreeNode<T> {
  value: T;
  children?: TreeNode<T>[];
}

// Deep partial
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};
```

**Type-Safe Event Emitter:**
```typescript
type EventMap = {
  'user:login': { userId: string };
  'user:logout': { userId: string };
  'data:update': { id: number; data: unknown };
};

class TypedEventEmitter<T extends Record<string, any>> {
  on<K extends keyof T>(event: K, handler: (data: T[K]) => void): void {
    // Implementation
  }

  emit<K extends keyof T>(event: K, data: T[K]): void {
    // Implementation
  }
}

const emitter = new TypedEventEmitter<EventMap>();
emitter.on('user:login', (data) => {
  // data is typed as { userId: string }
  console.log(data.userId);
});
```

**Anti-Patterns to Avoid:**
```typescript
// ✗ Avoid any
function process(data: any) { }  // Loses type safety

// ✓ Use generics or unknown
function process<T>(data: T) { }
function process(data: unknown) { }

// ✗ Avoid type assertions without validation
const value = data as string;  // Unsafe

// ✓ Use type guards
if (typeof data === 'string') {
  const value = data;  // Safe
}
```
