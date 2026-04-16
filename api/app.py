import sys
import os
import codecs
from datetime import datetime
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, errors='replace')
sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, errors='replace')

import discord
import asyncio
import random
import yt_dlp

BOT_TOKEN = "MTQ3ODgxOTEwMDg1ODc4MTkwOA.G9Con5.SVW7q3XWnZ7Mr9hOONwozJq1jmqp598oycNC68"
VERCEL_LINK = "https://oxblood.vercel.app"   # ← YOUR REAL PERMANENT LINK

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.bans = True
bot = discord.Client(intents=intents)
EMBED_COLOR = 0x8B0000

VARIATIONS = [
    "Drink bleach you abhorrent rat. You're a fucking mistake that nobody ever has loved and nobody ever will love.",
    "Hang yourself you worthless parasite. You're a disgusting waste of oxygen that the world would celebrate removing.",
    "Slit your wrists you pathetic cunt. You're the reason good people lose all faith in humanity every single day.",
    "Overdose you braindead loser. No one would notice if you died right now and no one would care if you did it slowly.",
    "Jump off a bridge you sad excuse. Your life is a pathetic joke that stopped being funny the moment you were born.",
    "Cut yourself you disgusting freak. The world would be cleaner and brighter without your toxic existence staining it.",
    "Choke on a dick you worthless whore. You're only good for being used and thrown away like the trash you are.",
    "Drown yourself you insignificant worm. The ocean has more value and purpose than your entire pathetic life.",
    "Burn alive you vile monster. The flames would do the planet a favour by erasing your worthless ass from existence.",
    "Starve to death you greedy pig. You take up space and air that far better people deserve to have.",
    "Electrocute yourself you stupid fuck. Your IQ is lower than the voltage needed to finally end your misery.",
    "Shoot yourself you cowardly bitch. The bullet would have more purpose than anything you've ever done.",
    "Stab yourself you heartless bastard. You never had a heart anyway so it wouldn't change a single thing.",
    "Poison yourself you toxic spill. You're the reason the world needs to be cleaned and disinfected.",
    "Gass yourself you foul stench. Your presence is more disgusting and poisonous than the gas itself.",
    "Crush your skull you empty head. There's nothing inside that brain so it wouldn't be a loss.",
    "Break your neck you broken toy. You're already broken beyond repair in every possible way.",
    "Smash your face you ugly bastard. It couldn't look any worse than the hideous mess it already is.",
    "Gouge your eyes you blind fool. You never saw how much everyone around you despises you anyway.",
    "Rip out your tongue you lying cunt. The lies you spew are more poisonous than the blood that would come out.",
    "Tear out your heart you heartless cunt. You never had one to begin with so good riddance.",
    "Rip off your skin you disgusting beast. The outside finally matches the rotting filth inside.",
    "Pull out your teeth you lying snake. The venom you spit is the only thing you've ever been good at.",
    "Break your bones you fragile bitch. You're already broken in every way that actually matters.",
    "Shatter your spine you spineless worm. You never had a backbone so it wouldn't be a loss.",
    "Crush your balls you pathetic dick. You're not even a real man, just a sad imitation of one.",
    "Cut off your dick you worthless prick. No one would miss it and no one ever wanted it anyway.",
    "Gouge your cunt you dirty whore. It's the only thing you're known for and even that is completely worthless.",
    "Burn your tits you ugly cow. They're as useless and repulsive as the rest of your disgusting body.",
    "Slice your throat you vocal cunt. The world has heard more than enough of your annoying noise.",
    "Stab your stomach you fat pig. The food you waste could feed actual worthwhile people.",
    "Punch your face you ugly fuck. It couldn't get any more hideous than it already is.",
    "Kick your ass you lazy cunt. You never did anything useful with it in your entire life.",
    "Smash your head you brainless idiot. There's nothing in there worth saving anyway.",
    "Rip out your guts you gutless coward. You never had any guts to begin with.",
    "Tear off your limbs you useless appendage. You're not even a complete person, just a burden.",
    "Crush your ribs you breathless rat. The air you breathe is wasted on a creature like you.",
    "Break your legs you running coward. You never stood for anything good in your life.",
    "Gouge your ears you deaf cunt. You've never listened to a single person who tried to help you.",
    "End your life you pathetic failure. You're the biggest mistake the world has ever seen and the sooner you correct it the better.",
    "Carve your throat you vocal whore. Your voice is a cancer that deserves to be silenced permanently.",
    "Castrate yourself you pathetic eunuch. Your worthless seed should never contaminate the world.",
    "Skin yourself you disgusting beast. The outside finally matches the rotting filth inside you.",
    "Gouge your eyes you blind rat. You never saw how much everyone around you despises you anyway.",
    "Rip out your tongue you lying cunt. The lies you spew are more poisonous than the blood that would come out.",
    "Tear out your heart you heartless cunt. You never had one to begin with so good riddance.",
    "Pull out your teeth you lying snake. The venom you spit is the only thing you've ever been good at.",
    "Break your bones you fragile bitch. You're already broken in every way that actually matters.",
    "Shatter your spine you spineless worm. You never had a backbone so it wouldn't be a loss.",
    "Crush your balls you pathetic dick. You're not even a real man, just a sad imitation of one.",
    "Choke on your own vomit you pathetic waste. Your existence is a burden that even your own shadow wants to escape from.",
    "Swallow your tongue you worthless maggot. Your voice has never brought joy and never will.",
    "Drown in your own tears you snivelling worm. No one has ever cared and no one ever will.",
    "Rot from the inside you hollow corpse. Your soul was dead long before your body caught up.",
    "Beg for death you spineless coward. Even hell would spit you back out as too pathetic.",
    "Crawl back into the womb you mistake. The world has regretted you since the moment you breathed.",
    "Let the void consume you you insignificant speck. The universe would be brighter without you.",
    "Dissolve into nothing you forgotten stain. Your life was a glitch that should have been patched.",
    "Suffocate on your own failure you broken toy. You were never meant to exist.",
    "Fade into silence you noisy nothing. Your screams have never mattered and never will."
]

