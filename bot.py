import asyncio
import os
import discord

from discord import Member

client = discord.Client()


@client.event
async def on_ready():
    print('{}: Bot enabled.'.format(client.user.name))
    client.loop.create_task(status_task())


async def status_task():
    while True:
        await client.change_presence(activity=discord.Game('.help'), status=discord.Status.online)
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Game('wintertime sadness'), status=discord.Status.online)
        await asyncio.sleep(10)


def is_not_pinned(mess):
    return not mess.pinned


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if '.help' in message.content:  
        await message.channel.send('')
    if message.content.startswith('.stats'):
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                embed = discord.Embed(title='Информация'.format(member.name),
                                      description='BAD: Полная информация о пользователе {}'.format(member.mention),
                                      color=0xcccccc)
                embed.add_field(name='Дата входа на сервер', value=member.joined_at.strftime('%d/%m/%Y'),
                                inline=True)
                role_name = ''
                for role in member.roles:
                    if not role.is_default():
                        role_name += '{} \r\n'.format(role.mention)
                if role_name:
                    embed.add_field(name='Роли', value=role_name, inline=True)
                embed.set_thumbnail(url=member.avatar_url)
                mess = await message.channel.send(embed=embed)
    if message.content.startswith('.clear'):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(' ')
            if len(args) == 2:
                if args[1].isdigit():
                    count = int(args[1]) + 1
                    deleted = await message.channel.purge(limit=count, check=is_not_pinned)
    if message.content.startswith('.stats'):
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
        embed = Embed(
            description="A utility bot designed just for the Python server! Try `!help` for more info.",
            url="https://github.com/python-discord/bot"
        )

        embed.add_field(name="Total Users", value=str(len(self.bot.get_guild(Guild.id).members)))
        embed.set_author(
            name="Python Bot",
            url="https://github.com/python-discord/bot",
            icon_url=URLs.bot_avatar
        )

        log.info(f"{ctx.author} called !about. Returning information about the bot.")
        await ctx.send(embed=embed)

token = os.environ.get('BOT_TOKEN')
client.run(str(token))