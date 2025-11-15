---
metadata:
  name: "TypeScript Type Safety"
  activation_keywords: ["strict", "type guard", "discriminated union", "narrowing"]
  category: "language-typescript"
principles: ['P_TYPE_SAFETY', 'P_LINTING_SAST', 'U_FAIL_FAST', 'U_EVIDENCE_BASED']
---

# TypeScript Type Safety

Master TypeScript strict mode and advanced type safety patterns for bulletproof code.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Strict Mode Configuration:**
- `strict: true` enables all strict type checks
- `noImplicitAny`: Disallow implicit any types
- `strictNullChecks`: Null/undefined must be explicit
- `strictFunctionTypes`: Strict function parameter checking
- `strictPropertyInitialization`: Class properties must be initialized

**Type Safety Patterns:**
1. Use discriminated unions for state management
2. Create custom type guards for runtime checking
3. Leverage exhaustiveness checking with never
4. Use branded types for primitive values
5. Prefer const assertions for literal types

**Type Narrowing:**
- typeof checks for primitives
- instanceof for class instances
- in operator for property checks
- Custom type guards for complex types
- Discriminated unions for tagged types

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**Strict Configuration (tsconfig.json):**
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "noPropertyAccessFromIndexSignature": true
  }
}
```

**Discriminated Unions:**
```typescript
// Type-safe state management
type State =
  | { status: 'loading' }
  | { status: 'success'; data: string }
  | { status: 'error'; error: Error };

function handleState(state: State) {
  switch (state.status) {
    case 'loading':
      console.log('Loading...');
      break;
    case 'success':
      // TypeScript knows state.data exists
      console.log(state.data.toUpperCase());
      break;
    case 'error':
      // TypeScript knows state.error exists
      console.error(state.error.message);
      break;
  }
}

// API response types
type ApiResponse<T> =
  | { success: true; data: T }
  | { success: false; error: string };

function processResponse<T>(response: ApiResponse<T>) {
  if (response.success) {
    return response.data;  // Type narrowed to T
  }
  throw new Error(response.error);
}
```

**Type Guards:**
```typescript
// Built-in type guards
function processValue(value: string | number) {
  if (typeof value === 'string') {
    // value is string
    return value.toUpperCase();
  }
  // value is number
  return value.toFixed(2);
}

// instanceof guard
class Dog {
  bark() { console.log('Woof!'); }
}

class Cat {
  meow() { console.log('Meow!'); }
}

function makeSound(animal: Dog | Cat) {
  if (animal instanceof Dog) {
    animal.bark();
  } else {
    animal.meow();
  }
}

// in operator guard
type Fish = { swim: () => void };
type Bird = { fly: () => void };

function move(animal: Fish | Bird) {
  if ('swim' in animal) {
    animal.swim();
  } else {
    animal.fly();
  }
}

// Custom type guard
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

function process(value: unknown) {
  if (isString(value)) {
    // value is string
    console.log(value.toUpperCase());
  }
}
```

**Assertion Functions:**
```typescript
// Assertion function
function assertIsDefined<T>(
  value: T,
  message?: string
): asserts value is NonNullable<T> {
  if (value === null || value === undefined) {
    throw new Error(message ?? 'Value is not defined');
  }
}

function processUser(user: User | undefined) {
  assertIsDefined(user, 'User must be defined');
  // TypeScript knows user is User here
  console.log(user.name.toUpperCase());
}

// Assert type
function assertIsNumber(value: unknown): asserts value is number {
  if (typeof value !== 'number') {
    throw new Error('Value must be a number');
  }
}
```

**Exhaustiveness Checking:**
```typescript
type Color = 'red' | 'green' | 'blue';

function getColorName(color: Color): string {
  switch (color) {
    case 'red':
      return 'Red';
    case 'green':
      return 'Green';
    case 'blue':
      return 'Blue';
    default:
      // Exhaustiveness check
      const _exhaustive: never = color;
      throw new Error(`Unhandled color: ${_exhaustive}`);
  }
}

// If new color is added, TypeScript will error at default case
// type Color = 'red' | 'green' | 'blue' | 'yellow';  // Error!
```

**Branded Types:**
```typescript
// Prevent mixing similar types
type UserId = string & { __brand: 'UserId' };
type ProductId = string & { __brand: 'ProductId' };

function createUserId(id: string): UserId {
  return id as UserId;
}

function createProductId(id: string): ProductId {
  return id as ProductId;
}

function getUser(id: UserId) {
  // Implementation
}

const userId = createUserId('123');
const productId = createProductId('456');

getUser(userId);      // ✓ OK
getUser(productId);   // ✗ Error: Type mismatch

