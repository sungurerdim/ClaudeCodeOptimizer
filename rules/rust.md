# Rust Rules
*Stack-specific rules for Rust projects*

**Trigger:** {rust_manifest}, {rust_ext}

## Error Handling

- **Result-Propagate**: Use ? operator for error propagation
- **Error-Thiserror**: Use thiserror for library errors, anyhow for applications
- **Error-Context**: Add context to errors with .context() or .with_context()
- **Custom-Errors**: Define domain-specific error types for better error handling

## Ownership & Memory

- **Ownership-Clear**: Clear ownership patterns, minimize clones
- **Borrow-Prefer**: Prefer borrowing over ownership when possible
- **Lifetime-Elision**: Rely on lifetime elision, annotate only when necessary
- **Arc-Mutex**: Use Arc<Mutex<T>> for shared mutable state across threads

## Modern Features

- **Async-Traits**: Use async fn in traits
- **Let-Chains**: Use let chains for complex conditionals
- **Return-Position-Impl**: Use -> impl Trait for return types
- **Const-Generics**: Use const generics for compile-time array sizes

## Quality

- **Clippy-Clean**: No clippy warnings - include in CI workflows, use `#![deny(clippy::all)]`
- **Unsafe-Minimize**: Minimize unsafe blocks, document safety invariants when used
- **Doc-Tests**: Include doc tests for public APIs
- **Feature-Flags**: Use feature flags for optional functionality
