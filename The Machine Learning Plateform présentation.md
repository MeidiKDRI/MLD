# The Machine Learning Plateform

> ### *Perform your data analyst and machine learning without any line of code !*



### Le concept :

The **Machine Learning Plateform** (MLP) est une application Flask permettant de faire de l'analyse de données ainsi que du Machine Learning (ML) via une interface graphique.

L’idée est de pouvoir effectuer toutes les étapes de ML sur une plateforme, **sans aucune ligne de code**.

<img src="F:\Programmation\Projets\Python\Machine Learning\Dash\MLP_Flask\static\img\Screenshot004.png" alt="Screenshot004" style="zoom:50%;" />

**MLP** est un projet imaginé en début d’année. Lors de la formation je me suis aperçu que le process pour faire du ML était sensiblement le même :

- Import et lecture d'un fichier.
- Exploration des données.
- Visualisation des datas pour mieux les comprendre.
- Sélections des features qui nous intéressent pour préparer le modèle.
- Entraînement du modèle avec un split en ```test_set``` et ```train_set``` et une standardisation si besoin.
- Évaluation du modèle et affinage des hyperparamètres.
- Prédiction.
- Export pour une utilisation future...

Bien sûr, ces étapes peuvent s'effectuer de plusieurs façons. Et il nous faut essayer différentes librairies et modules via de nombreuses lignes de codes sur Jupyter pour observer les données, les comprendre et les faire parler... Cela peut prendre énormément de temps. Pour parfois s'apercevoir finalement que l'on est sur une mauvaise piste !

C'est pourquoi j'ai eu l'idée de développer un outil qui me permettrait de gagner en productivité. Remplacer une ou plusieurs lignes de codes par un "simple" bouton sur une interface nous permettrait d'être plus rapide sans perdre en efficacité. 

### Le workflow et Fonctionnalités :

Dans cette version que je qualifie de Beta, le workflow est orienté par le menu de l'application. Invitant  ainsi l'utilisateur à passer par chaque page qui représente une étape du process de ML.

![](F:\Programmation\Projets\Python\Machine Learning\Dash\MLP_Flask\static\img\Screenshot008.png)

#### Dataset Upload :

Ici, l'utilisateur peut récupérer un dataset présent sur son disque dur ou bien utiliser l'un des 3 datasets de la librairie scikit learn importées directement dans l'app.

Une fois téléchargé, le dataset est affiché dans une table ainsi que diverses informations utiles comme le nom, nombre de lignes et de colonnes. Trois tableaux viennent apporter d'autres informations utiles sur le jeu de données comme un describe, les infos sur les types de datas de chaque colonne et un résumé du nombre de valeurs manquantes par colonne.

 #### Dataset Exploration :

Explorer un jeu de données est d'une importance capitale. De nombreuses options s'offrent à l'analyste. Malheureusement, il ne m'aura pas été possible de toutes les proposer dans cette version.

Cependant, comme dans chacune des étapes de l'application, mon objectif était d'inclure un minimum de fonctionnalités afin de faire la démonstration du concept de MLP.

Ainsi sont disponibles les fonctionnalités suivantes :

- **Drop NaN** : Supprimer les lignes comportant des valeurs manquantes (NaN) sur une ou plusieurs colonnes.
- **Fill NaN Values** : Remplacer les NaN d'une colonne soit par la moyenne, la médiane ou une valeur définie par l'utilisateur.
- **Drop duplicates** : La possibilité de supprimer les lignes en double dans le dataframe en filtrant sur une colonne sélectionnée par le user.
- **Drop Column** : Suppression d'une ou plusieurs colonnes sélectionnées par le user.  

#### Dataset Visualization :

<img src="C:\Users\majes\AppData\Roaming\Typora\typora-user-images\image-20200531021323587.png" alt="image-20200531021323587" style="zoom:50%;" />

Comme une image vaut mieux que 1000 mots, les graphiques sont largement utilisés pour observer et trouver ou confirmer des relations entre plusieurs données.  C'est ici que nous pourrons afficher les graphes suivants :

- **Heatmap** : Afin d'identifier les valeurs manquantes ou nulles.

- **Histogramme** : La fonction Hist nous permet d'observer les distributions de tout le dataset ou d'une colonne en particulier.

