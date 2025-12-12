# Fake Timers Best Practices for AI Code Assistants

**Last Updated:** 2025-11-27
**Applies To:** Vitest, Jest, and similar testing frameworks
**Purpose:** Guide for writing reliable tests with fake timers

---

## Overview

Fake timers allow tests to control time-based operations (setTimeout, setInterval, Date) without waiting for real time to pass. However, they introduce complexity around async operations that can cause flaky tests and confusing warnings.

---

## When to Use Fake Timers

### USE Fake Timers For:
- Testing debounce/throttle functions
- Testing setTimeout/setInterval logic
- Testing animations or transitions
- Testing cache TTL expiration
- Testing polling mechanisms
- Speeding up tests that would otherwise wait for delays

### DO NOT USE Fake Timers For:
- Simple async/await operations without timers
- Promise rejections in retry logic (use real timers with short delays)
- Network request mocking (use nock/msw instead)
- Tests where timing complexity outweighs benefits

---

## The Golden Rules

### Rule 1: Match Timer Scope to Test Scope

```typescript
// GOOD: Setup and teardown in each test
describe('MyComponent', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
  });
});

// BAD: Global fake timers without cleanup
vi.useFakeTimers(); // At module level - affects all tests!
```

### Rule 2: Advance Timers BEFORE Awaiting Promises

```typescript
// GOOD: Start promise, advance time, then await
const promise = functionWithTimeout();
await vi.advanceTimersByTimeAsync(1000);
const result = await promise;

// BAD: Await immediately (promise never resolves - timers frozen)
const result = await functionWithTimeout(); // Hangs forever!
```

### Rule 3: Use `runAllTimersAsync()` for Unknown Timer Counts

```typescript
// GOOD: When you don't know exact timing
const promise = retryableOperation();
await vi.runAllTimersAsync();
await promise;

// RISKY: Assumes exact timing
await vi.advanceTimersByTimeAsync(3000); // What if retry delay changes?
```

---

## Promise Rejection Patterns

### The Problem

Fake timers + rejected promises = unhandled rejection warnings:

```typescript
// BAD: Causes "PromiseRejectionHandledWarning"
it('should handle error', async () => {
  vi.useFakeTimers();
  const mockFn = vi.fn().mockRejectedValue(new Error('fail'));

  const promise = handler.execute(mockFn);
  await vi.runAllTimersAsync();  // Rejection happens HERE

  // By the time we get here, rejection is "unhandled"
  try {
    await promise;
  } catch (e) {
    expect(e.message).toBe('fail');
  }
});
```

### Solution 1: Use `rejects` Matcher (Preferred)

```typescript
// GOOD: Vitest handles the rejection properly
it('should handle error', async () => {
  vi.useFakeTimers();
  const mockFn = vi.fn().mockRejectedValue(new Error('fail'));

  await expect(handler.execute(mockFn)).rejects.toThrow('fail');
});
```

### Solution 2: Use Real Timers with Short Delays

```typescript
// GOOD: For complex retry scenarios
it('should exhaust retries', async () => {
  vi.useRealTimers(); // Switch to real timers

  const config = { maxRetries: 2, initialDelay: 1 }; // 1ms delay
  const handler = new RetryHandler(config);
  const mockFn = vi.fn().mockRejectedValue(new Error('fail'));

  await expect(handler.execute(mockFn)).rejects.toThrow('fail');
  expect(mockFn).toHaveBeenCalledTimes(3);
});
```

### Solution 3: Catch Rejection Early

```typescript
// GOOD: Attach catch handler before advancing timers
it('should handle error', async () => {
  vi.useFakeTimers();
  const mockFn = vi.fn().mockRejectedValue(new Error('fail'));

  const promise = handler.execute(mockFn);

  // Attach handler BEFORE advancing timers
  let caughtError: Error | undefined;
  promise.catch((e) => { caughtError = e; });

  await vi.runAllTimersAsync();
  await promise.catch(() => {}); // Swallow to prevent unhandled

  expect(caughtError?.message).toBe('fail');
});
```

---

## Common Patterns

### Pattern: Testing Cache Expiration

```typescript
it('should expire cached entries after TTL', async () => {
  vi.useFakeTimers();

  const cache = new Cache({ ttl: 5000 }); // 5 second TTL
  cache.set('key', 'value');

  // Before expiration
  expect(cache.get('key')).toBe('value');

  // Advance past TTL
  await vi.advanceTimersByTimeAsync(5001);

  // After expiration
  expect(cache.get('key')).toBeNull();
});
```

### Pattern: Testing Debounce

