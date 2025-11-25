---
name: cco-skill-documentation
description: Comprehensive documentation including API specs (OpenAPI/Swagger), ADRs, runbooks, changelogs, code docstrings, AI code documentation templates, and automated doc coverage metrics
keywords: [documentation, docs, OpenAPI, Swagger, ADR, runbook, changelog, docstring, API spec, code documentation, AI documentation, doc coverage, readme]
category: docs
related_commands:
  action_types: [audit, fix, generate]
  categories: [docs, quality]
pain_points: [12]
---

# Documentation - API, ADRs, Runbooks, Code Docs

> **Standards:** Format defined in [cco-standards.md](../cco-standards.md)  
> **Discovery:** See [cco-standards.md](../cco-standards.md#18-command-discovery-protocol)


Comprehensive documentation strategy with AI code documentation templates and coverage metrics.
---

---

## Domain

API documentation, architecture decision records, operational runbooks, code documentation.

---

## Purpose

**Documentation Gap Crisis (2025):**
- 76% of developers spend >4 hours/week searching for undocumented info
- AI-generated code often lacks explanatory comments (35% of AI code)
- 60% of API issues stem from missing/outdated documentation
- ADRs reduce decision re-litigation by 40%
- Runbooks reduce MTTR by 40%

**This Skill Provides:**
- Automated documentation coverage metrics
- AI code documentation templates
- OpenAPI spec generation from code
- ADR and runbook templates
- Detection of undocumented functions/classes

---

## Core Techniques

### 1. Documentation Coverage Assessment

**Detect Missing Documentation:**
```python
def assess_documentation_coverage(file_path: str) -> dict:
    """Calculate documentation coverage for Python file"""
    with open(file_path) as f:
        tree = ast.parse(f.read())

    total_functions = 0
    documented_functions = 0
    total_classes = 0
    documented_classes = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            total_functions += 1
            if ast.get_docstring(node):
                documented_functions += 1

        if isinstance(node, ast.ClassDef):
            total_classes += 1
            if ast.get_docstring(node):
                documented_classes += 1

    function_coverage = (documented_functions / total_functions * 100) if total_functions > 0 else 100
    class_coverage = (documented_classes / total_classes * 100) if total_classes > 0 else 100

    return {
        'total_functions': total_functions,
        'documented_functions': documented_functions,
        'total_classes': total_classes,
        'documented_classes': total_classes,
        'function_coverage': function_coverage,
        'class_coverage': class_coverage,
        'overall_coverage': (function_coverage + class_coverage) / 2,
        'grade': (
            'A' if function_coverage >= 90 else
            'B' if function_coverage >= 75 else
            'C' if function_coverage >= 60 else
            'D' if function_coverage >= 40 else
            'F'
        )
    }
```

**Find Undocumented Functions:**
```python
def find_undocumented_functions(file_path: str) -> List[dict]:
    """List all undocumented functions"""
    with open(file_path) as f:
        code = f.read()
        tree = ast.parse(code)

    undocumented = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not ast.get_docstring(node):
                # Check complexity to prioritize
                complexity = calculate_complexity(node)

                undocumented.append({
                    'type': 'missing_docstring',
                    'function': node.name,
                    'line': node.lineno,
                    'complexity': complexity,
                    'severity': (
                        'HIGH' if complexity > 10 else
                        'MEDIUM' if complexity > 5 else
                        'LOW'
                    ),
                    'message': f'Function {node.name} lacks docstring (complexity: {complexity})'
                })

    return undocumented
```

---

### 2. AI Code Documentation Templates

**For Complex AI-Generated Logic:**
```python
def process_payment_with_tax(amount: Decimal, user_id: int, tax_rate: float = 0.0) -> PaymentResult:
    """
    Process payment including tax calculation and fraud detection.

    [AI GENERATED CODE - IMPORTANT NOTES]
    This function combines payment processing with real-time fraud detection.
    The fraud check uses a third-party API that may timeout (configured to 3s).

    WHY THIS APPROACH:
    - Combined transaction ensures atomic payment+fraud check
    - Tax calculation happens before payment to avoid partial charges
    - Retry logic handles transient payment gateway failures

    EDGE CASES TO KNOW:
    - If fraud API times out, payment proceeds (configurable via FRAUD_CHECK_REQUIRED env)
    - Tax rate of 0.0 is valid for tax-exempt users (don't change to None)
    - amount must be > 0 but validation happens in Payment model

    Args:
        amount: Payment amount in USD (must be positive)
        user_id: User ID for fraud check and audit trail
        tax_rate: Tax percentage (0.0-1.0). Defaults to 0.0 for tax-exempt.

    Returns:
        PaymentResult containing:
            - transaction_id: Unique payment identifier
            - total_charged: Final amount including tax
            - fraud_score: 0-100 risk score (>80 = rejected)

    Raises:
        ValueError: If amount <= 0
        PaymentGatewayError: If payment fails after 3 retries
        FraudCheckError: If fraud_score > 80 (FRAUD_CHECK_REQUIRED=true)

    Examples:
        >>> process_payment_with_tax(Decimal('100.00'), user_id=123, tax_rate=0.08)
        PaymentResult(transaction_id='txn_...', total_charged=Decimal('108.00'), fraud_score=15)
    """
    # [AI NOTE] Fraud check BEFORE payment to avoid refunds
    fraud_score = check_fraud(user_id, amount)
    if fraud_score > 80 and os.getenv('FRAUD_CHECK_REQUIRED') == 'true':
        raise FraudCheckError(f"Fraud score too high: {fraud_score}")

    # [AI NOTE] Tax calculation uses decimal to avoid floating point errors
    total_amount = amount * (Decimal('1') + Decimal(str(tax_rate)))

    # [AI NOTE] Retry logic: payment gateway has 1% failure rate
    for attempt in range(3):
        try:
            result = payment_gateway.charge(user_id, total_amount)
            return PaymentResult(
                transaction_id=result.id,
                total_charged=total_amount,
                fraud_score=fraud_score
            )
        except TransientError as e:
            if attempt == 2:  # Last attempt
                raise PaymentGatewayError("Payment failed after 3 attempts") from e
            time.sleep(2 ** attempt)  # Exponential backoff
```

**For Simple AI-Generated Functions:**
```python
def calculate_discount(price: Decimal, discount_percentage: float) -> Decimal:
    """
    Calculate final price after applying percentage discount.

    Args:
        price: Original price (must be positive)
        discount_percentage: Discount as percentage (0-100)

    Returns:
        Final price after discount, rounded to 2 decimals

    Raises:
        ValueError: If price < 0 or discount not in 0-100 range

    Examples:
        >>> calculate_discount(Decimal('100.00'), 20)
        Decimal('80.00')
    """
    if price < 0:
        raise ValueError(f"Price cannot be negative: {price}")
    if not 0 <= discount_percentage <= 100:
        raise ValueError(f"Discount must be 0-100: {discount_percentage}")

    return round(price * (1 - Decimal(str(discount_percentage)) / 100), 2)
```

---

### 3. OpenAPI/Swagger Generation

**FastAPI Auto-Documentation:**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="User Management API",
    version="1.0.0",
    description="API for managing user accounts and permissions",
    contact={
        "name": "API Support",
        "email": "{API_CONTACT_EMAIL}",
    },
    license_info={
        "name": "MIT",
    }
)

