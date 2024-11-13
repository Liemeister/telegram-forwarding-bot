Here’s your README with improved formatting and structure:

---

# Telegram Forwarding Bot with Translation

This bot forwards photos and videos from a source Telegram group to one or more target groups, translating captions into English (or another specified language) via Google Translate. Built with Python and Telethon, it supports media albums, handles rate limits, and excludes GIFs for efficient media sharing.

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

3. **Configure API Credentials and Group IDs**:

    The repository includes a `config.py` file in the root directory as a template for setting up your bot's credentials and group IDs. Simply open `config.py` and replace the placeholder values with your actual Telegram API credentials and group IDs as shown below:

    ```python
    # config.py

    # Telegram API credentials
    api_id = 1234567  # Replace with your actual API_ID from my.telegram.org
    api_hash = 'your_api_hash_here'  # Replace with your actual API_HASH from my.telegram.org
    bot_token = 'your_bot_token_here'  # Replace with your bot's token from BotFather

    # Group IDs
    source_group = -1000000000000  # Replace with the source group ID where messages will be monitored
    target_group_1 = -1000000000001  # Replace with the first target group ID where messages will be forwarded
    target_group_2 = -1000000000002  # Replace with the second target group ID where messages will be forwarded
    ```

    **Security Note**: After filling in `config.py` with your actual API credentials and group IDs, make sure to keep your repository **private** if you’re pushing it to GitHub or another remote host. This will help prevent accidental exposure of sensitive information like your API tokens and group IDs.

4. **Run the Bot**:

    Start the bot by running the main script:

    ```bash
    python telegram-forwarding-bot.py
    ```

## Usage

The bot automatically listens for new messages in the source group. When it detects a message containing a photo or video:

- If the message includes a caption, the bot translates it to English.
- It then forwards the media and the translated caption to the target groups.

## Error Handling and Retries

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

## Hosting on Fly.io

You can easily deploy this bot on [Fly.io](https://fly.io/) to keep it running 24/7 without idle timeouts. Fly.io supports GitHub integration, allowing you to automate deployments directly from your GitHub repository.

### Deploying to Fly.io via GitHub Integration

1. **Sign Up on Fly.io and Link Your GitHub Repository**:

    - Go to [Fly.io](https://fly.io/) and sign up or log in.
    - In the Fly.io dashboard, select **Create New App** and choose **Deploy from GitHub**.
    - Connect your GitHub account and select the repository for this bot.
    - Choose your Fly.io app name and preferred region for deployment (e.g., `ams` for Amsterdam, `iad` for Virginia).

2. **Customize `fly.toml` with Your App Name**:

    - The repository includes a `fly.toml` file and a `Dockerfile` configured for Fly.io deployment.
    - Open `fly.toml` and update `app = "your-fly-app-name"` to match the app name you chose on Fly.io:

      ```toml
      app = "your-fly-app-name"  # Replace with your chosen Fly.io app name
      ```

3. **Set Port Configuration to 0**:

   - During deployment, select **Customize Deploy** and change the default port setting from `8080` to `0`. This ensures the bot functions correctly without a web server requirement.

4. **Trigger Deployment**:

    - After setting up GitHub integration, Fly.io will automatically deploy your bot each time you push changes to the repository.
    - You can monitor deployment logs and manage the app through the Fly.io dashboard.

### About the Dockerfile and `fly.toml`

- **Dockerfile**: This repository includes a `Dockerfile` that specifies a lightweight Python environment for deploying the bot. Fly.io uses this file to create a Docker container for the app.
- **fly.toml**: This file configures Fly.io’s deployment settings. Be sure to update the `app` field in `fly.toml` with the name of your Fly.io app to ensure it matches the setup in your Fly.io dashboard.

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for suggestions and bug reports.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### Notes

- **Dependencies**: Ensure that all required dependencies are listed in `requirements.txt`.
- **Testing**: Test the bot thoroughly before deploying it to production, especially if modifying the code to handle additional message types or languages.

---

This structure provides clear and professional documentation that’s easy to follow and covers all aspects of setup, configuration, and deployment. Let me know if you need any more tweaks!
