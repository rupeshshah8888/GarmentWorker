import pandas as pd

pd.set_option('max_rows',20)
import plotly.io as pio
pio.renderers.default = "browser"
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash

# Connect to main app.py file
from app import app

from apps import GarmentWorkerAgricultureround3 , GarmentworkersAgricultureround2
from apps import GarmentWorkersLivehoodround2 , GarmentWorkersLivehoodround3
from apps import GarmentWorkersSocialIssuesround2 , GarmentWorkersSocialIssuesround3
from apps import GarmentWorkersOverviewround2 , GarmentWorkersOverviewround3
from apps import GarmentWorkersHeathround2 , GarmentWorkersHeathRound3
from apps import GarmentWorkersMigrationround2 , GarmentWorkersMigrationround3
from apps import GarmentWorkersEducationround3 , GarmentWorkersEducationround2
from apps import GarmentWorkerSchemesandentitlementround2 , GarmentWorkerSchemesandentitlementround3
from apps import GarmentWorkersAccesstoFoodround2,GarmentWorkersAccesstoFoodround3
def buttonstyle():
    return {'text-align': 'center', 'font-size': '20px',
                                           'background-color': '#FF8C00',
                                             'color': 'white',
                                              'text-align': 'center',
                                              'text-decoration': 'none',
                                              'display': 'inline-block',
                                              'margin': '4px 2px',
                                                }


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div(
            [

                html.Div([
                    dbc.Button("Overview",style=buttonstyle(), className="mr-1",href="/apps/GarmentWorkerOverview"),
                    dbc.Button("Access of Food", style=buttonstyle(),className="mr-1", href="/apps/GarmentWorkerAccessofFood"),
                    dbc.Button("Agriculture",style=buttonstyle(), className="mr-1",href="/apps/GarmentWorkerAgriculture"),
                    dbc.Button("Livelihood",style=buttonstyle(), className="mr-1",href="/apps/GarmentWorkerLivelihood"),
                    dbc.Button("Education", style=buttonstyle(), className="mr-1",
                               href="/apps/GarmentWorkerEducation"),

                    dbc.Button("Social Issues",style=buttonstyle(), className="mr-1",href="/apps/GarmentWorkerSocialIssues"),
                    dbc.Button("Health",style=buttonstyle(), className="mr-1",href="/apps/GarmentWorkerHealth"),
                    dbc.Button("Schemes and Entitlements",style=buttonstyle(), className="mr-1",href="/apps/GarmentWorkerSchemesandEntitlements"),
                    dbc.Button("Migration", style=buttonstyle(),className="mr-1",href="/apps/GarmentWorkerMigration"),

                ],style={'font-size':20}),






            ],
            style={"display": "flex", "flexWrap": "wrap"},
),



    ], className="row" , style={'padding-right': '10%', 'padding-left': '10%', }),
    dcc.Dropdown(id='Roundtest',options=[{'label': 'Round 2', 'value': 'Round2'},
                                         {'label': 'Round 3', 'value': 'Round3'},],value='Round2'),
    html.H1(id='data' )              ,
    html.Div(id='page-content', children=[])
] , style={'padding-right': '0%', 'padding-left': '0%'}
)


@app.callback(Output('page-content', 'children'),

              [Input('url', 'pathname'),
               Input('Roundtest', 'value')

               ])
def display_page(pathname , round):
    round=pathname+round
    if round == '/apps/GarmentWorkerOverviewRound2':
        return GarmentWorkersOverviewround2.layout
    elif round == '/apps/GarmentWorkerOverviewRound3':
        return GarmentWorkersOverviewround3.layout
    elif round == '/apps/GarmentWorkerEducationRound2':
            return GarmentWorkersEducationround2.layout
    elif round == '/apps/GarmentWorkerEducationRound3':
            return GarmentWorkersEducationround3.layout
    elif round == '/apps/GarmentWorkerAccessofFoodRound2':
        return GarmentWorkersAccesstoFoodround2.layout
    elif round == '/apps/GarmentWorkerAccessofFoodRound3':
        return GarmentWorkersAccesstoFoodround3.layout
    elif round == '/apps/GarmentWorkerAgricultureRound2':
        return GarmentworkersAgricultureround2.layout
    elif round == '/apps/GarmentWorkerAgricultureRound3':
        return GarmentWorkerAgricultureround3.layout
    elif round == '/apps/GarmentWorkerLivelihoodRound2':
        return GarmentWorkersLivehoodround2.layout
    elif round == '/apps/GarmentWorkerLivelihoodRound3':
        return GarmentWorkersLivehoodround3.layout
    elif round == '/apps/GarmentWorkerSocialIssuesRound2':
        return GarmentWorkersSocialIssuesround2.layout
    elif round == '/apps/GarmentWorkerSocialIssuesRound3':
        return GarmentWorkersSocialIssuesround3.layout
    elif round == '/apps/GarmentWorkerHealthRound2':
        return GarmentWorkersHeathround2.layout
    elif round == '/apps/GarmentWorkerHealthRound3':
        return GarmentWorkersHeathRound3.layout
    elif round == '/apps/GarmentWorkerSchemesandEntitlementsRound2':
        return GarmentWorkerSchemesandentitlementround2.layout
    elif round == '/apps/GarmentWorkerSchemesandEntitlementsRound3':
        return GarmentWorkerSchemesandentitlementround3.layout
    elif round == '/apps/GarmentWorkerMigrationRound2':
        return GarmentWorkersMigrationround2.layout
    elif round == '/apps/GarmentWorkerMigrationRound3':
        return GarmentWorkersMigrationround3.layout
    elif round == 'Round3':
        return GarmentWorkersOverviewround2.layout
    elif round == 'Round2':
        return GarmentWorkersOverviewround3.layout
    else:
        return GarmentWorkersOverviewround3.layout


if __name__ == '__main__':
    app.run_server(debug=False,host='127.0.0.1', port=8081)
