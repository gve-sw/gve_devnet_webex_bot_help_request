# Request Help Bot

This prototype defines a Webex bot that a user can use to create a help request addressable by members of a specific Webex Team's Space. Once the request is accepted, a 1-1 space between the requester and accepter is created. The bot uses Webex APIs, the webex_bot Python library, and Webex Cards. Custom cards can be used (Note: the default cards target a Radiologist and Physician Assistant use case).

## Contacts
* Trevor Maco

## Solution Components
* Webex Teams
* Python 3.10

## Prerequisites

- **Webex Bot**: To create a Webex bot, you need a token from Webex for Developers.
1. Log in to `developer.webex.com`
2. Click on your avatar and select `My Webex Apps`
3. Click `Create a New App`
4. Click `Create a Bot` to start the wizard
5. Following the instructions of the wizard, provide your bot's name, username, and icon
6. Once the form is filled out, click `Add Bot` and you will be given an access token
7. Copy the access token and store it safely. Please note that the API key will be shown only once for security purposes. In case you lose the key, then you have to revoke the key and generate a new key

- **Help Space**: Ensure a Webex Teams space that will receive the help requests exists. The space name as well as the members of the space are left up to you.

## Installation/Configuration
1. Clone this repository with `git clone https://github.com/gve-sw/gve_devnet_webex_bot_help_request` and open the directory of the root repository.
2. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).
3. Install the required Python libraries with the command:
   ``` bash
   pip3 install -r requirements.txt
   ```
4. Fill in the `config.py` parameters. These include: Bot Token, Bot Name, and the name of the Webex Help Space.
    ``` python
    BOT_TOKEN = '<bot token>'
    BOT_NAME = '<bot name>'
    HELP_SPACE = '<help space name>'
    ```

## Usage

1. Launch the bot with the command:
    ``` python
    python3 bot.py
    ```

To use the bot, start a conversation by adding the bot to a 1-1 or Group space.

Send the string `request`. Once the bot processes the message, it responds with a Webex card containing an optional field to specify details about the request.
Click the `submit` button.

![/IMAGES/request_card](/IMAGES/request_card.png)

Once submitted, the bot will delete the card and post the request into the specified Help Space using a Webex card. The request card includes the requester name, optional request details, and a unique id.
To accept a request, click the `accept` button. 

![/IMAGES/accept_card](/IMAGES/accept_card.png)

Clicking the `accept` button will create a 1-1 space with the requester and delete the card from the help space. The 1-1 space name follows the format '{Requester} - {Accepter} Help Request ({unique id})'. The bot leaves the space, and this space can be used to help the requester!

![/IMAGES/1_1_Space.png](/IMAGES/1_1_Space.png)

# References
* Webex Bot library used: https://pypi.org/project/webex-bot/

# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.