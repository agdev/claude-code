# E2E Testing Resilience Guide

**Last Updated:** 2025-11-25

This guide covers best practices for writing resilient Playwright e2e tests that survive UI changes.

---

## Selector Priority (Playwright Recommended)

Use selectors in this order of preference:

| Priority | Method | Use For | Example |
|----------|--------|---------|---------|
| 1 | `getByRole()` | Buttons, headings, links | `getByRole('button', { name: /submit/i })` |
| 2 | `getByLabel()` | Form inputs with labels | `getByLabel('Email')` |
| 3 | `getByPlaceholder()` | Inputs with placeholder | `getByPlaceholder('Enter email')` |
| 4 | `getByText()` | Non-interactive elements | `getByText(/welcome/i)` |
| 5 | `getByTestId()` | Non-semantic elements | `getByTestId('error-message')` |
| 6 | CSS/XPath | Last resort only | `locator('.class-name')` |

---

## Bad vs Good Patterns

### Form Inputs

```typescript
// BAD - Breaks when placeholder changes
await page.fill('input[placeholder="John"]', name);

// GOOD - Uses accessible label
await page.getByLabel('First Name').fill(name);
```

### Buttons

```typescript
// BAD - Breaks when text changes
await page.click('button:has-text("Save Changes")');

// GOOD - Flexible regex matching
await page.getByRole('button', { name: /save/i }).click();
```

### Headings

```typescript
// BAD - Breaks when heading level changes
await page.locator('h1:has-text("App Master")').waitFor();

// GOOD - Role-based, flexible
await page.getByRole('heading', { name: /app master/i }).waitFor();
```

### Error Messages

```typescript
// BAD - Breaks when CSS classes change
await page.locator('.text-destructive').isVisible();

// GOOD - Stable test ID
await page.getByTestId('field-error').isVisible();
```

### Waiting

```typescript
// BAD - Arbitrary timeout
await page.waitForTimeout(3000);

// GOOD - Wait for actual content
await expect(page.getByText(/success/i)).toBeVisible();

// GOOD - Wait for navigation
await expect(page).toHaveURL(/\/users/);
```

---

## When to Use `data-testid`

Add `data-testid` only for elements without semantic meaning:

- Error messages and validation feedback
- Toast notifications
- Loading indicators
- Dynamic list items
- Complex third-party components

### Adding Test IDs to React Components

```tsx
// In React component
<FormMessage data-testid="email-error" />
<div data-testid="success-toast" role="status">
  User created successfully
</div>
<Spinner data-testid="loading-indicator" />
```

### Using Test IDs in Page Objects

```typescript
async hasEmailError(): Promise<boolean> {
  return await this.page.getByTestId('email-error').isVisible();
}

async waitForLoading(): Promise<void> {
  await this.page.getByTestId('loading-indicator').waitFor({ state: 'hidden' });
}
```

---

## Page Object Best Practices

### Keep Selectors Private

```typescript
// Page object
export class LoginPage extends BasePage {
  // NO selector objects exposed to tests

  async fillEmail(email: string): Promise<void> {
    await this.page.getByLabel('Email').fill(email);
  }

  async submit(): Promise<void> {
    await this.page.getByRole('button', { name: /sign in/i }).click();
  }
}

// Test reads like user story
await loginPage.fillEmail('test@example.com');
await loginPage.submit();
```

### Semantic Method Names

```typescript
// BAD - Implementation-focused
async clickSubmitButton(): Promise<void>
async fillInputField(selector: string, value: string): Promise<void>

// GOOD - User-action focused
async submitForm(): Promise<void>
async enterEmail(email: string): Promise<void>
async expectSuccessMessage(): Promise<void>
```

---

## Text Matching Strategies

### Use Case-Insensitive Regex

```typescript
// Matches: "Submit", "SUBMIT", "submit"
getByRole('button', { name: /submit/i })

// Matches: "Create User", "CREATE USER", "create user"
getByRole('heading', { name: /create user/i })
```

### Partial Matching

```typescript
// Matches: "Create", "Create User", "Create New User"
getByRole('button', { name: /create/i })

// Matches any heading containing "user"
getByRole('heading', { name: /user/i })
```

### Exact Matching (When Needed)

```typescript
// Use exact: true for precise matches
getByRole('button', { name: 'Submit', exact: true })
```

---

## Waiting Strategies

### Prefer Assertions Over Timeouts

