---
metadata:
  name: "Go Error Handling"
  activation_keywords: ["error", "wrap", "sentinel", "errors", "fmt"]
  category: "language-go"
---

# Go Error Handling

Master Go's error handling patterns with wrapping, sentinel errors, and custom error types.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Error Basics:**
- Errors are values (implement error interface)
- Return errors as last return value
- Check errors explicitly (no exceptions)
- Use `errors.New()` for simple errors
- Use `fmt.Errorf()` for formatted errors

**Key Patterns:**
1. Always check returned errors
2. Wrap errors with context using %w
3. Use sentinel errors for expected conditions
4. Create custom error types for complex cases
5. Use errors.Is() and errors.As() for checking

**Error Wrapping (Go 1.13+):**
- `fmt.Errorf("context: %w", err)` wraps error
- `errors.Is(err, target)` checks error chain
- `errors.As(err, &target)` extracts error type

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**Basic Error Handling:**
```go
package main

import (
    "errors"
    "fmt"
)

func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

func main() {
    result, err := divide(10, 0)
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    fmt.Println("Result:", result)
}

// Formatted errors
func validateAge(age int) error {
    if age < 0 {
        return fmt.Errorf("invalid age: %d (must be non-negative)", age)
    }
    return nil
}
```

**Error Wrapping:**
```go
import (
    "errors"
    "fmt"
)

func readConfig(path string) (*Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("failed to read config: %w", err)
    }

    var config Config
    if err := json.Unmarshal(data, &config); err != nil {
        return nil, fmt.Errorf("failed to parse config: %w", err)
    }

    return &config, nil
}

func main() {
    config, err := readConfig("config.json")
    if err != nil {
        fmt.Println("Error:", err)
        // Output: Error: failed to parse config: invalid character...
        return
    }
}
```

**Sentinel Errors:**
```go
import "errors"

var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrInvalidInput = errors.New("invalid input")
)

func getUser(id int) (*User, error) {
    if id < 0 {
        return nil, ErrInvalidInput
    }

    user, exists := database[id]
    if !exists {
        return nil, ErrNotFound
    }

    return user, nil
}

func main() {
    user, err := getUser(42)
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            fmt.Println("User not found")
        } else if errors.Is(err, ErrInvalidInput) {
            fmt.Println("Invalid user ID")
        }
        return
    }

    fmt.Println("User:", user.Name)
}
```

**Custom Error Types:**
```go
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error on field %s: %s", e.Field, e.Message)
}

func validateUser(user *User) error {
    if user.Name == "" {
        return &ValidationError{
            Field:   "name",
            Message: "cannot be empty",
        }
    }

    if user.Age < 0 {
        return &ValidationError{
            Field:   "age",
            Message: "must be non-negative",
        }
    }

    return nil
}

// Check error type with errors.As
func main() {
    user := &User{Name: "", Age: 25}
    err := validateUser(user)

    if err != nil {
        var validationErr *ValidationError
        if errors.As(err, &validationErr) {
            fmt.Printf("Field %s: %s\n",
                validationErr.Field,
                validationErr.Message)
        } else {
            fmt.Println("Unknown error:", err)
        }
    }
}
```

**Error Chain with Unwrap:**
```go
type QueryError struct {
    Query string
    Err   error
}

func (e *QueryError) Error() string {
    return fmt.Sprintf("query failed: %s", e.Query)
}

func (e *QueryError) Unwrap() error {
    return e.Err
}

func executeQuery(query string) error {
    err := database.Execute(query)
    if err != nil {
        return &QueryError{
            Query: query,
            Err:   err,
        }
    }
    return nil
}

func main() {
    err := executeQuery("SELECT * FROM users")
    if err != nil {
        // Can check wrapped error
        if errors.Is(err, sql.ErrNoRows) {
            fmt.Println("No rows found")
        }

        // Can extract QueryError
        var queryErr *QueryError
        if errors.As(err, &queryErr) {
            fmt.Println("Failed query:", queryErr.Query)
        }
    }
}
```

**Multiple Return Values:**
```go
// Return value and error
func parseNumber(s string) (int, error) {
    n, err := strconv.Atoi(s)
    if err != nil {
        return 0, fmt.Errorf("failed to parse %q: %w", s, err)
    }
    return n, nil
}

// Multiple values with error
func getUserProfile(id int) (*User, *Profile, error) {
    user, err := getUser(id)
    if err != nil {
        return nil, nil, fmt.Errorf("get user: %w", err)
    }

    profile, err := getProfile(id)
    if err != nil {
        return nil, nil, fmt.Errorf("get profile: %w", err)
    }

    return user, profile, nil
}
```