```typescript
it('should debounce rapid calls', async () => {
  vi.useFakeTimers();

  const callback = vi.fn();
  const debounced = debounce(callback, 100);

  // Rapid calls
  debounced('a');
  debounced('b');
  debounced('c');

  // Not called yet
  expect(callback).not.toHaveBeenCalled();

  // Advance past debounce delay
  await vi.advanceTimersByTimeAsync(100);

  // Called once with last value
  expect(callback).toHaveBeenCalledTimes(1);
  expect(callback).toHaveBeenCalledWith('c');
});
```

### Pattern: Testing Retry with Backoff

```typescript
// For simple cases: use fake timers
it('should retry with exponential backoff', async () => {
  vi.useFakeTimers();

  const mockFn = vi.fn()
    .mockRejectedValueOnce(new Error('fail'))
    .mockResolvedValueOnce('success');

  const promise = retryWithBackoff(mockFn);
  await vi.runAllTimersAsync();
  const result = await promise;

  expect(result).toBe('success');
  expect(mockFn).toHaveBeenCalledTimes(2);
});

// For error cases: use real timers with short delays
it('should throw after max retries', async () => {
  vi.useRealTimers();

  const mockFn = vi.fn().mockRejectedValue(new Error('fail'));
  const config = { maxRetries: 2, delay: 1 }; // 1ms delay

  await expect(retryWithBackoff(mockFn, config)).rejects.toThrow('fail');
  expect(mockFn).toHaveBeenCalledTimes(3);
});
```

---

## Retry Logic Testing Strategies

When testing code with retry/backoff logic, choose the right approach:

### When to Use Fake Timers for Retry Tests

Use fake timers when:
- Testing that retry succeeds eventually (happy path)
- Testing retry count/timing behavior
- Timer delays are the only async operation

```typescript
it('When transient failure then success, then retries and succeeds', async () => {
  vi.useFakeTimers();

  const mockFn = vi.fn()
    .mockRejectedValueOnce(new Error('Network error'))
    .mockRejectedValueOnce(new Error('Network error'))
    .mockResolvedValueOnce({ data: 'success' });

  const promise = retryWithBackoff(mockFn, { maxRetries: 3, delay: 1000 });
  await vi.runAllTimersAsync();
  const result = await promise;

  expect(result.data).toBe('success');
  expect(mockFn).toHaveBeenCalledTimes(3);
});
```

### When to Use Real Timers with Short Delays

Use real timers with 1ms delays when:
- Testing that retries exhaust and throw
- Testing error propagation after max retries
- Avoiding "unhandled promise rejection" warnings

```typescript
it('When all retries fail, then throws final error', async () => {
  vi.useRealTimers(); // Switch to real timers

  const mockFn = vi.fn().mockRejectedValue(new Error('Permanent failure'));

  // Use tiny delays - still tests behavior, but runs fast
  const config = { maxRetries: 3, initialDelay: 1, maxDelay: 1 };

  await expect(retryWithBackoff(mockFn, config)).rejects.toThrow('Permanent failure');
  expect(mockFn).toHaveBeenCalledTimes(4); // Initial + 3 retries
});
```

### Retry Test Decision Matrix

| Scenario | Use Fake Timers? | Why |
|----------|------------------|-----|
| Retry succeeds after N attempts | Yes | `runAllTimersAsync` handles all delays |
| Retry exhausts, throws error | **No** | Use real timers with 1ms delays to avoid rejection warnings |
| Testing exact delay timing | Yes | Can assert specific delay amounts |
| Testing with real network errors | **No** | Network mocking (nock) has its own timing |

### Advanced: Testing Retry with Specific Delays

```typescript
it('When retry, then uses exponential backoff delays', async () => {
  vi.useFakeTimers();

  const mockFn = vi.fn()
    .mockRejectedValueOnce(new Error('fail'))
    .mockRejectedValueOnce(new Error('fail'))
    .mockResolvedValueOnce('success');

  const promise = retryWithBackoff(mockFn, { initialDelay: 100 });

  // Verify first retry after 100ms
  await vi.advanceTimersByTimeAsync(100);
  expect(mockFn).toHaveBeenCalledTimes(2);

  // Verify second retry after 200ms (exponential backoff)
  await vi.advanceTimersByTimeAsync(200);
  expect(mockFn).toHaveBeenCalledTimes(3);

  await promise;
});
```

### Pattern: Testing Polling

```typescript
it('should poll until condition is met', async () => {
  vi.useFakeTimers();

  let counter = 0;
  const checkCondition = vi.fn(() => {
    counter++;
    return counter >= 3; // True on 3rd call
  });

  const promise = pollUntil(checkCondition, { interval: 100 });

  // First check (immediate)
  expect(checkCondition).toHaveBeenCalledTimes(1);

  // Advance to trigger more polls
  await vi.advanceTimersByTimeAsync(100);
  expect(checkCondition).toHaveBeenCalledTimes(2);

  await vi.advanceTimersByTimeAsync(100);
  expect(checkCondition).toHaveBeenCalledTimes(3);

  // Promise should resolve now
  await promise;
});
```

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Forgetting to Advance Timers

