# Error Handling Test Matrix

**Last Updated:** 2025-12-12
**Purpose:** Guide for testing error scenarios with correct HTTP semantics

---

## HTTP Status to Error Type Mapping

| HTTP Status | Category | Error Type | Meaning |
|-------------|----------|------------|---------|
| 400 | Client | `BadRequestError` / `ValidationError` | Invalid request syntax |
| 401 | Client | `UnauthorizedError` | Authentication required |
| 403 | Client | `ForbiddenError` | Authenticated but insufficient permissions |
| 404 | Client | `NotFoundError` | Resource does not exist |
| 409 | Client | `ConflictError` | State conflict (e.g., duplicate) |
| 422 | Client | `ValidationError` | Semantic validation failure |
| 500 | Server | `ServiceUnavailableError` | Internal server error |
| 502 | Server | `ServiceUnavailableError` | Bad gateway |
| 503 | Server | `ServiceUnavailableError` | Service unavailable |
| 504 | Server | `ServiceUnavailableError` | Gateway timeout |
| ECONNREFUSED | Network | `ServiceUnavailableError` | Connection refused |
| ETIMEDOUT | Network | `ServiceUnavailableError` | Connection timeout |
| ENOTFOUND | Network | `ServiceUnavailableError` | DNS lookup failed |

---

## Decision Tree

```
Is it a network error (no response)?
  → ServiceUnavailableError

Is it a 5xx server error?
  → ServiceUnavailableError

Is it a 404 error?
  → NotFoundError (NOT ServiceUnavailableError!)

Is it a 401 error?
  → UnauthorizedError

Is it a 403 error?
  → ForbiddenError

Is it a 400 or 422 error?
  → ValidationError or BadRequestError

Is it a 409 error?
  → ConflictError
```

---

## Test Template: Parameterized Error Tests

Use parameterized tests to cover all error scenarios systematically:

```typescript
describe('UserService.getUser() - Error Handling', () => {
  describe('HTTP 4xx Client Errors', () => {
    const clientErrorCases = [
      { status: 400, errorType: BadRequestError, desc: 'bad request' },
      { status: 401, errorType: UnauthorizedError, desc: 'unauthorized' },
      { status: 403, errorType: ForbiddenError, desc: 'forbidden' },
      { status: 404, errorType: NotFoundError, desc: 'not found' },
      { status: 409, errorType: ConflictError, desc: 'conflict' },
      { status: 422, errorType: ValidationError, desc: 'validation failure' },
    ];

    clientErrorCases.forEach(({ status, errorType, desc }) => {
      it(`When ${desc} (${status}), then throws ${errorType.name}`, async () => {
        // Arrange
        nock(API_URL).get('/users/123').reply(status, { message: desc });

        // Act & Assert
        await expect(service.getUser('123')).rejects.toThrow(errorType);
      });
    });
  });

  describe('HTTP 5xx Server Errors', () => {
    const serverErrorCases = [
      { status: 500, desc: 'internal server error' },
      { status: 502, desc: 'bad gateway' },
      { status: 503, desc: 'service unavailable' },
      { status: 504, desc: 'gateway timeout' },
    ];

    serverErrorCases.forEach(({ status, desc }) => {
      it(`When ${desc} (${status}), then throws ServiceUnavailableError`, async () => {
        nock(API_URL).get('/users/123').reply(status);
        await expect(service.getUser('123')).rejects.toThrow(ServiceUnavailableError);
      });
    });
  });

  describe('Network Errors', () => {
    const networkErrorCases = [
      { code: 'ECONNREFUSED', desc: 'connection refused' },
      { code: 'ETIMEDOUT', desc: 'timeout' },
      { code: 'ENOTFOUND', desc: 'host not found' },
      { code: 'ECONNRESET', desc: 'connection reset' },
    ];

    networkErrorCases.forEach(({ code, desc }) => {
      it(`When ${desc} (${code}), then throws ServiceUnavailableError`, async () => {
        nock(API_URL).get('/users/123').replyWithError({ code });
        await expect(service.getUser('123')).rejects.toThrow(ServiceUnavailableError);
      });
    });
  });
});
```

---

## Error Context Validation Pattern

Validate that errors contain useful debugging context:

```typescript
it('When error occurs, then preserves context for debugging', async () => {
  // Arrange
  nock(API_URL)
    .get('/users/123')
    .reply(404, { message: 'User not found' });

  // Act & Assert
  try {
    await service.getUser('123');
    fail('Expected NotFoundError to be thrown');
  } catch (error) {
    // Validate error type
    expect(error).toBeInstanceOf(NotFoundError);

    // Validate error message contains context
    expect(error.message).toMatch(/user.*not found/i);

    // Validate error properties (if your error classes support this)
    expect(error.statusCode).toBe(404);
    expect(error.context).toMatchObject({
      userId: '123',
      service: 'UserService',
    });
  }
});
```

