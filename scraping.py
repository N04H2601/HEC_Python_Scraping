############################################################
# Attention, le code prend entre 5 et 10 min à s'éxecuter. #
# Il permet de remplir les fichiers x_dataframe.txt déjà présents dans le dossier. #
# Il est donc inutile de l'éxécuter si vous ne souhaitez pas attendre. #
# Le fichier dataframe.csv généré par le fichier dataframe.py est lui aussi déjà présent dans le dossier. #
# Vous pouvez directement lancer le fichier visualizer.py pour avoir les réponses aux questions posées. #
############################################################


# Import des librairies nécessaires
from tqdm import tqdm  # Pour afficher la barre de progression
import requests  # Pour récupérer les pages web
from bs4 import BeautifulSoup  # Pour parser les pages web
import re  # Pour utiliser des expressions régulières


# Vider le contenu des fichiers affaires_dataframe.txt, cadres_dataframe.txt, cadres_raccourcis.txt, dates_dataframe.txt, documents_dataframe.txt, matieres_final.txt, liens_dataframe.txt, matieres.txt et pays_dataframe.txt
noms_fichiers = ['affaires_dataframe.txt', 'cadres_dataframe.txt', 'cadres_raccourcis.txt', 'dates_dataframe.txt',
                 'documents_dataframe.txt', 'matieres_final.txt', 'liens_dataframe.txt', 'matieres.txt', 'matieres_raccourcis.txt', 'pays_dataframe.txt']

# Pour chaque nom de fichier dans la liste des noms de fichiers
for nom_fichier in noms_fichiers:
    with open(nom_fichier, 'r+') as fichier:  # Ouverture du fichier en mode lecture et écriture
        fichier.truncate(0)  # Vider le contenu du fichier

# Récupération des liens des pages web contenant les documents de la CJUE et stockage dans une liste
urls = ['https://curia.europa.eu/juris/documents.jsf?lgrec=fr&nat=or&mat=FISC%252Cor&pcs=Oor&jur=C%2CT&td=%24mode%3DfromTo%24from%3D1952.01.01%24to%3D2023.03.04%3B%3B%3BPUB1%3BNPUB1%3B%3B%3BORDALL&lg=&dates=%2524type%253Dall%2524mode%253DfromTo%2524from%253D1954.01.01%2524to%253D2023.03.04&language=fr&pro=CONS%252COB%252C&cit=none%252CC%252CCJ%252CR%252C2008E%252C%252C%252C%252C%252C%252C%252C%252C%252C%252Ctrue%252Ctrue%252Ctrue&oqp=&page=' +
        str(page) + '&cid=756586' for page in range(1, 10)]

liens = []  # Liste vide pour stocker les liens des documents

barre_progression_urls = tqdm(
    total=len(urls), desc='Traitement des urls ', position=0, leave=True)  # Barre de progression pour le traitement des urls

