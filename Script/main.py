import discord 
from discord.ext import commands
import time
from enregistrement import *
from unidecode import unidecode

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command(name='aide')
async def aide(ctx):
    # Créer un objet Embed
    embed = discord.Embed(title="Aide - SpeedBot", color=0x3498DB)
    embed.add_field(name="!aide", value="Affiche ce message d'aide.", inline=False)
    embed.add_field(name="!enregistrement [nom] [ville] [region]", value="Enregistre votre nom dans la base de données.", inline=False)
    embed.add_field(name="!recherche", value="Recherche les motards près de chez toi.", inline=False)
    embed.set_footer(text="SpeedBot - Votre compagnon pour les motards")

    await ctx.send(embed=embed)

@bot.command(name='enregistrement')
async def enregistrement(ctx, nom: str, ville: str, region: str):
    pseudo = ctx.author.name
    ville_normalise = ville.lower()  # Convertir la ville en minuscules
    region_normalise = region.lower()  # Convertir la région en minuscules

    ville = unidecode(ville_normalise)
    region = unidecode(region_normalise)

    with open("donnees.json", "r") as file:
        donnees = json.load(file)

    # Vérifiez si le pseudo est déjà enregistré dans toutes les régions et villes
    pseudo_existe = False
    for r, regions_data in donnees.items():
        for v, ville_data in regions_data.items():
            if "Nom" in ville_data:
                for item in ville_data["Nom"]:
                    if item.get("Pseudo") == pseudo:
                        pseudo_existe = True
                        message1 = "Il me semble que vous êtes déjà enregistré dans mes données."
                        await ctx.channel.send(message1)
                        break
    
    if not pseudo_existe:
        actualiser(region, ville, nom, pseudo)
        message2 = f"Merci {nom}, votre nom a été enregistré dans la région {region} et la ville {ville} !"
        await ctx.channel.send(message2)
        
@bot.command(name='close')
@commands.has_permissions(administrator=True)
async def commande_admin(ctx):
    await ctx.send("A bientot 👋")
    time.sleep(1)
    await bot.close()

@bot.event
async def on_ready():
    print("SpeedBot est en ligne.")

if __name__ == '__main__':
    bot.run("")