import json

with open("donnees.json", "r") as file:
        donnees = json.load(file)

def actualiser(region, ville, nom, pseudo):
    if region not in donnees:
        donnees[region] = {}

    if ville not in donnees[region]:
        donnees[region][ville] = {"Nom": []}

    donnees[region][ville]["Nom"].append({"Nom": nom, "Pseudo": pseudo})

    # Enregistrer les modifications dans le fichier JSON
    with open("donnees.json", "w") as file:
        json.dump(donnees, file, indent=2)