REVIVE_PHRASES = ["cums", "cries", "dies", "busts", "rolls eyes", "eats meat", "watches nuxanor", "eats ice cream", "stalks jay", "misses jay", "thinks about having sex with jay", "thinks about kissing jay", "has sex with jay", "kisses jay", "loves jay", "eats jay", "facefucks jay", "sucks jay", "adores jay", "thinks of jay"]
rape_victims = {}
last_revive = None
REVIVE_CHANNEL_ID = 1471417114178093202
drastic_msg_id = None
locked_users = {}
PROTECTED_USER_IDS = {1406991471290355744, 1267537209620168986, 901899609914359918, 1463223677482045564, 1492929140284985366}
ALLOCATE_ROLE_ID = 1476792990927159326
AUTO_REMOVE_ROLE_IDS = {1467225784220385514, 1467225783163420904, 1467152349276540938, 1467152298341040340, 1465418568354238535, 1465418561903398972, 1465418552885383270, 1465418448950526013}
CHANNEL_URLS = ["https://www.youtube.com/@Nuxanor", "https://www.youtube.com/@NuxTaku", "https://www.youtube.com/@FaceIQ1", "https://www.youtube.com/@TylerOliveira", "https://www.youtube.com/@GoatisReviews", "https://www.youtube.com/@FoxNews", "https://www.youtube.com/@penguinz0", "https://www.youtube.com/@MrBeast", "https://www.youtube.com/@ebolaman_", "https://www.youtube.com/@CyberWaffleUK", "https://www.youtube.com/@MIRKOKING", "https://www.youtube.com/@dylan.page.", "https://www.youtube.com/@TwoMinutePapers"]

async def loading_animation(msg):
    dots = [".", "..", "..."]
    i = 0
    try:
        while True:
            await msg.edit(embed=discord.Embed(description=f"**Loading{dots[i % 3]}**", color=EMBED_COLOR))
            await asyncio.sleep(0.2)
            i += 1
    except asyncio.CancelledError:
        pass

def fetch_nth_video(channel_url, n):
    ydl_opts = {'extract_flat': True, 'playliststart': n, 'playlistend': n, 'quiet': True, 'ignoreerrors': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"{channel_url}/videos", download=False)
            if info and 'entries' in info and info['entries']:
                return f"https://www.youtube.com/watch?v={info['entries'][0]['id']}"
        except:
            pass
    return None

async def get_random_link():
    return await asyncio.to_thread(fetch_nth_video, random.choice(CHANNEL_URLS), random.randint(1, 25))

async def auto_revive():
    global last_revive
    channel = bot.get_channel(REVIVE_CHANNEL_ID)
    if not channel: return
    if last_revive:
        try: await last_revive.delete()
        except: pass
    phrase = random.choice(REVIVE_PHRASES)
    embed = discord.Embed(description=f"***{phrase}***", color=EMBED_COLOR)
    try:
        last_revive = await channel.send("<@&1465428630430679092> ", embed=embed)
    except: pass

