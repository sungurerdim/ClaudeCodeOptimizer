# U_NO_OVERENGINEERING: No Overengineering

**Severity**: Critical

Choose simplest solution. Avoid premature abstraction, unnecessary patterns, excessive architecture.

---

## Why

- Gold-plating builds features nobody asked for
- Premature abstraction creates frameworks before understanding needs
- Complexity creep makes simple solutions unmaintainable
- YAGNI violations ("You Aren't Gonna Need It")

**Core Questions:**
1. **Do we need this NOW?** (not "might need someday")
2. **Is there simpler solution?** (always yes until proven)
3. **Can we solve 80% with 20% effort?** (Pareto)
4. **Will this be harder to maintain?**
5. **Solving real or hypothetical problem?**

---

## Examples

### ✅ Start Simple
```python
# ✅ GOOD
def calculate_total(prices):
    return sum(prices)

# ❌ BAD: Overengineered
class TotalCalculationStrategy(ABC):
    @abstractmethod
    def calculate(self, prices: List[Decimal]) -> Decimal:
        pass

class SummationStrategy(TotalCalculationStrategy):
    def __init__(self, precision: int = 2, rounding: RoundingMode = ROUND_HALF_UP):
        self.precision = precision
        self.rounding = rounding
    # ... 50+ lines to do sum()
```

### ✅ Solve Current Problem
```python
# ✅ GOOD
class User:
    def __init__(self, name: str):
        self.name = name

# ❌ BAD: Future problems
class User:
    def __init__(self, name: str):
        self.names = {'legal': name, 'preferred': name, 'display': name}
        self.name_history = []
        self.name_metadata = {'source': 'registration', 'verified': False}
```

### ✅ Extract After Duplication (Rule of Three)
```python
# First use: Inline
def process_order():
    conn = db.connect()
    try:
        return conn.execute("SELECT * FROM orders")
    finally:
        conn.close()

# Second use: Copy OK temporarily

# Third use: NOW abstract
@contextmanager
def db_connection():
    conn = db.connect()
    try:
        yield conn
    finally:
        conn.close()
```

---

## Anti-Patterns

### ❌ Premature Abstraction
```python
# ❌ BAD: Abstract before understanding
class DataProcessorFactory:
    @staticmethod
    def create_processor(type):
        # 10 processor types nobody uses

# ✅ GOOD
def process_data(json_string):
    return json.loads(json_string)
```

### ❌ Future-Proofing
```python
# ❌ BAD: "Scale to 1B users" (have 10 today)
class ScalableUserService:
    def __init__(self):
        self.cache = Redis(host='redis-cluster')
        self.search = Elasticsearch(['es-1', 'es-2'])
        self.events = KafkaProducer(['kafka:9092'])

# ✅ GOOD: Scale when needed
users = {}  # Start here
# At 10K → add DB
# At 100K → add cache
# At 1M → add distributed
```

---

## Decision Framework

**Add complexity ONLY when:**
- ✅ Have 3+ real examples (Rule of Three)
- ✅ Requirements explicitly demand it
- ✅ Simpler solutions tried and failed
- ✅ Cost of complexity < Cost of alternative

**DON'T add when:**
- ❌ "Might need someday"
- ❌ "It's best practice" (context matters!)
- ❌ "Other project does it"
- ❌ "Want to learn this tech"

---

## Checklist

- [ ] Can I solve with existing code?
- [ ] Do I have 3 real examples?
- [ ] Can I write 50 lines instead of dependency?
- [ ] Is this necessary or cargo-culting?
- [ ] Do I have concrete use cases?