// Branded primitives
type PositiveNumber = number & { __brand: 'PositiveNumber' };

function createPositive(n: number): PositiveNumber {
  if (n <= 0) throw new Error('Must be positive');
  return n as PositiveNumber;
}
```

**Const Assertions:**
```typescript
// Without const assertion
const colors1 = ['red', 'green', 'blue'];
// type: string[]

// With const assertion
const colors2 = ['red', 'green', 'blue'] as const;
// type: readonly ['red', 'green', 'blue']

const config = {
  api: 'https://api.example.com',
  timeout: 5000,
} as const;
// All properties readonly and literal types

// Use in function parameters
function processColor(color: typeof colors2[number]) {
  // color is 'red' | 'green' | 'blue'
}
```

**Strict Null Checks:**
```typescript
// strictNullChecks: true

function getLength(str: string | null): number {
  // Error without null check
  // return str.length;

  // ✓ Correct
  if (str === null) {
    return 0;
  }
  return str.length;
}

// Optional chaining
interface User {
  profile?: {
    address?: {
      city?: string;
    };
  };
}

function getCity(user: User): string | undefined {
  return user.profile?.address?.city;
}

// Nullish coalescing
function getDisplayName(name: string | null | undefined): string {
  return name ?? 'Anonymous';
}
```

**Unknown vs Any:**
```typescript
// ✗ any - disables type checking
function badProcess(value: any) {
  return value.toUpperCase();  // No error, crashes at runtime
}

// ✓ unknown - requires type checking
function goodProcess(value: unknown) {
  // Error without type guard
  // return value.toUpperCase();

  if (typeof value === 'string') {
    return value.toUpperCase();  // ✓ Safe
  }
  return '';
}
```

**Readonly and Immutability:**
```typescript
// Readonly properties
interface Config {
  readonly apiKey: string;
  readonly timeout: number;
}

const config: Config = {
  apiKey: 'secret',
  timeout: 5000,
};

// config.apiKey = 'new';  // Error: readonly

// Readonly arrays
function sum(numbers: readonly number[]): number {
  // numbers.push(1);  // Error: readonly
  return numbers.reduce((a, b) => a + b, 0);
}

// Deep readonly
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object
    ? DeepReadonly<T[P]>
    : T[P];
};

interface User {
  name: string;
  profile: {
    age: number;
  };
}

type ReadonlyUser = DeepReadonly<User>;
// All nested properties are readonly
```

**Index Signature Safety:**
```typescript
// noUncheckedIndexedAccess: true

interface Dict {
  [key: string]: string;
}

const dict: Dict = { a: 'value' };

// Without noUncheckedIndexedAccess
const value1 = dict['missing'];  // Type: string (wrong!)

// With noUncheckedIndexedAccess
const value2 = dict['missing'];  // Type: string | undefined (correct!)

if (value2 !== undefined) {
  console.log(value2.toUpperCase());  // Safe
}
```

**Function Overloads for Type Safety:**
```typescript
// Overload signatures
function createElement(tag: 'div'): HTMLDivElement;
function createElement(tag: 'span'): HTMLSpanElement;
function createElement(tag: 'button'): HTMLButtonElement;
function createElement(tag: string): HTMLElement;

// Implementation
function createElement(tag: string): HTMLElement {
  return document.createElement(tag);
}

// Usage has correct types
const div = createElement('div');     // HTMLDivElement
const span = createElement('span');   // HTMLSpanElement
const button = createElement('button'); // HTMLButtonElement
```

**Strict Property Initialization:**
```typescript
class User {
  // Error: Property has no initializer
  // name: string;

  // ✓ Initialize in constructor
  name: string;

  // ✓ Initialize inline
  email: string = '';

  // ✓ Mark as definitely assigned (use carefully)
  id!: number;

  constructor(name: string) {
    this.name = name;
    this.initialize();
  }

  private initialize() {
    this.id = Math.random();
  }
}
```

**Anti-Patterns to Avoid:**
```typescript
// ✗ Don't use any
function bad(data: any) {
  return data.property;  // No type safety
}

// ✓ Use unknown or generics
function good<T>(data: T) {
  return data;
}

// ✗ Don't use non-null assertion without verification
function bad2(user: User | null) {
  return user!.name;  // Crashes if null
}

// ✓ Check for null
function good2(user: User | null) {
  if (user === null) {
    throw new Error('User is null');
  }
  return user.name;
}

// ✗ Don't use type assertions unnecessarily
const value = data as string;  // Unsafe

// ✓ Use type guards
if (typeof data === 'string') {
  const value = data;  // Safe
}
```
