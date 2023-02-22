![Alt text](https://github.com/molly-muffin/P10_OC_SoftDesk/blob/main/images/logo.PNG)

# API sécurisée RESTful pour gérer les problèmes techniques

## Contexte du projet : 
SoftDesk, une société d'édition de logiciels de développement et de collaboration, a décidé de publier une application permettant de remonter et suivre des problèmes techniques (issue tracking system). Cette solution s’adresse à des entreprises clientes, en B2B.


### Le site permet  :
De créer divers projets, d'ajouter des utilisateurs à des projets spécifiques, de créer des problèmes au sein des projets et d'attribuer des libellés à ces problèmes en fonction de leurs priorités, de balises, etc.

Voici les différentes spécifications techniques de l'API :

- **Authentification des utilisateurs** 
    Utilisation de JWT pour authentifier les utilisateurs.

- **Un projet** peut être défini comme une entité ayant plusieurs collaborateurs (utilisateurs), et chaque projet peut contenir plusieurs **problèmes**. Un projet ne doit être accessible qu'à son responsable et aux contributeurs. 

- Seuls les **contributeurs** sont autorisés à créer ou à consulter les **problèmes** d'un projet.

- Seuls les **contributeurs** peuvent créer (Create) et lire (Read) les **commentaires** relatifs à un problème. En outre, ils ne peuvent les actualiser (Update) et les supprimer (Delete) que s'ils en sont les auteurs

- **Un commentaire** doit être visible par tous les contributeurs du projet, mais il ne peut être actualisé ou supprimé que par son auteur



### Environnement de développement :
`Django`


### Instruction d’installation et d’utilisation :
- Prérequis et installation
    - Dans le terminal, aller dans le dossier ou vous souhaitez placer le projet et copier le projet 
    ```bash
    git clone https://github.com/molly-muffin/P10_OC_SoftDesk.git
    ```
    - Aller dans ce dossier
    ```bash
    cd P10_OC_SoftDesk\api\
    ```
    - Créer un environnement virtuel
    ```bash
    python -m venv env
    ```
    - Activer le script
    
    **Windows :**
    ```bash
    .\env\Scripts\activate
    ```
    **Linux :**
    ```bash
    source env\bin\activate
    ```
    - Installer les packages dans le requirements.txt
    ```bash
    pip install -r requirements.txt
    ```

- Lancement
    - Lancer le  **serveur local**, avec la commande
    ```bash
    python manage.py runserver
    ```
    - Puis rendez vous sur http://127.0.0.1:8000/login/ et accéder à la page d'authentification de l'API. Le fichier de données db.sqlite3 sera automatiquement chargé.


- Utilisation
    - Vous retrouverez tous les points de terminaisons de l'API et leur utilisation dans la documentation Postman : https://documenter.getpostman.com/view/23897812/2s93CLrYMV


    - Si vous souhaitez avoir accès à l'intégralités des données de l'API vous avez le pnael admin disponible sur http://127.0.0.1:8000/admin/ **- Username :** Admin **- Password :** AdminP@assword


### Vérification du code
- Contrôle du code avec **flake8** :
```bash
flake8 --max-line-length 130 --format=html --htmldir=flake-report --exclude=migrations
```


> Laureenda Demeule
> OpenClassroom

