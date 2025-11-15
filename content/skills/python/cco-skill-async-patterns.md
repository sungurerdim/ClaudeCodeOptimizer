---
metadata:
  name: "Python Async Patterns"
  activation_keywords: ["async", "await", "asyncio", "coroutine", "concurrent"]
  category: "language-python"
principles: ['P_ASYNC_IO', 'U_FAIL_FAST', 'P_GRACEFUL_SHUTDOWN', 'U_EVIDENCE_BASED']
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

**Basic Async Function:**
```python
import asyncio

async def fetch_data(url: str) -> dict:
    await asyncio.sleep(1)  # Simulated I/O
    return {"url": url, "data": "..."}

async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

asyncio.run(main())
```

**Concurrent Execution with gather:**
```python
async def fetch_multiple():
    urls = ["url1", "url2", "url3"]
    results = await asyncio.gather(
        *[fetch_data(url) for url in urls],
        return_exceptions=True  # Continue if one fails
    )
    return results
```

**Task Management with create_task:**
```python
async def background_tasks():
    # Start task immediately, don't wait
    task1 = asyncio.create_task(fetch_data("url1"))
    task2 = asyncio.create_task(fetch_data("url2"))

    # Do other work here
    await asyncio.sleep(0.5)

    # Wait for results when needed
    result1 = await task1
    result2 = await task2
```

**Error Handling:**
```python
async def safe_fetch(url: str):
    try:
        async with asyncio.timeout(5.0):  # Python 3.11+
            return await fetch_data(url)
    except asyncio.TimeoutError:
        return {"error": "timeout"}
    except Exception as e:
        return {"error": str(e)}
```

**Async Context Manager:**
```python
class AsyncDatabase:
    async def __aenter__(self):
        self.conn = await connect_db()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()

async def use_db():
    async with AsyncDatabase() as db:
        await db.query("SELECT * FROM users")
```

**Testing Async Code (pytest-asyncio):**
```python
import pytest

@pytest.mark.asyncio
async def test_fetch_data():
    result = await fetch_data("test_url")
    assert result["url"] == "test_url"

@pytest.fixture
async def db_connection():
    conn = await create_connection()
    yield conn
    await conn.close()
```

**Mixing Blocking and Async:**
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def blocking_io():
    # Legacy blocking code
    time.sleep(2)
    return "result"

async def async_wrapper():
    # Run blocking code in thread pool
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, blocking_io)
    return result
```

**Performance Tips:**
- Use `asyncio.TaskGroup()` (Python 3.11+) for structured concurrency
- Avoid creating too many tasks (use semaphores to limit concurrency)
- Profile with `asyncio.create_task(..., name="task_name")` for debugging
- Use `aiohttp` for HTTP, `asyncpg` for PostgreSQL, `motor` for MongoDB
