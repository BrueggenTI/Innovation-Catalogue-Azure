# Microsoft Azure AD Single Sign-On (SSO) Setup Guide

This guide will walk you through setting up Microsoft Azure Active Directory (Azure AD) authentication for the Brüggen Innovation Platform.

## Overview

The application uses Microsoft Authentication Library (MSAL) for Python to implement secure Single Sign-On with Azure AD. Users can authenticate using their Microsoft/Office 365 accounts.

## Prerequisites

- Azure AD tenant (organization account)
- Global Administrator or Application Administrator role in Azure AD
- Access to Azure Portal (https://portal.azure.com)

## Step 1: Register Application in Azure Portal

### 1.1 Navigate to Azure AD
1. Go to [Azure Portal](https://portal.azure.com)
2. Sign in with your administrator account
3. Search for **Azure Active Directory** in the search bar
4. Click on **App registrations** in the left menu

### 1.2 Create New Application Registration
1. Click **+ New registration**
2. Fill in the application details:
   - **Name**: `Brüggen Innovation Platform` (or your preferred name)
   - **Supported account types**: 
     - Select **"Accounts in this organizational directory only (Single tenant)"** for internal use
     - Or **"Accounts in any organizational directory (Any Azure AD directory - Multitenant)"** if you need external access
   - **Redirect URI**:
     - Platform: **Web**
     - URI: `https://your-replit-url.replit.app/auth/callback`
     - For development: `http://localhost:5000/auth/callback`
3. Click **Register**

### 1.3 Note the Application Details
After registration, you'll see the application overview page. **Save these values** (you'll need them later):
- **Application (client) ID**: Copy this value
- **Directory (tenant) ID**: Copy this value

## Step 2: Configure Authentication Settings

### 2.1 Add Redirect URIs (if needed)
1. In your app registration, go to **Authentication** in the left menu
2. Under **Platform configurations** → **Web**, add additional redirect URIs if needed:
   - Production: `https://your-production-domain.com/auth/callback`
   - Staging: `https://your-staging-domain.replit.app/auth/callback`
3. Click **Save**

### 2.2 Configure Logout URL
1. Still in **Authentication** section
2. Under **Front-channel logout URL**, add:
   - `https://your-replit-url.replit.app/logout`
3. Click **Save**

### 2.3 Enable ID Tokens
1. In **Authentication** section, scroll to **Implicit grant and hybrid flows**
2. Check **ID tokens (used for implicit and hybrid flows)**
3. Click **Save**

## Step 3: Create Client Secret

### 3.1 Generate Secret
1. Go to **Certificates & secrets** in the left menu
2. Click **+ New client secret**
3. Add a description: `Brüggen Innovation Platform Secret`
4. Select expiration period (recommended: 24 months)
5. Click **Add**

### 3.2 Save the Secret Value
**IMPORTANT**: Copy the **Value** immediately - it will only be shown once!
- **Secret Value**: Copy this value (not the Secret ID)
- Store it securely - you'll add it to your environment variables

## Step 4: Configure API Permissions

### 4.1 Add Required Permissions
1. Go to **API permissions** in the left menu
2. Click **+ Add a permission**
3. Select **Microsoft Graph**
4. Click **Delegated permissions**
5. Add the following permissions:
   - `User.Read` (should already be added)
   - `email`
   - `profile`
   - `openid`
6. Click **Add permissions**

### 4.2 Grant Admin Consent (Optional but Recommended)
1. Click **Grant admin consent for [Your Organization]**
2. Confirm by clicking **Yes**
3. All permissions should now show a green checkmark under "Status"

## Step 5: Configure Application Environment Variables

### 5.1 Set Environment Variables in Replit

Add the following secrets in your Replit project (Secrets tool in left sidebar):

```
AZURE_CLIENT_ID=<your-application-client-id>
AZURE_CLIENT_SECRET=<your-client-secret-value>
AZURE_TENANT_ID=<your-tenant-id>
AZURE_AUTHORITY=https://login.microsoftonline.com/<your-tenant-id>
AZURE_REDIRECT_URI=https://your-replit-url.replit.app/auth/callback
```

### 5.2 Example Configuration

```env
# Azure AD Configuration
AZURE_CLIENT_ID=12345678-1234-1234-1234-123456789abc
AZURE_CLIENT_SECRET=abC~defGhijKlmNopQrstUvwXyz123456789
AZURE_TENANT_ID=87654321-4321-4321-4321-987654321xyz
AZURE_AUTHORITY=https://login.microsoftonline.com/87654321-4321-4321-4321-987654321xyz
AZURE_REDIRECT_URI=https://bruggen-innovation.replit.app/auth/callback
```

### 5.3 Update Redirect URI for Production
When deploying to production:
1. Update `AZURE_REDIRECT_URI` with your production URL
2. Add the production URL to Azure AD app registration redirect URIs

## Step 6: Test Authentication

### 6.1 Test Login Flow
1. Start your application
2. Navigate to the application URL
3. Click on the user dropdown menu in the top right
4. Click **"Sign In with Microsoft"**
5. You should be redirected to Microsoft login page
6. Enter your Microsoft credentials
7. Grant consent if prompted
8. You should be redirected back to the application

### 6.2 Verify Authentication
1. Check that the user dropdown shows **"Microsoft SSO Active"** 
2. Navigate to **Profile** page
3. Verify your Microsoft account information is displayed
4. Verify the authentication status shows **"Authenticated"**

### 6.3 Test Logout
1. Click the user dropdown menu
2. Click **"Sign Out (Microsoft)"**
3. You should be signed out and redirected to Microsoft logout page
4. Verify the profile page now shows **"Not Authenticated"**

## Step 7: Protect Routes (Optional)

To require authentication for specific routes, use the `@login_required` decorator:

```python
from routes import login_required

@app.route('/protected')
@login_required
def protected_page():
    return render_template('protected.html')
```

Users trying to access protected routes without authentication will be redirected to the login page.

## Troubleshooting

### Common Issues

#### Error: "AADSTS50011: The reply URL specified in the request does not match"
- **Solution**: Ensure the redirect URI in your environment variables exactly matches the one configured in Azure AD

#### Error: "AADSTS700016: Application not found in the directory"
- **Solution**: Verify the `AZURE_CLIENT_ID` and `AZURE_TENANT_ID` are correct

#### Error: "AADSTS7000215: Invalid client secret is provided"
- **Solution**: Generate a new client secret and update `AZURE_CLIENT_SECRET`

#### Authentication works but user details are missing
- **Solution**: Ensure `User.Read`, `email`, `profile`, and `openid` permissions are granted in API permissions

#### Users from other organizations cannot sign in
- **Solution**: Change "Supported account types" in Azure AD to "Multitenant" if you need to allow external users

### Debug Mode
The application logs authentication events. Check the console logs for detailed error messages:
```bash
# In Replit console, look for authentication-related logs
```

## Security Best Practices

1. **Secret Rotation**: Regularly rotate your client secrets (every 6-12 months)
2. **Principle of Least Privilege**: Only request necessary API permissions
3. **HTTPS Only**: Always use HTTPS in production (automatic on Replit)
4. **Environment Variables**: Never commit secrets to version control
5. **Token Validation**: The application validates state tokens to prevent CSRF attacks
6. **Session Security**: Sessions are secured with Flask's session management

## Multi-Tenant Configuration (Advanced)

To allow users from any Microsoft organization:

1. In Azure AD app registration, change **Supported account types** to:
   - "Accounts in any organizational directory (Any Azure AD directory - Multitenant)"

2. Update `AZURE_AUTHORITY` to use common endpoint:
   ```env
   AZURE_AUTHORITY=https://login.microsoftonline.com/common
   ```

3. Update `AZURE_TENANT_ID` to:
   ```env
   AZURE_TENANT_ID=common
   ```

## Support

For issues related to:
- **Azure AD Configuration**: Contact your Azure AD administrator
- **Application Issues**: Check application logs and verify environment variables
- **Authentication Flow**: Review Microsoft documentation at https://docs.microsoft.com/en-us/azure/active-directory/

## Resources

- [Microsoft Identity Platform Documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/)
- [MSAL Python Documentation](https://msal-python.readthedocs.io/)
- [Azure AD App Registration Guide](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [Microsoft Graph Permissions Reference](https://docs.microsoft.com/en-us/graph/permissions-reference)
