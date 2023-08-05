# whatsapp-chat-analysis 
Try this app [here](https://whatsapp-chats-analysis.streamlit.app/)

This app reads an exported WhatsApp chat (in 24 hour format) and then visualizes the various stats.

## Features
* Top users
* Monthly timeline
* Daily timeline
* Most active days
* Most used words
* Most used emojis
* Word cloud
* Filter by user for each stat

## Getting chat source
* Open a chat/group chat
* Tap on three dots on the top right
* Tap "More"
* Choose "Export chat"
* Choose "Without Media"

## Notes
* Currently supports this format:
  > 27/05/22, 9:48 - Person 1: Any message <br>
  > 27/05/22, 15:07 - Person 2: Some other text
* English and Hindi stop words are included in alphabets.txt and stop_hinglish.txt

