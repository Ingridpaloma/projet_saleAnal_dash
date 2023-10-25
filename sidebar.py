# Code source: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import os
from dash import dash_table
import datetime
#import dash_html_components as html
#import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# data source: https://www.kaggle.com/chubak/iranian-students-from-1968-to-2017
# data owner: Chubak Bidpaa

# Lecture des données
files=[file for file in os.listdir(r'C:\Users\Ingrid\Desktop\Sales_analysis\dataBase')]
path = r'C:\Users\Ingrid\Desktop\Sales_analysis\dataBase'
all_data = pd.DataFrame()
for file in files:
    current_data = pd.read_csv(path + '\\' + file)
    all_data = pd.concat([all_data, current_data])

all_data.to_csv(path+'/New_Data.csv',index=False)

all_data=all_data.dropna(how='all')

def month(x):
    return x.split('/')[0]

def city(x):
    if ',' in x:
        return x.split(',')[1]
    else:
        return ''

all_data['city'] = all_data['Purchase Address'].apply(city)

all_data['Month']=all_data['Order Date'].apply(month)


all_data=all_data[all_data['Month']!='Order Date']

all_data['Month']=all_data['Month'].astype(int)

all_data['Hour'] = pd.to_datetime(all_data['Order Date'], format='%m/%d/%y %H:%M').dt.hour
keys = []  
hours = []

for key, hour in all_data.groupby('Hour'):
    keys.append(key)
    hours.append(len(hour))

all_data['Quantity Ordered'] = all_data['Quantity Ordered'].astype(float)
all_data['Price Each']=all_data['Price Each'].astype(float)
all_data['Product']=all_data['Product'].astype(str)

#SUPPRESSION DES DOUBLONS
all_data.drop_duplicates(inplace=True)

#PASSONS A L'OPERATION, ventes realisées par jour
all_data['Sales']=all_data['Quantity Ordered']*all_data['Price Each']

sales_by_month = all_data.groupby("Month")["Sales"].sum()

product_order = all_data.groupby('Product')['Quantity Ordered'].sum()

price = all_data.groupby('Product')['Price Each'].mean()

# Créer un graphique en utilisant Plotly
fig = go.Figure(data=go.Bar(x=sales_by_month.index, y=sales_by_month.values))
fig_product = go.Figure(data=go.Bar(x=product_order.index, y=product_order.values))
fig_commandes = go.Figure(data=go.Bar(x=all_data.groupby('city')['city'].count().index, y=all_data.groupby('city')['city'].count()))
fig_prix = go.Figure(data=go.Scatter(x=price.index, y=price, mode='lines+markers'))
fig_pub = go.Figure(data=go.Scatter(x=keys, y=hours, mode='lines+markers'))

# Configurer le layout du graphique
fig.update_layout(
    title="Évolution des ventes par mois",
    xaxis=dict(title="Mois"),
    yaxis=dict(title="Ventes"),
    plot_bgcolor="white",
    paper_bgcolor="lightgray",
    font=dict(color="black")
)

fig_pub.update_layout(
    title="Évolution des commandes dans la journée",
    xaxis=dict(title="heure de la journée"),
    yaxis=dict(title="nombre de commandes"),
    plot_bgcolor="white",
    paper_bgcolor="lightgray",
    font=dict(color="black")
)

fig_commandes.update_layout(
    title="Nombre de commandes par ville",
    xaxis=dict(title="Ville"),
    yaxis=dict(title="Nombre de commandes"),
    plot_bgcolor="white",
    paper_bgcolor="lightgray",
    font=dict(color="black")
)

fig_product.update_layout(
    title="Nombre de ventes par produit",
    xaxis=dict(title="produit"),
    yaxis=dict(title="Quantité vendu"),
    plot_bgcolor="white",
    paper_bgcolor="lightgray",
    font=dict(color="black")
)

fig_prix.update_layout(
    title="Prix des produits",
    xaxis=dict(title="Produit"),
    yaxis=dict(title="Prix"),
    plot_bgcolor="white",
    paper_bgcolor="lightgray",
    font=dict(color="black")
)

fig_imp = go.Figure()
fig_imp.add_trace(go.Bar(
    x=product_order.index,
    y=product_order.values,
    name="Quantité de commandes",
    marker_color='blue'
))

fig_imp.add_trace(go.Scatter(
    x=price.index,
    y=price,
    mode='lines+markers',
    name="Prix",
    marker=dict(
        color='orange',
        size=8,
        symbol='circle'
    )
))

