---
name: review-tests
description: |
  Stack-agnostic, black-box test review and TDD discipline. Use when reviewing
  test quality, writing or refactoring tests, or running /review-tests.
  Principles apply to any language; examples use TypeScript/Jest for illustration.
  Same file is synced for Claude Code, Cursor, and Codex in this repo.
---

# Review Tests

Enforce **behavior-driven, black-box** test standards. Tests describe **what** the system does, not **how** it does it. Assertions should read like truths about observable outcomes, not line-by-line reenactments of implementation.

The **Core Principles** through **Rationale** below are **general purpose** (Python, Go, Rust, etc.—translate “public API” to routes, modules, or packages your consumers use). The **Repository adapter** section at the end is **optional** and **project-specific**; replace it when you fork this skill into another codebase.

## Where this skill lives (keep in sync)

This repository keeps **identical** `SKILL.md` copies so tools can discover the same skill:

| Path | Tooling |
|------|-----------|
| `.claude/skills/review-tests/SKILL.md` | Claude Code |
| `.cursor/skills/review-tests/SKILL.md` | Cursor |
| `.codex/skills/review-tests/SKILL.md` | Codex CLI / project skills |

When editing, update **all three** files (e.g. edit one, then `cp` to the other two) so agents do not drift.

---

## Core Principles

### 1. Describe Behaviors, Not Methods

Test names should read like specifications. They describe outcomes, not implementation.

- Name tests as behaviors: `"user can checkout with valid payment"`
- Avoid method names: `"test_processPayment_returns_true"`
- Use domain language, not code language
- Assertions should match outcomes, not internal state

### 2. Decouple from Implementation

Tests should survive refactoring. If you rename a private method, no test should break.

- Never import or reference private/internal functions
- Don't assert on intermediate state or transient variables
- Mock at boundaries (APIs, databases, file system), not internal collaborators
- Avoid testing "how" — test "what"

### 3. Arrange – Act – Assert

Every test follows this structure. No exceptions.

```typescript
// Arrange: Set up only what is necessary
const cart = createCart();
cart.addItem({ id: 'SKU-001', price: 29.99 });

// Act: Execute exactly one action
const total = cart.calculateTotal();

// Assert: Verify externally observable behavior
expect(total).toBe(29.99);
```

Separate each section with a blank line. One Act per test. Clean setup, single action, assertions that read like truths. *(In pytest: arrange with fixtures/setup, `act = client.post(...)`, assert on `response.status_code` / JSON / substrings.)*

### 4. Test Boundaries, Not Internals

Public API is the contract. Internals are implementation details.

- Test through public interfaces only
- Don't reach into private state
- Don't mock what you own (mock what you don't control)
- Focus on: edge cases, error cases, limits, thresholds, invalid input handling

### 5. Use Meaningful Assertions

Assertions should fail with useful messages. They verify behavior, not existence.

- Assert on outcomes, not on calls made
- Prefer specific matchers: `toEqual`, `toContain`, `toThrow`
- Avoid `toBeTruthy()` when `toBe(true)` is what you mean
- Avoid tautological assertions or noise
- One logical assertion per test (multiple `expect` calls fine if testing one concept)

---

## Review Checklist

When reviewing a test file, verify:

- [ ] Test name clearly expresses behavior in plain language
- [ ] Arranges only what is necessary (no irrelevant setup)
- [ ] Exactly one main action in the Act phase
- [ ] Assertions reflect externally observable behavior
- [ ] No references to private methods or internal state
- [ ] Mocks used only at external boundaries
- [ ] Would survive refactoring while still validating the same behavior
- [ ] Readable by someone who does not know the implementation
- [ ] Edge cases and error paths are covered
- [ ] No shared mutable state between tests
- [ ] Meaningfully improves confidence (not noise)

---

## Red Flags

Immediately flag these anti-patterns:

| Red Flag | Problem |
|----------|---------|
| `test('processData works')` | Vague name; describes nothing |
| `expect(spy).toHaveBeenCalledTimes(3)` | Testing implementation order |
| Importing from `../utils/internal` | Coupling to internals |
| `jest.spyOn(obj, 'privateMethod')` | Testing private methods |
| `beforeEach` mutating shared state | Flaky tests waiting to happen |
| `expect(result).toBeTruthy()` | Weak assertion; hides real bugs |
| `test.skip` or `xtest` without issue link | Dead code or hidden failures |
| Copy-pasted test blocks | Missing abstraction or parameterization |
| Mocking the class under test | You're not testing anything real |
| `await sleep(1000)` | Flaky timing-dependent test |
| Asserting on intermediate variables | Implementation coupling |
| Large setup blocks with irrelevant details | Noise obscuring intent |
| Multiple behaviors in a single test | Lacks focus; hard to debug |
| Assertions that restate the implementation | Tautological; proves nothing |

---

## Questions to Ask

When reviewing tests, ask:

1. **"What behavior is being validated?"**
   - If unclear, the test lacks focus.

2. **"Can I understand the behavior from the test name alone?"**
   - If no, the name needs work.

3. **"Could this test be rewritten in plain English as user-visible behavior?"**
   - Tests should describe what users/consumers experience.

4. **"If I refactor the internals, would this test still hold true?"**
   - If no, the test is coupled to implementation.

5. **"Would this test catch a real bug?"**
   - If "maybe" or "it depends," the assertion is weak.

6. **"Could this test pass even if the feature is broken?"**
   - If yes, the assertion doesn't verify the right thing.

7. **"Is this testing our code or a library's code?"**
   - Don't test that `Array.map` works.

8. **"Does this test meaningfully improve confidence, or is it noise?"**
   - Every test should earn its place.

9. **"What happens when this test fails — will the error message help?"**
   - Assertions should fail clearly.

---

## Examples

### Bad: Testing Implementation

```typescript
// Testing method calls, not behavior
test('processOrder calls validateItems and calculateTotal', () => {
  const order = new Order(mockItems);
  const validateSpy = jest.spyOn(order, 'validateItems');
  const calculateSpy = jest.spyOn(order, 'calculateTotal');

  order.processOrder();

  expect(validateSpy).toHaveBeenCalled();
  expect(calculateSpy).toHaveBeenCalled();
});
```

**Problems:**
- Tests that methods are called, not that the order is processed
- Breaks if you refactor internal flow
- Doesn't verify the actual outcome

### Good: Testing Behavior

```typescript
// Testing the outcome of processing an order
test('processing an order with valid items returns a confirmed order', () => {
  const order = new Order([
    { sku: 'WIDGET-01', quantity: 2, price: 15.00 }
  ]);

  const result = order.process();

  expect(result.status).toBe('confirmed');
  expect(result.total).toBe(30.00);
});
```

**Why it's better:**
- Tests the public contract
- Survives internal refactoring
- Describes business behavior
- Verifies meaningful outcome

---

### Bad: Vague Test Name + Weak Assertion

```typescript
test('handleSubmit works', async () => {
  const result = await handleSubmit(formData);
  expect(result).toBeTruthy();
});
```

**Problems:**
- Name says nothing about expected behavior
- `toBeTruthy()` passes for `{}`, `[]`, `1`, `"error"`, etc.
- No clear specification

### Good: Specific Name + Precise Assertion

```typescript
test('submitting valid form data creates a new user account', async () => {
  const formData = { email: 'test@example.com', password: 'secure123' };

  const result = await handleSubmit(formData);

  expect(result).toEqual({
    success: true,
    userId: expect.any(String),
  });
});
```

**Why it's better:**
- Test name is a specification
- Assertion is precise and structural
- Fails clearly if behavior changes

---

### Bad: Testing Through Internals

```typescript
import { _parseConfig } from '../config/parser'; // internal export

test('parseConfig extracts database URL', () => {
  const result = _parseConfig(rawConfig);
  expect(result.dbUrl).toBe('postgres://...');
});
```

**Problems:**
- Imports internal function
- Test breaks if you reorganize internals
- Bypasses the real entry point

### Good: Testing Through Public API

```typescript
import { loadConfig } from '../config';

test('configuration includes database connection settings', () => {
  const config = loadConfig('test.env');

  expect(config.database.url).toBe('postgres://localhost/test');
  expect(config.database.poolSize).toBe(5);
});
```

