---
metadata:
  name: "Rust Testing Strategies"
  activation_keywords: ["test", "unit test", "integration", "benchmark", "cargo"]
  category: "language-rust"
principles: ['U_TEST_FIRST', 'U_EVIDENCE_BASED', 'P_TEST_COVERAGE', 'P_TEST_PYRAMID', 'P_CI_GATES', 'P_PROPERTY_TESTING']
---

# Rust Testing Strategies

Master Rust testing with unit tests, integration tests, benchmarks, and property-based testing.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Test Types:**
- Unit tests: Test individual functions/modules (in same file)
- Integration tests: Test public API (in tests/ directory)
- Documentation tests: Examples in doc comments
- Benchmarks: Performance testing (criterion crate)
- Property tests: Random input testing (proptest crate)

**Key Patterns:**
1. Use `#[cfg(test)]` for test modules
2. Place integration tests in tests/ directory
3. Use `assert_eq!`, `assert_ne!`, `assert!` for assertions
4. Mock dependencies with traits
5. Use `#[should_panic]` for expected panics

**Test Organization:**
- Unit tests: Same file as code
- Integration tests: tests/ directory
- Test helpers: tests/common/mod.rs
- One integration test file per crate feature

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**Basic Unit Tests:**
```rust
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
        assert_eq!(add(-1, 1), 0);
        assert_eq!(add(0, 0), 0);
    }

    #[test]
    fn test_add_negative() {
        assert_eq!(add(-5, -3), -8);
    }
}
```

**Assertions:**
```rust
#[cfg(test)]
mod tests {
    #[test]
    fn test_assertions() {
        assert!(true);  // Boolean assertion
        assert!(!false);

        assert_eq!(2 + 2, 4);  // Equality
        assert_ne!(2 + 2, 5);  // Inequality

        // Custom message
        assert_eq!(
            2 + 2,
            4,
            "Math is broken: {} != {}",
            2 + 2,
            4
        );
    }

    #[test]
    #[should_panic]
    fn test_panic() {
        panic!("This test should panic");
    }

    #[test]
    #[should_panic(expected = "division by zero")]
    fn test_specific_panic() {
        let _ = 1 / 0;
    }
}
```

**Testing Results:**
```rust
fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        Err("Division by zero".to_string())
    } else {
        Ok(a / b)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_divide_success() -> Result<(), String> {
        let result = divide(10, 2)?;
        assert_eq!(result, 5);
        Ok(())
    }

    #[test]
    fn test_divide_error() {
        let result = divide(10, 0);
        assert!(result.is_err());
        assert_eq!(result.unwrap_err(), "Division by zero");
    }
}
```

**Integration Tests:**
```rust
// tests/integration_test.rs
use my_crate::public_function;

#[test]
fn test_public_api() {
    let result = public_function(42);
    assert_eq!(result, 84);
}

// Test with setup
#[test]
fn test_with_setup() {
    let config = setup_test_config();
    let result = process_with_config(&config);
    assert!(result.is_ok());
}

fn setup_test_config() -> Config {
    Config::default()
}
```

**Test Helpers:**
```rust
// tests/common/mod.rs
use my_crate::*;

pub fn setup() -> TestContext {
    TestContext {
        db: Database::in_memory(),
        config: Config::test_config(),
    }
}

pub struct TestContext {
    pub db: Database,
    pub config: Config,
}

// tests/my_test.rs
mod common;

#[test]
fn test_with_helpers() {
    let ctx = common::setup();
    // Use ctx in test
}
```

**Mocking with Traits:**
```rust
// Production code
pub trait Repository {
    fn get_user(&self, id: u32) -> Option<User>;
    fn save_user(&self, user: User) -> Result<(), Error>;
}

pub struct UserService<R: Repository> {
    repo: R,
}

impl<R: Repository> UserService<R> {
    pub fn update_name(&self, id: u32, name: String) -> Result<(), Error> {
        let mut user = self.repo.get_user(id).ok_or(Error::NotFound)?;
        user.name = name;
        self.repo.save_user(user)
    }
}

// Test code
#[cfg(test)]
mod tests {
    use super::*;

    struct MockRepository {
        users: std::collections::HashMap<u32, User>,
    }

    impl Repository for MockRepository {
        fn get_user(&self, id: u32) -> Option<User> {
            self.users.get(&id).cloned()
        }

        fn save_user(&self, user: User) -> Result<(), Error> {
            // Mock implementation
            Ok(())
        }
    }

    #[test]
    fn test_update_name() {
        let mut users = std::collections::HashMap::new();
        users.insert(1, User { id: 1, name: "Alice".to_string() });

        let mock_repo = MockRepository { users };
        let service = UserService { repo: mock_repo };

        let result = service.update_name(1, "Bob".to_string());
        assert!(result.is_ok());
    }
}
```

**Parameterized Tests (using rstest):**
```rust
use rstest::rstest;

#[rstest]
#[case(2, 3, 5)]
#[case(0, 0, 0)]
#[case(-1, 1, 0)]
#[case(100, 200, 300)]
fn test_add(#[case] a: i32, #[case] b: i32, #[case] expected: i32) {
    assert_eq!(add(a, b), expected);
}

// With fixtures
#[fixture]
fn sample_user() -> User {
    User {
        id: 1,
        name: "Alice".to_string(),
    }
}

#[rstest]
fn test_user_operations(sample_user: User) {
    assert_eq!(sample_user.id, 1);
}
```

