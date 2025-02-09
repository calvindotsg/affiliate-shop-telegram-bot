# Telegram Affiliate Bot

## Overview

This Telegram bot enables seamless affiliate marketing within group chats by generating personalized tracking links for users. It simplifies the process of sharing and managing affiliate links while ensuring each user receives a unique, trackable link.

## Business Use Case

Affiliate marketing often requires users to register and generate unique tracking links manually, which can be cumbersome. This bot automates the process by integrating with an existing affiliate system and generating user-specific links based on their registration status.

### Key Benefits:

- **Automation**: Eliminates the need for manual link generation, ensuring users always receive the correct tracking link.
- **Personalization**: Each user gets a unique tracking link, improving accuracy in performance tracking.
- **Seamless Integration**: Works directly within Telegram groups, enabling real-time access to affiliate links.
- **Increased Engagement**: Encourages users to interact with the bot and participate in affiliate programs effortlessly.

## Problem Statement

Traditional affiliate marketing platforms require users to visit external sites, log in, and retrieve tracking links manually. This leads to:

- **User Drop-off**: Many users abandon the process due to complexity.
- **Tracking Issues**: Generic links make it harder to track individual user performance.
- **Lower Conversions**: Extra steps reduce engagement and conversion rates.

This Telegram bot solves these issues by allowing users to generate tracking links with a single command inside a group chat.

## Features

- **Group Command Support**: Users trigger the bot within a Telegram group using `/shop <MerchantName>`.
- **User Registration & Validation**: Checks if the user is registered and prompts for registration if needed.
- **Affiliate Link Generation**: Creates a tracking link unique to each user and merchant.
- **Firestore Database Integration**: Stores and retrieves user data for seamless tracking.
- **State Management**: Ensures smooth user interactions with different states:
  1. Not Started
  2. Received Merchant Command
  3. User Not Registered
  4. User Registered
  5. Sent Unique Tracking Link

## Requirements

- Python 3.7 or higher
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [firebase-admin](https://firebase.google.com/docs/admin/setup)
- A Telegram Bot API token
- Firestore database credentials (service account key)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/telegram-affiliate-bot.git
   cd telegram-affiliate-bot
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Environment**

   - Place your Firestore service account key file in the repository directory.
   - Update the configuration in the code with your Telegram Bot API token and the path to your Firestore credentials.

## Usage

Run the bot using the main script:

```bash
python main.py
```

### User Flow

1. A user in a Telegram group sends a command:
   ```
   /shop <MerchantName>
   ```
2. The bot checks if the user is registered:
   - If **not registered**, the bot sends a direct message requesting email registration.
   - If **registered**, the bot retrieves the user's unique affiliate tracking link.
3. The bot responds with a **"Your Unique Shop with Max Link"** button.
4. When clicked, the button opens the **user’s unique affiliate tracking link** in a browser.

## Code Structure

- **main.py**: Initializes and runs the bot.
- **bot.py**: Handles command processing, user state management, and response logic.
- **utils.py**: Contains helper functions, including the affiliate tracking link generation logic.
- **requirements.txt**: Lists all project dependencies.

## Contribution Guidelines

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
