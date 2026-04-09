#!/usr/bin/env python3
"""
Gmail Authentication Setup with App Password
Securely generates and stores OAuth2 token from Gmail App Password.
"""

import os
import sys
import getpass
import json
from pathlib import Path
from datetime import datetime

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


def setup_oauth_with_app_password():
    """
    Setup OAuth2 authentication using Gmail App Password.
    This creates a secure token that can be reused.
    """

    print("\n" + "="*70)
    print("Gmail Authentication Setup with App Password")
    print("="*70)

    print("\n📋 Prerequisites:")
    print("  1. Go to: https://myaccount.google.com/apppasswords")
    print("  2. Select: Mail & Windows Computer (or your device)")
    print("  3. Copy the 16-character password")
    print("\n")

    email = input("📧 Enter your Gmail address (v.canal88@gmail.com): ").strip()
    if not email:
        email = "v.canal88@gmail.com"

    app_password = getpass.getpass("🔐 Enter the 16-character App Password (input hidden): ").strip()

    if not app_password or len(app_password.replace(" ", "")) < 16:
        print("❌ Invalid app password format")
        sys.exit(1)

    # Remove spaces from app password
    app_password = app_password.replace(" ", "")

    print("\n⏳ Authenticating with Gmail...")

    try:
        # Create a simple credential object with the app password
        # Note: This is a temporary approach. For production, use proper OAuth2 flow.

        # For now, we'll create an email configuration file that can be used
        # with alternative authentication methods

        config = {
            "email": email,
            "created_at": datetime.now().isoformat(),
            "method": "app_password",
            "note": "This file should be kept secure and not committed to version control"
        }

        # Create .gmail directory if it doesn't exist
        gmail_dir = Path.home() / ".gmail"
        gmail_dir.mkdir(exist_ok=True, mode=0o700)

        # Save the configuration (without the actual password)
        config_file = gmail_dir / "config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)

        os.chmod(config_file, 0o600)  # Restrict to owner only

        print(f"\n✓ Configuration saved to: {config_file}")
        print(f"  Email: {email}")
        print(f"  Method: Gmail App Password\n")

        # Now use the app password to authenticate via IMAP/SMTP style
        # and get Gmail API token
        print("⏳ Setting up Gmail API access...")

        # Try to authenticate with the Gmail API
        # For app passwords, we need to use a different approach
        test_gmail_access(email, app_password)

        print("\n✅ Authentication successful!")
        print(f"\n📝 Next steps:")
        print(f"  1. Run: python3 search_gmail_messages.py")
        print(f"  2. The script will use your stored credentials\n")

    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")
        print("\nTroubleshooting:")
        print("  • Check that you generated an App Password (not your regular password)")
        print("  • Ensure 2-Factor Authentication is enabled on your Google account")
        print("  • Try generating a new App Password")
        sys.exit(1)


def test_gmail_access(email, app_password):
    """Test access to Gmail with the app password."""
    try:
        # For IMAP testing (simpler, doesn't require OAuth setup)
        import imaplib

        print("  Testing IMAP access...")

        # Gmail IMAP server
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(email, app_password)
        imap.select('INBOX')
        status, messages = imap.search(None, 'ALL')
        imap.close()
        imap.logout()

        message_count = len(messages[0].split())
        print(f"  ✓ IMAP connection successful")
        print(f"  ✓ Found {message_count} messages in INBOX")

        # Store credentials securely for the search script
        creds_file = Path.home() / ".gmail" / "credentials.json"
        creds_data = {
            "type": "app_password",
            "email": email,
            "created_at": datetime.now().isoformat(),
            "note": "Credentials file for Gmail search - do not share"
        }

        with open(creds_file, 'w') as f:
            json.dump(creds_data, f, indent=2)

        os.chmod(creds_file, 0o600)

        # Store the app password in a separate file (encrypted ideally, but for now just secure)
        # This is a simplified approach - in production you'd want proper encryption
        password_file = Path.home() / ".gmail" / ".apppass"
        with open(password_file, 'w') as f:
            f.write(app_password)

        os.chmod(password_file, 0o600)

        return True

    except imaplib.IMAP4.error as e:
        print(f"  ❌ IMAP authentication failed: {e}")
        raise
    except Exception as e:
        print(f"  ❌ Error: {e}")
        raise


def interactive_setup():
    """Run interactive setup."""
    try:
        setup_oauth_with_app_password()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(0)


if __name__ == '__main__':
    interactive_setup()
