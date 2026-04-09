#!/usr/bin/env python3
"""
Kontatec Gmail Search Tool
Search and retrieve emails from Kontatec domain.
"""

import os
import sys
import json
import imaplib
import email
import argparse
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime
from email.header import decode_header


class KontатecGmailSearcher:
    """Search Kontatec Gmail using IMAP."""

    def __init__(self, email_addr: str = None, app_password: str = None):
        """
        Initialize searcher.

        Args:
            email_addr: Gmail address
            app_password: App password (or None to load from storage)
        """
        self.email_addr = email_addr
        self.app_password = app_password
        self.imap = None
        self.auth()

    def auth(self):
        """Authenticate with Gmail IMAP."""
        try:
            # Load stored credentials if not provided
            if not self.email_addr or not self.app_password:
                self._load_stored_credentials()

            if not self.email_addr or not self.app_password:
                print("❌ Email and app password required")
                print("\nRun setup first: python3 setup_kontatec_auth.py")
                sys.exit(1)

            print(f"🔐 Authenticating as: {self.email_addr}")

            # Connect to Gmail IMAP
            self.imap = imaplib.IMAP4_SSL('imap.gmail.com')
            self.imap.login(self.email_addr, self.app_password)

            print("✓ Gmail authentication successful\n")

        except imaplib.IMAP4.error as e:
            print(f"❌ Authentication failed: {e}")
            print("\nTroubleshooting:")
            print("  • Check that you're using App Password (not regular password)")
            print("  • Ensure 2-Factor Authentication is enabled")
            print("  • Try running setup again: python3 setup_kontatec_auth.py")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)

    def _load_stored_credentials(self):
        """Load credentials from ~/.gmail/"""
        try:
            gmail_dir = Path.home() / ".gmail"

            # Load email from config
            config_file = gmail_dir / "config.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.email_addr = config.get('email', self.email_addr)

            # Load password
            password_file = gmail_dir / ".apppass"
            if password_file.exists():
                with open(password_file, 'r') as f:
                    self.app_password = f.read().strip()

        except Exception as e:
            print(f"Warning: Could not load stored credentials: {e}")

    def search_kontatec_emails(self, recipients: List[str] = None) -> List[Dict[str, Any]]:
        """
        Search for emails sent to Kontatec recipients.

        Args:
            recipients: List of recipient addresses (defaults to kontatec addresses)

        Returns:
            List of message data
        """
        if not recipients:
            recipients = ['vitor.canal@kontatec.com.br']

        all_messages = []

        for recipient in recipients:
            print(f"📧 Searching for messages to: {recipient}")

            try:
                # Search for messages
                status, message_ids = self.imap.search(None, f'TO "{recipient}"')

                if status != 'OK':
                    print(f"   ❌ Search failed\n")
                    continue

                ids = message_ids[0].split()
                message_count = len(ids)

                if message_count == 0:
                    print(f"   → Found 0 messages\n")
                    continue

                print(f"   → Found {message_count} messages")
                print(f"   → Processing messages...")

                # Process messages (limit to last 100)
                for msg_id in ids[-100:]:
                    try:
                        status, msg_data = self.imap.fetch(msg_id, '(RFC822)')

                        if status != 'OK':
                            continue

                        msg_body = msg_data[0][1]
                        msg = email.message_from_bytes(msg_body)

                        # Extract headers
                        subject = self._decode_header(msg.get('Subject', 'No subject'))
                        from_addr = self._decode_header(msg.get('From', 'Unknown'))
                        date_str = msg.get('Date', 'Unknown date')
                        to_addr = msg.get('To', recipient)

                        # Extract body
                        body = self._get_message_body(msg)

                        message_info = {
                            'id': msg_id.decode('utf-8') if isinstance(msg_id, bytes) else msg_id,
                            'from': from_addr,
                            'to': to_addr,
                            'subject': subject,
                            'date': date_str,
                            'body_preview': body[:500] if body else 'No body content'
                        }

                        all_messages.append(message_info)

                    except Exception as e:
                        print(f"   ⚠ Error processing message: {e}")
                        continue

                print(f"   ✓ Processed {len([m for m in all_messages if m['to'] == recipient])} messages\n")

            except Exception as e:
                print(f"   ❌ Error searching: {e}\n")
                continue

        return all_messages

    def _decode_header(self, header: str) -> str:
        """Decode email header."""
        if not header:
            return ""

        try:
            decoded_parts = decode_header(header)
            result = []

            for part, charset in decoded_parts:
                if isinstance(part, bytes):
                    result.append(part.decode(charset or 'utf-8', errors='ignore'))
                else:
                    result.append(str(part))

            return ''.join(result)
        except:
            return str(header)

    def _get_message_body(self, msg: email.message.Message) -> str:
        """Extract message body."""
        try:
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        try:
                            body = part.get_payload(decode=True)
                            return body.decode('utf-8', errors='ignore')
                        except:
                            pass
            else:
                body = msg.get_payload(decode=True)
                if body:
                    return body.decode('utf-8', errors='ignore')
        except:
            pass

        return msg.get('body', '')

    def print_results(self, messages: List[Dict[str, Any]]):
        """Print formatted results."""
        if not messages:
            print("❌ No messages found")
            return

        print(f"\n{'='*90}")
        print(f"📊 GMAIL KONTATEC SEARCH RESULTS")
        print(f"{'='*90}")
        print(f"Total messages found: {len(messages)}\n")

        # Group by recipient
        by_recipient = {}
        for msg in messages:
            recipient = msg['to']
            if recipient not in by_recipient:
                by_recipient[recipient] = []
            by_recipient[recipient].append(msg)

        # Print by recipient
        for recipient, msgs in by_recipient.items():
            print(f"\n📮 Messages to: {recipient}")
            print(f"   Count: {len(msgs)}")
            print(f"   {'-'*86}")

            for i, msg in enumerate(msgs[-20:], 1):  # Show last 20
                from_name = msg['from'].split('<')[0].strip() if '<' in msg['from'] else msg['from']
                print(f"\n   [{i}] From: {from_name}")
                print(f"       Subject: {msg['subject'][:70]}")
                print(f"       Date: {msg['date'][:30]}")
                preview = msg['body_preview'][:100].replace('\n', ' ')
                print(f"       Preview: {preview}...")

            if len(msgs) > 20:
                print(f"\n   ... and {len(msgs) - 20} more messages")

        print(f"\n{'='*90}")

        # Summary
        print("\n📈 SUMMARY STATISTICS")
        print(f"{'-'*90}")
        print(f"Total recipients: {len(by_recipient)}")
        print(f"Total messages: {len(messages)}\n")

        for recipient, msgs in sorted(by_recipient.items()):
            print(f"  • {recipient}: {len(msgs)} messages")

    def export_results(self, messages: List[Dict[str, Any]], filename: str = 'gmail_kontatec_results.json'):
        """Export results to JSON."""
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Results exported to: {os.path.abspath(filename)}")

    def close(self):
        """Close IMAP connection."""
        if self.imap:
            try:
                self.imap.close()
                self.imap.logout()
            except:
                pass


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description='Search Kontatec Gmail for messages'
    )
    parser.add_argument('--email', help='Gmail address')
    parser.add_argument('--recipients', nargs='+',
                        help='Email addresses to search for (default: vitor.canal@kontatec.com.br)')
    parser.add_argument('--output', default='gmail_kontatec_results.json',
                        help='Output JSON file name')

    args = parser.parse_args()

    # Default recipients
    recipients = args.recipients or ['vitor.canal@kontatec.com.br']

    print("🔍 Gmail Kontatec Search")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    searcher = None
    try:
        # Initialize
        searcher = KontатecGmailSearcher(email_addr=args.email)

        # Search
        messages = searcher.search_kontatec_emails(recipients)

        # Print results
        searcher.print_results(messages)

        # Export
        if messages:
            searcher.export_results(messages, args.output)

        print(f"\n✓ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    finally:
        if searcher:
            searcher.close()


if __name__ == '__main__':
    main()