for url in urls:  # Pour chaque URL dans la liste des URLs
    reponse = requests.get(url)  # Récupération de la page web

    # Utilisation de BeautifulSoup pour récupérer le contenu de la page web en html
    soup = BeautifulSoup(reponse.content, 'html.parser')

    # Trouver tous les élements td de la classe 'table_cell_nom_usuel' pour récupérer les noms des pays
    for td in soup.find_all('td', {'class': 'table_cell_nom_usuel'}):
        # Récupération du nom du pays
        pays = td.text.strip().split('/')[1].strip()

        # Suppression des parenthèses et du contenu entre parenthèses dans le nom du pays (ex: Royaume-Uni (Angleterre et Pays de Galles))
        pays = re.sub(' \([^)]+\)', '', pays)

        # Écriture du nom du pays dans le fichier pays_dataframe.txt
        # Ouverture du fichier pays_dataframe.txt en mode écriture et encodage en utf-8 pour les caractères spéciaux
        with open('pays_dataframe.txt', 'a', encoding='utf-8') as f:
            # Écriture du nom du pays dans le fichier pays_dataframe.txt sans le dernier caractère (espace)
            f.write(pays + '\n')

    # Trouver tous les élements td de la classe 'table_cell_date' pour récupérer les dates
    for td in soup.find_all('td', {'class': 'table_cell_date'}):
        date = td.text.strip()  # Récupération de la date

        # Écriture de la date dans le fichier dates_dataframe.txt
        # Ouverture du fichier dates_dataframe.txt en mode écriture
        with open('dates_dataframe.txt', 'a') as f:
            # Écriture de la date dans le fichier dates_dataframe.txt
            f.write(date + '\n')

    # Trouver tous les élements td de la classe 'table_cell_links_curia' pour récupérer les matières
    for td in soup.find_all('td', {'class': 'table_cell_links_curia'}):
        # Trouver l'élément div avec l'attribut id vide et récupérer le texte
        matiere = td.find('div', {'id': ''}).text.split()
        # Transformer la liste en chaîne de caractères
        matiere = ' '.join(matiere)

        # Expression régulière pour trouver les mots 'Fiscalité', 'Taxe sur la valeur ajoutée', 'Énergie', 'Libre circulation des marchandises - Restrictions quantitatives - Mesures d\'effet équivalent', 'Droits d\'accise' et 'Liberté d\'établissement'
        pattern1 = r'(?<!\S)(?:Fiscalité|Taxe sur la valeur ajoutée|Énergie|Libre circulation des marchandises - Restrictions quantitatives - Mesures d\'effet équivalent|Droits d\'accise|Liberté d\'établissement)(?!\S)'
        # Remplacer les mots par '- <mot>'
        matiere = re.sub(pattern1, r'- \g<0>', matiere)
        # Supprimer les mots 'Fiscalité - - '
        matiere = matiere.replace('Fiscalité - - ', '')

        # Expression régulière pour trouver les mots '- <mot> - Fiscalité'
        pattern2 = r'^-\s*([^-\n]*?)\s*-\s*Fiscalité\b'
        # Remplacer les mots par '- <mot>'
        matiere = re.sub(pattern2, r'- \1', matiere, flags=re.IGNORECASE)

        # Expression régulière pour trouver les mots '- <mot> - Énergie'
        pattern3 = r'^-\s*(?:.*-\s+)?([^-\n]*?)\s*-\s*Énergie\b'
        # Remplacer les mots par '- <mot>'
        matiere = re.sub(pattern3, r'- \1', matiere, flags=re.IGNORECASE)

        # Remplacer les mots '- - ' par '-'
        matiere = matiere.replace('- - ', '-')
        # Remplacer les mots ' - Fiscalité' par ' -'
        matiere = matiere.replace(' - Fiscalité', ' -')

        # Supprimer les mots ' -' en fin de chaîne et placer un '-' au début de la chaîne de caractères
        if matiere.endswith(' -'):
            matiere = '- ' + matiere[:-2].strip()

        # Supprimer les mots '- Fiscalité -', '- Fiscalité ', ' - ', ' -', '- ', '--' et les remplacer par '-'
        matiere = matiere.replace('- Fiscalité -', '-')
        matiere = matiere.replace('- Fiscalité ', '-')
        matiere = matiere.replace(' - ', '-')
        matiere = matiere.replace(' -', '-')
        matiere = matiere.replace('- ', '-')
        matiere = matiere.replace('--', '-')

        # Écriture de la matière dans le fichier matieres.txt
        # Ouverture du fichier matieres.txt en mode écriture
        with open('matieres.txt', 'a', encoding='utf-8') as f:
            # Écriture de la matière dans le fichier matieres.txt
            f.write(matiere + '\n')

    # Trouver tous les élements td de la classe 'table_cell_aff' pour récupérer les identifiants des affaires
    for td in soup.find_all('td', {'class': 'table_cell_aff'}):
        affaire = td.text.strip()  # Récupération de l'identifiant de l'affaire

        # Écriture de l'identifiant de l'affaire dans le fichier affaires_dataframe.txt
        # Ouverture du fichier affaires_dataframe.txt en mode écriture
        with open('affaires_dataframe.txt', 'a', encoding='utf-8') as f:
            # Écriture de l'identifiant de l'affaire dans le fichier affaires_dataframe.txt s'il n'est pas vide
            if affaire.strip():
                # Écriture de l'identifiant de l'affaire dans le fichier affaires_dataframe.txt
                f.write(affaire + '\n')

    # Trouver tous les élements td de la classe 'table_cell_doc' pour récupérer les identifiants des documents
    for td in soup.find_all('td', {'class': 'table_cell_doc'}):
        # Trouver l'élément span avec la classe 'outputEcli' et récupérer le texte
        ecli = td.find('span', {'class': 'outputEcli'}).text.strip()

        # Écriture de l'identifiant du document dans le fichier documents_dataframe.txt
        # Ouverture du fichier documents_dataframe.txt en mode écriture
        with open('documents_dataframe.txt', 'a', encoding='utf-8') as f:
            # Écriture de l'identifiant du document dans le fichier documents_dataframe.txt
            f.write(ecli + '\n')

    # Trouver tous les liens eur-lex de la page
    for lien in soup.find_all('a'):
        # Récupération de l'attribut href de l'élément a
        href = lien.get('href')

        if href and 'eur-lex' in href:  # Vérifier si l'attribut href n'est pas vide et contient 'eur-lex'
            # Ajout du lien eur-lex à la liste des liens eur-lex
            liens.append(href)

            # Écriture du lien eur-lex dans le fichier liens_dataframe.txt
            # Ouverture du fichier liens_dataframe.txt en mode écriture
            with open('liens_dataframe.txt', 'a') as f:
                # Écriture du lien eur-lex dans le fichier liens_dataframe.txt
                f.write(href + '\n')

    # Incrémenter la barre de progression des liens eur-lex
    barre_progression_urls.update(1)

