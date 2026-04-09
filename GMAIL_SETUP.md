# Gmail Search Tool Setup Guide

This guide explains how to configure and use the Gmail message search tool to retrieve emails sent to specific recipients.

## Prerequisites

- Python 3.7+
- Google Account with Gmail enabled
- Access to Google Cloud Console

## Setup Instructions

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use an existing one)
3. Enable the Gmail API:
   - Search for "Gmail API" in the search bar
   - Click on the Gmail API result
   - Click "Enable"

### Step 2: Create OAuth2 Credentials

#### Option A: Service Account (Recommended for automation)

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **Service Account**
3. Fill in the service account details
4. Click **Create and Continue**
5. Click **Create Key** > **JSON**
6. Save the JSON file securely (e.g., `gmail_credentials.json`)
7. Note the service account email address

Then authorize the service account:
1. Go to **APIs & Services** > **Domain-wide Delegation**
2. Enable it for the service account
3. Add the required scopes: `https://www.googleapis.com/auth/gmail.readonly`

#### Option B: OAuth2 Desktop Application

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. Choose **Desktop application**
4. Download the JSON file
5. Save it as `credentials.json`

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Script

#### Using Service Account Credentials

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/gmail_credentials.json
python3 search_gmail_messages.py
```

#### Using OAuth2 Credentials File

```bash
python3 search_gmail_messages.py --creds-file /path/to/credentials.json
```

#### Using Stored Token

```bash
python3 search_gmail_messages.py --token-file /path/to/token.pickle
```

## Usage

### Basic Search

The script searches for all messages sent to:
- `vitor.canal@kontatec.com.br`
- `vitor.canal@tetakon.com.br`

Run it simply:

```bash
python3 search_gmail_messages.py
```

### Custom Output File

```bash
python3 search_gmail_messages.py --output my_results.json
```

## Output

The script generates:

1. **Console Output:**
   - Summary of messages found per recipient
   - First 20 messages with subject, sender, and preview
   - Statistics and counts

2. **JSON Export:**
   - Complete message data
   - Headers, subject, sender, date
   - Message body preview
   - Labels and metadata

### JSON Output Format

```json
{
  "id": "message_id_here",
  "recipient": "vitor.canal@kontatec.com.br",
  "from": "sender@example.com",
  "to": "vitor.canal@kontatec.com.br",
  "subject": "Email subject",
  "date": "Wed, 01 Jan 2026 10:00:00 -0300",
  "snippet": "Email preview text...",
  "body_preview": "Full body text up to 500 chars...",
  "labels": ["INBOX", "IMPORTANT"]
}
```

## Advanced Features

### Filtering by Date Range

To search for messages in a specific date range, modify the script's search query:

```python
# In the search_messages method, change:
query = f'to:{recipient}'

# To add date filtering:
query = f'to:{recipient} after:2025-01-01 before:2026-12-31'
```

### Filtering by Subject

```python
query = f'to:{recipient} subject:"specific subject"'
```

### Excluding Certain Messages

```python
query = f'to:{recipient} -label:trash'
```

## Troubleshooting

### "Credentials not found" Error

Make sure either:
1. `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set
2. You passed `--creds-file` flag with valid path
3. Your credentials file is properly formatted JSON

### "Invalid grant" Error

- Your credentials file might be expired or invalid
- Try regenerating credentials from Google Cloud Console
- Ensure the service account has proper permissions

### "Rate limited" Error

Gmail API has rate limits. The script handles this by:
- Processing messages in batches of 100
- Adding delays between requests if needed
- Only reading message details (not performing bulk operations)

For higher quotas:
1. Go to **APIs & Services** > **Quotas**
2. Select "Gmail API"
3. Request quota increase if needed

## Security Notes

- **Never commit credential files** to version control
- Add credentials to `.gitignore`:
  ```
  gmail_credentials.json
  credentials.json
  token.pickle
  ```
- Use environment variables for production deployments
- Rotate credentials regularly
- Use service accounts instead of personal credentials when possible

## Integration with Claude Code

This tool is designed as a subagent for Claude Code. To use it:

1. Copy this folder or files to your project
2. Set up credentials as described above
3. Invoke the `gmail-search-specialist` subagent when you need email searches

## Examples

### Search all messages to both addresses

```bash
python3 search_gmail_messages.py
```

### Search and export to custom file

```bash
python3 search_gmail_messages.py --output email_audit.json
```

### Search with specific service account

```bash
python3 search_gmail_messages.py --creds-file ~/keys/service-account.json
```

## Support

For issues with:
- **Gmail API:** [Google Gmail API Docs](https://developers.google.com/gmail/api)
- **OAuth2:** [Google OAuth2 Setup](https://developers.google.com/identity/protocols/oauth2)
- **This Script:** Check the error message and troubleshooting section above

## Next Steps

1. Configure your credentials file
2. Test the script on your own Gmail
3. Customize the search queries as needed
4. Integrate with your automation workflows
