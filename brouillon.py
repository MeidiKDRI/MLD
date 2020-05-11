from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier

classif_selector = ['KNN',
                'KMeans',
                'Random Forest Classifier',
                'Decision Tree Classifier']

models = {'KNN' : KNeighborsClassifier(n_neighbors = 10),
        'Random Forest Classifier' : RandomForestClassifier(),
        'Decision Tree Classifier' : DecisionTreeClassifier(),
        'SGDClassifier' : SGDClassifier()
        }

mods = {}
for element in classif_selector :
    for k, v in models.items() :
        if k == element :
            mods[k] = v
    
print(mods)  
    
    




#print([value for key, value in models.items() if element in key])


 

