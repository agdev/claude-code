# AWS SDK Mocking Best Practices

**Last Updated:** 2025-12-12
**Applies To:** AWS SDK v3 with Vitest/Jest

This guide covers testing code that integrates with AWS services, preventing resource pollution and ensuring test isolation.

---

## Two Testing Approaches

### Option 1: aws-sdk-client-mock (Recommended for Unit Tests - 80%)

Intercepts AWS SDK v3 client calls before they reach the network.

**Installation:**
```bash
npm install --save-dev aws-sdk-client-mock aws-sdk-client-mock-vitest
```

**Setup (tests/setup.ts):**
```typescript
import 'aws-sdk-client-mock-vitest';
```

**Characteristics:**
| Aspect | Value |
|--------|-------|
| Network calls | None |
| Speed | Microseconds per test |
| AWS costs | $0 |
| Works offline | Yes |

### Option 2: LocalStack (For Integration Tests - 15%)

Docker container running fake AWS services locally.

**Docker Setup:**
```yaml
services:
  localstack:
    image: localstack/localstack:3.7.2
    environment:
      - SERVICES=secretsmanager,s3,dynamodb
    ports:
      - "4566:4566"
```

**Characteristics:**
| Aspect | Value |
|--------|-------|
| Network calls | Yes (localhost) |
| Speed | Milliseconds per test |
| AWS API fidelity | ~95% real behavior |

---

## Decision Matrix

| Scenario | Mock | LocalStack |
|----------|------|------------|
| Unit testing service logic | ✅ | ❌ |
| Testing error handling | ✅ | ❌ |
| Fast CI/CD feedback | ✅ | ❌ |
| Verifying AWS API contracts | ❌ | ✅ |
| Testing data round-trips | ❌ | ✅ |
| Cross-service integration | ❌ | ✅ |

---

## Global Mock Setup Pattern (Recommended)

Create a global mock that rejects unmocked commands as a safety net.

**tests/setup.ts:**
```typescript
import { beforeEach } from 'vitest';
import 'aws-sdk-client-mock-vitest';
import { mockClient } from 'aws-sdk-client-mock';
import { SecretsManagerClient } from '@aws-sdk/client-secrets-manager';
import { S3Client } from '@aws-sdk/client-s3';

// Create global mocks
export const smMock = mockClient(SecretsManagerClient);
export const s3Mock = mockClient(S3Client);

// Default: reject any unmocked command (safety net)
smMock.onAnyCommand().rejects(new Error('AWS mock not configured for this command'));
s3Mock.onAnyCommand().rejects(new Error('AWS mock not configured for this command'));

beforeEach(() => {
  smMock.reset();
  s3Mock.reset();
  // Re-apply default rejection after reset
  smMock.onAnyCommand().rejects(new Error('AWS mock not configured for this command'));
  s3Mock.onAnyCommand().rejects(new Error('AWS mock not configured for this command'));
});
```

**Benefits:**
- Unmocked commands fail immediately with clear error
- Test pollution prevented by reset in beforeEach
- Zero network calls possible

---

## Per-Test Configuration Pattern

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { smMock } from '../../setup.js';
import {
  CreateSecretCommand,
  GetSecretValueCommand,
  ResourceNotFoundException,
  ResourceExistsException
} from '@aws-sdk/client-secrets-manager';

describe('SecretsService', () => {
  beforeEach(() => {
    smMock.reset();
    SecretsService.resetClient(); // Reset singleton if applicable
  });

  it('When creating secret, then returns ARN', async () => {
    // Arrange
    smMock.on(CreateSecretCommand).resolves({
      ARN: 'arn:aws:secretsmanager:us-east-1:123:secret:test-AbCdEf',
      Name: 'test-secret'
    });

    // Act
    const result = await SecretsService.createSecret('my-app', 'data');

    // Assert
    expect(result.success).toBe(true);
    expect(smMock).toHaveReceivedCommandWith(CreateSecretCommand, {
      Name: expect.stringContaining('my-app')
    });
  });

  it('When secret exists, then returns error', async () => {
    // Arrange
    smMock.on(CreateSecretCommand).rejects(
      new ResourceExistsException({
        $metadata: {},
        message: 'Secret already exists'
      })
    );

    // Act
    const result = await SecretsService.createSecret('existing', 'data');

    // Assert
    expect(result.success).toBe(false);
    expect(result.error).toContain('already exists');
  });
});
```

---

## Common Patterns

### Pattern 1: Mock Reset (CRITICAL)

```typescript
const smMock = mockClient(SecretsManagerClient);

