import random
import time
import discord
from discord.ext import commands
from datetime import datetime
import os
import re
import pytz
import psycopg2

bot = commands.Bot(command_prefix="s!", intents=discord.Intents.all())
bot.remove_command('help')
lastdel = {}
lastedit = {}
lastmsg = {}
TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_URL = os.environ['DATABASE_URL']
db = psycopg2.connect(DATABASE_URL, sslmode='require')
c = db.cursor()

########################################################################################################################
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")
    print("list of visible members:")
    for member in bot.get_all_members():
        print(member)
    await bot.change_presence(activity=discord.Game(name='Overwatch'))
    ##
    create_table_query = 'CREATE TABLE IF NOT EXISTS users(id bigint PRIMARY KEY, name TEXT, level INT, exp INTEGER, rawexp INTEGER, time REAL, points INTEGER)'
    c.execute(create_table_query)
    db.commit()

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


    c.execute(
        "SELECT user.*, (SELECT count(*) FROM users AS members WHERE members.rawexp > user.rawexp) as Rank FROM users AS user WHERE id=%s", (ctx.message.author.id,))

    user = c.fetchone()

    rank = str(user[6] + 1)

    out = discord.Embed(title='{}\'s Information'.format(ctx.message.author.name), color=0xff0000)
    out.set_thumbnail(url=ctx.message.author.avatar_url)
    out.add_field(name='Rank', value='#' + rank)
    out.add_field(name='Level', value=user[2])
    out.add_field(name='EXP', value='{}/{}'.format(user[3], threshold(user[2])))
    out.add_field(name='Total EXP', value=user[4])
    await ctx.send(embed=out)

########################################################################################################################
@bot.event
async def on_message_delete(message):
    lastdel[message.channel] = message


@bot.command()
async def replay(ctx):
    deleted = lastdel[ctx.channel]
    out = discord.Embed(timestamp=deleted.created_at, description=lastdel[ctx.channel].content, color=0xff0000)
    out.set_author(icon_url=deleted.author.avatar_url, name=deleted.author.name)
    await ctx.send(embed=out)


@bot.event
async def on_message_edit(before, after):
    lastedit[before.channel] = before


@bot.command()
async def unedit(ctx):
    edited = lastedit[ctx.channel]
    out = discord.Embed(timestamp=edited.created_at, description=edited.content, color=0xff0000)
    out.set_author(icon_url=edited.author.avatar_url, name=edited.author.name)
    await ctx.send(embed=out)


########################################################################################################################

@bot.command()
async def ping(ctx):
    ping = "<@429160568973426691>"
    await ctx.send(ping)


@bot.command()
async def night(ctx, count=None):
    try:
        ping = "<@429160568973426691>"
        if (count is None or count == 1):
            await ctx.send(ping)
        elif (int(count) <= 10):
            for x in range(1, int(count) + 1):
                await ctx.send(ping)
                time.sleep(10)
        else:
            raise ValueError
    except ValueError:
        await ctx.send(
            f"The argument has to be an integer with max value 10{'.' if random.randrange(10) < 5 else ', idiot.'}")


########################################################################################################################

@bot.command()
async def ching(ctx):
    num = random.randrange(10)
    if num > 2:
        await ctx.send("<@490176293372166148> nerd")
    else:
        await ctx.send("<@490176293372166148> bu")




########################################################################################################################

@bot.command()
async def roll(ctx):
    await ctx.send(f"{ctx.message.author.mention} rolled {random.randrange(1, 101)}!")


@bot.command()
async def order(ctx, *args):
    out = ""
    if args:
        arglist = list(args)
        random.shuffle(arglist)
        for place, name in enumerate(arglist, 1):
            out += f"{place}. {name}\n"
        await ctx.send(out)
    else:
        await ctx.send("You need to provide at least 1 argument.")


########################################################################################################################
@bot.command()
async def highlow(ctx):
    num = random.randrange(1, 101)
    embed = discord.Embed(title="The Number I rolled is " + str(num), color=0xff0000)
    embed.add_field(name="Will the next number be higher or lower?", value="Type 's!higher' or 's!lower'")
    await ctx.send(embed=embed)

    @bot.command()
    async def higher(ctx):
        guess = random.randrange(1, 101)
        out = discord.Embed(title="The number rolled is " + str(guess), color=0xff0000)
        if (guess > num):
            out.add_field(name="You guessed correctly! <:EZ:788447395805265990>", value='\u200b', inline=True)
        elif (guess < num):
            out.add_field(name="You guessed wrong...Unlucky <:NotLikeThis:791431758024802336>", value='\u200b',
                          inline=True)
        elif (guess == num):
            out.add_field(name="We rolled the same number!", value='\u200b')
        await ctx.send(embed=out)


    @bot.command()
    async def lower(ctx):
        guess = random.randrange(1, 101)
        out = discord.Embed(title="The number rolled is " + str(guess), color=0xff0000)
        if (guess < num):
            out.add_field(name="You guessed correctly! <:EZ:788447395805265990>", value='\u200b', inline=True)
        elif (guess > num):
            out.add_field(name="You guessed wrong...Unlucky <:NotLikeThis:791431758024802336>", value='\u200b',
                          inline=True)
        elif (guess == num):
            out.add_field(name="We rolled the same number! Pog!", value='\u200b', inLine=True)
        await ctx.send(embed=out)


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
        out = discord.Embed(title=question, description='\n'.join(pairs), color=0xff0000)
        poll = await ctx.send(embed=out)
        for i in range(len(options)):
            await poll.add_reaction(emojis[i])
    except ValueError as ve:
        await ctx.send(ve)


