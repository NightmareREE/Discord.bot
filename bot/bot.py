import random
import time
import discord
from discord.ext import commands
from datetime import datetime
import os
import re


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
        length = names.count()
        half = length / 2
        for x in range(0,half):
            div1 = div1.append(names[x])
        for y in range(half,length):
            div2 = div2.append(names[y])
    except:
        await ctx.send("Invalid Argument")
########################################################################################################################
@bot.command(pass_context=True)          
async def dva(ctx):                                
    dva_images = [ 
"https://pbs.twimg.com/media/EmO79IeUYAAXqwf?format=jpg&name=large",
"https://i.imgur.com/wByUmlJ.jpg",
"https://i.imgur.com/7uJEvOh.jpg",
"https://i.imgur.com/Ql28ayO.jpg",
"https://i.imgur.com/UOSlAi4.jpg",
"https://i.imgur.com/LqiicDV.jpg",
"https://i.imgur.com/Bt8AKUC.jpg",
"https://i.imgur.com/9iBnnnv.jpg",
"https://i.imgur.com/VhPUemL.jpg",
"https://i.imgur.com/rPIYbHl.jpg",
"https://i.imgur.com/eJxhZy8.jpg",
"https://i.pinimg.com/originals/6d/cf/1b/6dcf1b21a9ba92982cade1e660b610d0.gif",
"https://media2.giphy.com/media/YknaabgtG0nCOlfpEI/giphy.gif?cid=ecf05e47nhmt45cqd2hns4dt6xyiu5cdyeu0pfs2goguygbz&rid=giphy.gif",
"https://media2.giphy.com/media/26gJAq9QKcrbxQoV2/giphy.gif?cid=ecf05e478vun5imnqamkcq2sphrm9a7yt5tsxj7rwyr14zsc&rid=giphy.gif",
"https://64.media.tumblr.com/e1151d39ab20fb6b2c91a4820d668e20/tumblr_pdv2rbXDTo1w9q1uyo2_500.gif",
"https://64.media.tumblr.com/e23339a77c1da2a986ed59a72235db0c/tumblr_pdv2rbXDTo1w9q1uyo4_1280.gif",
"https://images-ext-2.discordapp.net/external/86dE7B2sc39XHTW7vl9VOnVSkdUwMFjq9-HFW_sNCq0/https/danbooru.donmai.us/data/sample/__d_va_and_cruiser_d_va_overwatch_drawn_by_byam__sample-ffe621a063161dc9dabb5fe50c5e0214.jpg",
"https://images-ext-2.discordapp.net/external/YQ9qNOp6QFuT-lJXdbVgfaXOg4UVP7c09ZVNkoSGMJ4/https/danbooru.donmai.us/data/sample/__d_va_overwatch_drawn_by_maro_lij512__sample-73ae24572a4b1e0e7cb0382ca766e28c.jpg",
"https://images-ext-1.discordapp.net/external/uQVJSfZjhlSqAdFJhYZ5yuyfZsYMYA-Hc1Yj_18017M/https/danbooru.donmai.us/data/sample/__d_va_overwatch_drawn_by_maro_lij512__sample-73cbe796f073d761658f0a2ab4dddb41.jpg",
"https://images-ext-2.discordapp.net/external/vyZR1eNHJkbsZ0mJyaY2nNSka2RIlk8qmxmkmQEdAV4/https/danbooru.donmai.us/data/sample/__d_va_overwatch_drawn_by_16nfeiyu__sample-294badd6af298e5e8c9147207df72ae0.jpg",
"https://images-ext-1.discordapp.net/external/nrsfjEbMpSsW9lbToxHZNOOJKIju-L8d_lkmvYH5HZ0/https/danbooru.donmai.us/data/sample/__d_va_and_academy_d_va_overwatch_drawn_by_eito_nishikawa__sample-50f21a7342974b7e2e6fe414e681ba1c.jpg",
"https://images-ext-1.discordapp.net/external/BENNcDCidthrMe8PMyfoFAWc8dSrhYtlf9QhD_wQ-QU/https/cdn.donmai.us/sample/b4/84/__d_va_overwatch_drawn_by_ku_luo_mofa_shi__sample-b4849ec8088b46ba462bae9423bd0685.jpg",
"https://i.imgur.com/yTXLObH.jpg" ]
    image = random.choice(dva_images)    
    out = discord.Embed(color = 0xff0000)
    out.set_image(url=image)             
    await ctx.send(embed = out)          
########################################################################################################################
@bot.command()
async def choose(ctx, *args):
    try:
        choices = random.choice(args)
        choices = choices.upper()
        out = discord.Embed(title = choices,color=0xff0000)
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
        "faggot" ]
    for bad_word in bad_words:
        if bad_word in message.content:
            await message.delete()
            await message.author.send("No bad words please.")
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
    out.add_field(name = "!choose option1 option2 ...", value = "Randomly chooses one of the given options.", inline = False)
    await ctx.send(embed = out)




if __name__ == "__main__":
    bot.run(TOKEN)
