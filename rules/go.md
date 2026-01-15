# Go Rules
*Stack-specific rules for Go projects*

**Trigger:** {go_manifest}, {go_ext}

## Error Handling

- **Error-Wrap**: Wrap errors with context (fmt.Errorf %w)
- **Error-Is-As**: Use errors.Is and errors.As for error checking
- **Sentinel-Errors**: Define sentinel errors for expected conditions (var ErrNotFound = errors.New(...))
- **Error-Types**: Use custom error types for errors needing additional context

## Concurrency

- **Context-Pass**: Pass context.Context as first parameter for cancellation
- **Goroutine-Safe**: Channel or sync primitives for concurrency
- **Defer-Cleanup**: defer for cleanup operations
- **Errgroup**: Use errgroup for coordinated goroutine error handling
- **Context-Cancel**: Always cancel context when done to release resources

## Modern Features

- **Generics**: Use generics for type-safe collections and utilities
- **Slog-Logging**: Use slog for structured logging
- **Range-Int**: Use range over integers for simple loops
- **Range-Func**: Use range over functions for custom iteration

## Design Patterns

- **Interface-Small**: Small, focused interfaces (1-3 methods)
- **Accept-Interface**: Accept interfaces, return structs
- **Table-Tests**: Table-driven tests for comprehensive coverage
- **Functional-Options**: Use functional options for configurable constructors
