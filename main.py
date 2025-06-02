import discord
import os  # <-- lisätty tämä

intents = discord.Intents.default()
intents.message_content = True  # Tarvitaan viestisisällön lukemiseen
intents.members = True  # Tarvitaan roolien jakamiseen

client = discord.Client(intents=intents)

BOT_A_ID = 690474732310626354  # Vaihda tähän botin A käyttäjä-ID

RANK_ROLES = {
    "bronze": "Bronze",
    "silver": "Silver",
    "gold": "Gold",
    "platinum": "Platinum",
    "diamond": "Diamond",
    "master": "Master",
    "apex predator": "Apex Predator"
}

@client.event
async def on_message(message):
    if message.author.id != BOT_A_ID:
        return  # Vain botin A viestit kiinnostaa

    # Etsitään viestistä rankin nimi
    content = message.content.lower()
    found_rank = None
    for rank in RANK_ROLES:
        if rank in content:
            found_rank = rank
            break

    if found_rank and message.mentions:
        user = message.mentions[0]
        role_name = RANK_ROLES[found_rank]
        role = discord.utils.get(message.guild.roles, name=role_name)
        if role:
            # Poistetaan käyttäjältä kaikki muut rank-roolit (valinnainen)
            rank_role_names = RANK_ROLES.values()
            roles_to_remove = [r for r in user.roles if r.name in rank_role_names]
            if roles_to_remove:
                await user.remove_roles(*roles_to_remove)
            # Lisätään uusi rooli
            await user.add_roles(role)
            print(f"Annettiin {role_name} rooli käyttäjälle {user.name}")

client.run(os.environ['TOKEN'])  # <-- muutettu näin