```typescript
// BAD: Test hangs forever
it('should timeout', async () => {
  vi.useFakeTimers();

  const result = await functionWithTimeout(); // Never completes!
  expect(result).toBe('timeout');
});

// GOOD: Advance timers
it('should timeout', async () => {
  vi.useFakeTimers();

  const promise = functionWithTimeout();
  await vi.advanceTimersByTimeAsync(5000);
  const result = await promise;

  expect(result).toBe('timeout');
});
```

### Anti-Pattern 2: Not Restoring Real Timers

```typescript
// BAD: Affects subsequent tests
it('test one', () => {
  vi.useFakeTimers();
  // ... test code
  // Missing: vi.useRealTimers()
});

it('test two', async () => {
  // This test unexpectedly uses fake timers!
  await delay(100); // Hangs!
});

// GOOD: Always cleanup
afterEach(() => {
  vi.useRealTimers();
});
```

### Anti-Pattern 3: Mixing Fake and Real Time Expectations

```typescript
// BAD: Confusing and fragile
it('mixed timers', async () => {
  vi.useFakeTimers();

  const start = Date.now(); // Frozen!
  await vi.advanceTimersByTimeAsync(1000);
  const end = Date.now(); // Still frozen at same time!

  expect(end - start).toBe(1000); // FAILS! Both are same value
});

// GOOD: Use vi.advanceTimersByTime for elapsed time checks
it('check elapsed', async () => {
  vi.useFakeTimers();

  const startTime = vi.getMockedSystemTime()?.getTime() || Date.now();
  await vi.advanceTimersByTimeAsync(1000);
  const endTime = vi.getMockedSystemTime()?.getTime() || Date.now();

  expect(endTime - startTime).toBe(1000);
});
```

### Anti-Pattern 4: Using setImmediate/nextTick with Fake Timers

```typescript
// BAD: setImmediate may not work as expected
it('with setImmediate', async () => {
  vi.useFakeTimers();

  let called = false;
  setImmediate(() => { called = true; });

  await vi.runAllTimersAsync(); // May not trigger setImmediate!
  expect(called).toBe(true); // Can fail!
});

// GOOD: Use setTimeout(fn, 0) instead
it('with setTimeout 0', async () => {
  vi.useFakeTimers();

  let called = false;
  setTimeout(() => { called = true; }, 0);

  await vi.runAllTimersAsync();
  expect(called).toBe(true);
});
```

---

## Decision Matrix

| Scenario | Fake Timers? | Method |
|----------|--------------|--------|
| Simple timeout test | Yes | `advanceTimersByTimeAsync` |
| Cache TTL expiration | Yes | `advanceTimersByTimeAsync` |
| Debounce/throttle | Yes | `advanceTimersByTimeAsync` |
| Retry succeeds eventually | Yes | `runAllTimersAsync` |
| Retry exhausts and throws | **No** | Real timers, short delays |
| Promise rejection tests | **No** | Use `rejects` matcher |
| Network timeout | **No** | Mock the network layer |
| Animation/transition | Yes | `advanceTimersByTimeAsync` |
| Date-dependent logic | Yes | `setSystemTime` |
| Polling until condition | Yes | `advanceTimersByTimeAsync` |

---

## Framework-Specific Notes

### Vitest

```typescript
import { vi } from 'vitest';

vi.useFakeTimers();
vi.useRealTimers();
vi.advanceTimersByTime(ms);        // Sync
vi.advanceTimersByTimeAsync(ms);   // Async (preferred)
vi.runAllTimers();                 // Sync
vi.runAllTimersAsync();            // Async (preferred)
vi.setSystemTime(date);            // Mock Date.now()
vi.getMockedSystemTime();          // Get current mocked time
```

### Jest

```typescript
jest.useFakeTimers();
jest.useRealTimers();
jest.advanceTimersByTime(ms);
jest.runAllTimers();
jest.setSystemTime(date);
```

---

## Summary Checklist

Before using fake timers in a test:

- [ ] Is this test about timing/delays? (If no, don't use fake timers)
- [ ] Will promises reject? (If yes, use `rejects` matcher or real timers)
- [ ] Added `beforeEach(() => vi.useFakeTimers())`?
- [ ] Added `afterEach(() => vi.useRealTimers())`?
- [ ] Using async timer methods (`advanceTimersByTimeAsync`)?
- [ ] Starting promises BEFORE advancing timers?
- [ ] Using `runAllTimersAsync` when timer count is unknown?

---

## References

- [Vitest Timer Mocks](https://vitest.dev/guide/mocking.html#timers)
- [Jest Timer Mocks](https://jestjs.io/docs/timer-mocks)
- [Testing Library Async Utilities](https://testing-library.com/docs/dom-testing-library/api-async/)