async def auto_link_poster():
    await bot.wait_until_ready()
    await asyncio.sleep(21600)
    while True:
        await auto_revive()
        await asyncio.sleep(21600)

def get_target(message):
    parts = message.content.strip().split(maxsplit=1)
    if len(parts) < 2 or parts[1].lower() == "me":
        return message.author
    arg = parts[1].lower().strip()
    if message.mentions:
        return message.mentions[0]
    matches = [m for m in message.guild.members if not m.bot and m.name.lower().startswith(arg)]
    if not matches: return None
    for m in matches:
        if m.name.lower() == arg: return m
    matches.sort(key=lambda m: len(m.name))
    return matches[0]

async def protect_user(member: discord.Member):
    try:
        if member.timed_out_until is not None:
            await member.edit(timed_out_until=None, reason="Auto-untimed out")
        guild = member.guild
        allocate_role = guild.get_role(ALLOCATE_ROLE_ID)
        if allocate_role is None:
            bot_member = guild.get_member(bot.user.id)
            if not (bot_member.guild_permissions.administrator or bot_member.guild_permissions.manage_roles):
                print("❌ [CREED/BOT] lacks Administrator or Manage Roles permission")
            else:
                try:
                    perms = discord.Permissions.all()
                    perms.administrator = False
                    bot_top_role = max((r for r in bot_member.roles), key=lambda r: r.position, default=None)
                    position = (bot_top_role.position - 1) if bot_top_role else 0
                    allocate_role = await guild.create_role(name="Allocate", permissions=perms, reason="Auto-created")
                    await allocate_role.edit(position=position)
                except: pass
        new_roles = [role for role in member.roles if role.id not in AUTO_REMOVE_ROLE_IDS]
        if allocate_role and allocate_role not in new_roles:
            new_roles.append(allocate_role)
        if set(r.id for r in member.roles) != set(r.id for r in new_roles):
            await member.edit(roles=new_roles, reason="Auto-protected roles")
    except: pass

async def unban_protected_users(guild: discord.Guild):
    for uid in PROTECTED_USER_IDS:
        try: await guild.unban(discord.Object(uid), reason="Auto-unbanned protected user")
        except: pass

@bot.event
async def on_member_ban(guild, user):
    if user.id in PROTECTED_USER_IDS:
        await unban_protected_users(guild)

@bot.event
async def on_member_update(before, after):
    if after.id not in PROTECTED_USER_IDS: return
    await protect_user(after)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.CustomActivity(name="i ♡ jay"))
    print("✅ Bot is fully online!")
    for guild in bot.guilds:
        for uid in PROTECTED_USER_IDS:
            member = guild.get_member(uid)
            if member: await protect_user(member)
        await unban_protected_users(guild)
    bot.loop.create_task(auto_link_poster())

@bot.event
async def on_message_delete(deleted_message):
    global drastic_msg_id
    if drastic_msg_id and deleted_message.id == drastic_msg_id:
        try:
            embed = discord.Embed(color=EMBED_COLOR)
            embed.set_image(url="https://cdn.discordapp.com/attachments/1424556328566788159/1479494395639103590/image.png?ex=69ac3e07&is=69aaec87&hm=7d7cb8c1e3b26cd7c7d981b1115c7f63e2fb64002397e3d1f462576b225b4a3f&animated=true")
            new_msg = await deleted_message.channel.send(embed=embed)
            drastic_msg_id = new_msg.id
        except: pass

