import base64
import datetime
import io

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import numpy as np
import pandas as pd
import dash_table as dt

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression, SGDClassifier

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report

import datetime
import time
from time import strftime, gmtime
import seaborn as sns

# Init a bootstrap theme
app = dash.Dash(external_stylesheets=[dbc.themes.CERULEAN])

########################## PROJET FINAL ############################################


######################################################################################################
#############       Start Manual preprocessing      ##################################################
######################################################################################################
directory = 'F:\Programmation\Projets\Python\Machine Learning\Dash\ML_Dash'
data = pd.read_csv(directory + '/data/titanic.csv')
data1 = data.copy()
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

X = data.drop(['survived', 'ticket', 'name'], axis = 1)
y = data['survived']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 123456)
######################################################################################################
#############       End Manual preprocessing      ####################################################
######################################################################################################


#######################################
##### User Interface
########################################

# Mean Layout of the app
app.layout = html.Div(
    [
        dcc.Location(id="url"),
        
        # NavBar Menu
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("Data Visualization", href="/viz_page", id = "page-1-link"),
                dbc.NavLink("Preprocessing", href="/preprocessing_page", id = "page-2-link"),
                dbc.NavLink("Model Training", href="/train_page", id = "page-3-link"),
                dbc.NavLink("Model Prediction", href="/predic_page", id = "page-4-link"),
            ],
            brand="Machine Learning Dashboard",
            color="primary",
            dark=True,
        ),
        
        # Tab container
        dbc.Container(id="page-content", className="pt-10"),
    ]
)

# Control panel card
card_viz = [
    dbc.CardHeader("Visualization Control Panel"),
    dbc.CardBody(
        [
        # outline set a hover style btn
        dbc.Button("heatmap", color="primary", outline=True, block = True),
        html.Hr(),
        dbc.Button("hist", color="primary", outline=True, block = True),
        html.Hr(),
        dbc.Button("sns", color="primary", outline=True, block = True),
        html.Hr()
        ],
    ),
]

# Visu Tab
viz_page = dbc.Container(
    [
    dbc.Row([html.H2('Data Visualization')]),# row 1
    html.Hr(),
    
    dbc.Row(# row 2
        [
            dbc.Col(dbc.Card(card_viz), md=3), # col 1
            
            dbc.Col([ # col 2
                dbc.Row([  # col 2 row 1
                                                               
                    dbc.Card([dcc.Upload(
                        id='upload-data',
                        children = html.Div([
                            'Drag and Drop or ', 
                            html.A('Select Files',                                                      
                                    style={'font-weight': 'bold',
                                           'color': '#191FED'})
                            ]),
                        style={'textAlign': 'center',
                               'margin': '10px'},
                        # Allow multiple files to be uploaded
                        multiple= True
                        )]),
                    

                    ]),
                dbc.Row( # col 2 row 2
                    html.Div(id='output-data-upload'),
                    style={'textAlign': 'center', 'margin': '20px'},
                    className='six columns'),
                            
                
                dbc.Row(
                    dt.DataTable(
                        id = 'data1_table',
                        columns = [{'name': i, 'id': i, } for i in (data1.columns)],
                        data = data1.to_dict('record'),
                        style_cell={'textAlign' : 'center'},
                        style_table={'minWidth': '0px',
                                     'maxWidth': '830px',
                                     'overflowX': 'scroll',
                                     'maxHeight':'300px',
                                     'overflowY':'scroll',
                                     'border': 'thin lightgrey solid'}
                    )
                )          

                ])
            ]
        )
    ]
)

#data1tDT = dt.DataTable(data = data1, columns = columns)
# Control panel card
preproc_card = [
    dbc.CardHeader("Pre Processing Control Panel"),
    dbc.CardBody(
        [

        ],
    ),
]

# Preprocessing Page
preprocessing_page = dbc.Container(
    [
        dbc.Row([html.H2("PreProcessing")]),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Col(dbc.Card(preproc_card), md=3),
            dbc.Col([
                dbc.Row([
                    # Put some stuffs over here !
                    ])
                ])                
            ])
        ])    
    ]
)

# Control panel card
card_train = [
    dbc.CardHeader("Training Control Panel"),
    dbc.CardBody(
        [
        html.H5('Regression'),
        dcc.Dropdown(
            id = 'reg_model_ddmenu',
            options=[
                {'label': 'Linear Regressor', 'value': 'Linear Regression'},
                {'label': 'Logistic Regression', 'value': 'Logistic Regression'}
                ],
            multi=True,
            placeholder= 'Select a model'
        ),
        html.Hr(),
        html.H5('Classification'),
        dcc.Dropdown(
            id = 'classi_model_ddmenu',
            options=[
                {'label': 'KNN', 'value': 'KNN'},
                #{'label': 'KMeans', 'value': 'KMeans'},
                {'label': 'Random Forest', 'value': 'Random Forest Classifier'},
                {'label': 'Decision Tree', 'value': 'Decision Tree Classifier'},
                {'label': 'SGDClassifier', 'value' : 'SGDClassifier'}
                ],
            multi=True,
            placeholder= 'Select a model'
        ),
      
        html.Hr(),
        # outline set a hover style btn
        dbc.Button("Train", id = "train_btn", color="primary", outline=True, block = True),
        html.Hr()
        ],
    ),
]
 
