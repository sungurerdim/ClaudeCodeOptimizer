---
metadata:
  name: "Go Testing Strategies"
  activation_keywords: ["test", "table driven", "subtest", "testing", "benchmark"]
  category: "language-go"
principles: ['U_TEST_FIRST', 'U_EVIDENCE_BASED', 'P_TEST_COVERAGE', 'P_TEST_PYRAMID', 'P_CI_GATES', 'P_TEST_ISOLATION']
---

# Go Testing Strategies

Master Go testing with table-driven tests, subtests, benchmarks, and testing best practices.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Testing Basics:**
- Test files end with `_test.go`
- Test functions start with `Test` prefix
- Use `t *testing.T` for test control
- Run with `go test`
- Benchmarks start with `Benchmark` prefix

**Key Patterns:**
1. Use table-driven tests for multiple cases
2. Organize tests with subtests (t.Run)
3. Use testdata/ directory for fixtures
4. Mock dependencies with interfaces
5. Write benchmarks for performance testing

**Test Organization:**
- Unit tests: Same package as code
- Integration tests: Separate package with _test suffix
- Test helpers: Use testing.TB interface
- Setup/teardown: Use TestMain for package-level

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**Basic Tests:**
```go
package math

import "testing"

func TestAdd(t *testing.T) {
    result := Add(2, 3)
    expected := 5

    if result != expected {
        t.Errorf("Add(2, 3) = %d; want %d", result, expected)
    }
}

// Multiple assertions
func TestDivide(t *testing.T) {
    result, err := Divide(10, 2)
    if err != nil {
        t.Fatalf("Divide(10, 2) returned error: %v", err)
    }

    if result != 5 {
        t.Errorf("Divide(10, 2) = %f; want 5", result)
    }
}

// Test expected error
func TestDivideByZero(t *testing.T) {
    _, err := Divide(10, 0)
    if err == nil {
        t.Error("Divide(10, 0) should return error")
    }
}
```

**Table-Driven Tests:**
```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 2, 3, 5},
        {"negative", -1, -2, -3},
        {"zero", 0, 0, 0},
        {"mixed", -5, 10, 5},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}

// Table-driven with errors
func TestDivide(t *testing.T) {
    tests := []struct {
        name      string
        a, b      float64
        want      float64
        wantError bool
    }{
        {"valid", 10, 2, 5, false},
        {"zero dividend", 0, 5, 0, false},
        {"division by zero", 10, 0, 0, true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Divide(tt.a, tt.b)

            if tt.wantError {
                if err == nil {
                    t.Error("expected error, got nil")
                }
                return
            }

            if err != nil {
                t.Errorf("unexpected error: %v", err)
            }

            if got != tt.want {
                t.Errorf("got %f, want %f", got, tt.want)
            }
        })
    }
}
```

**Subtests:**
```go
func TestUserOperations(t *testing.T) {
    // Setup
    db := setupTestDB(t)
    defer db.Close()

    t.Run("Create", func(t *testing.T) {
        user := &User{Name: "Alice"}
        err := db.Create(user)
        if err != nil {
            t.Fatalf("Create failed: %v", err)
        }
        if user.ID == 0 {
            t.Error("ID not set after create")
        }
    })

    t.Run("Get", func(t *testing.T) {
        user, err := db.Get(1)
        if err != nil {
            t.Fatalf("Get failed: %v", err)
        }
        if user.Name != "Alice" {
            t.Errorf("got name %q, want %q", user.Name, "Alice")
        }
    })

    t.Run("Update", func(t *testing.T) {
        user := &User{ID: 1, Name: "Bob"}
        err := db.Update(user)
        if err != nil {
            t.Fatalf("Update failed: %v", err)
        }
    })

    t.Run("Delete", func(t *testing.T) {
        err := db.Delete(1)
        if err != nil {
            t.Fatalf("Delete failed: %v", err)
        }
    })
}
```

