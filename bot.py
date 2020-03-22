import asyncio
import os
import discord

from discord import Member

client = discord.Client()
token = os.environ.get('BOT_TOKEN')


@client.event
async def on_ready():
    print('{}: Bot enabled.'.format(client.user.name))
    client.loop.create_task(status_task())


async def status_task():
    while True:
        await client.change_presence(activity=discord.Game('.help'), status=discord.Status.online)


def is_not_pinned(mess):
    return not mess.pinned


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if 'commands' in message.content:  
        await message.channel.send('')
    if message.content.startswith('.help'): # Help on commands in the bot
        embed=discord.Embed(description='Для получения дополнительной информации о конкретной команде используйте `.help {command}`')
        embed.set_author(name="# Commands")
        embed.add_field(name='Основные',
                        value='`stats` `link`')
        embed.add_field(name='Модерирование',
                        value='`mute` `ban` `clear`')
        mess = await message.channel.send(embed=embed)
    if message.content.startswith('.stats'): # User statistics on the server
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                embed = discord.Embed(title='Информация'.format(member.name),
                                      description='BAD: Полная информация о пользователе {}'.format(member.mention))
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
    if message.content.startswith('.link'): # Invite a bot to your server
        embed=discord.Embed( )
        embed.set_author(name='discord.gg', 
                         url='https://discordapp.com/oauth2/authorize?&client_id=669249748909162513&scope=bot&permissions=26624',
                         icon_url='https://i.imgur.com/RYBI6Ad.png')
        embed.set_image(url='https://i.imgur.com/SbmwC1T.jpg')
        embed.set_footer(text='Developer : Wizel')
        mess = await message.channel.send(embed=embed)
    if message.content.startswith('.clear'): # Clearing messages in the server text channel
        if message.author.permissions_in(message.channel).manage_messages:
            deleted = await message.channel.purge(limit=10, check=is_not_pinned) 

client.run(str(token))