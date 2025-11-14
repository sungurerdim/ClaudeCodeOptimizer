---
metadata:
  name: "Async Programming with Tokio"
  activation_keywords: ["async", "tokio", "runtime", "future", "concurrent"]
  category: "language-rust"
principles: ['P_ASYNC_IO', 'U_FAIL_FAST', 'P_GRACEFUL_SHUTDOWN', 'U_EVIDENCE_BASED']
---

# Async Programming with Tokio

Master asynchronous programming in Rust using the Tokio runtime for high-performance concurrent applications.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Tokio Overview:**
- Async runtime for Rust (event loop, task scheduler)
- Async/await syntax for writing async code
- Futures represent asynchronous computations
- `tokio::spawn` creates concurrent tasks
- `tokio::join!` and `tokio::select!` for concurrency patterns

**Key Patterns:**
1. Use `#[tokio::main]` for async entry point
2. Spawn tasks with `tokio::spawn` for concurrency
3. Use `tokio::join!` for parallel execution
4. Use `tokio::select!` for racing futures
5. Leverage async traits and channels for communication

**Common Async Types:**
- `async fn` returns `Future<Output = T>`
- `tokio::time::sleep` for async delays
- `tokio::sync::mpsc` for async channels
- `tokio::task::JoinHandle` for spawned tasks

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**Basic Setup (Cargo.toml):**
```toml
[dependencies]
tokio = { version = "1", features = ["full"] }
```

**Async Main Function:**
```rust
#[tokio::main]
async fn main() {
    println!("Hello from async!");

    // Async delay
    tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;

    println!("One second later...");
}

// Multi-threaded runtime (default)
#[tokio::main]
async fn main_multi_thread() {
    // Automatically uses multi-threaded runtime
}

// Single-threaded runtime (lighter)
#[tokio::main(flavor = "current_thread")]
async fn main_single_thread() {
    // Single-threaded runtime
}
```

**Basic Async Function:**
```rust
async fn fetch_data(url: &str) -> Result<String, reqwest::Error> {
    let response = reqwest::get(url).await?;
    let body = response.text().await?;
    Ok(body)
}

#[tokio::main]
async fn main() {
    match fetch_data("https://api.example.com").await {
        Ok(data) => println!("Received: {}", data),
        Err(e) => eprintln!("Error: {}", e),
    }
}
```

**Spawning Tasks:**
```rust
use tokio::task;

#[tokio::main]
async fn main() {
    // Spawn task (runs concurrently)
    let handle = task::spawn(async {
        println!("Running in background");
        42
    });

    // Do other work
    println!("Main thread continues");

    // Wait for result
    let result = handle.await.unwrap();
    println!("Task returned: {}", result);
}

// Spawn multiple tasks
async fn spawn_multiple() {
    let handles: Vec<_> = (0..10)
        .map(|i| {
            task::spawn(async move {
                println!("Task {}", i);
                i * 2
            })
        })
        .collect();

    // Wait for all tasks
    for handle in handles {
        let result = handle.await.unwrap();
        println!("Result: {}", result);
    }
}
```

**Concurrent Execution with join!:**
```rust
use tokio::join;

async fn task1() -> u32 {
    tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
    1
}

async fn task2() -> u32 {
    tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
    2
}

#[tokio::main]
async fn main() {
    // Run concurrently (1 second total, not 2)
    let (result1, result2) = join!(task1(), task2());

    println!("{} + {} = {}", result1, result2, result1 + result2);
}

// Try join - handles errors
use tokio::try_join;

async fn fallible_task1() -> Result<u32, &'static str> {
    Ok(1)
}

async fn fallible_task2() -> Result<u32, &'static str> {
    Err("Task 2 failed")
}

async fn try_join_example() {
    match try_join!(fallible_task1(), fallible_task2()) {
        Ok((r1, r2)) => println!("Success: {} {}", r1, r2),
        Err(e) => println!("Error: {}", e),
    }
}
```

**Select! for Racing Futures:**
```rust
use tokio::select;
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    let mut delay1 = sleep(Duration::from_secs(1));
    let mut delay2 = sleep(Duration::from_secs(2));

    select! {
        _ = &mut delay1 => {
            println!("delay1 completed first");
        }
        _ = &mut delay2 => {
            println!("delay2 completed first");
        }
    }
}

// Select with channels
use tokio::sync::mpsc;

async fn select_channels() {
    let (tx1, mut rx1) = mpsc::channel(10);
    let (tx2, mut rx2) = mpsc::channel(10);

    loop {
        select! {
            Some(msg) = rx1.recv() => {
                println!("Received from channel 1: {}", msg);
            }
            Some(msg) = rx2.recv() => {
                println!("Received from channel 2: {}", msg);
            }
            else => break,
        }
    }
}
```

**Async Channels:**
```rust
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    // Create channel with capacity 32
    let (tx, mut rx) = mpsc::channel(32);

    // Spawn sender task
    tokio::spawn(async move {
        for i in 0..10 {
            tx.send(i).await.unwrap();
        }
    });

    // Receive messages
    while let Some(msg) = rx.recv().await {
        println!("Received: {}", msg);
    }
}

// Multiple producers, single consumer
async fn multiple_producers() {
    let (tx, mut rx) = mpsc::channel(32);

    for i in 0..3 {
        let tx_clone = tx.clone();
        tokio::spawn(async move {
            tx_clone.send(i).await.unwrap();
        });
    }

    drop(tx);  // Drop original sender

    while let Some(msg) = rx.recv().await {
        println!("Received: {}", msg);
    }
}
```

