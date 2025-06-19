# discord-pug

A basic Discord bot intended for community 10mans organised in isk's `CS2 Community`.

## Players. Read this.

When isk starts a queue, do the following.

- `.add <elo>` this is your Elo rating, not level. This is not a guarantee of anything.

Once 10 players are in the voice channel, do this.

- `.ready`

## Commands

### User Commands

- `.add <elo>`: Add yourself to the current queue.
- `.ready`: Notify the bot you're ready.

### Admin Commands

There's no checks in place for these at the moment, don't troll please.

- `.start`: Starts a queue
- `.stop`: Stops and empties the queue
- `.queue`: Shows everyone who queued
- `.suggest`: Suggests the teams based on Elo, it's not perfect but it is quick.