fig_imp.update_layout(
    title="Quantité de commandes et prix par produit",
    xaxis=dict(title="Produit"),
    yaxis=dict(title="Quantité de commandes / Prix"),
    plot_bgcolor="white",
    paper_bgcolor="lightgray",
    font=dict(color="black")
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{"name": "viewport", "content": "width=device-width"}])

current_date = datetime.date.today()
formatted_date = current_date.strftime("%B %d, %Y ")
current_time = current_date.strftime("%H:%M:%S")

# styling the sidebar

BAR_STYLE = {
  "position": "fixed",
  "top": 0,
  "left": 0,
  "width": "100%",
  "height": "6rem", #Changer la hauteur souhaitée 
  "padding": "2rem 1rem",
  "background-color": "#f8f9fa",
  "text-align": "center"
}

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": '6rem',
    "left": '0rem',
    "height": "120rem",
    "bottom": 0,
    "width": "15%",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-top": "10rem",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

bar = html.Div(
    [
        html.H1("Data Sales Analysies", className="display-4"),
        #html.Hr(),
    ],
    style=BAR_STYLE,
)

sidebar = html.Div(
    [
        html.P(
            "Number of students per education level", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content,
    bar
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        total_records = len(all_data)
        all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']  # Ajouter une colonne pour les ventes (quantité * prix unitaire)
        total_sales = all_data['Sales'].sum()  # Calculer la somme totale des ventes
        num_cities = all_data['Purchase Address'].apply(lambda x: x.split(",")[1].strip()).nunique()  # Compter le nombre de villes distinctes
        num_products_sold = all_data['Quantity Ordered'].sum()  # Calculer le nombre total de produits vendus
        return [
            html.Div([
                  html.Div([
                    html.H6('Last Updated: ' + formatted_date + ' ' + current_time + ' (UTC)',
                    style={'color': 'orange'}),

        ], className="one-third column", id='title1'),           
            ], id="header", className="row flex-display", style={"margin-bottom": "25px", "margin-left": "1rem"}),
        html.Div([
            html.Div([
                html.H6(children='NOMBRE TOTAL DE VENTES',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

                html.P(f"{total_records:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 30}
                   ),
            ], className="card_container two columns",),
            html.Div([
                html.H6(children='SOMME TOTAL DES VENTES',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

                html.P(f"{total_sales:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 30}
                   ),
            ], className="card_container two columns",),
            html.Div([
                html.H6(children='NOMBRE DE VILLE DISPONIBLE',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

                html.P(f"{num_cities:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 30}
                   ),
                   ], className="card_container two columns",),
            html.Div([
                    html.H6(children='NOMBRE DE PRODUITS VENDU',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

                    html.P(f"{num_products_sold:,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': '#e55467',
                       'fontSize': 30}
                   ),
                ], className="card_container two columns")
                            ]),
                
                html.Div([
                    html.Div([
                        dcc.Graph(
            id='sales-graph',
            figure=fig
        )
                    ], className="create_container five columns"),
                    html.Div([
                        dcc.Graph(
            id='commandes-graph',
            figure=fig_commandes
        )
                    ], className="create_container five columns"),

                ]),
                html.Div([
                    html.Div([
                        dcc.Graph(
            id='produits-graph',
            figure=fig_product
        )
                    ], className="create_container five columns"),
                html.Div([
                        dcc.Graph(
            id='produits-graph',
            figure=fig_prix
        )
                    ], className="create_container five columns"),
                ]),

                html.Div([
                    html.Div([
                        dcc.Graph(
            id='produits-graph',
            figure=fig_imp
        )
                    ], className="create_container dix columns"),
                ]),
                html.Div([
                    html.Div([
                        dcc.Graph(
            id='heures-graph',
            figure=fig_pub
        )
                    ], className="create_container dix columns"),
                ])
                ]
    elif pathname == "/page-1":
        return [
            html.Div([
            html.H1("Dernières ventes", style={'color': 'white'}),
            dash_table.DataTable(
        id='sales-table',
        columns=[{"name": col, "id": col} for col in all_data.columns],
        data=all_data.tail(10).to_dict('records'),
        style_cell={
            'textAlign': 'left',
            'color': 'black',  # Couleur du texte
            'backgroundColor': 'white'  # Couleur de fond bleu sombre
        },
        style_header={
            'backgroundColor': '#001f3f',  # Couleur de fond bleu sombre pour l'en-tête
            'color': 'white',
            'fontWeight': 'bold'  # Style de police en gras pour l'en-tête
        }
    )
        ], className="row flex-display")
             
                ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__=='__main__':
    app.run_server(debug=True, port=3000)
    