barre_progression_urls.close()  # Fermer la barre de progression des liens eur-lex

print()  # Saut de ligne entre les barres de progression

barre_progression_documents = tqdm(
    total=len(liens), desc='Traitement des documents ', position=0, leave=True)

# Parcourir tous les liens de la liste des liens eur-lex pour récupérer les mots clés des documents
for lien in liens:
    response = requests.get(lien)  # Récupération de la page du document
    soup = BeautifulSoup(response.content, 'html.parser',
                         from_encoding='utf-8')  # Récupération du contenu de la page du document

    # Ouverture du fichier mots_cles.txt en mode lecture
    with open('mots_cles.txt', 'r', encoding='utf-8') as f:
        b = True  # Variable booléenne pour vérifier si le mot clé est trouvé ou non

        # Parcourir tous les mots clés du fichier mots_cles.txt
        for ligne in f:
            # Vérifier si le mot clé est trouvé dans le contenu du document
            if ligne.strip().lower() in str(soup).lower():
                # Écriture du mot clé dans le fichier cadres_dataframe.txt
                with open('cadres_dataframe.txt', 'a', encoding='utf-8') as f:
                    # Écriture du mot clé dans le fichier cadres_dataframe.txt
                    f.write(ligne.strip().replace('.', '') + ';')
                    b = False  # Modifier la valeur de la variable booléenne
        # Écriture de 'None' dans le fichier cadres_dataframe.txt si le mot clé n'est pas trouvé
        if b:
            # Ouverture du fichier cadres_dataframe.txt en mode écriture
            with open('cadres_dataframe.txt', 'a') as f:
                # Écriture de 'None' dans le fichier cadres_dataframe.txt
                f.write('None;')

        # Écriture d'un saut de ligne dans le fichier cadres_dataframe.txt
        with open('cadres_dataframe.txt', 'a') as f:
            # Écriture d'un saut de ligne dans le fichier cadres_dataframe.txt
            f.write('\n')

    # Incrémenter la barre de progression
    barre_progression_documents.update(1)

barre_progression_documents.close()  # Fermer la barre de progression


# Préparation des données pour la création de la dataframe

# Ouverture du fichier cadres_dataframe.txt en mode lecture
with open('cadres_dataframe.txt', 'r', encoding='utf-8') as f:
    contenu = f.read()  # Récupération du contenu du fichier cadres_dataframe.txt

    # Remplacer la phrase 'Taxe sur la valeur ajoutée' par 'TVA'
    contenu = contenu.replace('Taxe sur la valeur ajoutée', 'TVA')

    # Remplacer les mots 'Importés' et 'Importées' par 'Importation'
    contenu = contenu.replace('Importés', 'Importation')
    contenu = contenu.replace('Importées', 'Importation')

    # Remplacer les mots 'Exportés' et 'Exportées' par 'Exportation'
    contenu = contenu.replace('Exportés', 'Exportation')
    contenu = contenu.replace('Exportées', 'Exportation')

    # Remplacer les mots 'Accises' et 'Accise' par 'Droits d'accises'
    contenu = contenu.replace('Accises', 'Droits d\'accises')
    contenu = contenu.replace('Accise', 'Droits d\'accises')

    # Remplacer la phrase 'Produits énergétiques' par 'Taxation des produits énergétiques et de l’électricité'
    contenu = contenu.replace(
        'Produits énergétiques', 'Taxation des produits énergétiques et de l’électricité')

    # Remplacer le caractère "’" par "'"
    contenu = contenu.replace('’', "'")

    # Remplacer le mot 'Douanier' par 'Douane'
    contenu = contenu.replace('Douanier', 'Douane')

    # Remplacer la phrase 'Droits d'accise' par 'Droits d'accises'
    contenu = contenu.replace('Droits d\'accise', 'Droits d\'accises')

    # Remplacer la phrase 'Droits d'accisess' par 'Droits d'accises'
    contenu = contenu.replace('Droits d\'accisess', 'Droits d\'accises')

    # Remplacer la phrase 'Union douanière' par 'Douane'
    contenu = contenu.replace('Union douanière', 'Douane')

    # Remplacer la phrase 'Tarif douanier commun' par 'Douane'
    contenu = contenu.replace('Tarif douanier commun', 'Douane')

    # Remplacer la phrase 'Importation' par 'Douane'
    contenu = contenu.replace('Importation', 'Douane')

    # Remplacer la phrase 'Exportation' par 'Douane'
    contenu = contenu.replace('Exportation', 'Douane')

    # Remplacer la phrase 'Impositions intérieures' par 'Douane'
    contenu = contenu.replace('Impositions intérieures', 'Douane')


