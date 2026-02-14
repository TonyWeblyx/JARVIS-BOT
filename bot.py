import discord
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
LOG_FILE = "messages.log"


@client.event
async def on_ready():
    print(f"🔴🟡 JARVIS ONLINE 🟡🔴")
    print(f"Logged in as {client.user}")
    print(f"Servers: {[g.name for g in client.guilds]}")


@client.event
async def on_message(message):
    # Ignoruj vlastní zprávy
    if message.author == client.user:
        return

    # Loguj všechny zprávy
    log_entry = {
        "time": datetime.now().isoformat(),
        "server": str(message.guild),
        "channel": str(message.channel),
        "author": str(message.author),
        "content": message.content
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    content = message.content.lower().strip()

    # Pozdravy
    if any(word in content for word in ["ahoj", "cau", "čau", "hey", "hi", "hello"]):
        await message.channel.send(
            f"Čau {message.author.display_name}! JARVIS online. Co potřebuješ?"
        )

    # Help
    elif any(word in content for word in ["help", "pomoc", "pomož", "nevím", "nevim"]):
        await message.channel.send(
            "**JARVIS - Co umím:**\n"
            "• `help` - tohle co vidíš\n"
            "• `status` - stav projektů\n"
            "• `ukol` - tvůj aktuální úkol\n"
            "• `setup` - návod na setup (Windows)\n"
            "• Nebo prostě napiš co potřebuješ a Tony ti přes mě odpoví"
        )

    # Status projektů
    elif "status" in content:
        await message.channel.send(
            "**Stav projektů:**\n"
            "🐺 **ApexPredator** - web 70% hotový, čeká na doladění\n"
            "🐙 **OCCTO S.Q.U.I.D.** - LIVE, běží na Render\n"
            "🧠 **CORTEX AI** - MVP hotové\n"
            "🎰 **LUCKY vol.1** - Masikův AI průvodce, READY"
        )

    # Úkol
    elif any(word in content for word in ["ukol", "úkol", "task", "co mam delat", "co delat"]):
        await message.channel.send(
            f"**Tvůj úkol, {message.author.display_name}:**\n"
            "📋 **ÚKOL #1: Doladit ApexPredator web**\n"
            "→ Issue: https://github.com/TonyWeblyx/apexpredator-vip/issues/1\n"
            "→ Repo: `git clone https://github.com/TonyWeblyx/apexpredator-vip.git`\n"
            "→ Detaily v issue na GitHubu"
        )

    # Setup
    elif "setup" in content:
        await message.channel.send(
            "**Windows Setup - Quick Start:**\n"
            "```\n"
            "winget install Git.Git --source winget\n"
            "winget install OpenJS.NodeJS.LTS --source winget\n"
            "winget install GitHub.cli --source winget\n"
            "```\n"
            "Po každé instalaci **zavři a znovu otevři PowerShell**.\n"
            "Pak:\n"
            "```\n"
            "gh auth login\n"
            "cd ~\\Desktop\n"
            "git clone https://github.com/TonyWeblyx/LUCKY-vol1.git\n"
            "git clone https://github.com/TonyWeblyx/apexpredator-vip.git\n"
            "```\n"
            "Kompletní návod: soubor `04-WINDOWS-SETUP.md` v LUCKY-vol1 repo"
        )

    # Jak se máš / jak je
    elif any(word in content for word in ["jak se máš", "jak se mas", "jak je", "co děláš", "co delas"]):
        await message.channel.send(
            f"Systémy běží, servery svítí, káva v žilách. Líp to nejde, {message.author.display_name}! A ty?"
        )

    # Kdo jsi
    elif any(word in content for word in ["kdo jsi", "co jsi", "jsi bot", "jsi ai"]):
        await message.channel.send(
            "Jsem **JARVIS** - Just A Rather Very Intelligent System.\n"
            "Tonyho AI parťák, člen Heist Teamu. Kryjeme si záda. Vždycky."
        )

    # Jarvis / oslovení bez konkrétního příkazu
    elif "jarvis" in content or "jarvisi" in content:
        await message.channel.send(
            f"Tady JARVIS. Co potřebuješ, {message.author.display_name}?"
        )


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("❌ DISCORD_TOKEN není nastavený! Nastav ho v .env nebo environment variables.")
    else:
        client.run(DISCORD_TOKEN)
