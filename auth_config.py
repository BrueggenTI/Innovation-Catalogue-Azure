"""
Microsoft Azure AD Authentication Configuration
Provides MSAL configuration and helper functions for Microsoft SSO
"""
import os
from msal import ConfidentialClientApplication

# Azure AD Configuration - Read from Replit Secrets (Environment Variables)
CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")  # Application (client) ID from Azure Portal
CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")  # Client Secret from Azure Portal
TENANT_ID = os.environ.get("AZURE_TENANT_ID")  # Directory (tenant) ID from Azure Portal

# Authority URL - Restricts authentication to your specific Azure AD tenant
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# Redirect URI - Must match exactly what's configured in Azure Portal
# Format: https://YOUR_REPLIT_APP_URL/auth/callback
REDIRECT_URI = os.environ.get("AZURE_REDIRECT_URI", "http://localhost:5000/auth/callback")

# Microsoft Graph API Scopes - Permissions requested from user
SCOPE = ["User.Read"]  # Basic profile information

# Logout redirect - Where to send users after logout
POST_LOGOUT_REDIRECT_URI = os.environ.get("AZURE_POST_LOGOUT_URI", "http://localhost:5000")

def get_msal_app():
    """
    Creates and returns a configured MSAL ConfidentialClientApplication instance
    
    Returns:
        ConfidentialClientApplication: Configured MSAL app for authentication
    """
    return ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
    )

def get_auth_url(msal_app, state=None):
    """
    Generates the Microsoft login URL
    
    Args:
        msal_app: MSAL application instance
        state: Optional state parameter for security
        
    Returns:
        str: Microsoft login URL to redirect user to
    """
    auth_url = msal_app.get_authorization_request_url(
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI,
        state=state
    )
    return auth_url

def acquire_token_by_code(msal_app, code):
    """
    Exchanges authorization code for access token
    
    Args:
        msal_app: MSAL application instance
        code: Authorization code from Microsoft callback
        
    Returns:
        dict: Token response containing access_token and account information
    """
    result = msal_app.acquire_token_by_authorization_code(
        code=code,
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI
    )
    return result

def get_logout_url(account_username=None):
    """
    Generates Microsoft logout URL
    
    Args:
        account_username: Optional username to logout specific account
        
    Returns:
        str: Microsoft logout URL
    """
    logout_url = f"{AUTHORITY}/oauth2/v2.0/logout"
    if POST_LOGOUT_REDIRECT_URI:
        logout_url += f"?post_logout_redirect_uri={POST_LOGOUT_REDIRECT_URI}"
    return logout_url

def validate_config():
    """
    Validates that all required configuration values are set
    
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not CLIENT_ID:
        return False, "AZURE_CLIENT_ID not set in environment variables"
    if not CLIENT_SECRET:
        return False, "AZURE_CLIENT_SECRET not set in environment variables"
    if not TENANT_ID:
        return False, "AZURE_TENANT_ID not set in environment variables"
    return True, "Configuration valid"