class User(BaseModel):
    """User model with validation"""
    id: int = Field(..., description="Unique user identifier", example=123)
    email: str = Field(..., description="User email address", example="{USER_EMAIL}")
    name: str = Field(..., description="Full name", min_length=1, max_length=100)
    is_active: bool = Field(default=True, description="Account active status")

    class Config:
        schema_extra = {
            "example": {
                "id": 123,
                "email": "{USER_EMAIL}",
                "name": "{USER_NAME}",
                "is_active": True
            }
        }

@app.get(
    "/users/{user_id}",
    response_model=User,
    summary="Get user by ID",
    description="Retrieve a user's detailed information by their unique ID",
    responses={
        200: {"description": "User found", "model": User},
        404: {"description": "User not found"},
        500: {"description": "Internal server error"}
    },
    tags=["Users"]
)
async def get_user(
    user_id: int = Field(..., description="User ID to retrieve", example=123)
) -> User:
    """
    Retrieve user details by ID.

    This endpoint returns complete user information including:
    - Basic profile (name, email)
    - Account status (active/inactive)
    - Internal ID for reference

    **Rate Limit:** 100 requests/minute per IP
    """
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user

# Auto-generated docs available at:
# - Swagger UI: /docs
# - ReDoc: /redoc
# - OpenAPI JSON: /openapi.json
```

**Detection Pattern:**
```python
def check_api_documentation(file_path: str) -> dict:
    """Check if API has proper OpenAPI documentation"""
    with open(file_path) as f:
        content = f.read()

    issues = []

    # Check for FastAPI/Flask routes
    routes = re.findall(r'@app\.(get|post|put|delete)\(["\'](.+?)["\']\)', content)

    for method, path in routes:
        # Check if route has docstring
        route_pattern = rf'@app\.{method}\(["\']({re.escape(path)})["\']\).*?def\s+(\w+)'
        match = re.search(route_pattern, content, re.DOTALL)

        if match:
            func_name = match.group(2)
            func_start = match.end()

            # Check for docstring
            docstring_pattern = rf'def {func_name}.*?:.*?"""(.+?)"""'
            if not re.search(docstring_pattern, content[func_start:func_start+500], re.DOTALL):
                issues.append({
                    'type': 'missing_api_docs',
                    'route': f'{method.upper()} {path}',
                    'function': func_name,
                    'severity': 'MEDIUM',
                    'message': f'API endpoint {method.upper()} {path} lacks docstring'
                })

    # Check for response model documentation
    if 'FastAPI' in content:
        if 'response_model' not in content:
            issues.append({
                'type': 'missing_response_model',
                'severity': 'LOW',
                'message': 'FastAPI routes missing response_model (helps auto-generate OpenAPI)'
            })

    return {
        'total_routes': len(routes),
        'undocumented_routes': len(issues),
        'documentation_coverage': ((len(routes) - len(issues)) / len(routes) * 100) if routes else 100,
        'issues': issues
    }
