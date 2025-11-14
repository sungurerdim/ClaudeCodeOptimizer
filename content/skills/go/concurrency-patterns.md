---
metadata:
  name: "Go Concurrency Patterns"
  activation_keywords: ["goroutine", "channel", "select", "concurrent", "sync"]
  category: "language-go"
principles: ['P_ASYNC_IO', 'U_FAIL_FAST', 'P_GRACEFUL_SHUTDOWN', 'P_RATE_LIMITING', 'U_EVIDENCE_BASED']
---

# Go Concurrency Patterns

Master Go's concurrency with goroutines, channels, and synchronization primitives for efficient parallel programs.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Concurrency Primitives:**
- Goroutines: Lightweight threads (use `go` keyword)
- Channels: Communicate between goroutines (typed, buffered/unbuffered)
- Select: Choose from multiple channel operations
- Sync package: Mutexes, WaitGroups, Once, etc.
- Context: Cancellation and timeouts

**Key Patterns:**
1. Use channels for communication, mutexes for state
2. Close channels to signal completion
3. Use select for multiplexing channels
4. WaitGroup for waiting on multiple goroutines
5. Context for cancellation propagation

**Common Patterns:**
- Worker pools for rate limiting
- Pipelines for data processing
- Fan-out/fan-in for parallel work
- Cancellation with context

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**Basic Goroutines:**
```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // Launch goroutine
    go printNumbers()

    // Main continues
    fmt.Println("Main function")

    // Wait for goroutine
    time.Sleep(time.Second)
}

func printNumbers() {
    for i := 1; i <= 5; i++ {
        fmt.Println(i)
        time.Sleep(100 * time.Millisecond)
    }
}

// Anonymous goroutine
func anonymousExample() {
    go func() {
        fmt.Println("Anonymous goroutine")
    }()
}
```

**Channels:**
```go
// Unbuffered channel (synchronous)
func unbufferedExample() {
    ch := make(chan int)

    go func() {
        ch <- 42  // Send (blocks until received)
    }()

    value := <-ch  // Receive (blocks until sent)
    fmt.Println(value)
}

// Buffered channel (asynchronous)
func bufferedExample() {
    ch := make(chan int, 2)  // Buffer size 2

    ch <- 1  // Non-blocking
    ch <- 2  // Non-blocking
    // ch <- 3  // Would block (buffer full)

    fmt.Println(<-ch)  // 1
    fmt.Println(<-ch)  // 2
}

// Close channel to signal completion
func closeExample() {
    ch := make(chan int, 5)

    go func() {
        for i := 0; i < 5; i++ {
            ch <- i
        }
        close(ch)  // Signal no more values
    }()

    // Range over channel until closed
    for value := range ch {
        fmt.Println(value)
    }
}
```

**Select Statement:**
```go
func selectExample() {
    ch1 := make(chan string)
    ch2 := make(chan string)

    go func() {
        time.Sleep(1 * time.Second)
        ch1 <- "one"
    }()

    go func() {
        time.Sleep(2 * time.Second)
        ch2 <- "two"
    }()

    // Select first available channel
    for i := 0; i < 2; i++ {
        select {
        case msg1 := <-ch1:
            fmt.Println("Received:", msg1)
        case msg2 := <-ch2:
            fmt.Println("Received:", msg2)
        }
    }
}

// Select with timeout
func selectTimeout() {
    ch := make(chan string)

    go func() {
        time.Sleep(2 * time.Second)
        ch <- "result"
    }()

    select {
    case res := <-ch:
        fmt.Println(res)
    case <-time.After(1 * time.Second):
        fmt.Println("Timeout!")
    }
}

// Select with default (non-blocking)
func selectNonBlocking() {
    ch := make(chan int)

    select {
    case value := <-ch:
        fmt.Println("Received:", value)
    default:
        fmt.Println("No value available")
    }
}
```

**WaitGroup:**
```go
import "sync"

func waitGroupExample() {
    var wg sync.WaitGroup

    for i := 0; i < 5; i++ {
        wg.Add(1)  // Increment counter
        go func(id int) {
            defer wg.Done()  // Decrement when done
            fmt.Printf("Worker %d starting\n", id)
            time.Sleep(time.Second)
            fmt.Printf("Worker %d done\n", id)
        }(i)
    }

    wg.Wait()  // Block until counter reaches 0
    fmt.Println("All workers done")
}
```

**Worker Pool Pattern:**
```go
func workerPool(jobs <-chan int, results chan<- int, numWorkers int) {
    var wg sync.WaitGroup

    // Start workers
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go worker(i, jobs, results, &wg)
    }

    // Wait and close results
    go func() {
        wg.Wait()
        close(results)
    }()
}

func worker(id int, jobs <-chan int, results chan<- int, wg *sync.WaitGroup) {
    defer wg.Done()

    for job := range jobs {
        fmt.Printf("Worker %d processing job %d\n", id, job)
        time.Sleep(time.Second)
        results <- job * 2
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)

    // Start pool with 3 workers
    workerPool(jobs, results, 3)

    // Send jobs
    for i := 1; i <= 9; i++ {
        jobs <- i
    }
    close(jobs)

    // Collect results
    for result := range results {
        fmt.Println("Result:", result)
    }
}
```

