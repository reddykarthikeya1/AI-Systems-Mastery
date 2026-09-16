# Module 08: Troubleshooting, Common Testing Traps & Mock Bugs

This reference guide details common errors and subtle bugs encountered when building automated test suites with Pytest and Mock.

---

## 1. The "Where to Patch" Bug

### The Bug
Suppose `app/payment.py` has:
```python
# app/payment.py
import stripe

def process_charge(amount):
    return stripe.Charge.create(amount=amount)
```
In your test:
```python
# ❌ BUGGY: Patching the origin package, NOT where it was imported!
@patch("stripe.Charge.create")
def test_charge(mock_create):
    process_charge(100)
    mock_create.assert_called_once() # Fails or calls real stripe!
```

### The Fix: Patch Where Looked Up!
Patch the symbol **inside the module where it is being used**:
```python
# ✅ CORRECT: Patch inside 'app.payment' where 'stripe' is looked up!
@patch("app.payment.stripe.Charge.create")
def test_charge(mock_create):
    mock_create.return_value = {"status": "succeeded"}
    process_charge(100)
    mock_create.assert_called_once_with(amount=100)
```

---

## 2. Mock Attribute Drift (`autospec=True`)

### The Bug
```python
class EmailClient:
    def send_email(self, recipient: str, body: str):
        pass

# Test accidentally typos the method name:
mock_client = MagicMock()
mock_client.send_emial("alice@example.com", "Hi")  # Typo! But MagicMock creates it silently!
mock_client.send_emial.assert_called_once()       # Test passes, but production breaks!
```

### The Fix
Use `autospec=True` or `spec=EmailClient` to strictly forbid nonexistent attributes:
```python
mock_client = MagicMock(spec=EmailClient)
mock_client.send_emial("alice@example.com", "Hi")  # ❌ AttributeError: Mock has no attribute 'send_emial'!
```

---

## 3. Leaky Fixtures Contaminating Tests

### The Bug
```python
@pytest.fixture(scope="session")  # Shared across ALL tests in entire test run!
def active_user_list():
    return []

def test_a(active_user_list):
    active_user_list.append("Alice")
    assert len(active_user_list) == 1

def test_b(active_user_list):
    # Fails if test_a ran first, because active_user_list already contains 'Alice'!
    assert len(active_user_list) == 0
```

### The Fix
Keep mutable fixtures at the default **`scope="function"`** so each test receives a clean, isolated instance:
```python
@pytest.fixture(scope="function")
def active_user_list():
    return []  # Brand new empty list for every single test
```
