import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
import io
import sys
from discord_components import DiscordComponents, Button, ButtonStyle

bot = commands.Bot(command_prefix=commands.when_mentioned_or('.'), intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
    DiscordComponents(bot)
    activity = discord.Game(name=".help", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print('зареган в {0}'.format(bot.user))

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member = None):
    if not member:
        await ctx.send( 'Ник то ты, не написал!' )
        return
    await member.kick()
    await ctx.send( ':partying_face: **{0}#{1}** Был изгнан. Легко кикнули уебана!'.format(member.name, member.discriminator))

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
      await ctx.send( ':clown: Вы еблан, у вас не получится (Нет прав, или же что-то другое...).' )

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    if not member:
        await ctx.send( 'Ник то ты, не написал!' )
    await member.ban(reason = reason) 

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
      await ctx.send( ':clown: Вы еблан, у вас не получится (Нет прав, или же что-то другое...).' )


@bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    if not member:
        await ctx.send( 'Ник то ты, не написал!' )
        return
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Ладно, разбаним его... {user.mention} получил вновь доступ к этому серверу! :partying_face:')
            return

@bot.command()
async def avatar(ctx, member:discord.Member = None):
    if member == None:
        member = ctx.author
    memberAvatar = member.avatar_url
    embed=discord.Embed(color = 0x2f3136, title = "Вот, пожалуйста. Фантазия школьника: **{0}**".format(member))
    embed.set_image(url = memberAvatar)
    await ctx.send(embed=embed)  

@bot.command() 
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount = 0):
    await ctx.channel.purge(limit=amount)
    await ctx.send( ':face_exhaling: Я снес вам '**{amount}**' сообщений...' )  

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
      await ctx.send( ':fearful: Что-то не получилось у тебя удалить сообщения, либо ты не указал количество сообщений, либо же у тебя нет прав.' )

@bot.command()
async def user(ctx,member:discord.Member = None, guild: discord.Guild = None):
    if member == None:
        emb = discord.Embed(title="Информация о пользователе", color=ctx.message.author.color)
        emb.add_field(name="Имя:", value=ctx.message.author.display_name,inline=False)
        emb.add_field(name="Айди пользователя:", value=ctx.message.author.id,inline=False)
        t = ctx.message.author.status
        if t == discord.Status.online:
            d = " В сети"

        t = ctx.message.author.status
        if t == discord.Status.offline:
            d = "⚪ Не в сети"

        t = ctx.message.author.status
        if t == discord.Status.idle:
            d = " Не активен"

        t = ctx.message.author.status
        if t == discord.Status.dnd:
            d = " Не беспокоить"

        emb.add_field(name="Активность:", value=d,inline=False)
        emb.add_field(name="Статус:", value=ctx.message.author.activity,inline=False)
        emb.add_field(name="Роль на сервере:", value=f"{ctx.message.author.top_role.mention}",inline=False)
        emb.add_field(name="Акаунт был создан:", value=ctx.message.author.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
        emb.set_thumbnail(url=ctx.message.author.avatar_url)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(title="Информация о пользователе", color=member.color)
        emb.add_field(name="Имя:", value=member.display_name,inline=False)
        emb.add_field(name="Айди пользователя:", value=member.id,inline=False)
        t = member.status
        if t == discord.Status.online:
            d = " В сети"

        t = member.status
        if t == discord.Status.offline:
            d = "⚪ Не в сети"

        t = member.status
        if t == discord.Status.idle:
            d = " Не активен"

        t = member.status
        if t == discord.Status.dnd:
            d = " Не беспокоить"
        emb.add_field(name="Активность:", value=d,inline=False)
        emb.add_field(name="Статус:", value=member.activity,inline=False)
        emb.add_field(name="Роль на сервере:", value=f"{member.top_role.mention}",inline=False)
        emb.add_field(name="Акаунт был создан:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
        await ctx.send(embed = emb)



@bot.command()
@commands.has_permissions(administrator=True)
async def send(ctx, * args):
    if not args:
        return await ctx.send("Не скажу, так как мне нечего тебе сказать...")
    await ctx.send(" ".join(args))
    await ctx.message.delete()

@send.error
async def send_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
      await ctx.send(':fearful: Команда .send была убрана у обычных пользователей, чтобы небыло лишних вопросов.')        

bot.run('insert token')