# Haskell Rules
*Stack-specific rules for Haskell projects*

**Trigger:** {haskell_manifest}, {haskell_ext}

- **Pure-Functions**: Prefer pure functions, isolate IO
- **Type-Signatures**: Explicit type signatures for top-level
- **Monad-Transform**: Monad transformers for effect stacking
- **Lazy-Strict**: Use strict where appropriate (BangPatterns, seq)
- **Lens-Optics**: Use lens/optics for nested data
- **Property-Tests**: QuickCheck for property-based testing
