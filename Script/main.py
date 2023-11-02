import discord 
from discord.ext import commands
import time
from enregistrement import *
from unidecode import unidecode

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.command(name='help')
async def aide(ctx):
    # Créer un objet Embed
    embed = discord.Embed(title="Aide - SpeedBot", color=0x3498DB)
    embed.add_field(name="!help", value="Affiche ce message d'aide.", inline=False)
    embed.add_field(name="!enregistrement [votre nom] [votre ville] [votre region]", value="Enregistre votre nom dans la base de données.\n⚠ Pour les villes a nom composer veillez mettre des **-** ⚠\n*Exemple : Romilly**-**sur**-**seine*.", inline=False)
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

@bot.command(name = 'recherche')
async def enregistrement(ctx):
    
    pseudo = ctx.author.name

    with open("donnees.json", "r") as file:
        donnees = json.load(file)

    # Vérifiez si le pseudo est déjà enregistré dans toutes les régions et villes
    pseudo_existe = False
    riders_pres_de_chez_toi = []

    for r, regions_data in donnees.items():
        for v, ville_data in regions_data.items():
            if "Nom" in ville_data:
                for item in ville_data["Nom"]:
                    if item.get("Pseudo") == pseudo:  # Remplacez "matthieu_moto" par votre pseudo
                        pseudo_existe = True
                        for other_item in ville_data["Nom"]:
                            ville = v
                            region = r
                            if other_item.get("Pseudo") != pseudo:  # Excluez votre propre pseudo
                                riders_pres_de_chez_toi.append(other_item["Pseudo"])

    if pseudo_existe:
        if riders_pres_de_chez_toi:
            message = f"Voici les riders de la même ville que vous ({ville}, {region}) :\nPseudo : "
            for pseudo in riders_pres_de_chez_toi:
                message += f"**{pseudo}** ; "
            await ctx.channel.send(message)
        else:
            await ctx.channel.send("Vous êtes le seul rider de cette ville.")
    else:
        message1 = "Je suis désolé... \nMais vous n'êtes pas inscrit dans ma base de données. Veuillez exécuter cette commande :\n`!enregistrement [votre nom] [votre ville] [votre région]` pour vous enregistrer."
        await ctx.channel.send(message1)

@bot.command(name='close')
@commands.has_permissions(administrator=True)
async def commande_admin(ctx):
    await ctx.send("A bientot ✌")
    await bot.close()

@bot.event
async def on_ready():
    print("SpeedBot est en ligne.")

if __name__ == '__main__':
    bot.run("")
