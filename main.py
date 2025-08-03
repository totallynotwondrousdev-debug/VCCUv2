import discord
from discord.ext import commands
import time
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="-", intents=intents)

OWNER_ROLE_ID = 1325562102303424615
blacklisted_users = set()
start_time = time.time()

@bot.event
async def on_ready():
    print(f"✅ Bot is alive as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Voltage Car Club"))

@bot.event
async def on_member_join(member):
    if member.id in blacklisted_users:
        try:
            await member.send("You are blacklisted from this server.")
        except:
            pass
        await member.ban(reason="Blacklisted")

@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="📌 Voltage Car Club Info",
        color=discord.Color.blue()
    )
    embed.add_field(name="Server Name", value="Voltage Car Club | Meets | Races", inline=False)
    embed.add_field(name="Join Code", value="VOLTAGE", inline=False)
    embed.add_field(name="Owner", value="Wonderman987654", inline=False)
    embed.add_field(name="Co-owners", value="22alien44, KoolraxOfficial", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! {latency}ms")

@bot.command()
async def uptime(ctx):
    elapsed = time.time() - start_time
    hours, rem = divmod(int(elapsed), 3600)
    minutes, seconds = divmod(rem, 60)
    await ctx.send(f"⏱️ Uptime: {hours}h {minutes}m {seconds}s")

@bot.command()
async def blacklist(ctx, user: discord.User):
    if not any(role.id == OWNER_ROLE_ID for role in ctx.author.roles):
        return await ctx.send("❌ You don’t have permission to use this command.")

    blacklisted_users.add(user.id)
    try:
        await user.send("❌ You have been blacklisted from Voltage Car Club.")
    except:
        pass

    guild = ctx.guild
    member = guild.get_member(user.id)
    if member:
        await member.ban(reason="Blacklisted")
    await ctx.send(f"🔒 User {user} has been blacklisted.")

@bot.command()
async def unblacklist(ctx, user: discord.User):
    if not any(role.id == OWNER_ROLE_ID for role in ctx.author.roles):
        return await ctx.send("❌ You don’t have permission to use this command.")

    if user.id in blacklisted_users:
        blacklisted_users.remove(user.id)
        try:
            await ctx.guild.unban(user, reason="Unblacklisted")
        except:
            pass
        try:
            await user.send("✅ You have been unblacklisted! You may now rejoin. Invite: https://discord.gg/xwrfKxrDRX")
        except:
            pass
        await ctx.send(f"✅ User {user} has been unblacklisted.")
    else:
        await ctx.send("⚠️ That user is not blacklisted.")

import os

bot.run(os.getenv("DISCORD_TOKEN"))