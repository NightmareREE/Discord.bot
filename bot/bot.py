import random
import time
import discord
from discord.ext import commands
from discord import User
from datetime import datetime
import os
import re
import pytz
import psycopg2
import matplotlib.pyplot as plt
import requests
from json import loads



bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())
bot.remove_command('help')
lastdel = {}
lastedit = {}
lastmsg = {}
TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_URL = os.environ['DATABASE_URL']
db = psycopg2.connect(DATABASE_URL, sslmode='require')
c = db.cursor()


bot.lava_nodes = [
    {
        'host': 'lava.link',
        'port': 80,
        'rest_uri': f'http://lava.link:80',
        'identifier': 'MAIN',
        'password': 'anything',
        'region': 'singapore'
    }
]

bot.load_extension('dismusic')
bot.load_extension('dch')
#######################################################################################################################
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
    create_table_query = 'CREATE TABLE IF NOT EXISTS bets(id bigint, name TEXT, bet INTEGER, result TEXT)'
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

    c.execute('SELECT * FROM users WHERE id=%s', (ctx.message.author.id,))
    user = c.fetchone()

    # c.execute('SELECT 1 + count(*) AS rank FROM users WHERE rawexp > (SELECT rawexp FROM users WHERE id=%s)', (ctx.message.author.id,))
    c.execute('SELECT 1 + count(*) AS rank FROM users WHERE points > (SELECT points FROM users WHERE id=%s)',
              (ctx.message.author.id,))
    rank = c.fetchone()
    out = discord.Embed(title='{}\'s Information'.format(ctx.message.author.name), color=0xff0000)
    out.set_thumbnail(url=ctx.message.author.avatar_url)
    out.add_field(name='Rank', value='#' + str(rank[0]))
    # out.add_field(name='Level', value=user[2])
    # out.add_field(name='EXP', value='{}/{}'.format(user[3], threshold(user[2])))
    # out.add_field(name='Total EXP', value=user[4])
    out.add_field(name='Points', value=user[6])
    await ctx.send(embed=out)


########################################################################################################################
@bot.command(pass_context=True)
async def leaderboard(ctx):
    c.execute('SELECT 1 + count(*) FROM users WHERE points > (SELECT points FROM users WHERE id=%s)',
              (ctx.message.author.id,))
    rank = c.fetchone()
    c.execute('SELECT name, points FROM users ORDER BY points DESC LIMIT 5')
    users = c.fetchall()
    out = discord.Embed(title='Points Leaderboard', color=0xff0000)
    for user in users:
        out.add_field(name=user[0], value=user[1], inline=False)
    out.set_footer(text="Your Rank is #" + str(rank[0]))
    await ctx.send(embed=out)