**Test Helpers:**
```go
// Helper for creating test users
func createTestUser(t *testing.T, name string) *User {
    t.Helper()  // Mark as helper for better error messages

    user := &User{Name: name}
    if err := db.Create(user); err != nil {
        t.Fatalf("failed to create test user: %v", err)
    }

    return user
}

// Helper for cleanup
func cleanup(t *testing.T, db *Database) {
    t.Helper()
    t.Cleanup(func() {
        if err := db.Close(); err != nil {
            t.Errorf("cleanup failed: %v", err)
        }
    })
}

// Usage
func TestWithHelpers(t *testing.T) {
    db := setupTestDB(t)
    cleanup(t, db)

    user := createTestUser(t, "Alice")
    // Test with user
}
```

**Mocking with Interfaces:**
```go
// Interface for dependency
type UserRepository interface {
    GetUser(id int) (*User, error)
    SaveUser(user *User) error
}

// Service using interface
type UserService struct {
    repo UserRepository
}

func (s *UserService) UpdateName(id int, name string) error {
    user, err := s.repo.GetUser(id)
    if err != nil {
        return err
    }

    user.Name = name
    return s.repo.SaveUser(user)
}

// Mock implementation for testing
type mockUserRepository struct {
    users map[int]*User
}

func (m *mockUserRepository) GetUser(id int) (*User, error) {
    user, exists := m.users[id]
    if !exists {
        return nil, ErrNotFound
    }
    return user, nil
}

func (m *mockUserRepository) SaveUser(user *User) error {
    m.users[user.ID] = user
    return nil
}

// Test with mock
func TestUpdateName(t *testing.T) {
    mock := &mockUserRepository{
        users: map[int]*User{
            1: {ID: 1, Name: "Alice"},
        },
    }

    service := &UserService{repo: mock}

    err := service.UpdateName(1, "Bob")
    if err != nil {
        t.Fatalf("UpdateName failed: %v", err)
    }

    user, _ := mock.GetUser(1)
    if user.Name != "Bob" {
        t.Errorf("name = %q, want %q", user.Name, "Bob")
    }
}
```

**Benchmarks:**
```go
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(2, 3)
    }
}

// Benchmark with setup
func BenchmarkMapAccess(b *testing.B) {
    m := make(map[string]int)
    for i := 0; i < 1000; i++ {
        m[fmt.Sprintf("key%d", i)] = i
    }

    b.ResetTimer()  // Reset timer after setup

    for i := 0; i < b.N; i++ {
        _ = m["key500"]
    }
}

// Benchmark with multiple cases
func BenchmarkSort(b *testing.B) {
    sizes := []int{10, 100, 1000, 10000}

    for _, size := range sizes {
        b.Run(fmt.Sprintf("size-%d", size), func(b *testing.B) {
            data := make([]int, size)
            for i := range data {
                data[i] = rand.Intn(1000)
            }

            b.ResetTimer()

            for i := 0; i < b.N; i++ {
                sort.Ints(data)
            }
        })
    }
}
```

**Test Fixtures:**
```go
// testdata/users.json
// {"users": [{"id": 1, "name": "Alice"}]}

func TestLoadUsers(t *testing.T) {
    data, err := os.ReadFile("testdata/users.json")
    if err != nil {
        t.Fatalf("failed to read fixture: %v", err)
    }

    var result struct {
        Users []User `json:"users"`
    }

    if err := json.Unmarshal(data, &result); err != nil {
        t.Fatalf("failed to parse fixture: %v", err)
    }

    if len(result.Users) != 1 {
        t.Errorf("got %d users, want 1", len(result.Users))
    }
}
```

**TestMain for Setup/Teardown:**
```go
func TestMain(m *testing.M) {
    // Setup
    db = setupDatabase()

    // Run tests
    code := m.Run()

    // Teardown
    db.Close()

    os.Exit(code)
}

// Tests use global db
func TestGetUser(t *testing.T) {
    user, err := db.GetUser(1)
    // ...
}
```

