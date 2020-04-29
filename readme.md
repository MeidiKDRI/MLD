# Machine Learning Dashboard
MLD est une plateforme destinée à faire du machine learning sans code !  
L'application sera codée en Flask ou Dash.  

## Le concept :
Après une connexion dans son espace membre, l'utilisateur accède à l'onglet **'Data Exploration'** où il pourra charger un fichier csv ou xls.  
Dans cette partie il pourra analyser et traiter son dataset afin de visualiser les données dans l'onglet **'Data Visualization'**.  

Il pourra également tester un ou plusieurs modèles de ML, les comparer et évaluer le plus performant dans l'onglet **'Model Training'**.  

Enfin, l'utilisateur pourra faire une prédiction dans l'espace **'Model Prediction'** et enregistrer son modèle sur son ordinateur.

![Screenshot001](https://user-images.githubusercontent.com/57437129/80616232-f1f31080-8a40-11ea-904b-8acaf8181f1c.png)  

## Les features :
- Espace membres == Connexion avec identifiants et MDP. BDD des membres stockées en Nosql.  
- Import de fichier csv (et peut être xls).  
- Affichage de tableau.  
- Traitement du dataset == describes() / Traitement des manquants / Suppression, ajout de colonnes...
- Visualisation des données == hist(df), seaborn, matplotlib, Correlation matrix...  
- Sélection de un ou plusieurs modèles == Création de pipeline, entrainement modèles, affihcage du score, du temps d'exécution et d'autres métrics dans un tableau...  
- Prédiction == Affichage des prédictions et évalutation pour affinage : Cross validation, courbe ROC, Confusion Matrix...

## En cours :
Etude de faisabilité du projet sous Flask avant migration du code existant.

## Crédit :
Plateforme imaginée et développée par Meidi KADRI - Fevrier 2020.  
Projet d'étude final Formation Développeur Data IA Simplon By Microsoft - Mai 2020.
