# Connect 4

This repository contains the code for the connect four twitter bot.

## Acknowledgments

#### The connect four twitter bot was imagined & developed by cristyn howard.

The gameplay is that of the classic [Connect Four](https://en.wikipedia.org/wiki/Connect_Four) (also known as Captain's Mistress, Four Up, Plot Four, Find Four, Four in a Row, Four in a Line and Gravitrips (in Soviet Union)), which has unknown origins.

The name "Connect Four", and the [plastic boardgame](https://www.hasb.com/en-us/product/connect-4-game:80FB5BCA-5056-9047-F5F4-5EB5DF88DAF4) from which the bot's emoji aesthetic is derived, are trademarks of Hasbro Inc.

## Infrastructure

@BotConnectFour is written in [Python](https://www.python.org/about/), and makes use of the [Tweepy](http://www.tweepy.org), [PyMongo](https://pypi.org/project/pymongo/), and [Emoji](https://pypi.org/project/emoji/) libraries.

It is run from a [Digital Ocean](https://www.digitalocean.com) Ubuntu 16.04 droplet.

It stores game data in a Sandbox-tier MongoDB instance, hosted with [mLab](https://mlab.com/welcome/).


## How to Play

1. START: mention @BotConnectFour in a new tweet, type the word "new" followed by a space, & then mention the user you want to play a game with.

2. PLAY: on your turn (indicated by a "next" beside your name), reply to the board with the number of the column you want to put your piece in.

3. WIN: when you get 4 in a row!

## Code of Conduct

* Users are prohibited from using @BotConnectFour to harass or annoy other Twitter users with repeated, unwanted game requests.

* Users are prohibited from using @BotConnectFour circumvent another Twitter user's block settings and deliver unwanted notifications.

* Users who violate the CoC are subject to blocks from @BotConnectFour

## Accessibility

@BotConnectFour only accepts Arabic numerals as player inputs.

Unfortunately, due to the highly visual game-play, @BotConnectFour is not accessible to Twitter users who rely on text-to-speech software.


