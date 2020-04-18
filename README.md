Phrases Tracking Slack Bot
==========================

### Overview

What the bot can do:
- Listen for a specific phrases and notifies user into Direct Message (DM) in Slack
- Phrases and channel can be configurable by the user using exisiting Slack functionality

### API

- POST /addphrase
- POST /deletephrase

### Database Schema

Table: phrases
Fields:
- channel (PK) VARCHAR(10) - *Slack channel id*
- text (PK) VARCHAR(30) - *phrase to be tracked*
- is_active BOOLEAN - *determine if the phrase is active*
- user_id VARCHAR(10) - *user_id of the first Slack user who add the phrase*

### Steps for User to Use

1. Go to the associated Slack app - https://join.slack.com/t/vgs-space/shared_invite/zt-dspmprcx-8eNjGl~TLSclzR3RawVbrw
2. Go in a channel
3. Send a command /invite roboear *(name of the bot)* to add bot to the channel
4. Send a commnd /addphrase *some_phrase*
5. When someone in that channel mention that phrase, the bot will DM the user
6. Send a command /deletephrase to delete that phrase
7. When someone in that channel mention that pharse again, the bot will **not** DM the user this time

### Steps to Run the App Locally
Note: the app is already running in Heroku and the bot Slack Event API and commands are linked with Heroku domain. The step below would work locally if localhost (or proxy of it) is linked with Slack app.
- Run 'docker-compose up'

### Technologies
- Flask/Python
- MySQL
- Docker
- Slack API
- Heroku

### Other details
- The application is hosted in Heroku https://blooming-sea-92675.herokuapp.com/
- Slack app associated with the bot can be joined via https://join.slack.com/t/vgs-space/shared_invite/zt-dspmprcx-8eNjGl~TLSclzR3RawVbrw
