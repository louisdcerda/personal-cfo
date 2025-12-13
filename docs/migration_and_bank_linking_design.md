# Design Document: Email to Phone Migration & Bank Linking Page

---

## 1. Overview

**Purpose:** This document outlines the plan to:
1. Complete the migration from email-based authentication to phone number-based authentication
2. Create a dedicated bank linking page separate from the Dashboard

**Status:** Design Phase - Awaiting Review

---

## 2. Current State Analysis

### 2.1 Email Usage (To Be Migrated)

**Backend:**
- `User` model has `email` field (String, unique, indexed)
- All Pydantic schemas use `EmailStr` validation
- User routes query/filter by email
- CRUD operations use `get_user_by_email()`
- Error messages reference "email"

**Frontend:**
- SignUpPage uses email input field
- SignInPage uses email input field
- LandingPage has email capture form
- localStorage stores "email" key
- Form validation uses `type="email"`

**Database:**
- `users` table has `email` column (String(255), unique, indexed)

### 2.2 Bank Linking (Current Implementation)

**Current State:**
- Bank linking is embedded in Dashboard component
- Plaid integration is functional
- Backend endpoints exist (`/api/plaid/link-token`, `/api/plaid/exchange-public-token`)
- `has_linked_bank` flag is tracked in User model
- User can link bank directly from Dashboard

**Issues:**
- No dedicated page for bank linking flow
- Bank linking UI is mixed with dashboard content
- No clear separation of concerns

---

## 3. Migration Plan: Email → Phone Number

### 3.1 Database Changes

**Migration Strategy:**
- Create new `phone_number` column (nullable initially for migration)
- Migrate existing data (if any) - N/A for fresh start
- Make `phone_number` unique and indexed
- Remove `email` column after migration complete

**SQLAlchemy Model Changes:**
```python
# User model
phone_number = Column(String(20), unique=True, index=True, nullable=False)
# Remove: email = Column(String(255), unique=True, index=True, nullable=False)
```

**Phone Number Format:**
- Store in E.164 format: `+1234567890` (with country code)
- Validation: 10-15 digits, must start with `+`
- Frontend will handle formatting, backend stores normalized

### 3.2 Backend Changes

**Schema Updates (`backend/app/schemas.py`):**
- Replace `EmailStr` with phone number validation
- Create custom Pydantic validator for phone numbers
- Update `UserBase`, `UserCreate`, `UserLogin` schemas

**Router Updates (`backend/app/api/routers/users.py`):**
- Change signup to check for existing phone number
- Change login to query by phone number
- Update error messages to reference "phone number"

**CRUD Updates (`backend/app/crud.py`):**
- Rename `get_user_by_email()` → `get_user_by_phone()`
- Update all references

**Model Updates (`backend/app/models.py`):**
- Replace `email` field with `phone_number` field
- Update relationships if needed (none affected)

### 3.3 Frontend Changes

**SignUpPage (`frontend/src/pages/SignUpPage.jsx`):**
- Replace email input with phone number input
- Add phone number formatting (e.g., `(123) 456-7890`)
- Update form state from `email` to `phone_number`
- Update localStorage key from "email" to "phone_number"
- Add phone number validation

**SignInPage (`frontend/src/pages/SignInPage.jsx`):**
- Replace email input with phone number input
- Add phone number formatting
- Update form state and localStorage

**LandingPage (`frontend/src/pages/LandingPage.jsx`):**
- Replace email capture with phone number capture (optional - may keep email for marketing)
- Or remove email capture entirely if not needed

**Input Component:**
- Consider creating reusable `PhoneInput` component with formatting
- Use `type="tel"` for better mobile UX

### 3.4 Validation & Formatting

**Phone Number Validation:**
- Backend: Pydantic validator using `phonenumbers` library or regex
- Frontend: Real-time formatting as user types
- Normalize to E.164 format before storing

**Error Handling:**
- "Invalid phone number format"
- "Phone number already registered"
- "Phone number not found" (login)

---

## 4. Bank Linking Page Design

