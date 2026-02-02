# Rust Rules
*Stack-specific rules for Rust projects*

**Trigger:** {rust_manifest}, {rust_ext}

## Borrow Checker Gotchas

- **Borrowing in loops**: `for item in &mut vec { vec.push(x) }` won't compile -- you can't mutably borrow `vec` while iterating. Collect indices first or use `retain`/`drain`
- **Temporary value drops**: `let s = String::from("hi").as_str();` -- the String drops at semicolon, leaving a dangling ref. Bind the String to a variable first
- **Move after partial borrow**: Destructuring a struct borrows fields individually, but moving one field invalidates the whole struct. Clone or restructure
- **Closure capture granularity**: Closures capture entire variables, not sub-fields. Use `let field = &self.field;` before the closure to narrow the borrow
- **`Rc`/`RefCell` panics**: `RefCell::borrow_mut()` panics at runtime if already borrowed -- this is the borrow checker deferred to runtime. Minimize `RefCell` scope

## Async Gotchas

- **`Pin` requirement**: Futures that borrow across `.await` points must be `Pin<Box<dyn Future>>`. If you get "cannot be unpinned" errors, `Box::pin()` the future
- **`Send` bounds**: Holding a non-`Send` type (like `Rc`, `MutexGuard`) across `.await` makes the future non-`Send`, breaking `tokio::spawn`. Drop the guard before `.await`
- **Async trait methods**: Use `async fn` in traits (stabilized in 1.75), but the returned futures are not `Send` by default. For `Send` requirement, use `#[trait_variant::make(SendTrait)]` or return `Box<dyn Future + Send>`
- **Blocking in async**: `std::thread::sleep()` or CPU-heavy work in async blocks the entire runtime thread. Use `tokio::task::spawn_blocking()` or `tokio::time::sleep()`
- **Cancellation safety**: `.await` can be cancelled (e.g., via `select!`). If your future has side effects before an `.await`, partial work may be lost. Use `tokio::select! { biased; }` or cancellation-safe alternatives

## Error Handling Gotchas

- **`thiserror` vs `anyhow`**: Libraries use `thiserror` (typed errors callers can match on). Applications use `anyhow` (ergonomic, context-rich). Mixing them: library defines errors with `thiserror`, app wraps with `anyhow`
- **Lost context**: `fs::read("f.txt")?` gives "No such file" with no path info. Always `.context("reading f.txt")` or `.with_context(|| format!("reading {path}"))`
- **`unwrap` in production**: Every `.unwrap()` is a potential panic. Use `.expect("reason")` at minimum, prefer `?` propagation. Reserve `unwrap` for cases provably infallible

## One-Liners

- Run clippy in CI: `#![deny(clippy::all)]`, include `cargo clippy -- -D warnings` in pipeline
- Minimize `unsafe` blocks, document safety invariants with `// SAFETY:` comments
- Write doc-tests for public API: they serve as both tests and examples
- Use feature flags for optional deps: `#[cfg(feature = "serde")] impl Serialize for T`