beforeEach(() => {
  smMock.reset(); // ALWAYS reset between tests
});
```

### Pattern 2: Chained Responses

```typescript
smMock
  .on(GetSecretValueCommand)
  .resolvesOnce({ SecretString: '{"version": 1}' })  // First call
  .resolvesOnce({ SecretString: '{"version": 2}' }); // Second call
```

### Pattern 3: Conditional Responses

```typescript
smMock
  .on(GetSecretValueCommand, { SecretId: 'app-a' })
  .resolves({ SecretString: '{"key": "value-a"}' })
  .on(GetSecretValueCommand, { SecretId: 'app-b' })
  .resolves({ SecretString: '{"key": "value-b"}' });
```

### Pattern 4: Singleton Service Reset

Services using singleton pattern need reset method for testing:

```typescript
// Service implementation
class SecretsServiceClass {
  private static client: SecretsManagerClient | null = null;

  private static getClient(): SecretsManagerClient {
    if (!this.client) {
      this.client = new SecretsManagerClient({ region: 'us-east-1' });
    }
    return this.client;
  }

  // Reset for testing
  public static resetClient(): void {
    this.client = null;
  }
}

// Test usage
beforeEach(() => {
  smMock.reset();
  SecretsService.resetClient(); // Pick up fresh mock
});
```

### Pattern 5: LocalStack Cleanup

```typescript
const TEST_PREFIX = 'test-vitest-';

afterEach(async () => {
  const secrets = await client.send(new ListSecretsCommand({
    Filters: [{ Key: 'name', Values: [TEST_PREFIX] }]
  }));
  for (const secret of secrets.SecretList || []) {
    await client.send(new DeleteSecretCommand({
      SecretId: secret.Name,
      ForceDeleteWithoutRecovery: true
    }));
  }
});
```

---

## Anti-Patterns

### ❌ Don't: Test against real AWS in unit tests
```typescript
// Creates real resources, costs money, slow
const client = new SecretsManagerClient({ region: 'us-east-1' });
await client.send(new CreateSecretCommand({ Name: 'test', SecretString: '{}' }));
```

### ❌ Don't: Forget to reset mocks
```typescript
it('test 1', async () => {
  smMock.on(CreateSecretCommand).resolves({ Name: 'a' });
});

it('test 2', async () => {
  // Still has mock from test 1! Unpredictable behavior
});
```

### ❌ Don't: Share state between tests
```typescript
it('creates secret', async () => {
  await createSecret('shared-secret');
});

it('reads secret', async () => {
  // Fails if run alone or in different order
  const secret = await getSecret('shared-secret');
});
```

### ✅ Do: Self-contained tests
```typescript
it('When secret exists, then retrieves it', async () => {
  // Arrange - Create what this test needs
  smMock.on(GetSecretValueCommand).resolves({
    SecretString: JSON.stringify({ key: 'value' })
  });

  // Act
  const result = await service.getSecret('my-secret');

  // Assert
  expect(result.key).toBe('value');
});
```

---

## Applicability to Other Cloud SDKs

These patterns apply to other cloud provider SDKs:

| Provider | Mock Library | LocalStack Equivalent |
|----------|-------------|----------------------|
| AWS | aws-sdk-client-mock | LocalStack |
| GCP | @google-cloud/xxx mocks | Cloud SDK emulators |
| Azure | @azure/xxx mocks | Azurite |
| Stripe | stripe-mock | stripe-mock server |
| Twilio | Manual mocking | - |

The core principles remain the same:
1. Mock at SDK boundary for unit tests
2. Use emulators for integration tests
3. Reset mocks between tests
4. Never test against production services

---

## References

- [aws-sdk-client-mock](https://github.com/m-radzikowski/aws-sdk-client-mock)
- [LocalStack](https://docs.localstack.cloud/)
- [AWS SDK v3 Mocking](https://aws.amazon.com/blogs/developer/mocking-modular-aws-sdk-for-javascript-v3-in-unit-tests/)
