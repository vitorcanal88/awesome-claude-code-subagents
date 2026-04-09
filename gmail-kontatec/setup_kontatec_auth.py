#!/usr/bin/env python3
"""
Kontatec Gmail Authentication Setup
Secure configuration of Google App Password for Kontatec email access.
"""

import os
import sys
import getpass
import json
from pathlib import Path
from datetime import datetime


def setup_kontatec_auth():
    """Setup secure authentication for Kontatec Gmail access."""

    print("\n" + "="*70)
    print("🏢 Kontatec Gmail - Authentication Setup")
    print("="*70)

    print("\n📋 Prerequisites:")
    print("  1. Go to: https://myaccount.google.com/apppasswords")
    print("  2. Select: Mail & Windows Computer (or your device)")
    print("  3. Copy the 16-character App Password")
    print("  4. Ensure 2-Factor Authentication is enabled")
    print("\n")

    # Get email
    email = input("📧 Enter your Gmail address (default: v.canal88@gmail.com): ").strip()
    if not email:
        email = "v.canal88@gmail.com"

    # Validate email
    if not "@" in email or "." not in email.split("@")[1]:
        print("❌ Invalid email format")
        sys.exit(1)

    # Get app password
    app_password = getpass.getpass("🔐 Enter the 16-character App Password (input hidden): ").strip()

    if not app_password:
        print("❌ App password cannot be empty")
        sys.exit(1)

    # Remove spaces for validation
    app_password_clean = app_password.replace(" ", "")

    if len(app_password_clean) < 16:
        print("❌ Invalid app password (must be 16 characters)")
        sys.exit(1)

    print("\n⏳ Testing authentication...")

    try:
        # Test IMAP connection
        test_imap_access(email, app_password_clean)

        # Save configuration
        save_credentials(email, app_password_clean)

        print("\n✅ Authentication successful!")
        print(f"\n📝 Next steps:")
        print(f"  1. Run: python3 search_kontatec_emails.py")
        print(f"  2. Results will be saved to: gmail_kontatec_results.json")
        print(f"\n📁 Credentials saved to: ~/.gmail/\n")

    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")
        print("\nTroubleshooting:")
        print("  • Verify you're using the App Password (not your regular password)")
        print("  • Ensure 2-Factor Authentication is enabled on your Google account")
        print("  • Check that your email is correct")
        print("  • Try generating a new App Password from Google")
        sys.exit(1)


def test_imap_access(email, app_password):
    """Test IMAP connection to Gmail."""
    try:
        import imaplib

        print(f"  Testing IMAP connection to: {email}")

        # Connect to Gmail IMAP server
        imap = imaplib.IMAP4_SSL('imap.gmail.com')

        # Login
        imap.login(email, app_password)

        # Select inbox
        imap.select('INBOX')

        # Count messages
        status, messages = imap.search(None, 'ALL')
        message_count = len(messages[0].split()) if messages[0] else 0

        # Close connection
        imap.close()
        imap.logout()

        print(f"  ✓ IMAP connection successful")
        print(f"  ✓ Found {message_count} messages in INBOX")

        return True

    except imaplib.IMAP4.error as e:
        print(f"  ❌ IMAP authentication failed: {e}")
        raise
    except Exception as e:
        print(f"  ❌ Error: {e}")
        raise


def save_credentials(email, app_password):
    """Save credentials securely."""
    try:
        # Create ~/.gmail directory
        gmail_dir = Path.home() / ".gmail"
        gmail_dir.mkdir(exist_ok=True, mode=0o700)

        # Save configuration (email only)
        config_file = gmail_dir / "config.json"
        config = {
            "email": email,
            "created_at": datetime.now().isoformat(),
            "method": "app_password",
            "source": "kontatec_gmail",
            "note": "Credentials file - keep secure and do not share"
        }

        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)

        os.chmod(config_file, 0o600)

        # Save app password (with restricted permissions)
        password_file = gmail_dir / ".apppass"
        with open(password_file, 'w') as f:
            f.write(app_password)

        os.chmod(password_file, 0o600)

        print(f"\n✓ Configuration saved to: {config_file}")
        print(f"✓ Credentials secured in: ~/.gmail/")

    except Exception as e:
        print(f"❌ Error saving credentials: {e}")
        raise


def main():
    """Main execution."""
    try:
        setup_kontatec_auth()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
