import discord
import pytesseract
from PIL import Image
import io

# TESSERACTIN POLKU (muuta tämä jos asensit eri paikkaan)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

BOT_A_ID = 690474732310626354  # Vaihda tähän botti A:n käyttäjä-ID

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
    # Tarkistetaan, että viesti on botilta A
    if message.author.id != BOT_A_ID:
        return

    # Tarkistetaan, että viestissä on kuva
    if not message.attachments:
        return

    attachment = message.attachments[0]
    # Ladataan kuva muistiin
    image_bytes = await attachment.read()
    image = Image.open(io.BytesIO(image_bytes))

    # Luetaan kuva OCR:lla
    text = pytesseract.image_to_string(image).lower()

    print(f"Löydetty teksti kuvasta: {text}")

    # Etsitään rankki tekstistä
    found_rank = None
    for rank in RANK_ROLES:
        if rank in text:
            found_rank = rank
            break

    if found_rank and message.mentions:
        user = message.mentions[0]
        role_name = RANK_ROLES[found_rank]
        role = discord.utils.get(message.guild.roles, name=role_name)
        if role:
            # Poistetaan muut rank-roolit käyttäjältä
            rank_role_names = RANK_ROLES.values()
            roles_to_remove = [r for r in user.roles if r.name in rank_role_names]
            if roles_to_remove:
                await user.remove_roles(*roles_to_remove)
            # Lisätään uusi rooli
            await user.add_roles(role)
            print(f"Annettiin rooli {role_name} käyttäjälle {user.name}")

client.run("MTM3ODc0NDUyMjM5NzE5MjIzMg.GZnR1l.qNUjaLN8faGKwzvsUcT7Zl_ti3yZoLJZC2x-Ks")
