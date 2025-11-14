---
metadata:
  name: "Rust Error Handling"
  activation_keywords: ["error", "result", "option", "unwrap", "propagate"]
  category: "language-rust"
principles: ['U_FAIL_FAST', 'U_ROOT_CAUSE_ANALYSIS', 'P_TYPE_SAFETY', 'U_EVIDENCE_BASED']
---

# Rust Error Handling

Master Rust's error handling with Result, Option, and custom error types for robust applications.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Error Handling Types:**
- `Result<T, E>`: For recoverable errors (Ok or Err)
- `Option<T>`: For optional values (Some or None)
- `?` operator: Propagate errors up the call stack
- `unwrap()`/`expect()`: For prototyping (panics on error)
- Custom error types: Domain-specific errors

**Key Patterns:**
1. Return Result for fallible operations
2. Use ? operator for error propagation
3. Use match or if let for error handling
4. Create custom error types with thiserror or anyhow
5. Use Option for values that may not exist

**Best Practices:**
- Avoid unwrap() in production code
- Provide context with custom error types
- Use anyhow for applications, thiserror for libraries
- Implement From trait for error conversion

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**Basic Result Usage:**
```rust
use std::fs::File;
use std::io::{self, Read};

fn read_file(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?;  // Propagate error
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;  // Propagate error
    Ok(contents)
}

fn main() {
    match read_file("file.txt") {
        Ok(contents) => println!("File: {}", contents),
        Err(e) => eprintln!("Error: {}", e),
    }
}
```

**Option Usage:**
```rust
fn find_user(id: u32) -> Option<User> {
    if id == 1 {
        Some(User { id, name: "Alice".to_string() })
    } else {
        None
    }
}

fn main() {
    match find_user(1) {
        Some(user) => println!("Found: {}", user.name),
        None => println!("User not found"),
    }

    // Using if let
    if let Some(user) = find_user(1) {
        println!("Found: {}", user.name);
    }

    // Using map
    let name = find_user(1)
        .map(|u| u.name)
        .unwrap_or_else(|| "Unknown".to_string());
}
```

**? Operator:**
```rust
use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?;
    let mut username = String::new();
    file.read_to_string(&mut username)?;
    Ok(username)
}

// Chained with methods
fn read_username_short(path: &str) -> Result<String, io::Error> {
    let mut username = String::new();
    File::open(path)?.read_to_string(&mut username)?;
    Ok(username)
}

// Even shorter with fs::read_to_string
fn read_username_shortest(path: &str) -> Result<String, io::Error> {
    std::fs::read_to_string(path)
}
```

