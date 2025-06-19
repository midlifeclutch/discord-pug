import itertools
import textwrap
from discord.ext import commands

SAMPLE_DATA = [
    ['flusha', 1528],
    ['coldzera', 1318],
    ['kennyS', 1501],
    ['Xyp9x', 2208],
    ['sh1ro', 1838],
    ['s1mple', 3124],
    ['ropz', 2579],
    ['niko', 1363],
    ['f0rest', 1101],
    ['zywOo', 2069],
]

ALLOWED_CHANNELS = {
    'bot',                  # test
    1383801344514592839,    # isk: community-5v5
}

def check_channel(*chan):
    def predicate(ctx):
        channel = ctx.channel
        return (
            channel.name in ALLOWED_CHANNELS or
            channel.id in ALLOWED_CHANNELS
        )
    return commands.check(predicate)

def probability(team_a, team_b, size=5):
    rating_a = team_a / size
    rating_b = team_b / size

    exp = 1 / 10**((rating_b - rating_a) / 400)

    return (round(exp*100,2), round((1-exp)*100,2))

class PUG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @check_channel()
    async def start(self, ctx):
        if self.bot.queue_status:
            await ctx.send(f'{ctx.author.mention} queue already started.')
        else:
            self.bot.queue_status = True
            await ctx.send(f'{ctx.author.mention} started queue.')

    @commands.command()
    @check_channel()
    async def stop(self, ctx):
        if not self.bot.queue_status:
            await ctx.send(f'{ctx.author.mention} queue already stopped.')
        else:
            self.bot.queue_status = False
            await ctx.send(f'{ctx.author.mention} queue stopped.')

    @commands.command()
    @check_channel()
    async def add(self, ctx, *args):
        if not self.bot.queue_status:
            await ctx.send(f'{ctx.author.mention} queue is currently disabled.')
            return

        player = ctx.author
        try:
            elo = args[0]
        except IndexError:
            await ctx.send(f'{player.mention} did not provide a valid Elo.')
            return

        if player.id in self.bot.queue:
            await ctx.send(f'{player.mention}, you\'re already in the queue.')
        else:
            self.bot.queue[player.id] = {'name': player.nick, 'elo': elo}
            await ctx.send(f'{player.mention} joined the queue, Elo {elo}.')

    @commands.command()
    @check_channel()
    async def ready(self, ctx):
        if not self.bot.queue_status:
            await ctx.send(f'{ctx.author.mention} queue is currently disabled.')
            return

        player = ctx.author
        if player.id not in self.bot.queue:
            await ctx.send(f'{player.mention}, could not find you in the queue. Use `.add <elo>` and retry')
            return

        data = self.bot.queue[player.id]
        self.bot.ready.append([
            data['name'],
            data['elo'],
        ])

        await ctx.send(f'{player.mention} is ready!')

    @commands.command()
    @check_channel()
    async def queue(self, ctx):
        position = 0
        strings = []
        for k, v in self.bot.queue.items():
            position +=1 
            strings.append(f"`{position:02}. {v['name']} ({v['elo']})`")

        self.bot.logger.debug(strings)
            
        await ctx.send('\n'.join(strings))

    @commands.command()
    @check_channel()
    async def suggest(self, ctx, *args):
        elo_diff = float('inf')
        team_1, team_2 = (None, None)

        players = self.bot.ready

        if args:
            players = SAMPLE_DATA

        for team_a in itertools.combinations(players, 5):
            team_b = [p for p in players if p not in team_a]

            elo_a = sum(p[1] for p in team_a)
            elo_b = sum(p[1] for p in team_b)
            diff = abs(elo_a - elo_b)

            if diff < elo_diff:
                elo_diff = diff
                team_1, team_2, team_1_elo, team_2_elo = (team_a, team_b, elo_a, elo_b)

        #prob_a, prob_b = probability(team_1_elo, team_2_elo, len(team_1))

        message = [
            f'### Team 1',
            ''.join([f'- {p[0]}\n' for p in team_1]),
            f'### Team 2',
            ''.join([f'- {p[0]}\n' for p in team_2]),
        ]

        await ctx.send('\n'.join(message))

async def setup(bot):
    await bot.add_cog(PUG(bot))