### 4.1 New Page Structure

**Route:** `/link-bank` or `/bank-linking`

**Purpose:**
- Dedicated page for bank account linking flow
- Clear onboarding experience
- Can be accessed from Dashboard or as standalone step

### 4.2 Page Components

**BankLinkingPage.jsx:**
- Hero section explaining why to link bank
- Security/privacy messaging
- Plaid Link button/flow
- Success state after linking
- Error handling

**Flow:**
1. User lands on `/link-bank`
2. Page checks if bank already linked
3. If linked: Show success message + redirect option
4. If not linked: Show Plaid Link button
5. On success: Show confirmation + redirect to Dashboard

### 4.3 Integration Points

**Backend Endpoints (Already Exist):**
- `GET /api/users/should_link_bank` - Check if linking needed
- `GET /api/plaid/link-token` - Get Plaid Link token
- `POST /api/plaid/exchange-public-token` - Exchange token
- `POST /api/users/update_link_bank` - Update flag

**Frontend Integration:**
- Use existing `react-plaid-link` hook
- Reuse Plaid Link configuration from Dashboard
- Handle success/error states

### 4.4 Navigation Flow

**Entry Points:**
- Dashboard redirects to `/link-bank` if `has_linked_bank === false`
- Direct navigation to `/link-bank`
- Post-signup redirect (optional)

**Exit Points:**
- After successful linking → Dashboard
- Cancel/back button → Dashboard or previous page
- Already linked → Dashboard with message

### 4.5 UI/UX Considerations

**Design:**
- Match existing auth page styling
- Clear call-to-action
- Trust indicators (security badges, encryption info)
- Loading states during Plaid flow
- Success animation/confirmation

**Accessibility:**
- Proper ARIA labels
- Keyboard navigation
- Screen reader support

---

## 5. Implementation Steps

### Phase 1: Phone Number Migration

1. **Database Migration**
   - Add `phone_number` column to User model
   - Create Alembic migration script
   - Update model definition

2. **Backend Updates**
   - Update schemas with phone validation
   - Update user routes (signup/login)
   - Update CRUD operations
   - Update error messages

3. **Frontend Updates**
   - Update SignUpPage
   - Update SignInPage
   - Create PhoneInput component (optional)
   - Update localStorage usage

4. **Testing**
   - Test signup with phone number
   - Test login with phone number
   - Test validation edge cases
   - Test existing sessions (if any)

### Phase 2: Bank Linking Page

1. **Create New Page**
   - Create `BankLinkingPage.jsx`
   - Add route to App.jsx
   - Create styling file

2. **Implement Plaid Flow**
   - Integrate Plaid Link hook
   - Handle token exchange
   - Update `has_linked_bank` flag
   - Handle success/error states

3. **Update Navigation**
   - Add redirect logic in Dashboard
   - Update post-signup flow (if needed)
   - Add navigation links

4. **Testing**
   - Test bank linking flow
   - Test redirect logic
   - Test error handling
   - Test already-linked state

### Phase 3: Cleanup

1. **Remove Email References**
   - Remove email column from database (after migration)
   - Remove email-related code
   - Update documentation

2. **Update Dashboard**
   - Remove embedded bank linking UI
   - Add redirect to `/link-bank` if needed
   - Clean up unused code

---

## 6. Technical Details

### 6.1 Phone Number Library

**Option 1: `phonenumbers` (Python)**
```python
from phonenumbers import parse, format_number, PhoneNumberFormat
# Validate and format phone numbers
```

**Option 2: Custom Regex**
```python
import re
PHONE_PATTERN = re.compile(r'^\+?[1-9]\d{1,14}$')  # E.164 format
```

**Frontend: `react-phone-number-input` or custom formatter**

### 6.2 Database Migration

**Alembic Migration:**
```python
def upgrade():
    op.add_column('users', sa.Column('phone_number', sa.String(20), nullable=True))
    op.create_unique_constraint('uq_users_phone_number', 'users', ['phone_number'])
    op.create_index('ix_users_phone_number', 'users', ['phone_number'])
    # Later: op.drop_column('users', 'email')
```