**Custom Error Types (thiserror):**
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("User not found: {0}")]
    UserNotFound(u32),

    #[error("Invalid input: {0}")]
    InvalidInput(String),

    #[error("Database error")]
    DatabaseError(#[from] sqlx::Error),

    #[error("I/O error")]
    IoError(#[from] std::io::Error),
}

fn get_user(id: u32) -> Result<User, AppError> {
    if id == 0 {
        return Err(AppError::InvalidInput("ID cannot be 0".to_string()));
    }

    database_query(id)
        .map_err(|_| AppError::UserNotFound(id))
}

fn main() {
    match get_user(0) {
        Ok(user) => println!("User: {:?}", user),
        Err(AppError::UserNotFound(id)) => eprintln!("User {} not found", id),
        Err(AppError::InvalidInput(msg)) => eprintln!("Invalid: {}", msg),
        Err(e) => eprintln!("Error: {}", e),
    }
}
```

**Application Errors (anyhow):**
```rust
use anyhow::{Context, Result};

fn process_config(path: &str) -> Result<Config> {
    let contents = std::fs::read_to_string(path)
        .context("Failed to read config file")?;

    let config: Config = serde_json::from_str(&contents)
        .context("Failed to parse config")?;

    Ok(config)
}

fn main() -> Result<()> {
    let config = process_config("config.json")?;
    println!("Config loaded: {:?}", config);
    Ok(())
}

// With additional context
fn fetch_data(url: &str) -> Result<String> {
    reqwest::blocking::get(url)
        .context(format!("Failed to fetch {}", url))?
        .text()
        .context("Failed to read response body")
}
```

**Error Conversion:**
```rust
use std::num::ParseIntError;

#[derive(Debug)]
enum MyError {
    Parse(ParseIntError),
    Validation(String),
}

impl From<ParseIntError> for MyError {
    fn from(e: ParseIntError) -> Self {
        MyError::Parse(e)
    }
}

fn parse_and_validate(s: &str) -> Result<i32, MyError> {
    let num: i32 = s.parse()?;  // Automatically converts ParseIntError

    if num < 0 {
        return Err(MyError::Validation("Number must be positive".to_string()));
    }

    Ok(num)
}
```

**Combinators:**
```rust
fn main() {
    let num: Option<i32> = Some(42);

    // map: Transform value inside Option
    let doubled = num.map(|n| n * 2);  // Some(84)

    // and_then: Chain operations
    let result = num.and_then(|n| {
        if n > 0 { Some(n * 2) } else { None }
    });

    // or: Provide alternative
    let value = None.or(Some(10));  // Some(10)

    // unwrap_or: Provide default
    let value = None.unwrap_or(0);  // 0

    // unwrap_or_else: Compute default
    let value = None.unwrap_or_else(|| expensive_computation());

    // ok_or: Convert Option to Result
    let result: Result<i32, &str> = num.ok_or("No value");
}

// Result combinators
fn result_combinators() {
    let result: Result<i32, &str> = Ok(42);

    // map: Transform Ok value
    let doubled = result.map(|n| n * 2);  // Ok(84)

    // map_err: Transform Err value
    let result = result.map_err(|e| format!("Error: {}", e));

    // and_then: Chain fallible operations
    let result = result.and_then(|n| {
        if n > 0 { Ok(n * 2) } else { Err("Negative") }
    });
}
```

**Early Returns:**
```rust
fn validate_user(user: &User) -> Result<(), String> {
    if user.name.is_empty() {
        return Err("Name cannot be empty".to_string());
    }

    if user.age < 18 {
        return Err("User must be 18 or older".to_string());
    }

    if user.email.is_empty() {
        return Err("Email is required".to_string());
    }

    Ok(())
}
```

**Multiple Error Types:**
```rust
use std::error::Error;

fn process() -> Result<(), Box<dyn Error>> {
    let file = std::fs::read_to_string("file.txt")?;  // io::Error
    let num: i32 = file.trim().parse()?;  // ParseIntError
    println!("Number: {}", num);
    Ok(())
}

// Or use anyhow
use anyhow::Result;

fn process_anyhow() -> Result<()> {
    let file = std::fs::read_to_string("file.txt")?;
    let num: i32 = file.trim().parse()?;
    println!("Number: {}", num);
    Ok(())
}
```

**Pattern Matching:**
```rust
fn handle_result(result: Result<i32, String>) {
    match result {
        Ok(value) if value > 0 => println!("Positive: {}", value),
        Ok(value) if value < 0 => println!("Negative: {}", value),
        Ok(_) => println!("Zero"),
        Err(e) => eprintln!("Error: {}", e),
    }
}

// Nested Result/Option
fn handle_nested(result: Result<Option<i32>, String>) {
    match result {
        Ok(Some(value)) => println!("Value: {}", value),
        Ok(None) => println!("No value"),
        Err(e) => eprintln!("Error: {}", e),
    }
}
```

**Try Blocks (unstable):**
```rust
// #![feature(try_blocks)]

fn try_block_example() {
    let result: Result<i32, Box<dyn Error>> = try {
        let file = std::fs::read_to_string("file.txt")?;
        let num: i32 = file.trim().parse()?;
        num * 2
    };

    match result {
        Ok(n) => println!("Result: {}", n),
        Err(e) => eprintln!("Error: {}", e),
    }
}
```

**Logging Errors:**
```rust
use log::{error, warn};

fn process_with_logging(id: u32) -> Result<User, AppError> {
    match get_user(id) {
        Ok(user) => Ok(user),
        Err(e) => {
            error!("Failed to get user {}: {}", id, e);
            Err(e)
        }
    }
}

// Or use context with anyhow
use anyhow::{Context, Result};

fn process_with_context(id: u32) -> Result<User> {
    get_user(id).context(format!("Failed to get user {}", id))
}
```

**Panic vs Error:**
```rust
// ✗ Panic for unrecoverable errors
fn divide_panic(a: i32, b: i32) -> i32 {
    if b == 0 {
        panic!("Division by zero");
    }
    a / b
}

// ✓ Result for recoverable errors
fn divide_result(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        return Err("Division by zero".to_string());
    }
    Ok(a / b)
}

// Unwrap for prototyping only
fn prototype() {
    let value = get_value().unwrap();  // OK for prototyping
}

// Expect with message for better debugging
fn with_expect() {
    let value = get_value().expect("Failed to get value");
}
```

**Error Recovery:**
```rust
fn fetch_with_retry(url: &str, max_attempts: u32) -> Result<String, Error> {
    let mut attempts = 0;

    loop {
        attempts += 1;

        match fetch(url) {
            Ok(data) => return Ok(data),
            Err(e) if attempts < max_attempts => {
                eprintln!("Attempt {} failed: {}", attempts, e);
                std::thread::sleep(std::time::Duration::from_secs(1));
            }
            Err(e) => return Err(e),
        }
    }
}
```

**Anti-Patterns to Avoid:**
```rust
// ✗ Don't ignore errors
fn bad_ignore() {
    let _ = std::fs::read_to_string("file.txt");  // Error ignored
}

// ✓ Handle errors
fn good_handle() -> Result<(), std::io::Error> {
    std::fs::read_to_string("file.txt")?;
    Ok(())
}

// ✗ Don't use unwrap() in production
fn bad_unwrap() {
    let value = get_value().unwrap();  // Can panic!
}

// ✓ Use proper error handling
fn good_match() {
    match get_value() {
        Ok(value) => process(value),
        Err(e) => eprintln!("Error: {}", e),
    }
}

// ✗ Don't create untyped errors
fn bad_error() -> Result<(), Box<dyn Error>> {
    // Hard to handle specific errors
}

// ✓ Use typed errors
fn good_error() -> Result<(), AppError> {
    // Easy to match on specific error types
}
```