# Training Page
train_page = dbc.Container(
    [
        
        dbc.Row([html.H2("Model Training Page")]),
        html.Hr(),
        dbc.Row(
            [
            dbc.Col(dbc.Card(card_train), md=3),
            html.Hr(),          
            dbc.Col([
                html.H5('Regression'),
                html.Div(id='reg_mod_ddmenu_output'),
                html.Hr(),
                html.H5('Classification'),
                html.Div(id='classi_mod_ddmenu_output'),
                html.Hr(), 
                html.H5('Training results'),   
                html.Div(id="train_btn_output", style={"vertical-align": "middle"})                                             
                ])
            ]
        )    
    ]
)

# Predictions panel card
predict_card = [
    dbc.CardHeader("Prediction Control Panel"),
    dbc.CardBody(
        [

        ],
    ),
]
#Prediction Page
prediction_page = dbc.Container(
    [
        dbc.Row([html.H2("Model Prediction Page")]),
        html.Hr(),
        
        dbc.Row([
            dbc.Col([
                dbc.Col(dbc.Card(predict_card), md=3),
            dbc.Col([
                dbc.Row([
                    # Put some stuffs over here !
                    ])
                ])                
            ])
        ])                   
    ]
)

#######################################
#####        Server
########################################

app.config.suppress_callback_exceptions=True

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/preprocessing_page"]:
        return preprocessing_page
    elif pathname == "/viz_page":
        return viz_page
    elif pathname == "/train_page":
        return train_page
    elif pathname == "/predic_page":
        return prediction_page
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

#######################################
##### Import file with drag and drop 
########################################

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('ISO-8859-1')), sep="\s+|;|:|,")
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename, style={'textAlign':'left'}),
        dash_table.DataTable(
            data = df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_cell={'textAlign' : 'center'},
            style_table={'overflowX': 'scroll',
                         'maxHeight':'320px',
                         'overflowY':'scroll'},
            style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
        )
    ])
    
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])

def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

#######################################
##### Train Page 
########################################

### Dropdown Menu Models
############
### Regression

reg_list = []
reg_selector = ['Linear Regression', 'Logistic Regression']

@app.callback(
    dash.dependencies.Output('reg_mod_ddmenu_output', 'children'),
    [dash.dependencies.Input('reg_model_ddmenu', 'value')])

def update_output(reg_value):
    for i in range(len(reg_selector)) :
        # We compare the select input with our list of models
        if reg_selector[i] in reg_value :
            # If the model is not in the list we add it
            if reg_selector[i] not in reg_list :
                reg_list.append(reg_selector[i])
            
    return 'Model(s) selected : {}'.format(reg_value)

##################
### Classification

classif_list = []
classif_selector = ['KNN',
                'KMeans',
                'Random Forest Classifier',
                'Decision Tree Classifier',
                'SGDClassifier']

@app.callback(
    dash.dependencies.Output('classi_mod_ddmenu_output', 'children'),
    [dash.dependencies.Input('classi_model_ddmenu', 'value')])

def update_output(classif_value):
    for i in range(len(classif_selector)) :
        # We compare the select input with our list of models
        if classif_selector[i] in classif_value :
            # If the model is not in the list we add it            
            if classif_selector[i] not in classif_list :
                classif_list.append(classif_selector[i])
                
    return 'Model(s) selected : {}'.format(classif_value)

##########################
### Training button handler

@app.callback(
    Output("heatmap_return", "children"), [Input("heatmap_btn", "n_clicks")]
)

def on_heatmap_click(click) :
    if click is None :
        return ''
    else :
        fig = data1.hist(data1['survived'])
        return fig
        


# Empty list & dict for the training loop management
models_list = []
mods = {}

@app.callback(
    Output("train_btn_output", "children"), [Input("train_btn", "n_clicks")]
)

def on_button_click(click):
    if click is None :
        return ''
    else :
        # We concat the 2 models lists
        models_list = reg_list + classif_list
        if len(models_list) == 0 :
            return 'No model selected. Please select at least one model.'
        else :
            
            # Training Loop        
            models = {'Linear Regression': LinearRegression(),
                      'Logistic Regression' : LogisticRegression(solver= 'lbfgs', max_iter= 10000),
                      'KNN' : KNeighborsClassifier(n_neighbors = 10),
                      'Random Forest Classifier' : RandomForestClassifier(),
                      'Decision Tree Classifier' : DecisionTreeClassifier(),
                      'SGDClassifier' : SGDClassifier()
                      }
            
            # Check element in the moelds list is in the models dict
            for element in models_list :
                for k, v in models.items() :
                    if k == element :
                        # Add the key and value model in a new dict
                        mods[k] = v

            # Empties lists for the result dataTable
            model_list = []
            model_list = []
            runtime_list = []
            scor_list = []
            csv_list = []

            for k, v in mods.items() :
                
                start_time = time.time()                
                model = v
                model = model.fit(X_train, y_train)
                runtime = time.time() - start_time

                model_list.append(k)
                runtime_list.append(strftime("%H:%M:%S", gmtime(runtime)))

                # Scores
                scor = model.score(X_train, y_train)
                scor_list.append(round(scor, 3))

                y_predict = model.predict(X_test)
                
            # We pass all statistics into a dataframe to compare models
            result = pd.DataFrame({'Model ' : model_list,
                                   'Run time' : runtime_list,
                                   'Accuracy Score' : scor_list})
            
            # dataframe to datatable transformation
            results = result.to_dict('rows')
            columns = [{'name': i, 'id': i, } for i in (result.columns)]
            resultDT = dt.DataTable(data = results, columns = columns)
            
            return resultDT

if __name__ == "__main__":
    # dev_tools_ui=True affiche les erreurs dans l'UI. False permet de ne pas les afficher
    app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=False)