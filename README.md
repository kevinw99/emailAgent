# Email Agent

This project is a Python Flask web application that connects to your Gmail account, detects subscription emails, and helps you manage (subscribe/unsubscribe) them. It supports automation rules for high-confidence unsubscribe actions (e.g., archived emails, low engagement, bulk/promotions label).

## Features
- Gmail OAuth2 authentication
- Detects subscription/newsletter emails
- Prompts user to confirm unsubscribe actions
- Auto-unsubscribe based on user-defined and AI rules

## Getting Started
1. Ensure you have Python 3.8+ installed.
2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask app:
   ```bash
   flask run
   ```

## Next Steps
- Integrate Gmail API and OAuth2
- Implement subscription detection and automation logic
- Build the web UI for user interaction

---

For more details, see `.github/copilot-instructions.md`.
