import random
import time
import pytz
import discord
from discord.ext import commands
from datetime import datetime
import os
from dotenv import load_dotenv
import re
import sqlite3

load_dotenv()
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
    ##
    db = sqlite3.connect("C://Users//david//PycharmProjects//NightmareBot//data//users.db")
    c = db.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, level INT, exp INTEGER, rawexp INTEGER, time REAL)')
    db.commit()

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
    num = random.randrange(10)
    if num > 1:
        await ctx.send("<@490176293372166148> nerd")
    else:
        await ctx.send("<@490176293372166148> bu")
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
async def times(ctx):
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
@bot.command()
async def choice(ctx, *args):
    try:
        choices = random.choice(args)
        choices = choices.upper()
        out = discord.Embed(title = choices,color=0xff0000)
        await ctx.send(embed=out)
    except:
        await ctx.send("Invalid Argument")
########################################################################################################################

def threshold(n):
    level_threshold = 5 * (n ** 2) + 50 * n + 100
    return level_threshold


@bot.command(pass_context=True)
async def rank(ctx):
    try:
        _, member = (ctx.message.content).split(' ', 1)
        member = re.sub("[^0-9]", "", member)
    except:
        member = ctx.message.author.id

    db = sqlite3.connect("C://Users//david//PycharmProjects//NightmareBot//data//users.db")
    c = db.cursor()

    c.execute(
        'SELECT user.*, (SELECT count(*) FROM users AS members WHERE members.rawexp > user.rawexp) as Rank FROM users AS user WHERE id = ?',
        (ctx.message.author.id,))

    user = c.fetchone()
    db.close()

    rank = str(user[6] + 1)

    out = discord.Embed(title='{}\'s Information'.format(ctx.message.author.name), color=0xff0000)
    out.set_thumbnail(url=ctx.message.author.avatar_url)
    out.add_field(name='Rank', value='#' + rank)
    out.add_field(name='Level', value=user[2])
    out.add_field(name='EXP', value='{}/{}'.format(user[3], threshold(user[2])))
    out.add_field(name='Total EXP', value=user[4])
    await ctx.send(embed=out)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.bot:
        return

    if message.content.startswith('l>'):
        await bot.process_commands(message)
        return

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

    db = sqlite3.connect("C://Users//david//PycharmProjects//NightmareBot//data//users.db")
    c = db.cursor()

    c.execute('SELECT * FROM users WHERE id= ?', (message.author.id,))
    user = c.fetchone()

    if user is None:
        c.execute('INSERT INTO users(id, name, level, exp, rawexp, time) VALUES(?,?,?,?,?,?)',
                  (message.author.id, message.author.name, 1, 0, 0, time.time()))
        db.commit()
        db.close()
        return

    if message.author.name != user[1]:
        c.execute('UPDATE users SET name = ? WHERE id= ?', (message.author.name, message.author.id))

    if (time.time() - user[5]) > 60:
        addedexp = random.randint(10, 25)
        exp = user[3] + addedexp
        rawexp = user[4] + addedexp
        c.execute('UPDATE users SET exp = ?, rawexp = ?, name = ?, time = ? WHERE id= ?',
                  (exp, rawexp, message.author.name, time.time(), message.author.id))

        if (exp > threshold(user[2])):
            level = user[2] + 1
            c.execute('UPDATE users SET exp = ?, level = ? WHERE id= ?', (0, level, message.author.id))
            await message.channel.send(f"{message.author.mention} Pog! You leveled up! You're now level {level}")
            #** {} **.'.format(level)
    db.commit()
    db.close()

    await bot.process_commands(message)

########################################################################################################################
@bot.command()
async def help(ctx):

    out = discord.Embed(title = "Commands:", color = 0xff0000)
    out.add_field(name = "!roll", value = "Rolls a random number between 1 and 100.", inline= False)
    out.add_field(name = "!order arg1 arg2 ...", value = "Puts the given arguments in a random order.", inline= False)
    out.add_field(name = "!replay", value = "Sends the last deleted message.", inline = False)
    out.add_field(name = "!unedit", value = "Displays the last edited message as before it was edited.", inline = False)
    out.add_field(name = "!poll question: choice1 choice2...", value = "Posts a poll with given choices.", inline = False)
    out.add_field(name = "!times", value = "Displays the current time in different timezones.", inline = False)
    out.add_field(name = "!choice option1 option2 ...", value = "Randomly chooses one of the given options.", inline = False)
    out.add_field(name = "!rank", value="Checks your rank in the server", inline=False)
    await ctx.send(embed = out)




if __name__ == "__main__":
    bot.run(TOKEN)