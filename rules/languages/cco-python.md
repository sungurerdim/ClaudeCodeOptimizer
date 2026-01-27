# Python Rules
*Modern patterns (3.10+)*

**Trigger:** {py_manifest}, {py_ext}

## Modern Types

- `str | None` not `Optional[str]`
- `list[str]` not `List[str]`
- `Self` for methods returning self
- `@override` for parent method overrides

## Modern Syntax

- `match`/`case` for complex conditionals
- `:=` walrus operator: `if (n := len(items)) > 10:`

## Async (3.11+)

- `async with asyncio.TaskGroup() as tg:` for structured concurrency
- `async with asyncio.timeout(5):` for timeouts

## Data Classes

- `@dataclass(slots=True)` for memory efficiency
- `class Status(StrEnum):` for string enums
- Pydantic: `strict=True`, `Field(min_length=1, max_length=N)`
