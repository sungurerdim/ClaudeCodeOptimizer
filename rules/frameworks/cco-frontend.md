# Frontend
*Frontend framework rules and best practices*

**Trigger:** React/Vue/Angular/Svelte/Solid/Astro detected

## Base Frontend Rules
- **A11y-WCAG**: WCAG 2.2 AA, keyboard navigation
- **Perf-Core-Vitals**: LCP<2.5s, INP<200ms, CLS<0.1
- **State-Predictable**: Single source of truth for state
- **Code-Split**: Lazy load routes and heavy components

## React (Frontend:React)
**Trigger:** {react_deps}, {react_ext}

### Core Patterns
- **Hooks-Rules**: Rules of Hooks (top-level, same order)
- **Key-Stable**: Stable keys for lists (not index)
- **Effect-Cleanup**: Cleanup in useEffect return

### Modern Patterns
- **Use-Hook**: Use use() hook for promises and context
- **UseActionState**: Use useActionState for form handling
- **UseFormStatus**: Use useFormStatus for pending states in form submissions
- **UseOptimistic**: Use useOptimistic for instant UI feedback during mutations
- **Ref-As-Prop**: Pass ref as regular prop

### Server Components (RSC)
- **Server-Components**: Use Server Components for data fetching, Client for interactivity
- **Server-Actions**: Use Server Actions for mutations (async functions with 'use server')
- **Client-Directive**: Add 'use client' only when needed (state, effects, browser APIs)
- **Suspense-Boundary**: Wrap async components in Suspense with fallback

### Performance
- **Memo-Strategic**: useMemo/useCallback only for expensive operations
- **Lazy-Loading**: Use React.lazy and Suspense for code splitting
- **Transition-API**: Use useTransition for non-urgent state updates

## Vue (Frontend:Vue)
**Trigger:** {vue_deps}, {vue_ext}

- **Composition-API**: Prefer Composition API over Options API
- **Reactive-Unwrap**: .value access for refs in script
- **Provide-Inject**: Provide/inject for deep prop drilling
- **SFC-Style**: Scoped styles in single-file components
- **Script-Setup**: Use <script setup> for cleaner syntax
- **Definemodel**: Use defineModel for v-model with props

## Angular (Frontend:Angular)
**Trigger:** {angular_deps}, {angular_ext}

- **Standalone-Components**: Prefer standalone components
- **Signals-Reactive**: Use signals for reactive state
- **OnPush-Strategy**: OnPush change detection for performance
- **Lazy-Modules**: Lazy load feature modules
- **Input-Signal**: Use input() and model() signal functions
- **Output-Function**: Use output() function instead of @Output
- **Deferrable-Views**: Use @defer for lazy loading components
- **Control-Flow**: Use @if/@for/@switch over *ngIf/*ngFor

## Svelte (Frontend:Svelte)
**Trigger:** {svelte_deps}, {svelte_ext}

- **Reactivity-Native**: Use framework reactivity (runes or stores)
- **Transitions-Native**: Use built-in transitions
- **Actions-Reusable**: Reusable actions for DOM behavior
- **Runes-State**: Use $state for reactive state, $derived for computed
- **Runes-Effect**: Use $effect for side effects
- **Props-Rune**: Use $props() for component props
- **Snippets**: Use {#snippet} for reusable markup

## Solid (Frontend:Solid)
**Trigger:** {solid_deps}

- **Signal-Fine-Grained**: Fine-grained reactivity with signals
- **Memo-Derived**: createMemo for derived computations
- **Effect-Track**: Track dependencies explicitly
- **Props-Direct**: Access props directly via `props.name` (preserves reactivity)

## Astro (Frontend:Astro)
**Trigger:** {astro_deps}, {astro_ext}

- **Islands-Minimal**: client:* directives only when needed
- **Content-Collections**: Content collections for markdown/MDX
- **Static-Default**: Static by default, SSR when needed
- **Partial-Hydration**: Selective hydration strategies

## HTMX (Frontend:HTMX)
**Trigger:** {htmx_deps}, {htmx_attrs}

- **Hypermedia-API**: Return HTML fragments, not JSON
- **Target-Precise**: Precise hx-target selectors
- **Swap-Strategy**: Appropriate hx-swap (innerHTML, outerHTML, etc)
- **Indicator-Feedback**: Loading indicators with hx-indicator

## Qwik (Frontend:Qwik)
**Trigger:** {qwik_deps}

- **Resumability-First**: Leverage resumability, avoid eager hydration
- **Dollar-Sign**: Use $() for lazy-loaded code boundaries
- **Task-Types**: useTask$ for server, useVisibleTask$ for client-only
- **Signal-State**: Signals for fine-grained reactivity
- **Component-Lazy**: component$() for automatic code splitting
- **Serialization-Aware**: Keep state serializable for resumability
- **Event-QRL**: QRL-based event handlers for optimal loading
- **City-Routing**: Use Qwik City for routing and data loading

---

## Internationalization (i18n)
**Trigger:** locales/i18n/translations detected

- **Strings-External**: No hardcoded user-facing text
- **UTF8-Encoding**: Consistent UTF-8 encoding
- **RTL-Support**: Bidirectional layout for RTL languages
- **Locale-Format**: Culture-aware date/time/number formatting
