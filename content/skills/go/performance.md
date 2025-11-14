---
metadata:
  name: "Go Performance Optimization"
  activation_keywords: ["performance", "pprof", "profiling", "memory", "goroutine"]
  category: "language-go"
principles: ['U_EVIDENCE_BASED', 'P_PERFORMANCE_PROFILE_BEFORE_OPTIMIZE', 'P_CONTINUOUS_PROFILING', 'U_NO_OVERENGINEERING', 'P_CACHING_STRATEGY']
---

# Go Performance Optimization

Master Go performance profiling and optimization techniques for high-performance applications.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Profiling Tools:**
- pprof: CPU and memory profiling
- trace: Execution trace analysis
- benchstat: Benchmark comparison
- escape analysis: Stack vs heap allocation
- race detector: Find data races

**Key Patterns:**
1. Profile before optimizing (measure, don't guess)
2. Use benchmarks to measure improvements
3. Minimize heap allocations
4. Use sync.Pool for temporary objects
5. Avoid goroutine leaks

**Common Bottlenecks:**
- Excessive allocations
- Lock contention
- Goroutine leaks
- Inefficient algorithms
- Unnecessary copies

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**CPU Profiling:**
```go
import (
    "os"
    "runtime/pprof"
)

func main() {
    // Start CPU profiling
    f, err := os.Create("cpu.prof")
    if err != nil {
        panic(err)
    }
    defer f.Close()

    if err := pprof.StartCPUProfile(f); err != nil {
        panic(err)
    }
    defer pprof.StopCPUProfile()

    // Run your code
    doWork()
}

// Analyze profile:
// go tool pprof cpu.prof
// (pprof) top
// (pprof) list functionName
// (pprof) web
```

**Memory Profiling:**
```go
import (
    "os"
    "runtime"
    "runtime/pprof"
)

func profileMemory() {
    f, err := os.Create("mem.prof")
    if err != nil {
        panic(err)
    }
    defer f.Close()

    runtime.GC()  // Get up-to-date stats

    if err := pprof.WriteHeapProfile(f); err != nil {
        panic(err)
    }
}

// Analyze:
// go tool pprof mem.prof
// (pprof) top
// (pprof) list functionName
```

**HTTP Server Profiling:**
```go
import (
    _ "net/http/pprof"
    "net/http"
)

func main() {
    // Automatically exposes /debug/pprof endpoints
    go func() {
        http.ListenAndServe("localhost:6060", nil)
    }()

    // Your application code
    runServer()
}

// Access profiling endpoints:
// CPU: go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
// Heap: go tool pprof http://localhost:6060/debug/pprof/heap
// Goroutines: go tool pprof http://localhost:6060/debug/pprof/goroutine
// View in browser: http://localhost:6060/debug/pprof/
```

**Benchmarking:**
```go
func BenchmarkStringConcat(b *testing.B) {
    for i := 0; i < b.N; i++ {
        s := ""
        for j := 0; j < 100; j++ {
            s += "x"  // Slow!
        }
    }
}

func BenchmarkStringBuilder(b *testing.B) {
    for i := 0; i < b.N; i++ {
        var sb strings.Builder
        for j := 0; j < 100; j++ {
            sb.WriteString("x")  // Fast!
        }
        _ = sb.String()
    }
}

// Run benchmarks:
// go test -bench=. -benchmem
// -benchmem shows memory allocations

// Compare benchmarks:
// go test -bench=. -benchmem > old.txt
// # Make changes
// go test -bench=. -benchmem > new.txt
// benchstat old.txt new.txt
```

**Reducing Allocations:**
```go
// ✗ Bad: Allocates on every call
func badConcat(a, b string) string {
    return a + b  // New allocation
}

// ✓ Good: Use strings.Builder
func goodConcat(parts []string) string {
    var sb strings.Builder
    sb.Grow(totalLength(parts))  // Pre-allocate
    for _, p := range parts {
        sb.WriteString(p)
    }
    return sb.String()
}

// ✗ Bad: Allocates slice on every call
func badAppend() []int {
    var result []int
    for i := 0; i < 1000; i++ {
        result = append(result, i)  // Multiple reallocations
    }
    return result
}

// ✓ Good: Pre-allocate capacity
func goodAppend() []int {
    result := make([]int, 0, 1000)  // Pre-allocate
    for i := 0; i < 1000; i++ {
        result = append(result, i)  // No reallocation
    }
    return result
}
```

**sync.Pool for Object Reuse:**
```go
import "sync"

var bufferPool = sync.Pool{
    New: func() interface{} {
        return new(bytes.Buffer)
    },
}

func processData(data []byte) {
    // Get buffer from pool
    buf := bufferPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        bufferPool.Put(buf)  // Return to pool
    }()

    // Use buffer
    buf.Write(data)
    // Process...
}
```

**Escape Analysis:**
```bash
# Check if variables escape to heap
go build -gcflags="-m" main.go

# Example output:
# ./main.go:10: moved to heap: x  # x escapes
# ./main.go:15: y does not escape # y stays on stack
```

```go
// ✗ Escapes to heap
func badAlloc() *int {
    x := 42
    return &x  // x escapes to heap
}

// ✓ Stays on stack
func goodAlloc() int {
    x := 42
    return x  // x stays on stack
}

// ✗ Interface causes allocation
func badInterface(i interface{}) {
    // i is boxed (allocated)
}

// ✓ Concrete type avoids allocation
func goodConcrete(i int) {
    // No boxing
}
```

**Goroutine Optimization:**
```go
// ✗ Bad: Goroutine leak
func badGoroutineLeak() {
    ch := make(chan int)
    go func() {
        val := <-ch  // Blocks forever if ch never receives
        process(val)
    }()
    // Goroutine never exits!
}

// ✓ Good: Use context for cancellation
func goodGoroutine(ctx context.Context) {
    ch := make(chan int)
    go func() {
        select {
        case val := <-ch:
            process(val)
        case <-ctx.Done():
            return  // Clean exit
        }
    }()
}

// ✓ Good: Limit goroutine count
func limitedGoroutines(tasks []Task, maxWorkers int) {
    sem := make(chan struct{}, maxWorkers)

    for _, task := range tasks {
        sem <- struct{}{}  // Acquire semaphore
        go func(t Task) {
            defer func() { <-sem }()  // Release semaphore
            t.Execute()
        }(task)
    }

    // Wait for all goroutines
    for i := 0; i < cap(sem); i++ {
        sem <- struct{}{}
    }
}
```

**Lock Optimization:**
```go
import "sync"

// ✗ Bad: Lock contention
type BadCounter struct {
    mu    sync.Mutex
    count int
}

func (c *BadCounter) Increment() {
    c.mu.Lock()
    c.count++
    c.mu.Unlock()
}

// ✓ Good: Use atomic operations
import "sync/atomic"

type GoodCounter struct {
    count int64
}

func (c *GoodCounter) Increment() {
    atomic.AddInt64(&c.count, 1)
}

// ✓ Good: Use RWMutex for read-heavy workloads
type Cache struct {
    mu   sync.RWMutex
    data map[string]string
}

func (c *Cache) Get(key string) (string, bool) {
    c.mu.RLock()  // Multiple readers allowed
    defer c.mu.RUnlock()
    val, ok := c.data[key]
    return val, ok
}

func (c *Cache) Set(key, value string) {
    c.mu.Lock()  // Exclusive writer
    defer c.mu.Unlock()
    c.data[key] = value
}
```

**Struct Field Ordering:**
```go
// ✗ Bad: 24 bytes (padding)
type BadStruct struct {
    a bool   // 1 byte + 7 padding
    b int64  // 8 bytes
    c bool   // 1 byte + 7 padding
}

// ✓ Good: 16 bytes (optimized)
type GoodStruct struct {
    b int64  // 8 bytes
    a bool   // 1 byte
    c bool   // 1 byte + 6 padding
}

// Check struct size:
// unsafe.Sizeof(GoodStruct{})
```

**String vs []byte:**
```go
// ✗ Allocates on conversion
func badStringConversion(b []byte) int {
    s := string(b)  // Allocation!
    return len(s)
}

// ✓ No allocation needed
func goodByteSlice(b []byte) int {
    return len(b)
}

// ✓ Unsafe conversion (use carefully)
import "unsafe"

func unsafeString(b []byte) string {
    return *(*string)(unsafe.Pointer(&b))  // No allocation
}
```

**Map Pre-allocation:**
```go
// ✗ Bad: Map grows incrementally
func badMapGrowth() map[string]int {
    m := make(map[string]int)  // No capacity
    for i := 0; i < 1000; i++ {
        m[fmt.Sprintf("key%d", i)] = i
    }
    return m
}

// ✓ Good: Pre-allocate capacity
func goodMapCapacity() map[string]int {
    m := make(map[string]int, 1000)  // Pre-allocate
    for i := 0; i < 1000; i++ {
        m[fmt.Sprintf("key%d", i)] = i
    }
    return m
}
```

**Inline Functions:**
```go
// Small functions are inlined by compiler
func add(a, b int) int {
    return a + b  // Inlined
}

// Force inline with //go:inline (compiler hint)
//go:inline
func fastPath(x int) int {
    return x * 2
}

// Prevent inline with //go:noinline
//go:noinline
func complexFunction(x int) int {
    // Complex logic
    return x
}
```

**Trace Analysis:**
```go
import (
    "os"
    "runtime/trace"
)

func main() {
    f, _ := os.Create("trace.out")
    defer f.Close()

    trace.Start(f)
    defer trace.Stop()

    // Your code
    doWork()
}

// Analyze trace:
// go tool trace trace.out
// Opens web UI showing:
// - Goroutine execution
// - Network blocking
// - Syscalls
// - GC events
```

**Race Detector:**
```bash
# Run with race detector
go test -race
go run -race main.go
go build -race

# Example race:
var counter int

func increment() {
    counter++  # Race detected!
}

go increment()
go increment()
```

**Memory Ballast:**
```go
// Reduce GC frequency for high-throughput apps
func init() {
    // Allocate 10GB ballast (not actually used)
    ballast := make([]byte, 10<<30)
    runtime.KeepAlive(ballast)
}
```

**Performance Tips:**
```go
// 1. Use constants instead of variables
const MaxSize = 1000  // Compiler optimization

// 2. Avoid interface{} when possible
func slowInterface(v interface{}) {
    // Type assertion overhead
}

func fastConcrete(v int) {
    // No overhead
}

// 3. Use byte slices for I/O
func writeString(w io.Writer, s string) {
    w.Write([]byte(s))  # Allocation
}

func writeBytes(w io.Writer, b []byte) {
    w.Write(b)  # No allocation
}

// 4. Reuse buffers
var buf bytes.Buffer
buf.Reset()  # Reuse existing capacity

// 5. Avoid defer in hot paths
func hotPath() {
    // defer has small overhead
    // Explicit cleanup in critical sections
}
```

**Benchstat for Comparison:**
```bash
# Baseline
go test -bench=. -count=10 > old.txt

# After optimization
go test -bench=. -count=10 > new.txt

# Compare
benchstat old.txt new.txt

# Output shows:
# name        old time/op  new time/op  delta
# MyFunc-8    1.23µs ± 2%  0.98µs ± 1%  -20.33%
```

**Anti-Patterns to Avoid:**
```go
// ✗ Don't optimize prematurely
func prematureOptimization() {
    // Complex, hard-to-read code for 1% gain
}

// ✓ Optimize hot paths only
func measureFirst() {
    // Profile first, then optimize bottlenecks
}

// ✗ Don't ignore allocations
func ignoreAllocs() {
    for i := 0; i < 1000000; i++ {
        s := fmt.Sprintf("%d", i)  // 1M allocations!
        _ = s
    }
}

// ✓ Minimize allocations
func reduceAllocs() {
    buf := make([]byte, 0, 20)
    for i := 0; i < 1000000; i++ {
        buf = strconv.AppendInt(buf[:0], int64(i), 10)
    }
}

// ✗ Don't leak goroutines
func leakGoroutine() {
    go func() {
        for {
            // Never exits!
            time.Sleep(1 * time.Second)
        }
    }()
}

// ✓ Use context for cancellation
func cleanupGoroutine(ctx context.Context) {
    go func() {
        ticker := time.NewTicker(1 * time.Second)
        defer ticker.Stop()

        for {
            select {
            case <-ticker.C:
                // Work
            case <-ctx.Done():
                return  // Clean exit
            }
        }
    }()
}
```
