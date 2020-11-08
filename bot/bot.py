import random
import time
import pytz
import discord
from discord.ext import commands
from datetime import datetime
import os
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command('help')
lastdel = {}
lastedit = {}
lastmsg = {}
TOKEN = os.getenv("DISCORD_TOKEN")
########################################################################################################################
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")
    print("list of visible members:")
    for member in bot.get_all_members():
        print(member)
    await bot.change_presence(activity=discord.Game(name='Overwatch'))
########################################################################################################################

@bot.event
async def on_message_delete(message):
    lastdel[message.channel] = message

@bot.command()
async def replay(ctx):
    deleted = lastdel[ctx.channel]
    out = discord.Embed(timestamp = deleted.created_at, description = lastdel[ctx.channel].content, color = 0xff0000)
    out.set_author(icon_url = deleted.author.avatar_url, name=deleted.author.name)
    await ctx.send(embed = out)


@bot.event
async def on_message_edit(before,after):
    lastedit[before.channel] = before

@bot.command()
async def unedit(ctx):
    edited = lastedit[ctx.channel]
    out = discord.Embed(timestamp = edited.created_at, description = edited.content,color = 0xff0000 )
    out.set_author(icon_url = edited.author.avatar_url, name=edited.author.name)
    await ctx.send(embed = out)
########################################################################################################################

@bot.command()
async def ping(ctx):
    ping = "<@429160568973426691>"
    await ctx.send(ping)


@bot.command()
async def night(ctx, count=None):
    try:
        ping = "<@429160568973426691>"
        if(count is None or count == 1):
            await ctx.send(ping)
        elif(int(count) <= 10):
            for x in range(1,int(count)+1):
                await ctx.send(ping)
                time.sleep(10)
        else:
            raise ValueError
    except ValueError:
        await ctx.send(f"The argument has to be an integer with max value 10{'.' if random.randrange(10) < 5 else ', idiot.'}")
########################################################################################################################

@bot.command()
async def ching(ctx):
    await ctx.send("<@490176293372166148> nerd")

@bot.command()
async def jess(ctx):
    await ctx.send("<@341981835124801547> idiot")
########################################################################################################################

@bot.command()
async def roll(ctx):
    await ctx.send(f"{ctx.message.author.mention} rolled {random.randrange(1,101)}!")


@bot.command()
async def order(ctx, *args):
    out = ""
    if args:
        arglist = list(args)
        random.shuffle(arglist)
        for place, name in enumerate(arglist,1):
            out += f"{place}. {name}\n"
        await ctx.send(out)
    else:
        await ctx.send("You need to provide at least 1 argument.")
########################################################################################################################

@bot.command()
async def time(ctx):
    #now = datetime.now()
    #current_time = now.strftime("%H:%M:%S")
    #await ctx.send(current_time)
    out = discord.Embed(title="Current Time:", color = 0xff0000)

    tz_Los_Angel = pytz.timezone('America/Los_Angeles')
    datetime_LA = datetime.now(tz_Los_Angel)
    la_time = datetime_LA.strftime("%H:%M:%S")
    out.add_field(name="Los Angeles Time: ", value=la_time, inline=False)

    tz_NY = pytz.timezone('America/New_York')
    datetime_NY = datetime.now(tz_NY)
    ny_time = datetime_NY.strftime("%H:%M:%S")
    out.add_field(name = "New York Time: ", value = ny_time, inline = False)

    tz_London = pytz.timezone('Europe/London')
    datetime_London = datetime.now(tz_London)
    ldn_time = datetime_London.strftime("%H:%M:%S")
    out.add_field(name = "London Time: ", value = ldn_time, inline = False)

    tz_Hong_Kong = pytz.timezone('Asia/Hong_Kong')
    datetime_HK = datetime.now(tz_Hong_Kong)
    hk_time = datetime_HK.strftime("%H:%M:%S")
    out.add_field(name = "Hong Kong Time: ", value = hk_time, inline = False)

    #out.add_field(name = current_time, value = ".", inline = True)
    await ctx.send(embed = out)
########################################################################################################################
emojis = [f"{num}\u20e3" for num in range(1, 10)]

@bot.command()
async def poll(ctx, *args):
    try:
        if not args:
            raise ValueError("You haven't given any arguments idiot!")
        question_words = []
        options = []
        reached = False
        for arg in args:
            if arg[-1] == ':' and not reached:
                question_words.append(arg[:-1])
                reached = True
            elif reached:
                options.append(arg)
            else:
                question_words.append(arg)
        if len(options) > len(emojis):
            raise ValueError(f"You can only have up to {len(emojis)} options!")
        if not len(options):
            raise ValueError("You haven't given any options (every argument after a word ending with : is an option.)")
        question = ' '.join(question_words)
        pairs = [f'{emojis[emoji]}: {option}' for emoji, option in enumerate(options)]
        out = discord.Embed(title=question, description='\n'.join(pairs), color = 0xff0000)
        poll = await ctx.send(embed=out)
        for i in range(len(options)):
            await poll.add_reaction(emojis[i])
    except ValueError as ve:
        await ctx.send(ve)
#######################################################################################################################



@bot.command(pass_context=True)
async def dva(ctx):
    f = open("dva.txt", "r")
    dva_images = f.read().splitlines()
    image = random.choice(dva_images)
    out = discord.Embed(color = 0xff0000)
    out.set_image(url=image)
    await ctx.send(embed = out)

    
########################################################################################################################

x = open("pokemon.txt", "r")
pokemon = x.read().splitlines()
@bot.command()
async def team(ctx):
    out = discord.Embed(color = 0xff0000)
    teams = random.sample(pokemon, k=6)
    lst = [x.capitalize() for x in teams]
    out.add_field(name=f"{ctx.message.author.name}'s Pokemon:", value=f"{(' ' + chr(10)).join(lst)}")
    await ctx.send(embed=out)

########################################################################################################################
@bot.event
async def on_message(message):
    f = open("bad_words.txt", "r")
    bad_words = f.read().splitlines()
    for bad_word in bad_words:
        if bad_word in message.content:
            await message.delete()
            await message.author.send("No bad words please.")
    emotes = ['🧀', '😂']
    for emote in emotes:
        if emote in message.content:
            await message.delete()
            await message.author.send("No bad emotes please.")
    await bot.process_commands(message)



########################################################################################################################




@bot.command()
async def help(ctx):
    out = discord.Embed(title = "Commands:", color = 0xff0000)
    out.add_field(name = "!roll", value = "Rolls a random number between 1 and 100.", inline= False)
    out.add_field(name = "!order arg1 arg2 ...", value = "Puts the given arguments in a random order.", inline= False)
    out.add_field(name = "!replay", value = "Sends the last deleted message.", inline = False)
    out.add_field(name = "!unedit", value = "Displays the last edited message as before it was edited.", inline = False)
    out.add_field(name = "!poll", value = "Posts a poll with passed options. !poll question: arg1 arg2", inline = False)
    out.add_field(name = "!time", value = "Displays the current time in different timezones.", inline = False)
    await ctx.send(embed = out)




if __name__ == "__main__":
    bot.run(TOKEN)