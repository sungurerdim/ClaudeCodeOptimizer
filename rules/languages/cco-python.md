# Python Rules
*Stack-specific rules for Python projects*

**Trigger:** {py_manifest}, {py_ext}

## Type Annotations

- **Modern-Types**: Use `str | None` not `Optional[str]`, use `list[str]` not `List[str]`
- **Self-Type**: Use `Self` for return type in methods that return self: `def clone(self) -> Self`
- **Protocol-Prefer**: Use `Protocol` for structural typing when duck typing is intended
- **Override-Decorator**: Use `@override` decorator when overriding parent methods

## Modern Syntax

- **Match-Case**: Use `match`/`case` for complex conditionals instead of if/elif chains
- **Walrus-Operator**: Use `:=` for assignment expressions: `if (n := len(items)) > 10:`
- **F-Strings**: Use f-strings: `f"Hello {name}"` not `"Hello {}".format(name)`
- **Comprehensions**: Use comprehensions for simple transforms: `[x*2 for x in items]`

## Async Patterns

- **Async-Context**: Use `async with` for async resources: `async with aiofiles.open() as f:`
- **TaskGroup**: Use `async with asyncio.TaskGroup() as tg:` for structured concurrency
- **Timeout-Context**: Use `async with asyncio.timeout(5):` for timeouts
- **Async-Generators**: Use `async for` with async generators for streaming

## Data Classes

- **Dataclasses**: Use `@dataclass(slots=True)` for data containers
- **Pydantic-Validators**: Use `@field_validator` for custom validation, `BeforeValidator` for normalization
- **Pydantic-Bounds**: Set `Field(min_length=1, max_length=N)` for string fields
- **Pydantic-Strict**: Use `strict=True` on models for no implicit coercion
- **Enum-StrEnum**: Use `class Status(StrEnum):` for string enums

## Resource Management

- **Import-Order**: stdlib > third-party > local (isort compatible)
- **Context-Managers**: Use `with open() as f:` for files, connections, locks
- **Exception-Chain**: Use `raise NewError() from original_error` for chaining
- **Subprocess-Encoding**: Use `subprocess.run(..., encoding='utf-8', errors='replace')`
