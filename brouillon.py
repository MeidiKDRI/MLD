from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.datasets import load_iris

from sklearn.datasets import load_digits

file = 'iris'
test  = 'load_' + file + '()'
f = eval('load_' + file + '()')
print(f.feature_names)




#print([value for key, value in models.items() if element in key])


 