**Why it's better:**
- Uses public API
- Tests what consumers actually use
- Resilient to internal changes

---

### Bad: Multiple Behaviors in One Test

```typescript
test('user authentication', async () => {
  // Testing login
  const loginResult = await auth.login('user@test.com', 'password');
  expect(loginResult.token).toBeDefined();

  // Testing token refresh
  const refreshResult = await auth.refresh(loginResult.token);
  expect(refreshResult.token).toBeDefined();

  // Testing logout
  await auth.logout(refreshResult.token);
  const status = await auth.checkSession(refreshResult.token);
  expect(status.valid).toBe(false);
});
```

**Problems:**
- Three behaviors crammed into one test
- If it fails, which behavior broke?
- Hard to maintain and understand

### Good: One Behavior Per Test

```typescript
test('valid credentials return an authentication token', async () => {
  const result = await auth.login('user@test.com', 'password');

  expect(result.token).toMatch(/^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$/);
});

test('logout invalidates the session', async () => {
  const { token } = await auth.login('user@test.com', 'password');

  await auth.logout(token);

  const status = await auth.checkSession(token);
  expect(status.valid).toBe(false);
});
```

**Why it's better:**
- Each test validates one behavior
- Failures are immediately diagnostic
- Easy to understand and maintain

---

## Rationale

Tests are specifications. They document what the system does and protect against regressions. When tests are coupled to implementation:

- **Refactoring becomes painful** — every internal change breaks tests
- **False confidence** — tests pass but don't verify real behavior
- **Maintenance burden** — you're testing implementation twice

Black-box tests treat the system as a consumer would. They verify contracts, not wiring. They survive refactors, catch real bugs, and serve as living documentation.

Write tests that answer: *"Does this system behave correctly?"* — not *"Does this code execute in the order I expect?"*

A test should be readable by someone who has never seen the implementation. If understanding the test requires understanding the code, the test has failed as documentation.

---

## Adapting to another repository

1. Copy `review-tests/SKILL.md` (any of the three synced paths) into the target repo under the same relative paths your tools expect (`.claude/skills/`, `.cursor/skills/`, `.codex/skills/` as applicable).
2. **Replace** the **Repository adapter** section below with your project’s conventions: test runner, directory layout, markers/tags, fixtures, external services to stub, CI constraints.
3. Optionally add a second adapter section (e.g. “Mobile client”) if you maintain multiple test surfaces in one repo.

---

## Repository adapter — QuantumBank (Flask + pytest)

**Project-specific.** General rules above still apply.

- **HTTP black box:** Shared `client` fixture in `test/conftest.py` (`app.test_client()`, lazy `from app import app`). Assert status codes, `Location` on redirects, JSON bodies, and **small stable substrings** — not full HTML snapshots.
- **Discovery:** `pytest.ini` sets `testpaths = test`, `pythonpath = .`, and markers **`public`**, **`banking`**, **`api`**. Test modules must be named `test_*.py`.
- **Markers:** `public` (no session), `banking` (login + HTML banking routes), `api` (JSON under `/api/`). Prefer `test_public_routes.py`, `test_banking_routes.py`, `test_api_routes.py` unless a new surface needs its own file.
- **Split.io:** CI often has no `SPLIT_API_KEY`. Do not assert copy that exists only on one home/pricing variant; use broad markers or JSON keys (see `test_home_root_200_has_known_shell`, `test_home_content_json_shape`).
- **Sample data:** `demo` user + SQLite (`init_db` / `create_sample_data`). Transfers in tests should use **small amounts**; avoid asserting exact balances unless the test controls DB state.

**Python / Flask red flags (same spirit as the Red Flags table):**

| Red Flag | Problem |
|----------|---------|
| Full-page `assert response.data == open("fixture.html").read()` | Brittle; any template tweak breaks CI |
| `from models import ...` inside route tests | Bypasses HTTP contract unless the test is a true unit test elsewhere |
| Asserting a single marketing string only on one Split treatment | Fails in CI when Split is off |

When in doubt, match patterns in `test/test_public_routes.py`, `test/test_banking_routes.py`, and `test/test_api_routes.py`.
