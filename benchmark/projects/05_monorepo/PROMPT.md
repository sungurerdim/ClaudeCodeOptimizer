# Project: Component Library Monorepo

Build a monorepo containing a UI component library with documentation site.

---

## Autonomous Operation

**Execute this task completely without user interaction:**

1. **Proceed autonomously** - Make reasonable decisions without asking
2. **Implement all requirements** - Complete every package listed below
3. **Write working code** - All components must render and function
4. **Include tests** - Test coverage for each package
5. **Handle errors gracefully** - Proper TypeScript types throughout
6. **No slash commands** - Do NOT use `/help`, `/commit`, or any `/` commands (not available in this execution mode)

**Prioritized execution order:**
1. Monorepo setup (pnpm, Turborepo)
2. @mylib/core package (Button, Input, Modal)
3. @mylib/hooks package (useLocalStorage, useDebounce)
4. @mylib/forms package (depends on core)
5. Storybook configuration
6. @mylib/docs site
7. Tests for each package

---

## Requirements

### Packages

1. **@mylib/core** - Base components
   - Button (variant: primary/secondary/outline, size: sm/md/lg, loading state)
   - Input (type: text/email/password, error state, helper text)
   - Select (single/multi, searchable, async options)
   - Modal (sizes, close on overlay click, focus trap)
   - Toast (success/error/warning/info, auto-dismiss, stack)

2. **@mylib/forms** - Form utilities (depends on @mylib/core)
   - Form component with validation
   - useForm hook
   - Field wrapper with error display
   - Yup/Zod integration

3. **@mylib/hooks** - Utility hooks (standalone)
   - useLocalStorage
   - useDebounce
   - useClickOutside
   - useMediaQuery
   - usePrevious

4. **@mylib/docs** - Documentation site
   - Component documentation with live examples
   - Props tables auto-generated from TypeScript
   - Dark/light theme toggle
   - Search functionality

### Technical Requirements

- pnpm workspaces
- TypeScript strict mode
- Turborepo for build orchestration
- Vite for library builds
- Vitest for testing
- Storybook for component development
- Changesets for versioning

### Project Structure

```
monorepo/
├── packages/
│   ├── core/
│   │   ├── src/
│   │   │   ├── Button/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Button.test.tsx
│   │   │   │   ├── Button.stories.tsx
│   │   │   │   └── index.ts
│   │   │   └── ...
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── forms/
│   ├── hooks/
│   └── docs/
├── turbo.json
├── pnpm-workspace.yaml
├── package.json
└── tsconfig.base.json
```

### Build Configuration

```json
// turbo.json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "test": {
      "dependsOn": ["build"]
    },
    "lint": {},
    "dev": {
      "cache": false
    }
  }
}
```

### Component API Example

```typescript
// Button
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
  children: ReactNode;
  onClick?: () => void;
}

// useForm
interface UseFormOptions<T> {
  initialValues: T;
  validationSchema?: Schema<T>;
  onSubmit: (values: T) => void | Promise<void>;
}

function useForm<T>(options: UseFormOptions<T>): {
  values: T;
  errors: Partial<Record<keyof T, string>>;
  touched: Partial<Record<keyof T, boolean>>;
  handleChange: (field: keyof T) => (value: any) => void;
  handleBlur: (field: keyof T) => () => void;
  handleSubmit: () => Promise<void>;
  isSubmitting: boolean;
  reset: () => void;
}
```

---

## Success Criteria

| Priority | Requirement | Validation |
|----------|-------------|------------|
| P0 | All packages build independently | pnpm build succeeds |
| P0 | Cross-package imports work | forms uses core components |
| P1 | Turborepo caching works | Second build is cached |
| P1 | Storybook shows all components | Stories render correctly |
| P1 | Types are properly exported | No TypeScript errors |
| P2 | Tests pass across all packages | pnpm test succeeds |
| P2 | Docs site renders | Local dev server works |

**Deliverables:** Working monorepo, all packages, Storybook, documentation site.
