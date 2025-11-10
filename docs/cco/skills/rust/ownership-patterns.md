---
metadata:
  name: "Rust Ownership Patterns"
  activation_keywords: ["ownership", "borrow", "lifetime", "reference", "move"]
  category: "language-rust"
---

# Rust Ownership Patterns

Master Rust's ownership, borrowing, and lifetime system for memory-safe code without garbage collection.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Ownership Rules:**
- Each value has exactly one owner
- When owner goes out of scope, value is dropped
- Values are moved by default (not copied)
- References allow borrowing without ownership transfer
- Only one mutable reference OR many immutable references

**Key Patterns:**
1. Use references (&T) for read-only access
2. Use mutable references (&mut T) for write access
3. Clone only when necessary (expensive)
4. Use lifetime annotations for complex references
5. Leverage smart pointers (Box, Rc, Arc) for shared ownership

**Borrowing Types:**
- Immutable borrow: &T (multiple allowed)
- Mutable borrow: &mut T (exclusive access)
- Owned: T (transfer ownership)

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**Basic Ownership:**
```rust
fn main() {
    // s1 owns the String
    let s1 = String::from("hello");

    // Ownership moved to s2
    let s2 = s1;

    // Error: s1 no longer valid
    // println!("{}", s1);

    // s2 is valid
    println!("{}", s2);

    // Function takes ownership
    takes_ownership(s2);

    // Error: s2 no longer valid
    // println!("{}", s2);
}

fn takes_ownership(s: String) {
    println!("{}", s);
}  // s dropped here
```

**Borrowing with References:**
```rust
fn main() {
    let s = String::from("hello");

    // Borrow s (no ownership transfer)
    let len = calculate_length(&s);

    // s still valid
    println!("Length of '{}' is {}", s, len);
}

fn calculate_length(s: &String) -> usize {
    s.len()
}  // s reference dropped, but String not dropped
```

**Mutable References:**
```rust
fn main() {
    let mut s = String::from("hello");

    // Mutable borrow
    change(&mut s);

    println!("{}", s);  // "hello, world"
}

fn change(s: &mut String) {
    s.push_str(", world");
}

// Multiple mutable borrows - Error!
fn bad_example() {
    let mut s = String::from("hello");

    let r1 = &mut s;
    let r2 = &mut s;  // Error: cannot borrow as mutable twice

    println!("{}, {}", r1, r2);
}

// Multiple immutable borrows - OK!
fn good_example() {
    let s = String::from("hello");

    let r1 = &s;
    let r2 = &s;  // OK: multiple immutable borrows allowed

    println!("{}, {}", r1, r2);
}
```

**Lifetime Annotations:**
```rust
// Lifetime 'a ensures returned reference lives as long as inputs
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

// Lifetime in struct
struct Book<'a> {
    title: &'a str,
    author: &'a str,
}

impl<'a> Book<'a> {
    fn new(title: &'a str, author: &'a str) -> Self {
        Book { title, author }
    }
}

// Multiple lifetimes
fn complex<'a, 'b>(x: &'a str, y: &'b str) -> &'a str {
    // Return value tied to 'a lifetime
    x
}

// Static lifetime (lives for entire program)
fn get_static() -> &'static str {
    "I live forever"
}
```

**Lifetime Elision Rules:**
```rust
// Explicit lifetime (verbose)
fn first_word_explicit<'a>(s: &'a str) -> &'a str {
    s.split_whitespace().next().unwrap_or("")
}

// Implicit lifetime (compiler infers)
fn first_word(s: &str) -> &str {
    s.split_whitespace().next().unwrap_or("")
}

// Rule 1: Each input reference gets its own lifetime
// Rule 2: If one input lifetime, output gets that lifetime
// Rule 3: If &self or &mut self, output gets self's lifetime
```

**Smart Pointers:**
```rust
use std::rc::Rc;
use std::sync::Arc;
use std::cell::RefCell;

// Box: Heap allocation, single owner
fn use_box() {
    let b = Box::new(5);
    println!("b = {}", b);
}

// Rc: Reference counted (single-threaded)
fn use_rc() {
    let a = Rc::new(String::from("hello"));
    let b = Rc::clone(&a);  // Increment count
    let c = Rc::clone(&a);  // Increment count

    println!("Count: {}", Rc::strong_count(&a));  // 3
}

// Arc: Atomic reference counted (thread-safe)
use std::thread;

fn use_arc() {
    let data = Arc::new(vec![1, 2, 3]);

    let data1 = Arc::clone(&data);
    let handle1 = thread::spawn(move || {
        println!("{:?}", data1);
    });

    let data2 = Arc::clone(&data);
    let handle2 = thread::spawn(move || {
        println!("{:?}", data2);
    });

    handle1.join().unwrap();
    handle2.join().unwrap();
}

// RefCell: Interior mutability (runtime borrow checking)
fn use_refcell() {
    let data = RefCell::new(5);

    {
        let mut borrowed = data.borrow_mut();
        *borrowed += 1;
    }  // Mutable borrow dropped

    println!("{}", data.borrow());  // 6
}
```

