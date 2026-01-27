# Frontend Rules
*Performance targets and framework gotchas*

## Core Web Vitals [CRITICAL]

| Metric | Target | Impact |
|--------|--------|--------|
| LCP | < 2.5s | Perceived load speed |
| INP | < 200ms | Interactivity |
| CLS | < 0.1 | Visual stability |

---

## Framework Gotchas

### React
- **Keys**: Never use array index as key (breaks reconciliation)
- **Effect Cleanup**: Always return cleanup function from useEffect
- **Server Components**: 'use client' only when needed (state, effects, browser APIs)

### Vue
- **Ref Access**: .value required in script, not in template
- **Reactivity Loss**: Destructuring reactive objects loses reactivity

### Angular
- **OnPush**: Requires immutable data or explicit markForCheck()
- **Signals**: Can't use signals in class fields initialized before injection

### Svelte
- **Runes**: $state, $derived, $effect replace old reactive syntax
- **Snippets**: Replace slots in Svelte 5

### Solid
- **Props Access**: Access via `props.name` (not destructure) to preserve reactivity
- **No Virtual DOM**: Direct DOM updates - be careful with external DOM manipulation

### Astro
- **Islands**: client:* directives only when interactivity needed
- **Hydration**: Static by default - explicit opt-in to JS

---

## i18n Requirements

- No hardcoded user-facing text
- RTL layout support for applicable locales
- UTF-8 encoding throughout