########################################################################################################################
@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    c.execute('SELECT points FROM users WHERE id=%s', (ctx.message.author.id,))
    user = c.fetchone()
    oldpoints = user[0]
    newpoints = oldpoints + 1000
    c.execute('UPDATE users SET points=%s WHERE id=%s', (newpoints, ctx.message.author.id))
    await ctx.send(
        f"{ctx.message.author.mention} redeemed the daily bonus and won 1000 and now has {newpoints} points <:EZ:788447395805265990>")


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
        c.execute("UPDATE users SET name = %s WHERE id= %s", (message.author.name, message.author.id))

    if (time.time() - user[5]) > 60:
        addedexp = random.randint(10, 25)
        exp = user[3] + addedexp
        rawexp = user[4] + addedexp
        points = user[6] + addedexp
        c.execute("UPDATE users SET exp=%s, rawexp=%s, name=%s, time=%s, points=%s WHERE id=%s",
                  (exp, rawexp, message.author.name, time.time(), points, message.author.id))

        if (exp > threshold(user[2])):
            level = user[2] + 1
            c.execute("UPDATE users SET exp=%s, level=%s WHERE id=%s", (0, level, message.author.id))
            # await message.channel.send(f"{message.author.mention} Pog! You leveled up! You're now level {level}")
            # ** {} **.'.format(level)
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
async def roulette(ctx, bet):
    try:
        c.execute('SELECT * FROM users WHERE id=%s', (ctx.message.author.id,))
        user = c.fetchone()
        oldpoints = user[6]
        num = random.choice([0, 1])
        ch = '%'
    
        if (bet == "all"):
            if (oldpoints == 0):
                out = discord.Embed(title="You cant bet 0 idiot!", color=0xff0000)
                await ctx.send(embed=out)
            elif (num == 0):
                c.execute('UPDATE users SET points=%s WHERE id=%s', (0, ctx.message.author.id))
                c.execute('INSERT INTO bets(id, name, bet, result) VALUES (%s, %s, %s, %s)',(ctx.message.author.id, ctx.message.author.name, int(oldpoints), "lost",))
                await ctx.send(
                    f"{ctx.message.author.mention} Lost {oldpoints} and now has 0 points <:NotLikeThis:791431758024802336>")
            elif (num == 1):
                newpoints = oldpoints * 2
                c.execute('UPDATE users SET points=%s WHERE id=%s', (newpoints, ctx.message.author.id))
                c.execute('SELECT * FROM users WHERE id=%s', (ctx.message.author.id,))
                user1 = c.fetchone()
                c.execute('INSERT INTO bets(id, name, bet, result) VALUES (%s, %s, %s, %s)',(ctx.message.author.id, ctx.message.author.name, int(oldpoints), "won",))
                await ctx.send(
                    f"{ctx.message.author.mention} Won {oldpoints} and now has {user1[6]} points! <:EZ:788447395805265990>")
        elif ch in bet:
            s = bet.replace("%", "")
            if int(s) <= 100 and int(s) > 0:
                s1 = int(s) * 0.01
                points = oldpoints * s1
                if int(points) <= 0:
                    await ctx.send("Wrong command")
                elif (num == 0):
                    newpoints = oldpoints - int(points)
                    c.execute('UPDATE users SET points=%s WHERE id=%s', (newpoints, ctx.message.author.id))
                    c.execute('INSERT INTO bets(id, name, bet, result) VALUES (%s, %s, %s, %s)',
                              (ctx.message.author.id, ctx.message.author.name, points, "lost",))
                    await ctx.send(
                        f"{ctx.message.author.mention} Lost {int(points)} and now has {newpoints} points <:NotLikeThis:791431758024802336>")
                elif (num == 1):
                    newpoints = oldpoints + int(points)
                    c.execute('UPDATE users SET points=%s WHERE id=%s', (newpoints, ctx.message.author.id))
                    c.execute('INSERT INTO bets(id, name, bet, result) VALUES (%s, %s, %s, %s)',
                              (ctx.message.author.id, ctx.message.author.name, points, "won",))
                    c.execute('SELECT * FROM users WHERE id=%s', (ctx.message.author.id,))
                    user1 = c.fetchone()
                    await ctx.send(
                        f"{ctx.message.author.mention} Won {int(points)} and now has {user1[6]} points! <:EZ:788447395805265990>")
                else:
                    await ctx.send(f"{ctx.message.author.mention} you cant bet higher than 100%")
        elif (int(bet) == 0):
            out = discord.Embed(title="You cant bet 0 idiot!", color=0xff0000)
            await ctx.send(embed=out)
        elif (int(bet) <= oldpoints):
            if (num == 0):
                newpoints = oldpoints - int(bet)
                c.execute('UPDATE users SET points=%s WHERE id=%s', (newpoints, ctx.message.author.id))
                c.execute('INSERT INTO bets(id, name, bet, result) VALUES (%s, %s, %s, %s)',(ctx.message.author.id, ctx.message.author.name, bet, "lost",))
                await ctx.send(
                    f"{ctx.message.author.mention} Lost {bet} and now has {newpoints} points <:NotLikeThis:791431758024802336>")
            elif (num == 1):
                newpoints = oldpoints + int(bet)
                c.execute('UPDATE users SET points=%s WHERE id=%s', (newpoints, ctx.message.author.id))
                c.execute('INSERT INTO bets(id, name, bet, result) VALUES (%s, %s, %s, %s)',(ctx.message.author.id, ctx.message.author.name, bet, "won",))
                c.execute('SELECT * FROM users WHERE id=%s', (ctx.message.author.id,))
                user1 = c.fetchone()
                await ctx.send(
                    f"{ctx.message.author.mention} Won {bet} and now has {user1[6]} points! <:EZ:788447395805265990>")
        else:
            out = discord.Embed(title="You betted more points than you own", color=0xff0000)
            await ctx.send(embed=out)
    except:
        await ctx.send("Wrong command")


