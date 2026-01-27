# Go Rules
*Modern patterns (1.21+)*

**Trigger:** {go_manifest}, {go_ext}

## Error Handling

- Wrap: `fmt.Errorf("context: %w", err)`
- Check: `errors.Is(err, target)` / `errors.As(err, &target)`
- Group: `errgroup.Group` for concurrent error collection

## Modern Features (1.21+)

- `slog` for structured logging
- `range` over integers: `for i := range 10`
- `range` over functions (1.23+)
- `slices` and `maps` packages

## Concurrency

- `context.WithTimeout` for deadlines
- `sync.OnceValue` / `sync.OnceFunc` for lazy init
