# Reddit Karma Farming Project

This project focuses on developing a Reddit karma farming bot that automates the process of generating comments and receiving upvotes on the platform. The bot aims to help users increase their karma score by participating in discussions and contributing valuable content.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Features

- Automated comment generation: The bot generates comments based on predefined templates and submits them to relevant discussions.
- Strategic upvoting: The bot identifies popular and trending posts to strategically upvote them, increasing the visibility of the user's account.
- Customizable settings: Users can configure various parameters such as comment templates, frequency of interactions, and targeting specific subreddits.

## Installation

1. Clone the repository to your local machine.
2. Install the required dependencies by running the following command:
  `pip install -r requirements.txt`
3. Obtain Reddit API credentials by creating a new application on the Reddit Developer website.
4. Update the configuration file (`praw.ini`) with your API credentials and desired settings.

## Usage

1. Run the bot script by executing the following command:
  `python3 karma_farm.py bot_name_here`
2. The bot will start interacting with Reddit, generating comments, and upvoting posts based on the configured settings.
3. Monitor the bot's activity and adjust the settings as needed to optimize karma farming.

## License

This project is licensed under the [MIT License](LICENSE).