@bot.command()
async def stats(ctx):
    c.execute('SELECT count(*) FROM bets WHERE id=%s', (ctx.message.author.id,))
    user = c.fetchone()
    totalbets = user[0]
    c.execute('SELECT count(*) FROM bets WHERE id=%s AND result = %s', (ctx.message.author.id,"won",))
    user = c.fetchone()
    totalwins = user[0]
    c.execute('SELECT count(*) FROM bets WHERE id=%s AND result = %s', (ctx.message.author.id,"lost",))
    user = c.fetchone()
    totalloss = user[0]
    c.execute('SELECT SUM(bet) FROM bets WHERE id=%s AND result = %s', (ctx.message.author.id,"won",))
    user = c.fetchone()
    wonpoints = user[0]
    c.execute('SELECT SUM(bet) FROM bets WHERE id=%s AND result = %s', (ctx.message.author.id,"lost",))
    user = c.fetchone()
    lostpoints = user[0]
    
    
    if wonpoints is None:
        wonpoints = 0
    if lostpoints is None:
        lostpoints = 0
    
    profit = wonpoints - lostpoints

    out = discord.Embed(title=f"{ctx.message.author.name}'s Wins and Losses", color=0xff0000)
    out.add_field(name="Total amount of bets: ", value=totalbets, inline=False)
    out.add_field(name="# of Won bets: ", value=totalwins, inline=False)
    out.add_field(name="# of Lost bets: ", value=totalloss, inline=False)
    out.add_field(name="Total Lost Points: ", value=lostpoints, inline=False)
    out.add_field(name="Total Won Points: ", value=wonpoints, inline=False)
    out.add_field(name="Profit: ", value=profit, inline=False)



    my_data = [totalwins, totalloss]
    my_labels = 'wins', 'losses'
    plt.pie(my_data, labels=my_labels, autopct='%1.1f%%')
    plt.title(f"{ctx.message.author.name}'s Win Loss Ratio")
    plt.axis('equal')
    plt.savefig("image1.png")
    image = discord.File("image1.png")
    plt.close()
    await ctx.send(embed=out)
    await ctx.send(file=image)

        
        
@bot.command()
async def reset(ctx, user: User):
    try:
        if(ctx.message.author.id == 429160568973426691):
            c.execute('UPDATE users SET points=1000 WHERE id=%s', (user.id,))
            await ctx.send(f"{user.mention} has been reset to 1000 points")
        else:
            await ctx.send("You cannot use this command")
    except:
        await ctx.send("Wrong Command Idiot")
@bot.command()
async def resetall(ctx):
    try:
        if(ctx.message.author.id == 429160568973426691):
            c.execute('UPDATE users SET points=1000')
            await ctx.send("all users have been reset to 1000 points")
        else:
            await ctx.send("You cannot use this command")
    except:
        await ctx.send("Wrong Command Idiot")
########################################################################################################################
@bot.command()
async def give(ctx, arg: User, money):
    try:
        if (int(money) > 0):
            giver = ctx.message.author.id
            taker = arg.id
            if(giver != taker):
                c.execute('SELECT * FROM users WHERE id=%s', (ctx.message.author.id,))
                user = c.fetchone()
                oldpoints = user[6]
                if(oldpoints < int(money)):
                    await ctx.send(f"{ctx.message.author.mention} You dont have enough money you broke ass")
                else:
                    c.execute('UPDATE users SET points= points - %s WHERE id=%s', (money, giver))
                    c.execute('UPDATE users SET points= points + %s WHERE id=%s', (money, taker))
                    await ctx.send(f"{ctx.message.author.mention} Gave {arg.mention} {money} Points!")
            else:
                await ctx.send(f"{ctx.message.author.mention} Why do you want to give yourself money?")
        else:
            await ctx.send("Nice try")
    except:
        await ctx.send(f"{ctx.message.author.mention} Wrong command idiot")

########################################################################################################################
@bot.command()
async def twitch(ctx, arg):

    API_ENDPOINT = f"https://api.twitch.tv/helix/search/channels?query={arg}&first=1"

    Client_ID = "3td506yd0tekl9mgihf3xo3e629yg3"

    head = {
    "Authorization" : "Bearer vcxir5at5bmqeq5r5dfwig2mcy5tdx",
    "Client-ID" : Client_ID
    }

    r = requests.get(url = API_ENDPOINT, headers = head)

    print(r.text)
    id = loads(r.text)['data'][0]['id']
    profilepic= loads(r.text)['data'][0]['thumbnail_url']
    name = loads(r.text)['data'][0]['display_name']
    title = loads(r.text)['data'][0]['title']
    status = loads(r.text)['data'][0]['is_live']
    started = loads(r.text)['data'][0]['started_at']
    game = loads(r.text)['data'][0]['game_name']
    #2021-06-03T15:02:18Z
    #date_time_obj = datetime.strptime(started, '%Y-%m-%d %H:%M:%S')
    #diff = datetime.now() - date_time_obj

    API_ENDPOINT=f"https://api.twitch.tv/helix/users/follows?to_id={id}"
    r = requests.get(url = API_ENDPOINT, headers = head)
    total = loads(r.text)['total']

    embed = discord.Embed(title=name, url=f"https://www.twitch.tv/{name}", color=0x8120cf)
    if status == True:
        embed.set_footer(text="They are Live!")
        embed.add_field(name=f"Currently Playing {game}", value='\u200b', inline=False)
        embed.add_field(name=title, value='\u200b', inline=False)
        #embed.add_field(name="Live for ", value=diff, inline=False)


    else:
        embed.set_footer(text="They are not Live")

    embed.set_thumbnail(url=profilepic)
    embed.add_field(name="Amount of Followers: ", value=total, inline=False)
    await ctx.send(embed=embed)

########################################################################################################################



if __name__ == "__main__":
    bot.run(TOKEN)
