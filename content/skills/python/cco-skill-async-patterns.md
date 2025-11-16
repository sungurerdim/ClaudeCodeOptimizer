---
title: Python Async Patterns Skill
category: performance
description: asyncio, async/await, concurrency patterns
metadata:
  name: "Python Async Patterns"
  activation_keywords: ["async", "await", "asyncio", "coroutine", "concurrent"]
  category: "language-python"
  language: "python"
principles: ['P_ASYNC_IO', 'U_FAIL_FAST', 'P_GRACEFUL_SHUTDOWN', 'U_EVIDENCE_BASED']
use_cases:
  project_purpose: [backend, microservice, data-pipeline, web-app]
  project_maturity: [active-dev, production]
---

# Python Async Patterns

Master async/await patterns and asyncio best practices for writing concurrent Python code.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Core Async Concepts:**
- `async def` creates coroutine function, `await` calls coroutines
- Event loop manages task execution (asyncio.run() for entry point)
- Tasks wrap coroutines for concurrent execution
- `asyncio.gather()` runs multiple coroutines concurrently
- `asyncio.create_task()` schedules coroutine immediately

**Key Patterns:**
1. Always use `asyncio.run()` as single entry point
2. Use `async with` for async context managers (connections, sessions)
3. Never mix blocking I/O with async code - use `asyncio.to_thread()` for blocking calls
4. Handle CancelledError for graceful shutdown
5. Use `asyncio.wait_for()` for timeouts

**Common Mistakes:**
- Forgetting `await` (creates unawaited coroutine)
- Using `time.sleep()` instead of `asyncio.sleep()`
- Creating event loops manually (use asyncio.run())
- Not handling task exceptions

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**Key Examples:**
- Basic: `async def`, `await`, `asyncio.run()`
- Concurrency: `asyncio.gather()`, `asyncio.create_task()`
- Error handling: `asyncio.timeout()`, try/except
- Async context: `async with AsyncDatabase() as db:`
- Testing: `@pytest.mark.asyncio` decorator
- Blocking code: `loop.run_in_executor(None, blocking_func)`

**Performance Tips:**
- Use `asyncio.TaskGroup()` (Python 3.11+) for structured concurrency
- Avoid creating too many tasks (use semaphores to limit concurrency)
- Profile with `asyncio.create_task(..., name="task_name")` for debugging
- Use `aiohttp` for HTTP, `asyncpg` for PostgreSQL, `motor` for MongoDB