```

---

### 4. ADR (Architecture Decision Record) Detection

**Check for ADRs:**
```python
def check_adr_presence() -> dict:
    """Check if project has ADRs and how current they are"""
    adr_dirs = ['docs/adr', 'docs/architecture', 'adr', 'architecture']
    adr_files = []

    for adr_dir in adr_dirs:
        if os.path.exists(adr_dir):
            adr_files.extend(glob.glob(f'{adr_dir}/**/*.md', recursive=True))

    if not adr_files:
        return {
            'has_adrs': False,
            'adr_count': 0,
            'severity': 'MEDIUM',
            'message': 'No ADRs found - architecture decisions not documented'
        }

    # Check ADR recency
    newest_adr = max(os.path.getmtime(f) for f in adr_files)
    days_since_last = (datetime.now() - datetime.fromtimestamp(newest_adr)).days

    return {
        'has_adrs': True,
        'adr_count': len(adr_files),
        'days_since_last_adr': days_since_last,
        'stale': days_since_last > 180,  # 6 months
        'recommendation': (
            f'Last ADR {days_since_last} days ago - consider documenting recent decisions'
            if days_since_last > 180 else
            'ADRs current'
        )
    }
```

---

### 5. Runbook Detection

**Check Operational Documentation:**
```python
def check_runbook_presence() -> dict:
    """Check if project has operational runbooks"""
    runbook_patterns = [
        'docs/runbook*.md',
        'docs/operations/*.md',
        'runbooks/**/*.md',
        'ops/**/*.md'
    ]


---

## Checklist

### Code Documentation
- [ ] All public functions have docstrings
- [ ] Complex logic has inline comments
- [ ] Type hints on all function signatures
- [ ] AI-generated code has context comments

### API Documentation
- [ ] OpenAPI/Swagger spec exists
- [ ] All endpoints documented
- [ ] Request/response schemas defined
- [ ] Error responses documented

### Architecture
- [ ] README with project overview
- [ ] ADRs for major decisions
- [ ] Architecture diagram
- [ ] CONTRIBUTING.md

### Operations
- [ ] Runbooks for common issues
- [ ] Deployment documentation
- [ ] Environment setup guide
- [ ] Incident response procedures
