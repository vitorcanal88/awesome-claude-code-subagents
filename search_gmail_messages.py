#!/usr/bin/env python3
"""
Gmail Message Search Tool
Searches Gmail for messages sent to specific email addresses.
Supports multiple authentication methods for flexibility.
"""

import os
import sys
import json
import base64
import pickle
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GmailSearcher:
    """Search Gmail for messages with advanced filtering."""

    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self, creds_file: str = None, token_file: str = None):
        """
        Initialize Gmail API service.

        Args:
            creds_file: Path to credentials JSON file
            token_file: Path to pickled token file
        """
        self.service = None
        self.creds_file = creds_file
        self.token_file = token_file
        self.auth()

    def auth(self):
        """Authenticate with Gmail API using available methods."""
        try:
            creds = None

            # Try 1: Use existing token file
            if self.token_file and os.path.exists(self.token_file):
                with open(self.token_file, 'rb') as f:
                    creds = pickle.load(f)
                print("✓ Using stored token credentials")

            # Try 2: Use provided credentials file
            elif self.creds_file and os.path.exists(self.creds_file):
                try:
                    # Try as service account
                    creds = ServiceAccountCredentials.from_service_account_file(
                        self.creds_file,
                        scopes=self.SCOPES
                    )
                    print("✓ Using service account credentials")
                except:
                    # Try as OAuth2
                    creds = Credentials.from_authorized_user_file(
                        self.creds_file,
                        scopes=self.SCOPES
                    )
                    print("✓ Using OAuth2 credentials")

            # Try 3: Use application default credentials
            else:
                creds, project = google.auth.default(scopes=self.SCOPES)
                print("✓ Using application default credentials")

            # Refresh if needed
            if creds and hasattr(creds, 'refresh_needed') and creds.refresh_needed:
                creds.refresh(Request())

            # Build the Gmail service
            self.service = build('gmail', 'v1', credentials=creds)
            print("✓ Gmail API authenticated successfully\n")

        except Exception as e:
            print(f"❌ Authentication error: {e}")
            print("\nTo use this script, provide Gmail API credentials:")
            print("  1. Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
            print("  2. Pass --creds-file /path/to/credentials.json")
            print("  3. Or configure application default credentials with: gcloud auth application-default login")
            sys.exit(1)

    def search_messages(self, recipients: List[str]) -> List[Dict[str, Any]]:
        """
        Search for messages sent to specific recipients.

        Args:
            recipients: List of email addresses to search for

        Returns:
            List of message data with metadata
        """
        all_messages = []

        for recipient in recipients:
            print(f"📧 Searching for messages sent to: {recipient}")

            try:
                # Build the search query for messages sent TO this recipient
                query = f'to:{recipient}'

                # Get message IDs with pagination
                request = self.service.users().messages().list(
                    userId='me',
                    q=query,
                    maxResults=100
                )

                message_count = 0
                while request is not None:
                    results = request.execute()
                    messages = results.get('messages', [])

                    if not messages and message_count == 0:
                        print(f"   → Found 0 messages")
                        break

                    message_count += len(messages)
                    print(f"   → Processing {message_count} messages...")

                    # Get full message details for each message
                    for msg in messages:
                        try:
                            message_data = self.service.users().messages().get(
                                userId='me',
                                id=msg['id'],
                                format='full'
                            ).execute()

                            # Extract relevant information
                            headers = message_data['payload'].get('headers', [])
                            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No subject')
                            from_addr = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                            date_str = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown date')
                            to_addr = next((h['value'] for h in headers if h['name'] == 'To'), recipient)

                            # Try to extract body
                            body = self._get_message_body(message_data)

                            message_info = {
                                'id': msg['id'],
                                'recipient': recipient,
                                'from': from_addr,
                                'to': to_addr,
                                'subject': subject,
                                'date': date_str,
                                'snippet': message_data.get('snippet', ''),
                                'body_preview': body[:500] if body else 'No body content',
                                'labels': message_data.get('labelIds', [])
                            }

                            all_messages.append(message_info)

                        except HttpError as error:
                            if error.resp.status != 404:
                                print(f"   ⚠ Error retrieving message: {error}")
                            continue

                    # Get next page
                    if 'nextPageToken' in results:
                        request = self.service.users().messages().list(
                            userId='me',
                            q=query,
                            pageToken=results['nextPageToken'],
                            maxResults=100
                        )
                    else:
                        request = None

                print(f"   ✓ Found {len([m for m in all_messages if m['recipient'] == recipient])} messages\n")

            except HttpError as error:
                print(f"   ❌ Error searching Gmail: {error}\n")
                continue

        return all_messages

    def _get_message_body(self, message: Dict[str, Any]) -> str:
        """Extract message body from message data."""
        try:
            payload = message.get('payload', {})

            if 'parts' in payload:
                # Multipart message
                for part in payload['parts']:
                    if part.get('mimeType') == 'text/plain':
                        if 'data' in part.get('body', {}):
                            data = part['body']['data']
                            return base64.urlsafe_b64decode(data).decode('utf-8')

            elif 'data' in payload.get('body', {}):
                # Simple message
                data = payload['body']['data']
                return base64.urlsafe_b64decode(data).decode('utf-8')
        except Exception as e:
            pass

        return message.get('snippet', '')

    def print_results(self, messages: List[Dict[str, Any]]):
        """Print formatted results."""
        if not messages:
            print("❌ No messages found")
            return

        print(f"\n{'='*90}")
        print(f"📊 GMAIL SEARCH RESULTS")
        print(f"{'='*90}")
        print(f"Total messages found: {len(messages)}\n")

        # Group by recipient
        by_recipient = {}
        for msg in messages:
            recipient = msg['recipient']
            if recipient not in by_recipient:
                by_recipient[recipient] = []
            by_recipient[recipient].append(msg)

        # Print results by recipient
        for recipient, msgs in by_recipient.items():
            print(f"\n📮 Messages to: {recipient}")
            print(f"   Count: {len(msgs)}")
            print(f"   {'-'*86}")

            # Sort by date (most recent first)
            try:
                msgs_sorted = sorted(msgs, key=lambda m: m['date'], reverse=True)
            except:
                msgs_sorted = msgs

            for i, msg in enumerate(msgs_sorted[:20], 1):  # Show first 20
                from_name = msg['from'].split('<')[0].strip() if '<' in msg['from'] else msg['from']
                print(f"\n   [{i}] From: {from_name}")
                print(f"       Subject: {msg['subject'][:70]}")
                print(f"       Date: {msg['date'][:30]}")
                preview = msg['body_preview'][:100].replace('\n', ' ')
                print(f"       Preview: {preview}...")

            if len(msgs) > 20:
                print(f"\n   ... and {len(msgs) - 20} more messages")

        print(f"\n{'='*90}")

        # Print summary statistics
        print("\n📈 SUMMARY STATISTICS")
        print(f"{'-'*90}")
        print(f"Total recipients searched: {len(by_recipient)}")
        print(f"Total messages found: {len(messages)}")
        print()

        # Count by recipient
        for recipient, msgs in sorted(by_recipient.items()):
            print(f"  • {recipient}: {len(msgs)} messages")

    def export_results(self, messages: List[Dict[str, Any]], filename: str = 'gmail_search_results.json'):
        """Export results to JSON file."""
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Results exported to: {os.path.abspath(filename)}")


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Search Gmail for messages sent to specific recipients'
    )
    parser.add_argument(
        '--creds-file',
        help='Path to Gmail API credentials JSON file'
    )
    parser.add_argument(
        '--token-file',
        help='Path to pickled OAuth2 token file'
    )
    parser.add_argument(
        '--output',
        default='gmail_search_results.json',
        help='Output JSON file name (default: gmail_search_results.json)'
    )

    args = parser.parse_args()

    # Email addresses to search for
    recipients = [
        'vitor.canal@kontatec.com.br',
        'vitor.canal@tetakon.com.br'
    ]

    print("🔍 Gmail Message Search Tool")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Initialize searcher
    searcher = GmailSearcher(
        creds_file=args.creds_file or os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'),
        token_file=args.token_file
    )

    # Search for messages
    messages = searcher.search_messages(recipients)

    # Print results
    searcher.print_results(messages)

    # Export results
    if messages:
        searcher.export_results(messages, args.output)

    print(f"\n✓ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == '__main__':
    main()
