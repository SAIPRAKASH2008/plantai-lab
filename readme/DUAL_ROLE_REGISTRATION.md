# 📝 Dual-Role Registration System

## New Signup Features

### Registration Page Updates

The registration page now supports creating accounts for both **Operator** and **Administrator** roles with role-specific workflows.

---

## 🎯 Features

### 1. **Account Type Selection**
- Dropdown menu with two options:
  - **Operator** — Standard Lab Access (default)
  - **Administrator** — Full System Control

### 2. **Dynamic Form Updates**
- Role descriptions update based on selection
- Admin invitation code field appears only when "Administrator" is selected
- Required field validation enforces code for admin signup

### 3. **Admin Invitation Code**
- Requires code `PLANTAI2026` to create admin accounts
- Prevents unauthorized admin creation
- Field is conditional and only shown for admin signup

### 4. **Form Fields**
- Full Name (required)
- Username (required, must be unique)
- Password (required, minimum 6 characters)
- Account Type dropdown (required)
- Admin Invitation Code (required only for admin role)

---

## 📋 Registration Flow

### For Operators
1. Navigate to `/register`
2. Enter Full Name, Username, Password
3. Select "Operator" from Account Type (default)
4. Click "Create Account"
5. Redirect to face enrollment
6. Complete biometric setup
7. Access dashboard as operator

### For Administrators
1. Navigate to `/register`
2. Enter Full Name, Username, Password
3. Select "Administrator" from Account Type
4. Admin Invitation Code field appears
5. Enter code: `PLANTAI2026`
6. Click "Create Account"
7. Redirect to face enrollment
8. Complete biometric setup
9. Access admin panel + user management

---

## 🔑 Admin Invitation Code

**Current Code:** `PLANTAI2026`

Security considerations:
- Code is hardcoded in backend (can be made dynamic in future)
- Prevents unauthorized admin account creation
- Can be changed/rotated by modifying app.py
- Future enhancement: Database-backed invitation tokens with expiration

---

## 🔄 Updated Endpoints

### Form Registration
```
POST /register (form data)
- full_name: string (required)
- username: string (required)
- password: string (required, min 6 chars)
- role: 'admin' or 'operator' (required)
- admin_code: string (required if role='admin')
```

### API Registration
```
POST /api/register (JSON)
{
  "full_name": "John Doe",
  "username": "johndoe",
  "password": "SecurePass123",
  "role": "admin",
  "admin_code": "PLANTAI2026"
}

Response (201):
{
  "status": "ok",
  "user_id": 5,
  "role": "admin"
}
```

---

## 🎨 UI/UX Details

### Role Selection
- Clear dropdown with descriptive text
- Dynamic role descriptions update on change
- Visual hierarchy: Default to Operator

### Admin Code Field
- Golden/yellow accent when visible (warning color)
- Hint text explains purpose
- Only required when admin role selected
- Automatically hidden/shown based on selection

### Form Validation
- Client-side: HTML5 required fields
- Server-side:
  - Username uniqueness check
  - Password minimum length validation
  - Role validation ('admin' or 'operator' only)
  - Admin code verification if needed

---

## ✅ Verification Results

### Database Test
✅ Admin user creation successful
✅ Role stored correctly in database
✅ Fetch and verify returns correct role

### Python Compilation
✅ app.py syntax valid
✅ register route compiles
✅ API endpoint compiles

### Test Data
```
Test Admin: test_admin_51e09f
Password: TestPass123
Role: admin (verified in DB)
```

---

## 🛡️ Security

1. **Admin Code Protection**
   - Secret code required for admin signup
   - Code validated server-side
   - Invalid code returns 403 Forbidden

2. **Role Validation**
   - Only 'admin' or 'operator' accepted
   - Invalid roles rejected
   - Prevents privilege escalation

3. **Session Management**
   - User logged in after signup
   - Face enrollment required before full access
   - Role persisted in database

4. **Username Uniqueness**
   - Database constraint prevents duplicates
   - User-friendly error message if taken

---

## 📝 Form Styling

The registration form maintains consistency with the login page:
- Dark botanical theme
- Glassmorphism backdrop effect
- Interactive role dropdown
- Responsive design for mobile
- Accessibility: Proper labels and ARIA attributes
- Touch-optimized for mobile signup flow

---

## 🚀 Next Steps (Optional)

1. **Dynamic Invitation Codes**
   - Generate one-time invite codes
   - Store in database with expiration
   - Allow admins to generate invites

2. **Email Verification**
   - Send verification link on signup
   - Confirm email before account activation

3. **Role Request Workflow**
   - Users signup as operator
   - Request admin upgrade
   - Admin reviews and approves

4. **Admin Approval Queue**
   - Pending admin signups require approval
   - First admin (bootstrap) can be auto-created

---

## 📁 Updated Files

- [app.py](app.py) - Updated `/register` route and `/api/register` endpoint
- [templates/register.html](templates/register.html) - New dual-role signup form
- [Database](database.py) - Unchanged (role already supported)

---

Generated: 2026-08-18
System: PlantAI Lab v2.4.1