**Shared State with Arc and Mutex:**
```rust
use std::sync::Arc;
use tokio::sync::Mutex;

#[tokio::main]
async fn main() {
    let data = Arc::new(Mutex::new(0));

    let mut handles = vec![];

    for _ in 0..10 {
        let data_clone = Arc::clone(&data);
        let handle = tokio::spawn(async move {
            let mut num = data_clone.lock().await;
            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.await.unwrap();
    }

    println!("Result: {}", *data.lock().await);  // 10
}
```

**Async Traits (using async-trait):**
```rust
use async_trait::async_trait;

#[async_trait]
trait Repository {
    async fn get_user(&self, id: u64) -> Option<User>;
    async fn save_user(&self, user: User) -> Result<(), Error>;
}

struct DatabaseRepo {
    // fields
}

#[async_trait]
impl Repository for DatabaseRepo {
    async fn get_user(&self, id: u64) -> Option<User> {
        // Implementation
        None
    }

    async fn save_user(&self, user: User) -> Result<(), Error> {
        // Implementation
        Ok(())
    }
}
```

**Timeouts:**
```rust
use tokio::time::{timeout, Duration};

async fn fetch_with_timeout(url: &str) -> Result<String, Box<dyn std::error::Error>> {
    let result = timeout(
        Duration::from_secs(5),
        reqwest::get(url)
    ).await?;

    let response = result?;
    Ok(response.text().await?)
}

#[tokio::main]
async fn main() {
    match fetch_with_timeout("https://api.example.com").await {
        Ok(data) => println!("Success: {}", data),
        Err(e) => eprintln!("Timeout or error: {}", e),
    }
}
```

**Task Cancellation:**
```rust
use tokio::sync::oneshot;
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    let (cancel_tx, cancel_rx) = oneshot::channel();

    let task = tokio::spawn(async move {
        select! {
            _ = long_running_operation() => {
                println!("Completed");
            }
            _ = cancel_rx => {
                println!("Cancelled");
            }
        }
    });

    // Cancel after 2 seconds
    sleep(Duration::from_secs(2)).await;
    cancel_tx.send(()).unwrap();

    task.await.unwrap();
}

async fn long_running_operation() {
    sleep(Duration::from_secs(10)).await;
}
```

**Async Iteration:**
```rust
use tokio_stream::{self as stream, StreamExt};

#[tokio::main]
async fn main() {
    let mut stream = stream::iter(vec![1, 2, 3, 4, 5]);

    while let Some(value) = stream.next().await {
        println!("Value: {}", value);
    }
}

// Interval stream
use tokio::time::{interval, Duration};

async fn periodic_task() {
    let mut interval = interval(Duration::from_secs(1));

    for _ in 0..5 {
        interval.tick().await;
        println!("Tick");
    }
}
```

**Error Handling:**
```rust
use tokio::task::JoinError;

#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        panic!("Task panicked!");
    });

    match handle.await {
        Ok(_) => println!("Task completed"),
        Err(e) => {
            if e.is_panic() {
                println!("Task panicked");
            } else if e.is_cancelled() {
                println!("Task cancelled");
            }
        }
    }
}
```

**Blocking Operations:**
```rust
use tokio::task;

#[tokio::main]
async fn main() {
    // ✗ Bad: Blocks async runtime
    // let data = std::fs::read_to_string("file.txt").unwrap();

    // ✓ Good: Run blocking code in dedicated thread pool
    let data = task::spawn_blocking(|| {
        std::fs::read_to_string("file.txt")
    })
    .await
    .unwrap()
    .unwrap();

    println!("File content: {}", data);
}
```

**Resource Management:**
```rust
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::fs::File;

async fn read_file(path: &str) -> std::io::Result<String> {
    let mut file = File::open(path).await?;
    let mut contents = String::new();
    file.read_to_string(&mut contents).await?;
    Ok(contents)
}

async fn write_file(path: &str, content: &str) -> std::io::Result<()> {
    let mut file = File::create(path).await?;
    file.write_all(content.as_bytes()).await?;
    Ok(())
}
```

**Anti-Patterns to Avoid:**
```rust
// ✗ Don't block the runtime
async fn bad_blocking() {
    std::thread::sleep(std::time::Duration::from_secs(1));  // Blocks!
}

// ✓ Use async sleep
async fn good_sleep() {
    tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
}

// ✗ Don't create runtime inside async
async fn bad_nested_runtime() {
    let rt = tokio::runtime::Runtime::new().unwrap();  // Don't do this!
}

// ✓ Use the existing runtime
async fn good_spawn() {
    tokio::spawn(async {
        // Work here
    });
}

// ✗ Don't forget to await
async fn bad_no_await() {
    fetch_data("url");  // Future not awaited!
}

// ✓ Always await futures
async fn good_await() {
    fetch_data("url").await;
}
```