---

## Error Propagation Testing

Test that errors propagate correctly through layers:

```typescript
describe('Error Propagation Through Layers', () => {
  describe('HTTP Client Layer', () => {
    it('When 404 response, then throws NotFoundError', async () => {
      nock(API_URL).get('/users/123').reply(404);
      await expect(httpClient.get('/users/123')).rejects.toThrow(NotFoundError);
    });
  });

  describe('Service Layer', () => {
    it('When NotFoundError from client, then propagates NotFoundError', async () => {
      vi.spyOn(httpClient, 'get').mockRejectedValue(new NotFoundError('Not found'));
      await expect(userService.getUser('123')).rejects.toThrow(NotFoundError);
    });

    it('When NotFoundError, then adds business context', async () => {
      vi.spyOn(httpClient, 'get').mockRejectedValue(new NotFoundError('Not found'));

      try {
        await userService.getUser('123');
        fail('Expected error');
      } catch (error) {
        expect(error).toBeInstanceOf(NotFoundError);
        expect(error.message).toContain('User'); // Service added context
      }
    });
  });

  describe('Controller Layer', () => {
    it('When NotFoundError, then returns 404 response', async () => {
      vi.spyOn(userService, 'getUser').mockRejectedValue(
        new NotFoundError('User not found')
      );

      const response = await request(app)
        .get('/api/users/123')
        .expect(404);

      expect(response.body).toMatchObject({
        error: 'Not Found',
        message: expect.stringMatching(/user not found/i),
      });
    });
  });
});
```

---

## Common Anti-Patterns

### ❌ Anti-Pattern 1: Wrong Error Mapping

```typescript
// BAD - 404 is NOT service unavailable
it('When user not found, then throws ServiceUnavailableError', async () => {
  nock(API_URL).get('/user/123').reply(404);
  await expect(service.getUser('123')).rejects.toThrow(ServiceUnavailableError);
});

// GOOD - 404 means resource doesn't exist
it('When user not found (404), then throws NotFoundError', async () => {
  nock(API_URL).get('/user/123').reply(404);
  await expect(service.getUser('123')).rejects.toThrow(NotFoundError);
});
```

### ❌ Anti-Pattern 2: Generic Error Assertions

```typescript
// BAD - Any error passes, doesn't validate type
await expect(service.getUser('123')).rejects.toThrow();

// GOOD - Validates specific error type
await expect(service.getUser('123')).rejects.toThrow(NotFoundError);
```

### ❌ Anti-Pattern 3: Testing Implementation

```typescript
// BAD - Testing what code DOES, not what it SHOULD do
it('converts all errors to ServiceUnavailableError', async () => {
  nock(API_URL).get('/user/123').reply(404);
  await expect(service.getUser('123')).rejects.toThrow(ServiceUnavailableError);
});

// GOOD - Testing business requirements
it('When user not found, then indicates resource does not exist', async () => {
  nock(API_URL).get('/user/123').reply(404);
  await expect(service.getUser('123')).rejects.toThrow(NotFoundError);
});
```

### ❌ Anti-Pattern 4: Combined Error Tests

```typescript
// BAD - Multiple scenarios in one test
it('handles all errors', async () => {
  nock(API_URL).get('/a').reply(404);
  nock(API_URL).get('/b').reply(500);
  // Hard to understand which error maps to which
});

// GOOD - One test per error scenario
it('When 404, then throws NotFoundError', async () => { /* ... */ });
it('When 500, then throws ServiceUnavailableError', async () => { /* ... */ });
```

---

## Checklist for Error Handling Tests

When writing tests for API error handling, verify:

- [ ] **HTTP 404** → `NotFoundError` (NOT ServiceUnavailableError)
- [ ] **HTTP 401** → `UnauthorizedError`
- [ ] **HTTP 403** → `ForbiddenError`
- [ ] **HTTP 400/422** → `ValidationError` or `BadRequestError`
- [ ] **HTTP 409** → `ConflictError`
- [ ] **HTTP 5xx** → `ServiceUnavailableError`
- [ ] **Network errors** → `ServiceUnavailableError`
- [ ] Each error scenario has **separate test**
- [ ] Error messages contain **useful context**
- [ ] Tests validate **business requirements**, not just implementation

---

## References

- [MDN HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [RFC 7231 - HTTP/1.1 Semantics](https://tools.ietf.org/html/rfc7231)
