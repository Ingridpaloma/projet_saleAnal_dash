import dash
import os
from dash import dcc, html
import pandas as pd
from dash import dash_table
from dash.dependencies import Input, Output


# Création de l'application Dash
app = dash.Dash(__name__)

app.css.append_css({
    'external_url': 'https://cdn.jsdelivr.net/npm/tachyons/css/tachyons.min.css'
})

# Lecture des données
files=[file for file in os.listdir(r'C:\Users\Ingrid\Desktop\Sales_analysis\dataBase')]
path = r'C:\Users\Ingrid\Desktop\Sales_analysis\dataBase'
all_data = pd.DataFrame()
for file in files:
    current_data = pd.read_csv(path + '\\' + file)
    all_data = pd.concat([all_data, current_data])

# Affichage des données dans le navigateur

# Affichage des données dans le navigateur
# Barre de menu
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div([
            html.A('Tableau', href='/', className='menu-item'),
            html.A('Graphiques', href='/graphiques', className='menu-item')
        ], className='menu')
    ]),
    html.Div(id='page-content')
])

# Gestion des routes pour le contenu de la page
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/graphiques':
        return html.H1('Page des graphiques')
    else:
        return html.Div([
            html.H1("Dernières ventes"),
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
        ])

# Ajouter le CSS personnalisé
app.css.append_css({
    'external_url': 'https://cdn.jsdelivr.net/npm/tachyons/css/tachyons.min.css'
})
# Lancement de l'application
if __name__ == '__main__':
    app.run_server(debug=True, port = 4050)