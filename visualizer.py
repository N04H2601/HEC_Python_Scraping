import pandas as pd  # Importation du module pandas pour la création du dataframe

pd.set_option('display.expand_frame_repr', False) # Affichage complet des colonnes du dataframe

# Création du dataframe à partir du fichier dataframe.csv
df = pd.read_csv('dataframe.csv', sep=',', encoding='utf-8')

# Création d'un dataframe contenant la somme des totaux par pays
total_par_pays = df.groupby('Pays')['Total'].sum()
# Création d'un dataframe contenant les 5 pays ayant le plus de totaux
top_5_pays = total_par_pays.nlargest(5)

print(top_5_pays)  # Affichage du dataframe

# Création d'un dictionnaire pour stocker les dataframes pour chaque pays
dataframes_par_pays = {}

# Création d'un dataframe pour chaque pays dans le dataframe top_5_pays avec les 5 matières les plus présentes
for pays in top_5_pays.index:  # Parcours des pays
    # Création d'un dataframe contenant les lignes du pays
    pays_df = df[df['Pays'] == pays]
    # Création d'une liste contenant les noms des colonnes des matières
    matieres = pays_df.columns[6:-1]
    # Création d'un dataframe contenant les 5 matières les plus présentes pour le pays
    top_matieres = pays_df[matieres].sum().nlargest(5)
    # Création d'un dataframe contenant les colonnes Pays et les 5 matières les plus présentes pour le pays
    pays_df = pays_df[['Pays'] + list(top_matieres.index)]
    # Réinitialisation des index du dataframe
    pays_df.reset_index(drop=True, inplace=True)
    # Aggrégation des lignes du dataframe pour avoir une seule ligne contenant le pays et le total de chaque matiere
    pays_df = pays_df.groupby('Pays')[list(top_matieres.index)].sum()
    # Ajout du dataframe dans le dictionnaire
    dataframes_par_pays[pays] = pays_df

# Afficher les dataFrames pour chaque pays dans le top 5
for pays, df in dataframes_par_pays.items():
    print(f"\nTop 5 matières pour {pays}")  # Affichage du nom du pays
    print(df)  # Affichage du dataframe