### 6.3 Phone Number Formatting

**Frontend Formatting:**
- Display: `(123) 456-7890`
- Store: `+11234567890` (E.164)
- Use library like `libphonenumber-js` or custom formatter

---

## 7. Risk Assessment

### 7.1 Migration Risks

**Data Loss:**
- Risk: Low (fresh project, no existing users)
- Mitigation: Backup before migration, test on staging

**Breaking Changes:**
- Risk: Medium (all auth endpoints change)
- Mitigation: Update all frontend calls, test thoroughly

**Phone Number Validation:**
- Risk: Medium (different formats, international)
- Mitigation: Use proven library, test edge cases

### 7.2 Bank Linking Page Risks

**User Experience:**
- Risk: Low (isolated page, clear flow)
- Mitigation: User testing, clear messaging

**Plaid Integration:**
- Risk: Low (already working in Dashboard)
- Mitigation: Reuse existing code, test thoroughly

---

## 8. Testing Checklist

### 8.1 Phone Number Migration

- [ ] Sign up with valid phone number
- [ ] Sign up with invalid phone number (should fail)
- [ ] Sign up with duplicate phone number (should fail)
- [ ] Login with valid phone number
- [ ] Login with invalid phone number (should fail)
- [ ] Phone number formatting works correctly
- [ ] Phone number stored in E.164 format
- [ ] localStorage updated correctly
- [ ] Error messages are user-friendly

### 8.2 Bank Linking Page

- [ ] Page loads correctly
- [ ] Plaid Link button appears when not linked
- [ ] Plaid Link flow completes successfully
- [ ] Success message displays after linking
- [ ] Redirect to Dashboard works
- [ ] Already-linked state handled correctly
- [ ] Error handling works (network errors, etc.)
- [ ] Loading states display correctly
- [ ] Mobile responsive design

---

## 9. Success Criteria

### 9.1 Phone Number Migration

✅ All authentication uses phone numbers
✅ No email references in codebase
✅ Phone numbers validated and formatted correctly
✅ User can sign up and login with phone number
✅ All tests pass

### 9.2 Bank Linking Page

✅ Dedicated page exists at `/link-bank`
✅ Plaid integration works correctly
✅ User can complete bank linking flow
✅ Navigation flow is intuitive
✅ Dashboard no longer has embedded bank linking

---

## 10. Open Questions

1. **Phone Number Format:**
   - Should we support international numbers from the start?
   - What's the default country code?

2. **Landing Page:**
   - Keep email capture for marketing, or remove entirely?

3. **Bank Linking Page:**
   - Should it be accessible only when `has_linked_bank === false`?
   - Or always accessible for re-linking?

4. **Post-Signup Flow:**
   - Redirect to `/link-bank` immediately after signup?
   - Or let user explore Dashboard first?

5. **Phone Number Library:**
   - Use `phonenumbers` (Python) + `libphonenumber-js` (JS)?
   - Or custom validation?

---

## 11. Timeline Estimate

**Phase 1 (Phone Migration):** 2-3 hours
- Database changes: 30 min
- Backend updates: 1 hour
- Frontend updates: 1 hour
- Testing: 30 min

**Phase 2 (Bank Linking Page):** 1-2 hours
- Page creation: 30 min
- Plaid integration: 30 min
- Navigation updates: 30 min
- Testing: 30 min

**Total:** 3-5 hours

---

## 12. Dependencies

- `phonenumbers` library (Python) - for backend validation
- `libphonenumber-js` or similar (JavaScript) - for frontend formatting
- Existing Plaid integration (already working)
- `react-plaid-link` (already installed)

---

## 13. Notes

- This migration assumes a fresh project with no existing users
- If users exist, need data migration strategy
- Consider adding phone number verification (SMS) in future
- Bank linking page can be enhanced with more features later (multiple accounts, etc.)

---

**Document Version:** 1.0  
**Created:** 2024  
**Status:** Awaiting Review