# Remplacement des mots dans le fichier cadres_raccourcis.txt
# Ouverture du fichier cadres_raccourcis.txt en mode écriture
with open('cadres_raccourcis.txt', 'w', encoding='utf-8') as f:
    # Écriture du contenu du fichier cadre_raccourcis.txt
    f.write(contenu)

# Ouverture du fichier matieres.txt en mode lecture
with open('matieres.txt', 'r', encoding='utf-8') as f:
    contenu = f.read()  # Récupération du contenu du fichier cadres_dataframe.txt

    # Remplacer la phrase 'Taxe sur la valeur ajoutée' par 'TVA'
    contenu = contenu.replace('Taxe sur la valeur ajoutée', 'TVA')

    # Remplacer les mots 'Importés' et 'Importées' par 'Importation'
    contenu = contenu.replace('Importés', 'Importation')
    contenu = contenu.replace('Importées', 'Importation')

    # Remplacer les mots 'Exportés' et 'Exportées' par 'Exportation'
    contenu = contenu.replace('Exportés', 'Exportation')
    contenu = contenu.replace('Exportées', 'Exportation')

    # Remplacer les mots 'Accises' et 'Accise' par 'Droits d'accises'
    contenu = contenu.replace('Accises', 'Droits d\'accises')
    contenu = contenu.replace('Accise', 'Droits d\'accises')

    # Remplacer la phrase 'Produits énergétiques' par 'Taxation des produits énergétiques et de l’électricité'
    contenu = contenu.replace(
        'Produits énergétiques', 'Taxation des produits énergétiques et de l’électricité')

    # Remplacer le mot 'Douanier' par 'Douane'
    contenu = contenu.replace('Douanier', 'Douane')

    # Remplacer la phrase 'Droits d'accise' par 'Droits d'accises'
    contenu = contenu.replace('Droits d\'accise', 'Droits d\'accises')

    # Remplacer le caractère "’" par "'"
    contenu = contenu.replace('’', "'")

    # Remplacer la phrase 'Droits d'accisess' par 'Droits d'accises'
    contenu = contenu.replace('Droits d\'accisess', 'Droits d\'accises')

    # Remplacer la phrase 'Union douanière' par 'Douane'
    contenu = contenu.replace('Union douanière', 'Douane')

    # Remplacer la phrase 'Tarif douanier commun' par 'Douane'
    contenu = contenu.replace('Tarif douanier commun', 'Douane')

    # Remplacer la phrase 'Importation' par 'Douane'
    contenu = contenu.replace('Importation', 'Douane')

    # Remplacer la phrase 'Exportation' par 'Douane'
    contenu = contenu.replace('Exportation', 'Douane')

    # Remplacer la phrase 'Impositions intérieures' par 'Douane'
    contenu = contenu.replace('Impositions intérieures', 'Douane')


# Remplacement des mots dans le fichier matieres_raccourcis.txt
# Ouverture du fichier matieres_raccourcis.txt en mode écriture
with open('matieres_raccourcis.txt', 'w', encoding='utf-8') as f:
    # Écriture du contenu du fichier matieres_raccourcis.txt
    f.write(contenu)

# Ouverture des fichiers matieres_raccourcis.txt et cadres_raccourcis.txt en mode lecture
with open('matieres_raccourcis.txt', 'r', encoding='utf-8') as matieres, open('cadres_raccourcis.txt', 'r', encoding='utf-8') as cadres:
    # Ouverture du fichier matieres_final.txt en mode écriture
    with open('matieres_final.txt', 'w', encoding='utf-8') as final:
        # Parcours des lignes du fichier matieres.txt et cadres_raccourcis.txt
        for ligne_matieres, ligne_cadres in zip(matieres, cadres):
            # Si la ligne contient '-Fiscalité', on prend la ligne correspondante dans cadres_raccourcis.txt
            if '-Fiscalité' in ligne_matieres:
                final.write('-' + ligne_cadres)
            else:
                # Sinon, on copie la ligne du fichier matieres.txt dans matieres_final.txt
                final.write(ligne_matieres)
