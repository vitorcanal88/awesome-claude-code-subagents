# Gmail Search - Quick Start Guide

Get up and running in 3 minutes!

## Step 1️⃣: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Select: **Mail** & **Windows Computer** (or your device)
3. Google generates a 16-character password
4. **Copy it** (you'll use it next)

## Step 2️⃣: Run Setup

```bash
python3 setup_gmail_auth.py
```

When prompted:
- **Email:** `v.canal88@gmail.com` (press Enter for default)
- **Password:** Paste the 16-char password (input is hidden)

You'll see:
```
✓ IMAP connection successful
✓ Found XXX messages in INBOX
✓ Configuration saved
✅ Authentication successful!
```

## Step 3️⃣: Search Emails

```bash
python3 search_gmail_messages_apppass.py
```

Output shows:
- 📧 Messages found for each recipient
- 📮 Sender, subject, date, preview
- 📈 Statistics
- 💾 Results exported to `gmail_search_results.json`

## Emails Searched

The script automatically searches for messages sent to:
- `vitor.canal@kontatec.com.br`
- `vitor.canal@tetakon.com.br`

## Results

Results are saved in: `gmail_search_results.json`

Each message includes:
- From address
- Subject
- Date
- Body preview (first 500 characters)

## Troubleshooting

### ❌ "Invalid app password format"
- Make sure it's the 16-character password from Google
- Remove any accidental spaces

### ❌ "Authentication failed"
- Verify you're using the App Password (not your regular password)
- Check that 2-Factor Authentication is enabled on your account
- Try generating a new App Password

### ❌ "Connection timeout"
- Check your internet connection
- Try again in a few moments

## Security Notes

Your credentials are stored in: `~/.gmail/`
- Never share these files
- Never commit them to version control
- You can delete them anytime (just run setup again)

## What Gets Stored

- **~/.gmail/config.json** - Your email address (safe)
- **~/.gmail/.apppass** - Your app password (keep private!)

Both files have restricted permissions (read-only for your user).

## Need More Help?

See `GMAIL_SETUP.md` for advanced setup options and troubleshooting.
