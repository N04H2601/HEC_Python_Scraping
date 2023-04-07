import re  # Importation du module re pour les expressions régulières
import pandas as pd  # Importation du module pandas pour la création du dataframe

# Préparation de la donnée (matières) pour le dataframe
# Vider le contenu du fichier matieres_dataframe.txt
# Ouverture du fichier en mode lecture et écriture
with open('matieres_dataframe.txt', 'r+') as fichier:
    fichier.truncate(0)  # Vider le contenu du fichier

doublons = ['TVA', 'Droits d\'accises', 'Taxation des produits énergétiques et de l\'électricité', 'Importation'
            'Exportation'
            'Douane']  # Liste des mots à supprimer

# Ouverture des fichiers en mode lecture et écriture
with open('matieres_final.txt', 'r', encoding='utf-8') as f_entree, open('matieres_dataframe.txt', 'w', encoding='utf-8') as f_sortie:
    # Parcours du fichier d'entrée
    for ligne in f_entree:
        mots = re.split(r'[-;]', ligne)  # Séparation des mots
        mots_uniques = []  # Liste des mots uniques

        # Parcours des mots
        for mot in mots:
            if mot not in mots_uniques:  # Si le mot n'est pas déjà présent dans la liste des mots uniques
                # Ajout du mot dans la liste des mots uniques
                mots_uniques.append(mot)
        # Création de la nouvelle ligne
        new_line = '-'.join(mots_uniques)
        # Ecriture de la nouvelle ligne dans le fichier de sortie
        f_sortie.write(new_line)


# Création du dataframe
# Création d'une liste contenant la liste des fichiers à lire
fichiers = ['affaires_dataframe.txt', 'dates_dataframe.txt',
            'documents_dataframe.txt', 'liens_dataframe.txt', 'pays_dataframe.txt']

dfs = []  # Liste des dataframes

# Parcours des fichiers
for fichier in fichiers:
    # Création du dataframe à partir du fichier et ajout dans la liste des dataframes
    df = pd.read_csv(fichier, sep=' ', names=[
                     fichier[:-14].capitalize()], encoding='utf-8')
    # Réinitialiser l'index du dataframe
    df.reset_index(drop=True, inplace=True)
    dfs.append(df)  # Ajout du dataframe dans la liste des dataframes

colonnes = ['TVA', 'Droits d\'accises', 'Taxation des produits énergétiques et de l\'électricité', 'Douane',
            'Droits de succession', 'Fusion', 'Taxe sur les véhicules', 'Libre circulation des capitaux',
            'Principes, objectifs et missions des Traités', 'Boissons spiritueuses', 'Libre circulation des marchandises',
            'Restrictions quantitatives', 'Mesures d\'effet équivalent', 'Liberté d\'établissement', 'Plus-values',
            'Coopération administrative', 'Tabacs manufacturés', 'Impôts indirects',
            'Citoyenneté de l\'Union', 'Libre circulation des travailleurs', 'Relations extérieures',
            'Association européenne de libre-échange', 'Taxe d\'immatriculation', 'Rapprochement des législations',
            'Adhésion', 'Dispositions financières', 'Ressources propres', 'Transports', 'Agriculture et Pêche',
            'Environnement', 'Départements français d\'outre-mer', 'Denrées alimentaires',
            'Monopoles d\'État à caractère commercial', 'Concurrence', 'Aides accordées par les États']

for colonne in colonnes:  # Parcours des colonnes
    # Création d'une nouvelle colonne dans le dataframe
    # Initialisation de la colonne à 0
    df[colonne] = [0 for i in range(len(df))]

df = pd.concat(dfs, axis=1)  # Concaténation des dataframes

with open('matieres_dataframe.txt', 'r', encoding='utf-8') as fichier:
    lignes = fichier.readlines()  # Lecture des lignes du fichier

for i in range(len(df)):
    # Remplacement des doublons par des mots uniques dans la ligne i du fichier
    lignes[i].replace('Alcool', 'Boissons spiritueuses') \
        .replace('Tabac', 'Tabacs manufacturés') \
        .replace('Taxes sur l\'électricité', 'Taxation des produits énergétiques et de l\'électricité') \
        .replace('Taxes d\'effet équivalent', 'Mesures d\'effet équivalent') \
        .replace('Tarif douanier commun', 'Union douanière') \
        .replace('Sucre', 'Denrées alimentaires') \
        .replace('Vin', 'Boissons spiritueuses') \
        .replace('Fruits et légumes', 'Denrées alimentaires').replace('Douane-Douane', 'Douane').replace('Douane;Douane', 'Douane')

    # Boucle sur chaque colonne du dataframe
    for colonne in colonnes:
        # Si la colonne est présente dans la ligne i du fichier, on passe la valeur à 1
        if colonne in lignes[i]:
            df.loc[i, colonne] = 1

df['Total'] = df.iloc[:, 5:].sum(axis=1)  # Création de la colonne Total

# Enregistrement du dataframe dans un fichier csv
df.to_csv('dataframe.csv', index_label='Index')