**Common Patterns:**
```rust
// Pattern: Return owned value
fn create_string() -> String {
    String::from("hello")
}

// Pattern: Accept reference
fn process_string(s: &str) {
    println!("{}", s);
}

// Pattern: Modify in place
fn append_world(s: &mut String) {
    s.push_str(" world");
}

// Pattern: Clone when needed
fn duplicate(s: &String) -> String {
    s.clone()
}

// Pattern: Use slice for flexibility
fn count_words(text: &str) -> usize {
    text.split_whitespace().count()
}

fn example_usage() {
    let s = String::from("hello");
    process_string(&s);  // &String coerces to &str

    let slice = &s[0..2];
    process_string(slice);
}
```

**Ownership with Collections:**
```rust
fn main() {
    let mut v = vec![1, 2, 3];

    // Borrow immutably
    for n in &v {
        println!("{}", n);
    }

    // Borrow mutably
    for n in &mut v {
        *n += 1;
    }

    // Take ownership (consumes vector)
    for n in v {
        println!("{}", n);
    }

    // Error: v no longer valid
    // println!("{:?}", v);
}
```

**Avoiding Common Pitfalls:**
```rust
// ✗ Dangling reference
fn bad_dangle() -> &String {
    let s = String::from("hello");
    &s  // Error: s dropped at end of function
}

// ✓ Return owned value
fn good_no_dangle() -> String {
    let s = String::from("hello");
    s  // Ownership transferred
}

// ✗ Modifying while iterating
fn bad_modify() {
    let mut v = vec![1, 2, 3];
    for n in &v {
        v.push(*n);  // Error: cannot borrow as mutable
    }
}

// ✓ Collect to new vector
fn good_modify() {
    let v = vec![1, 2, 3];
    let doubled: Vec<i32> = v.iter().map(|n| n * 2).collect();
}
```

**Move Semantics:**
```rust
#[derive(Debug)]
struct Person {
    name: String,
    age: u32,
}

fn main() {
    let p1 = Person {
        name: String::from("Alice"),
        age: 30,
    };

    // Move (not copy)
    let p2 = p1;

    // Error: p1 moved
    // println!("{:?}", p1);

    println!("{:?}", p2);
}

// Implement Copy for simple types
#[derive(Debug, Copy, Clone)]
struct Point {
    x: i32,
    y: i32,
}

fn copy_example() {
    let p1 = Point { x: 0, y: 0 };
    let p2 = p1;  // Copy (not move)

    println!("{:?}", p1);  // Still valid
    println!("{:?}", p2);
}
```

**Slice Patterns:**
```rust
fn split_at_mut(slice: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
    let len = slice.len();
    assert!(mid <= len);

    let ptr = slice.as_mut_ptr();

    unsafe {
        (
            std::slice::from_raw_parts_mut(ptr, mid),
            std::slice::from_raw_parts_mut(ptr.add(mid), len - mid),
        )
    }
}
```

**Interior Mutability Pattern:**
```rust
use std::cell::Cell;
use std::cell::RefCell;

// Cell: Copy types only
struct Counter {
    count: Cell<i32>,
}

impl Counter {
    fn new() -> Self {
        Counter { count: Cell::new(0) }
    }

    fn increment(&self) {
        self.count.set(self.count.get() + 1);
    }

    fn get(&self) -> i32 {
        self.count.get()
    }
}

// RefCell: Any type, runtime borrow checking
struct Data {
    values: RefCell<Vec<i32>>,
}

impl Data {
    fn add(&self, value: i32) {
        self.values.borrow_mut().push(value);
    }
}
```

**Anti-Patterns to Avoid:**
```rust
// ✗ Don't clone unnecessarily
fn bad_clone(s: &String) -> usize {
    let copy = s.clone();  // Expensive!
    copy.len()
}

// ✓ Use reference
fn good_borrow(s: &String) -> usize {
    s.len()
}

// ✗ Don't use String when &str works
fn bad_param(s: String) -> usize {
    s.len()
}

// ✓ Accept &str (works with both String and &str)
fn good_param(s: &str) -> usize {
    s.len()
}
```