**Pipeline Pattern:**
```go
// Stage 1: Generate numbers
func generate(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n
        }
        close(out)
    }()
    return out
}

// Stage 2: Square numbers
func square(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * n
        }
        close(out)
    }()
    return out
}

// Stage 3: Print results
func printResults(in <-chan int) {
    for n := range in {
        fmt.Println(n)
    }
}

func pipelineExample() {
    // Pipeline: generate -> square -> print
    nums := generate(1, 2, 3, 4, 5)
    squared := square(nums)
    printResults(squared)
}
```

**Fan-Out/Fan-In Pattern:**
```go
// Fan-out: Multiple goroutines read from same channel
func fanOut(in <-chan int, n int) []<-chan int {
    channels := make([]<-chan int, n)

    for i := 0; i < n; i++ {
        channels[i] = process(in)
    }

    return channels
}

func process(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * 2
            time.Sleep(time.Second)
        }
        close(out)
    }()
    return out
}

// Fan-in: Merge multiple channels into one
func fanIn(channels ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    out := make(chan int)

    output := func(c <-chan int) {
        defer wg.Done()
        for n := range c {
            out <- n
        }
    }

    wg.Add(len(channels))
    for _, c := range channels {
        go output(c)
    }

    go func() {
        wg.Wait()
        close(out)
    }()

    return out
}

func fanExample() {
    in := generate(1, 2, 3, 4, 5, 6, 7, 8)

    // Fan-out to 3 workers
    workers := fanOut(in, 3)

    // Fan-in results
    results := fanIn(workers...)

    // Print results
    for result := range results {
        fmt.Println(result)
    }
}
```

**Context for Cancellation:**
```go
import "context"

func contextExample() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    go func() {
        time.Sleep(2 * time.Second)
        cancel()  // Cancel after 2 seconds
    }()

    worker(ctx)
}

func worker(ctx context.Context) {
    for {
        select {
        case <-ctx.Done():
            fmt.Println("Worker cancelled:", ctx.Err())
            return
        default:
            fmt.Println("Working...")
            time.Sleep(500 * time.Millisecond)
        }
    }
}

// Context with timeout
func contextTimeout() {
    ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer cancel()

    select {
    case <-time.After(3 * time.Second):
        fmt.Println("Operation completed")
    case <-ctx.Done():
        fmt.Println("Timeout:", ctx.Err())
    }
}
```

**Mutex for Shared State:**
```go
import "sync"

type Counter struct {
    mu    sync.Mutex
    value int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.value++
}

func (c *Counter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.value
}

func mutexExample() {
    counter := &Counter{}
    var wg sync.WaitGroup

    for i := 0; i < 100; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            counter.Increment()
        }()
    }

    wg.Wait()
    fmt.Println("Final count:", counter.Value())
}

// RWMutex for read-heavy workloads
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

**Once for Single Execution:**
```go
import "sync"

var (
    instance *Singleton
    once     sync.Once
)

type Singleton struct {
    value int
}

func GetInstance() *Singleton {
    once.Do(func() {
        instance = &Singleton{value: 42}
    })
    return instance
}
```

**Rate Limiting:**
```go
import "time"

// Token bucket rate limiter
func rateLimiter() {
    requests := make(chan int, 5)
    limiter := time.NewTicker(200 * time.Millisecond)
    defer limiter.Stop()

    for i := 1; i <= 5; i++ {
        requests <- i
    }
    close(requests)

    for req := range requests {
        <-limiter.C  // Wait for token
        fmt.Println("Processing request", req, time.Now())
    }
}

// Burst limiter
func burstLimiter() {
    burstyLimiter := make(chan time.Time, 3)

    // Fill bucket
    for i := 0; i < 3; i++ {
        burstyLimiter <- time.Now()
    }

    // Refill bucket
    go func() {
        ticker := time.NewTicker(200 * time.Millisecond)
        defer ticker.Stop()
        for t := range ticker.C {
            burstyLimiter <- t
        }
    }()

    requests := make(chan int, 5)
    for i := 1; i <= 5; i++ {
        requests <- i
    }
    close(requests)

    for req := range requests {
        <-burstyLimiter
        fmt.Println("Request", req, time.Now())
    }
}
```

**Anti-Patterns to Avoid:**
```go
// ✗ Don't forget to close channels
func badNoClose() {
    ch := make(chan int)
    go func() {
        for i := 0; i < 5; i++ {
            ch <- i
        }
        // Missing close(ch)
    }()

    for v := range ch {  // Will deadlock!
        fmt.Println(v)
    }
}

// ✓ Always close when done
func goodClose() {
    ch := make(chan int)
    go func() {
        for i := 0; i < 5; i++ {
            ch <- i
        }
        close(ch)
    }()

    for v := range ch {
        fmt.Println(v)
    }
}

// ✗ Don't share memory without synchronization
var counter int  // Race condition!

func badRace() {
    for i := 0; i < 100; i++ {
        go func() {
            counter++  // Unsafe!
        }()
    }
}

// ✓ Use mutex or channels
func goodSync() {
    var mu sync.Mutex
    counter := 0

    for i := 0; i < 100; i++ {
        go func() {
            mu.Lock()
            counter++
            mu.Unlock()
        }()
    }
}
```