**Testing HTTP Handlers:**
```go
func TestUserHandler(t *testing.T) {
    tests := []struct {
        name       string
        method     string
        url        string
        body       string
        wantStatus int
        wantBody   string
    }{
        {
            name:       "valid request",
            method:     "POST",
            url:        "/users",
            body:       `{"name":"Alice"}`,
            wantStatus: http.StatusCreated,
            wantBody:   `{"id":1,"name":"Alice"}`,
        },
        {
            name:       "invalid JSON",
            method:     "POST",
            url:        "/users",
            body:       `{invalid}`,
            wantStatus: http.StatusBadRequest,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest(tt.method, tt.url, strings.NewReader(tt.body))
            rec := httptest.NewRecorder()

            handler := UserHandler()
            handler.ServeHTTP(rec, req)

            if rec.Code != tt.wantStatus {
                t.Errorf("status = %d, want %d", rec.Code, tt.wantStatus)
            }

            if tt.wantBody != "" {
                got := strings.TrimSpace(rec.Body.String())
                if got != tt.wantBody {
                    t.Errorf("body = %q, want %q", got, tt.wantBody)
                }
            }
        })
    }
}
```

**Test Coverage:**
```bash
# Run tests with coverage
go test -cover

# Generate coverage profile
go test -coverprofile=coverage.out

# View coverage in browser
go tool cover -html=coverage.out

# Coverage by function
go tool cover -func=coverage.out

# Coverage for specific packages
go test -cover ./...
```

**Parallel Tests:**
```go
func TestParallel(t *testing.T) {
    tests := []struct {
        name  string
        input int
    }{
        {"test1", 1},
        {"test2", 2},
        {"test3", 3},
    }

    for _, tt := range tests {
        tt := tt  // Capture range variable
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()  // Run in parallel

            result := processInput(tt.input)
            // Assertions
        })
    }
}
```

**Testing with Golden Files:**
```go
import (
    "flag"
    "os"
    "testing"
)

var update = flag.Bool("update", false, "update golden files")

func TestFormat(t *testing.T) {
    input := "some input data"
    got := Format(input)

    goldenPath := "testdata/format.golden"

    if *update {
        os.WriteFile(goldenPath, []byte(got), 0644)
    }

    want, err := os.ReadFile(goldenPath)
    if err != nil {
        t.Fatalf("failed to read golden file: %v", err)
    }

    if got != string(want) {
        t.Errorf("got:\n%s\nwant:\n%s", got, want)
    }
}

// Update golden files: go test -update
```

**Example Tests (Documentation):**
```go
func ExampleAdd() {
    result := Add(2, 3)
    fmt.Println(result)
    // Output: 5
}

func ExampleDivide() {
    result, _ := Divide(10, 2)
    fmt.Println(result)
    // Output: 5
}

// Unordered output
func ExampleMultipleOutputs() {
    results := GetResults()
    for _, r := range results {
        fmt.Println(r)
    }
    // Unordered output:
    // result1
    // result2
}
```

**Testing Private Functions:**
```go
// Same package test (can access private functions)
package math

func TestinternalAdd(t *testing.T) {
    result := internalAdd(2, 3)  // Can test private function
    if result != 5 {
        t.Errorf("got %d, want 5", result)
    }
}

// Different package test (only public API)
package math_test

import (
    "testing"
    "myproject/math"
)

func TestAdd(t *testing.T) {
    result := math.Add(2, 3)  // Only public functions
    if result != 5 {
        t.Errorf("got %d, want 5", result)
    }
}
```

**Anti-Patterns to Avoid:**
```go
// ✗ Don't use global state without cleanup
var testDB *Database

func TestWithGlobal(t *testing.T) {
    testDB.Insert(data)  // Affects other tests!
}

// ✓ Use fresh state per test
func TestWithLocal(t *testing.T) {
    db := setupTestDB(t)
    defer db.Close()
    db.Insert(data)
}

// ✗ Don't ignore test errors
func TestBadError(t *testing.T) {
    result, _ := MightFail()  // Ignoring error!
    if result != expected {
        t.Error("wrong result")
    }
}

// ✓ Check all errors
func TestGoodError(t *testing.T) {
    result, err := MightFail()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if result != expected {
        t.Error("wrong result")
    }
}

// ✗ Don't write brittle tests
func TestBrittle(t *testing.T) {
    json := getJSON()
    if json != `{"id":1,"name":"Alice","created":"2024-01-01"}` {
        t.Error("wrong JSON")  // Fails on timestamp change
    }
}

// ✓ Test meaningful properties
func TestRobust(t *testing.T) {
    var data Data
    json.Unmarshal(getJSON(), &data)
    if data.ID != 1 || data.Name != "Alice" {
        t.Error("wrong data")
    }
}
```