#######################################################################################################################
@bot.command()
async def divs(ctx, *args):
    try:
        if not args:
            raise ValueError("You haven't given any names idiot!")
        names = []
        for arg in args:
            names.append(arg)
        random.shuffle(names)
        div1 = []
        div2 = []
        div1 = names[:len(names) // 2]
        div2 = names[len(names) // 2:]
        out = discord.Embed()
        out.add_field(name="Division 1", value=f"{(', ' + chr(10)).join(div1)}")
        out.add_field(name="Division 2", value=f"{(', ' + chr(10)).join(div2)}")
        await ctx.send(embed=out)
    except:
        await ctx.send("Invalid Argument")


########################################################################################################################
@bot.command(pass_context=True)
async def donowall(ctx):
    image = 'https://media1.tenor.com/images/90421f6bc6e6aa99f33da41afde90925/tenor.gif'
    out = discord.Embed(color=0xff0000)
    out.set_image(url=image)
    await ctx.send(embed=out)


########################################################################################################################
@bot.command()
async def choose(ctx, *args):
    try:
        choices = random.choice(args)
        choices = choices.upper()
        out = discord.Embed(title=choices, color=0xff0000)
        await ctx.send(embed=out)
    except:
        await ctx.send("Invalid Argument")


########################################################################################################################


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.bot:
        return

    if message.content.startswith('l>'):
        await bot.process_commands(message)
        return

    bad_words = [
        "nigga",
        "nigger",
        "faggot"]
    for bad_word in bad_words:
        if bad_word in message.content:
            await message.delete()
            await message.author.send("No bad words please.")
    c.execute('SELECT * FROM users WHERE id= %d' % message.author.id)
    user = c.fetchone()

    if user is None:
        SQL = "INSERT INTO users(id, name, level, exp, rawexp, time, points) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        data = (message.author.id, message.author.name, 1, 0, 0, time.time(), 0,)
        c.execute(SQL, data)
        db.commit()
        return

    if message.author.name != user[1]:
        c.execute('UPDATE users SET name = %s WHERE id= %d'% message.author.name, message.author.id)

    if (time.time() - user[5]) > 60:
        addedexp = random.randint(10, 25)
        exp = user[3] + addedexp
        rawexp = user[4] + addedexp
        c.execute("UPDATE users SET exp=%s, rawexp=%s, name=%s, time=%s WHERE id=%s", (exp, rawexp, message.author.name, time.time(), message.author.id))


        if (exp > threshold(user[2])):
            level = user[2] + 1
            c.execute("UPDATE users SET exp=%s, level=%s WHERE id=%s", (0, level, message.author.id))
            await message.channel.send(f"{message.author.mention} Pog! You leveled up! You're now level {level}")
            #** {} **.'.format(level)
    db.commit()

    await bot.process_commands(message)


########################################################################################################################
@bot.command()
async def times(ctx):
    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # await ctx.send(current_time)
    out = discord.Embed(title="Current Time:", color=0xff0000)

    tz_Los_Angel = pytz.timezone('America/Los_Angeles')
    datetime_LA = datetime.now(tz_Los_Angel)
    la_time = datetime_LA.strftime("%H:%M:%S")
    out.add_field(name="Los Angeles Time: ", value=la_time, inline=False)

    tz_NY = pytz.timezone('America/New_York')
    datetime_NY = datetime.now(tz_NY)
    ny_time = datetime_NY.strftime("%H:%M:%S")
    out.add_field(name="New York Time: ", value=ny_time, inline=False)

    tz_London = pytz.timezone('Europe/London')
    datetime_London = datetime.now(tz_London)
    ldn_time = datetime_London.strftime("%H:%M:%S")
    out.add_field(name="London Time: ", value=ldn_time, inline=False)

    tz_Hong_Kong = pytz.timezone('Asia/Hong_Kong')
    datetime_HK = datetime.now(tz_Hong_Kong)
    hk_time = datetime_HK.strftime("%H:%M:%S")
    out.add_field(name="Hong Kong Time: ", value=hk_time, inline=False)

    # out.add_field(name = current_time, value = ".", inline = True)
    await ctx.send(embed=out)


########################################################################################################################
@bot.command()
async def help(ctx):
    out = discord.Embed(title="Commands:", color=0xff0000)
    out.add_field(name="s!roll", value="Rolls a random number between 1 and 100.", inline=False)
    out.add_field(name="s!order arg1 arg2 ...", value="Puts the given arguments in a random order.", inline=False)
    out.add_field(name="s!replay", value="Sends the last deleted message.", inline=False)
    out.add_field(name="s!unedit", value="Displays the last edited message as before it was edited.", inline=False)
    out.add_field(name="s!poll question: choice1 choice2...", value="Posts a poll with given choices.", inline=False)
    out.add_field(name="s!choose option1 option2 ...", value="Randomly chooses one of the given options.", inline=False)
    out.add_field(name="s!highlow", value="Play a game of higher or lower.", inline=False)
    out.add_field(name="s!times", value="Gives current time in multiple timezones.", inline=False)
    await ctx.send(embed=out)


if __name__ == "__main__":
    bot.run(TOKEN)
