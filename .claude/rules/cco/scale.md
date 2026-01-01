# Scale Rules (Small: 100-1K)

- **Caching**: TTL + invalidation strategy for data fetching
- **Lazy-Load**: Defer loading of non-critical resources
- **Simple-First**: Straightforward solutions, avoid over-engineering
- **Single-Process**: No need for complex async/multiprocessing yet
- **File-Based**: Simple file-based state management acceptable
- **Direct-Deps**: Flat dependency structure, avoid deep hierarchies
- **Minimal-Abstraction**: Avoid premature abstraction
- **Readable**: Optimize for readability over cleverness
- **Inline**: Inline small functions if clarity improves
- **Refactor-Later**: Don't refactor until patterns emerge