- **Mosaic** : La fonction "mosaic" nous aide à visualiser la répartition de deux ou plusieurs variables qualitatives. Par exemple une variable explicative et la target.

- **Plot** : Dans cette version un simple scatter plot de seaborn est disponible.

- **Correlation Matrix** : Une matrice de corrélation afin d'observer les corrélation entre les varibales.


#### Model Training :

C'est ici que nous allons pouvoir faire tourner nos modèles.

Grâce à l'analyse des variables précédentes, nous pouvons désormais sélectionner une cible [Target Y] ainsi que les variables pour entraîner le ou les modèles. 

Une partie preprocessing sera également disponible pour gérer les dummies et les standardisations.

Nous pouvons définir la répartition de notre split avec la fonction **test_size**, puis il nous reste plus qu'à choisir les modèles que nous souhaitons essayer. Dans cette version sont disponibles :

- **Régression** : Logistique et Linéaire.
- **Classification** : KNN, KMeans, Random Forest Classifier, Decision Tree et SGDClassifier.

Un tableau affiche les scores des modèles entrainés pour que l'utilisateur puisse choisir le plus performant à exporter.

<img src="C:\Users\majes\AppData\Roaming\Typora\typora-user-images\image-20200531022254565.png" alt="image-20200531022254565" style="zoom:80%;" />

#### Prédiction & Export :

Dans cette page, le user peut observer la pertinence des prédictions du modèle choisit.

Sera disponible une **Matrice de confusion** ainsi qu'un tableau affichant les prédictions et des outils comme la **Courbe RoC** pour optimiser les hyperparamètres du modèle.

#### Sauvegarde des fichiers :

Sur chaque page, l'utilisateur peut enregistrer divers fichiers dans une base de données afin de garder une trace de son travail.

- **Tableaux** : En format csv.
- **Graphiques** : En format png.
- **Modèles **: En format pikle.
- **Pages** : En format pdf.

#### User :

Pour accéder à la plateforme, l'utilisateur doit s'enregistrer. Pour cela j'ai utiliser l'api d'authentification de Google **Firebase**. Cette librairie est assez puissante et permet de gérer les modifications/ pertes de mots de passe, les connexions aux bases de données et la sécurité.

Le user_id permet ensuite de créer des bases de données directement liées à un utilisateur précis. **Firebase database** est une base de données NoSql réactive et plutôt robuste. Mais surtout facile à utiliser.

C'était un choix pertinent pour mon projet car firebase offre aussi un service pour stocker les images, csv, pdf et modèles grâce à **firebase storage**.

### Technologies utilisées :

#### Flask:

Il s'agit d'une application Flask. Le code contient donc une partie en Python et une partie HTML. A cela s'ajoute un fichier CSS et Javascript/ Ajax pour ajouter du design et du dynamisme au projet. Pour ajouter du style, j'ai également utilisé Bootstrap.

#### Firebase :

Comme indiqué plus haut,  pour gérer la base de données, le stockage et les authentifications j'ai utilisé la librairie Python **Pyrebase** qui permet d'utiliser l'API de google Firebase.

- **Authentication **: Permet de gérer les connexions au site, de créer des identifiants utilisateur réutilisables pour les bases de données. Un système de gestion des pertes ou modifications de mots de passe est également inclus.
- **Database**: Base de données NoSQL.
- **Storage** : Base de données de stockage pour les graphiques, les pages et les tableaux du projet.





### Commentaires :

Ce projet a été très enrichissant pour moi. Il représente une **Proof Of Skills** assez intéressante qui démontre ma capacité à imaginer des outils de productivité, et à trouver des solutions pour les concevoir. Je suis assez satisfait du résultat mais je reste mobiliser car cette version est bien trop basique.

En effet, je pense avoir sous évaluer la charge de travail et le délai nécessaire pour mener à bien la mission et intégrer la totalité des fonctionnalités que j'avais en tête.

J'ai également perdu du temps sur certaines problématiques comme la gestion de l'asynchrone avec Ajax ou XML. Je cherchais une dynamique aussi efficace que RShiny. Je pense que cela viendra avec les futures mises à jour.

Il s'agit ici d'un projet de démonstration du concept de **Machine Learning Plateform**. Il reste encore beaucoup de travail pour que cette application soit à la hauteur de ce que je souhaite. Je continuerai à y consacrer du temps pour l'optimiser autant que possible.