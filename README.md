<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h1 align="center">Shop with heymax Telegram bot</h1>
</p>
<!-- PROJECT LOGO -->

🛍️ Get your unique shopping link and start earning Max Miles today! 🚀

## Description
The `heymax_shop_bot` is a Telegram bot designed for the heymax shopping app. This bot facilitates unique affiliate tracking links for users based on their interactions within a Telegram group. It manages user registration, handles inline commands, and generates personalized affiliate links for different merchants.

## Installation Instructions
To set up and run the `heymax_shop_bot`, follow these steps:

1. **Clone the Repository:**
   ```
   git clone https://github.com/calvindotsg/heymax_shop_bot.git
   cd heymax_shop_bot
   ```

2. **Create and Activate a Virtual Environment:**
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   Create a `.env` file in the project root directory and add your Telegram bot token and Firestore credentials:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   GOOGLE_APPLICATION_CREDENTIALS=path_to_your_firestore_credentials.json
   ```

## Usage
To use `heymax_shop_bot`, start the bot by running:
```
python main.py
```

## Contributing
We welcome contributions to improve `heymax_shop_bot`. If you want to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a Pull Request.

Please make sure to update tests as appropriate and adhere to the coding standards.

## Documentation
Additional documentation can be found in the `docs` directory. This includes detailed descriptions of the bot's functionality, state management, and database schemas.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact Information
If you have any questions, issues, or suggestions, feel free to open an issue in the GitHub repository or contact the project maintainer at `your-email@example.com`.

## Acknowledgments
We would like to acknowledge the contributors of the `python-telegram-bot` and `google-cloud-firestore` libraries, whose work made this project possible.

---

**Good Practices:**
- **Keep it updated:** Reflect any changes in your project within the README.
- **Make it visually appealing:** Use headers, bullet points, and images when possible.
- **Use clear language:** Avoid jargon and complex words.
- **Stay concise:** Be as concise as possible. For extensive documentation, link separate documents within the README.

---

This README provides an overview and instructions to effectively use and contribute to the `heymax_shop_bot` project. For more detailed information, refer to the additional documentation provided.