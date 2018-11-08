# MoviesAnalysis

MachineLearning sur les metadonnées d'un film pour définir une note en se basant les goûts cinématographique de l'utilisateur.
L'analyse s'entraine sur une base de données de films dont l'utilisateur a attribué une note.

# Pré-requis
> Attention: chargement d'un venv python dans le script `run.sh`
-  python3
-  sqlite3
-  sbt
-  `pip3 install -r requirementPip.txt`

# Utilisation
>  Présence possible de bug => encore en dev.
1.  Édition de la DB sqlite dans `src/main/resources/MyVideos107.db`. 
    Il s'agit de la DB utilisée par [https://kodi.tv/](Kodi).
2.  Lancement.
    ```bash
    ./run.sh
    ```
