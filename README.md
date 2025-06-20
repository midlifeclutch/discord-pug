# discord-pug

A basic Discord bot intended for community 10mans organised in isk's `CS2 Community`.

## Players. Read this.

When isk starts a queue, do the following.

- `.add <elo>` this is your Elo rating, not level.

Once 10 players are in the voice channel, __and you are one of those 10 players__, do this.

- `.ready`

## Commands

### User Commands

- `.add <elo>`: Add yourself to the current queue.
- `.ready`: Notify the bot you're ready.
- `.queue`: Shows everyone who queued

### Admin Commands

- `.start`: Starts a queue
  - `.start` has optional arguments:
    - `--noq`: By default you are automatically added to the queue, disable this behaviour.
- `.stop`: Stops and empties the queue
- `.suggest`: Suggests the teams based on Elo, it's not perfect but it is quick.
