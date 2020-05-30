# The Machine Learning Plateform

> ### *Perform your data analyst and machine learning without any line of code !*



### Le concept :

The Machine Learning Plateform (MLP) est une application Flask permettant de traiter des cas de Machine Learning ainsi que d’essayer des modèles, de les évaluer et de les exporter.

L’idée est de pouvoir effectuer toutes les étapes de machine learning via **une plateforme, sans aucune ligne de code**.

<img src="F:\Programmation\Projets\Python\Machine Learning\Dash\MLP_Flask\static\img\Screenshot004.png" alt="Screenshot004" style="zoom:50%;" />

**MLP** est un projet imaginé en début d’année. Lors de la formation je me suis aperçu que le process pour faire du Machine Learning (ML) était sensiblement le même :

- Import et lecture d'un fichier.
- Exploration des données.
- Visualisation des datas pour mieux les comprendre.
- Sélections des features qui nous intéressent pour préparer le modèle.
- Entraînement du modèle avec un split en ```test_set``` et ```train_set```.
- Évaluation du modèle et affinage des hyperparamètres.
- Prédiction.
- Export pour une utilisation future...

Bien sûr, ces étapes peuvent s'effectuer de plusieurs façons. Et il nous faut essayer des tas de lignes de codes sur Jupyter pour observer les données, les comprendre, les faire parler... Cela peut prendre énormément de temps. Pour parfois s'apercevoir que l'on est sur une mauvaise ou bonne piste !

C'est pourquoi j'ai eu l'idée de développer un outil qui me permettrait de gagner en productivité en supprimant les tâches inutilement répétitives. En effet, à chaque cas et projet, nous avons dû écrire les mêmes lignes de codes à chaques mêmes étapes.

Il va de soit que chaque étude est différente. Il existe une multitude de possibilité d'analyse. Cependant, je suis convaincu qu'une première approche, une première observation, évaluation et test de modèle sur un dataset via cette plateforme peut aider à gagner du temps, et orienter nos projets vers une piste en peu de temps.