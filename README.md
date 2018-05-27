# Connect Four

This repository contains the development stages of the connect four twitter bot.

### Phase 1

Initially I developed code to automatically process and respond to twitter mentions. This code, which interfaces with the Twitter API, was developed independently of any game board actions. This implementation, upon processing a mention, loads and stores a pre-written tweet with it's accompanying metadata to be sent. Then, in a separate process, the bot composes and sends out tweets in a FIFO manner.

At this point in the development process, I had not allocated any VPS for this bot, so I used a glitch Flask server as a sandbox environment to test my code. 

### Phase 2

In the second phase, I wrote a class responsible for the implementation of the game board functionality. 

### Phase 3

In the third phase, I adapted the phase 1 code to create, interact with, and store game boards as written in phase 2, in response to mentions of the bot. 

In support of this, I wrote a group of functions to optimize the storage of game information in text files.

By this point in the development process, I had realized the necessity of upgrading to a VPS, and had allocated a Ubuntu server upon which to test my code. 