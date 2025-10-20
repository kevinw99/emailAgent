<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Project Context
This is a Python Flask web application for managing Gmail subscriptions and automating unsubscribe actions based on user rules and AI confidence. Integrate Gmail API with OAuth2, detect subscription emails, prompt user for unsubscribe, and support auto-unsubscribe based on rules (e.g., archived emails, low engagement, bulk/promotions label).

# Coding Guidelines
- Use Flask for the web framework.
- Use the official Google API Python client for Gmail integration.
- Follow best practices for OAuth2 authentication.
- Implement logic for detecting subscription emails and automating unsubscribe actions.
- Prioritize user privacy and security.