**Benchmarking (criterion):**
```rust
// benches/my_benchmark.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion};
use my_crate::fibonacci;

fn fibonacci_benchmark(c: &mut Criterion) {
    c.bench_function("fib 20", |b| {
        b.iter(|| fibonacci(black_box(20)))
    });
}

criterion_group!(benches, fibonacci_benchmark);
criterion_main!(benches);
```

**Property-Based Testing (proptest):**
```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_add_commutative(a in 0..100, b in 0..100) {
        assert_eq!(add(a, b), add(b, a));
    }

    #[test]
    fn test_string_length(s in ".*") {
        let reversed = s.chars().rev().collect::<String>();
        assert_eq!(s.len(), reversed.len());
    }

    #[test]
    fn test_vec_push_pop(mut v in prop::collection::vec(0..100, 0..10)) {
        let original_len = v.len();
        v.push(42);
        assert_eq!(v.len(), original_len + 1);
        assert_eq!(v.pop(), Some(42));
        assert_eq!(v.len(), original_len);
    }
}
```

**Async Tests (tokio):**
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_async_function() {
        let result = fetch_data("https://api.example.com").await;
        assert!(result.is_ok());
    }

    #[tokio::test]
    async fn test_concurrent_operations() {
        let (result1, result2) = tokio::join!(
            fetch_data("url1"),
            fetch_data("url2")
        );

        assert!(result1.is_ok());
        assert!(result2.is_ok());
    }
}
```

**Test Organization:**
```rust
// src/lib.rs
pub mod math {
    pub fn add(a: i32, b: i32) -> i32 {
        a + b
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[test]
        fn test_add() {
            assert_eq!(add(2, 3), 5);
        }
    }
}

// Nested test modules
#[cfg(test)]
mod tests {
    use super::*;

    mod addition {
        use super::*;

        #[test]
        fn test_positive() {
            assert_eq!(add(2, 3), 5);
        }

        #[test]
        fn test_negative() {
            assert_eq!(add(-2, -3), -5);
        }
    }

    mod subtraction {
        use super::*;

        #[test]
        fn test_positive() {
            assert_eq!(subtract(5, 3), 2);
        }
    }
}
```

**Documentation Tests:**
```rust
/// Adds two numbers together.
///
/// # Examples
///
/// ```
/// use my_crate::add;
///
/// let result = add(2, 3);
/// assert_eq!(result, 5);
/// ```
///
/// # Panics
///
/// This function never panics.
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

/// Example that should fail to compile:
///
/// ```compile_fail
/// use my_crate::add;
/// add("string", 5);  // Type error
/// ```
pub fn compile_fail_example() {}
```

**Test Configuration:**
```rust
// Run tests in sequence
#[test]
#[serial]
fn test_sequential() {
    // Tests run one at a time
}

// Ignore slow tests by default
#[test]
#[ignore]
fn expensive_test() {
    // Run with: cargo test -- --ignored
}

// Conditional compilation
#[test]
#[cfg(target_os = "linux")]
fn linux_only_test() {
    // Only runs on Linux
}
```

**Coverage (with tarpaulin):**
```bash
# Install tarpaulin
cargo install cargo-tarpaulin

# Run coverage
cargo tarpaulin --out Html

# With specific test filter
cargo tarpaulin --test integration_test

# Exclude files
cargo tarpaulin --exclude-files 'tests/*'
```

**Running Tests:**
```bash
# Run all tests
cargo test

# Run specific test
cargo test test_add

# Run tests in package
cargo test --package my_crate

# Run with output
cargo test -- --nocapture

# Run ignored tests
cargo test -- --ignored

# Run single-threaded
cargo test -- --test-threads=1

# Run benchmarks
cargo bench

# Integration tests only
cargo test --test integration_test
```

**Anti-Patterns to Avoid:**
```rust
// ✗ Don't test private implementation details
#[test]
fn test_internal_state() {
    let obj = MyStruct::new();
    assert_eq!(obj.internal_counter, 0);  // Fragile
}

// ✓ Test public behavior
#[test]
fn test_public_api() {
    let obj = MyStruct::new();
    assert_eq!(obj.count(), 0);  // Stable API
}

// ✗ Don't use unwrap in tests
#[test]
fn bad_test() {
    let result = function_that_might_fail().unwrap();  // Unclear error
}

// ✓ Use proper assertions
#[test]
fn good_test() {
    let result = function_that_might_fail();
    assert!(result.is_ok());
    assert_eq!(result.unwrap(), expected_value);
}

// ✗ Don't share mutable state
static mut COUNTER: i32 = 0;  // Unsafe and unreliable

#[test]
fn bad_shared_state() {
    unsafe { COUNTER += 1; }
}

// ✓ Use isolated test data
#[test]
fn good_isolated() {
    let counter = 0;
    // Test with local state
}
```