```typescript
// BAD
await page.waitForTimeout(2000);
await page.click('button');

// GOOD - Playwright auto-waits for actionable elements
await page.getByRole('button').click();

// GOOD - Wait for specific condition
await expect(page.getByRole('button')).toBeEnabled();
await page.getByRole('button').click();
```

### Network Waiting

```typescript
// Wait for all network requests to complete
await page.waitForLoadState('networkidle');

// Wait for specific API response
await page.waitForResponse(resp =>
  resp.url().includes('/api/users') && resp.status() === 200
);
```

### Element State Waiting

```typescript
// Wait for element to appear
await page.getByTestId('user-list').waitFor({ state: 'visible' });

// Wait for element to disappear (loading spinner)
await page.getByTestId('loading').waitFor({ state: 'hidden' });

// Wait for element to be attached to DOM
await page.getByRole('dialog').waitFor({ state: 'attached' });
```

---

## Testing User Behavior, Not Implementation

### Focus on Outcomes

```typescript
// BAD - Testing implementation
await expect(page.locator('.bg-green-500')).toBeVisible();
await expect(page.locator('[data-state="success"]')).toBeVisible();

// GOOD - Testing user-visible outcome
await expect(page.getByText(/user created successfully/i)).toBeVisible();
await expect(page.getByRole('alert')).toContainText(/success/i);
```

### Test User Flows

```typescript
// BAD - Testing isolated DOM elements
test('submit button exists', async () => {
  await expect(page.locator('button[type="submit"]')).toBeVisible();
});

// GOOD - Testing user flow
test('user can create account', async () => {
  await page.getByLabel('Email').fill('test@example.com');
  await page.getByLabel('Password').fill('SecurePass123!');
  await page.getByRole('button', { name: /create account/i }).click();
  await expect(page.getByText(/welcome/i)).toBeVisible();
});
```

---

## Accessibility Benefits

Using semantic selectors improves accessibility:

```typescript
// This test passes only if the page is accessible
await page.getByRole('button', { name: /submit/i }).click();

// Requires:
// - Proper button element (not div with onclick)
// - Accessible name (button text, aria-label, or aria-labelledby)
```

### Adding ARIA When Needed

```tsx
// When button text isn't descriptive enough
<button aria-label="Submit user registration form">
  <Icon name="check" /> {/* No visible text */}
</button>

// Test can now find it
await page.getByRole('button', { name: /submit user registration/i }).click();
```

---

## Quick Reference

### Form Fields
```typescript
getByLabel('Email')                    // Input with label
getByPlaceholder('Enter email')        // Input with placeholder
getByRole('textbox', { name: /email/i }) // Generic text input
getByRole('combobox')                  // Select/dropdown
getByRole('checkbox', { name: /agree/i }) // Checkbox
```

### Interactive Elements
```typescript
getByRole('button', { name: /submit/i })  // Button
getByRole('link', { name: /home/i })      // Anchor link
getByRole('tab', { name: /settings/i })   // Tab
getByRole('menuitem', { name: /logout/i }) // Menu item
```

### Content Elements
```typescript
getByRole('heading', { name: /title/i })  // h1-h6
getByRole('heading', { level: 1 })        // Specific h1
getByRole('alert')                        // Alert/notification
getByRole('dialog')                       // Modal/dialog
getByRole('table')                        // Table
getByRole('row')                          // Table row
```

### Multiple Elements
```typescript
getByRole('listitem').first()             // First list item
getByRole('listitem').nth(2)              // Third list item
getByRole('listitem').last()              // Last list item
getByRole('row').filter({ hasText: 'John' }) // Row containing text
```

---

## Migration Checklist

When updating existing tests:

- [ ] Replace `input[placeholder="..."]` with `getByLabel()`
- [ ] Replace `button:has-text("...")` with `getByRole('button', { name: /.../ })`
- [ ] Replace `h1:has-text("...")` with `getByRole('heading', { name: /.../ })`
- [ ] Replace CSS class selectors with `getByTestId()` (add test IDs first)
- [ ] Replace `waitForTimeout()` with assertion-based waits
- [ ] Use case-insensitive regex for text matching
- [ ] Keep selectors internal to page objects

---

## Sources

- [Playwright Locators Documentation](https://playwright.dev/docs/locators)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Testing Library Guiding Principles](https://testing-library.com/docs/guiding-principles/)
- [WAI-ARIA Roles](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles)
