# telegram-forwarding-bot
A Telegram bot that forwards photos and videos from a source group to target groups, translating captions into English (or another specified language) via Google Translate. Built with Python and Telethon, it supports media albums, handles rate limits, and excludes GIFs for efficient media sharing.

# Telegram Forwarding Bot with Translation

This is a Telegram bot built with Python and Telethon that forwards messages containing photos and videos from a source Telegram group to one or more target groups. The bot translates the captions to English (or another specified language) using Google Translate. It handles individual media files and albums, and includes robust error handling to manage rate limits and connection errors effectively.

## Features

- **Message Forwarding**: Forwards media messages (photos and videos) from a source group to target groups.
- **Caption Translation**: Translates captions to English (or another specified language) using Google Translate.
- **Album Support**: Ensures that grouped media (albums) are forwarded in the correct order and as a cohesive unit.
- **Flood Wait Handling**: Manages Telegram’s rate limits by respecting flood wait errors with automatic retries.
- **GIF Filtering**: Excludes GIFs to focus on photos and videos only.

## Requirements

- Python 3.7+
- A Telegram account with API credentials (API ID and API hash)
- Bot token from [BotFather](https://core.telegram.org/bots#botfather)

## Setup

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/yourusername/telegram-forwarding-bot.git
    cd telegram-forwarding-bot
    ```

2. **Install Dependencies**:

    Use `pip` to install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

    **Note**: Ensure `telethon` and `googletrans` are included in `requirements.txt`.

3. **Configure API Credentials and Group IDs**:

    Create a `config.py` file in the root directory of the project, and add your Telegram API credentials and group IDs as follows:

    ```python
    # config.py

    # Your Telegram API credentials
    api_id = 1234567  # Replace with your actual API_ID from my.telegram.org
    api_hash = 'your_api_hash_here'  # Replace with your actual API_HASH from my.telegram.org
    bot_token = 'your_bot_token_here'  # Replace with your bot's token from BotFather on Telegram

    # Group IDs
    source_group = -1001234567890  # Replace with the source group ID
    target_group_1 = -1009876543210  # Replace with the first target group ID
    target_group_2 = -1001122334455  # Replace with the second target group ID
    ```

    - **API ID and API Hash**: Obtain these from [my.telegram.org](https://my.telegram.org) by creating a new application.
    - **Bot Token**: Get this from [BotFather](https://t.me/BotFather) on Telegram by creating a new bot.
    - **Group IDs**: Use [@IDBot](https://t.me/myidbot) in Telegram to get the group IDs for `source_group`, `target_group_1`, and `target_group_2`.

4. **Run the Bot**:

    Start the bot by running the main script:

    ```bash
    python bot.py
    ```

    The bot will start listening to messages in the specified source group and forward translated media messages to the target groups.

## Usage

The bot automatically listens for new messages in the source group. When it detects a message containing a photo or video:

- If the message includes a caption, the bot translates it to English.
- It then forwards the media and the translated caption to the target groups.

### Error Handling and Retries

- The bot uses a retry mechanism for sending messages with incremental delays.
- It manages rate limits by handling `FloodWaitError` exceptions, waiting the required time before retrying.

## Customization

- **Translation Language**: By default, captions are translated to English. To change the target language, update the `dest` parameter in the translation function within the code.
  
- **Additional Target Groups**: You can add more target groups by including their IDs in `config.py` and adjusting the `target_groups` list in the code accordingly.

## Security Considerations

1. **API Credentials**: Keep `config.py` private and secure. **Do not commit it to public repositories**. Add `config.py` to `.gitignore` if using Git.

    ```bash
    echo "config.py" >> .gitignore
    ```

2. **Rate Limits**: Be mindful of Telegram’s rate limits. The bot includes flood wait handling, but excessive requests may lead to temporary restrictions.

3. **Environment Variables (Optional)**: For enhanced security, consider using environment variables for sensitive information instead of `config.py`.

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for suggestions and bug reports.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### Notes

- **Dependencies**: Ensure that all required dependencies are listed in `requirements.txt`.
- **Testing**: Test the bot thoroughly before deploying it to production, especially if modifying the code to handle additional message types or languages.

By following these setup instructions, you should be able to run the Telegram Forwarding Bot with translation functionality. If you encounter issues, please refer to the documentation or open an issue.
