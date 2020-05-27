from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.datasets import load_iris


lista = ['a', 'b', 'c']
listb = ['a', 'b']


def Diff(li1, li2): 
    return (list(set(li1) - set(li2))) 
  
# Driver Code 
li1 = [10, 15, 20, 25, 30, 35, 40] 
li2 = [25, 40, 35] 
print(list(set(lista) - set(listb))) 


            ###########################################
            ###########################################
            ##### FOR TEST ONLY #######################
            ###########################################
            data = df.copy()
            data.drop(['cabin', 'body', 'boat', 'home.dest'], axis = 1, inplace = True)
            data.dropna()
            data['age'] = data['age'].fillna(data.groupby(['pclass', 'sex'])['age'].transform('mean'))
            data.head()
            data.dropna(axis = 0, inplace = True)

            dummies = pd.get_dummies(data['pclass'])
            data = pd.concat([data, dummies], axis = 1)
            data.drop(['pclass', 3.0], inplace = True, axis = 1)

            dummies = pd.get_dummies(data['sex'])
            data = pd.concat([data, dummies], axis = 1)
            data.drop(['sex', 'male'], inplace = True, axis = 1)

            dummies = pd.get_dummies(data['embarked'])
            data = pd.concat([data, dummies], axis = 1)
            data.drop(['embarked', 'C'], inplace = True, axis = 1)





            ###########################################
            ###########################################
            ##### FOR TEST ONLY #######################
            ###########################################


#print([value for key, value in models.items() if element in key])


 