**Defer for Cleanup:**
```go
func writeFile(path string, data []byte) error {
    file, err := os.Create(path)
    if err != nil {
        return fmt.Errorf("create file: %w", err)
    }
    defer file.Close()  // Always close, even on error

    if _, err := file.Write(data); err != nil {
        return fmt.Errorf("write data: %w", err)
    }

    return nil
}

// Handle error from defer
func writeFileWithDeferError(path string, data []byte) (err error) {
    file, err := os.Create(path)
    if err != nil {
        return fmt.Errorf("create file: %w", err)
    }

    defer func() {
        if closeErr := file.Close(); closeErr != nil && err == nil {
            err = fmt.Errorf("close file: %w", closeErr)
        }
    }()

    if _, err = file.Write(data); err != nil {
        return fmt.Errorf("write data: %w", err)
    }

    return nil
}
```

**Error Handling Patterns:**
```go
// Early return pattern
func processUser(id int) error {
    user, err := getUser(id)
    if err != nil {
        return err
    }

    if err := validateUser(user); err != nil {
        return err
    }

    if err := saveUser(user); err != nil {
        return err
    }

    return nil
}

// Error aggregation
type Errors []error

func (e Errors) Error() string {
    var msgs []string
    for _, err := range e {
        msgs = append(msgs, err.Error())
    }
    return strings.Join(msgs, "; ")
}

func validateAll(users []*User) error {
    var errs Errors

    for _, user := range users {
        if err := validateUser(user); err != nil {
            errs = append(errs, err)
        }
    }

    if len(errs) > 0 {
        return errs
    }

    return nil
}
```

**Panic vs Error:**
```go
// Use errors for expected failures
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// Use panic for programmer errors (invariant violations)
func processSlice(data []int, index int) {
    if index < 0 || index >= len(data) {
        panic("index out of bounds")  // Should never happen
    }
    // Process data[index]
}

// Recover from panic if needed
func safeProcess() (err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("panic recovered: %v", r)
        }
    }()

    // Code that might panic
    riskyOperation()
    return nil
}
```

**Error Logging:**
```go
import "log"

func processRequest(req *Request) error {
    user, err := getUser(req.UserID)
    if err != nil {
        log.Printf("Failed to get user %d: %v", req.UserID, err)
        return fmt.Errorf("get user: %w", err)
    }

    // Process user
    return nil
}

// Structured logging
import "github.com/sirupsen/logrus"

func processWithStructuredLogging(req *Request) error {
    user, err := getUser(req.UserID)
    if err != nil {
        logrus.WithFields(logrus.Fields{
            "user_id": req.UserID,
            "error":   err,
        }).Error("Failed to get user")
        return fmt.Errorf("get user: %w", err)
    }

    return nil
}
```

**Error Context:**
```go
type contextError struct {
    op  string  // Operation
    err error   // Underlying error
}

func (e *contextError) Error() string {
    return fmt.Sprintf("%s: %v", e.op, e.err)
}

func (e *contextError) Unwrap() error {
    return e.err
}

func operation(name string, fn func() error) error {
    if err := fn(); err != nil {
        return &contextError{
            op:  name,
            err: err,
        }
    }
    return nil
}

func example() error {
    return operation("fetch user", func() error {
        return operation("query database", func() error {
            return errors.New("connection failed")
        })
    })
}
// Error chain: fetch user: query database: connection failed
```

**Testing Errors:**
```go
import "testing"

func TestDivide(t *testing.T) {
    tests := []struct {
        name    string
        a, b    float64
        want    float64
        wantErr bool
    }{
        {"valid", 10, 2, 5, false},
        {"division by zero", 10, 0, 0, true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := divide(tt.a, tt.b)
            if (err != nil) != tt.wantErr {
                t.Errorf("divide() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("divide() = %v, want %v", got, tt.want)
            }
        })
    }
}

// Test error types
func TestValidationError(t *testing.T) {
    user := &User{Name: ""}
    err := validateUser(user)

    var validationErr *ValidationError
    if !errors.As(err, &validationErr) {
        t.Fatal("expected ValidationError")
    }

    if validationErr.Field != "name" {
        t.Errorf("got field %q, want %q", validationErr.Field, "name")
    }
}
```

**Anti-Patterns to Avoid:**
```go
// ✗ Don't ignore errors
func badIgnore() {
    file, _ := os.Open("file.txt")  // Ignoring error!
    defer file.Close()
}

// ✓ Handle errors
func goodHandle() error {
    file, err := os.Open("file.txt")
    if err != nil {
        return fmt.Errorf("open file: %w", err)
    }
    defer file.Close()
    return nil
}

// ✗ Don't panic for normal errors
func badPanic(id int) *User {
    user, err := getUser(id)
    if err != nil {
        panic(err)  // Bad!
    }
    return user
}

// ✓ Return errors
func goodReturn(id int) (*User, error) {
    return getUser(id)
}

// ✗ Don't lose error context
func badContext() error {
    _, err := doSomething()
    if err != nil {
        return errors.New("operation failed")  // Lost original error
    }
    return nil
}

// ✓ Wrap errors
func goodContext() error {
    _, err := doSomething()
    if err != nil {
        return fmt.Errorf("operation failed: %w", err)
    }
    return nil
}
```