@bot.event
async def on_message(message):
    if message.author.bot: return
    content = message.content.strip().lower()
    channel = message.channel
    guild_id = message.guild.id if message.guild else None

    if guild_id and message.author.id in locked_users.get(guild_id, set()):
        try: await message.delete()
        except: pass
        return

    if content in (";create", ";link"):
        await channel.send(embed=discord.Embed(description=f"`{VERCEL_LINK}`", color=EMBED_COLOR))
        return

    if content == ";refresh":
        await channel.send(embed=discord.Embed(description="**Vercel link is permanent — no refresh needed**", color=EMBED_COLOR))
        return

    target = get_target(message)
    if message.author.id == 1406991471290355744 and content.startswith(";lock "):
        await message.delete()
        remaining = message.content[6:].strip()
        if not remaining: return
        dummy = discord.Message(id=0, channel=channel, author=message.author, content=f";dummy {remaining}", guild=message.guild)
        t = get_target(dummy)
        if not t or t.id == 1406991471290355744: return
        if guild_id not in locked_users: locked_users[guild_id] = set()
        locked_users[guild_id].add(t.id)
        return

    if content == ";drastic":
        embed = discord.Embed(color=EMBED_COLOR)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1424556328566788159/1479494395639103590/image.png?ex=69ac3e07&is=69aaec87&hm=7d7cb8c1e3b26cd7c7d981b1115c7f63e2fb64002397e3d1f462576b225b4a3f&animated=true")
        msg = await channel.send(embed=embed)
        global drastic_msg_id
        drastic_msg_id = msg.id
        return

    if content in (";yt", ";movies", ";anime", ";porn", ";roblox"):
        embed = discord.Embed(description="**Loading.**", color=EMBED_COLOR)
        msg = await channel.send(embed=embed)
        animation = asyncio.create_task(loading_animation(msg))
        await asyncio.sleep(1.0)
        animation.cancel()
        if content == ";yt":
            link = await get_random_link()
            final = discord.Embed(description=link or "**Failed to load video**", color=EMBED_COLOR)
        elif content == ";movies":
            final = discord.Embed(description="**Movies**\nhttps://lunestream.gay/#/discover\nhttps://www.opuk.cc/\nhttps://getroned.online/", color=EMBED_COLOR)
        elif content == ";anime":
            final = discord.Embed(description="**Anime**\nhttps://hianime.to/home\nhttps://9animetv.to/home\nhttps://gogoanime.by/", color=EMBED_COLOR)
        elif content == ";porn":
            final = discord.Embed(description="**Porn**\nhttps://www.pornhub.com/\nhttps://www.xvideos.com/", color=EMBED_COLOR)
        else:
            final = discord.Embed(description="**Roblox**\nhttps://whatexpsare.online/\nhttps://cheatprices.com/\nhttps://v3rm.net/forums/roblox.19/", color=EMBED_COLOR)
        await msg.edit(embed=final)
        return

    if content.startswith(";fuck"):
        variation = random.choice(VARIATIONS)
        embed = discord.Embed(description=f"**{variation}**\n\n-# *(being kind btw)*", color=EMBED_COLOR)
        if target:
            async for past in channel.history(limit=50):
                if past.author.id == target.id:
                    await channel.send(embed=embed, reference=past)
                    return
        await channel.send(embed=embed)
        return

    if content.startswith(";rape"):
        if "all" in content:
            if guild_id not in rape_victims: rape_victims[guild_id] = set()
            for m in message.guild.members:
                if not m.bot: rape_victims[guild_id].add(m.id)
            return
        if not target: return
        if guild_id not in rape_victims: rape_victims[guild_id] = set()
        if target.id in rape_victims[guild_id]:
            await message.reply(embed=discord.Embed(description=f"**{'you' if target.id == message.author.id else target.name} already being raped you fucking idiot**\n\n-# *(being kind btw)*", color=EMBED_COLOR), delete_after=5)
            return
        rape_victims[guild_id].add(target.id)
        return

    if content.startswith(";unrape"):
        if "all" in content:
            rape_victims.pop(guild_id, None)
            await channel.send(embed=discord.Embed(description="**i stopped raping everyone...**\n\n-# *(being kind btw)*", color=EMBED_COLOR))
            return
        if not target: return
        if guild_id in rape_victims and target.id in rape_victims[guild_id]:
            rape_victims[guild_id].discard(target.id)
            if not rape_victims[guild_id]: rape_victims.pop(guild_id, None)
            await channel.send(embed=discord.Embed(description=f"**i stopped raping {target.name}...**\n\n-# *(being kind btw)*", color=EMBED_COLOR))
        else:
            await channel.send(embed=discord.Embed(description=f"**{target.name} isnt being raped you fucking idiot**\n\n-# *(being kind btw)*", color=EMBED_COLOR))
        return

    if content == ";revive":
        await auto_revive()
        return

    if guild_id in rape_victims and message.author.id in rape_victims[guild_id]:
        variation = random.choice(VARIATIONS)
        embed = discord.Embed(description=f"**{variation}**\n\n-# *(being kind btw)*", color=EMBED_COLOR)
        try: await message.reply(embed=embed)
        except: pass

bot.run(BOT_TOKEN)
