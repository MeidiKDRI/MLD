from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.datasets import load_iris

a = [1,5,6,7,99,15]
b = sorted(a)
print(b[-1])


hist = hist, heatmap = heatmap, corr_matrix = corr_matrix, mosaic = data_mosaic


            col_selected = 'sex'
            corr_matrix = do_corr_matrix(df)
            data_mosaic = do_mosaic(df, col_selected)
            hist = do_global_hist(df)

'''lista = ['a', 'b', 'c']
listb = ['a', 'b']


def Diff(li1, li2): 
    return (list(set(li1) - set(li2))) 
  
# Driver Code 
li1 = [10, 15, 20, 25, 30, 35, 40] 
li2 = [25, 40, 35] 
print(list(set(lista) - set(listb))) 
'''

'''dic = {'1':4500, '2':9000, '3':13500 ,'4':18000}

a = 4600
keys = []

for k, v in dic.items() :
    if a > v :
        keys.append(k)
        
print(keys[-1])'''

'''            ###########################################
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
            ###########################################'''


#print([value for key, value in models.items() if element in key])


 

