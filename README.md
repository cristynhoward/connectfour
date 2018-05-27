# Connect Four

This repository contains the development stages of the connect four twitter bot.

### Phase 1

Initially I developed code to automatically process and respond to twitter mentions. 

The tweet_reader.get_mentions() script is automatically triggered on a regular interval, and collects all mentions of the bot made available by the Twitter API since the last mention read. Upon processing each mention, the script constructs and stores a pre-written tweet with it's accompanying metadata. 

Then, in a separate process, the tweet_writer.tweet() method composes and sends out tweets based on the stored information, in a FIFO manner.

### Phase 2

In the second phase, I wrote a class responsible for the implementation of the game board functionality. 

### Phase 3

In the third phase, I adapted the phase 1 code to create, interact with, and store game boards as written in phase 2, in response to mentions of the bot. 

In support of this, I wrote a group of functions to optimize the storage of game information in text files.

By this point in the development process, I had realized the necessity of upgrading to a VPS, and had allocated a Ubuntu server upon which to test my code. 

In the the process of setting up the VPS, I had to:
* learn about & set up SSH authentication
* create & configure a sudo non-root user
* configure firewall
* configure local programming environment
