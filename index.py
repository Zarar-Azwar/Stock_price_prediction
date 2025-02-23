from dash import dcc
from dash import  html
from dash.dependencies import Input, Output
from apps import Home,companies,sector,graphicalView,realtimeChart,treemap,modelsAI,gold,oil,portfolio,recommendation
# Connect to main app.py file
from app import app
from app import server
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
import dash_daq as daq
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
import datetime

FA="https://use.fontawesome.com/releases/v5.12.1/css/all.css"
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
headerStyle={'color': 'white'}
logo = dbc.Navbar(

    dbc.Container(
        [
            
            dbc.Row([
                dbc.Col([html.Img(src=app.get_asset_url('appLogo.png'), height="45px")]),
                dbc.Col([dbc.NavbarBrand("STOCKBUZZ", className="ms-2",
                            style={'font-weight': 'bold','color': 'white','font-size':'30px'})]),
                    ],
                    align="center",
                    className="g-0",

            ),
            #dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
            dbc.Collapse(
                
                dbc.Nav(
                    [dbc.NavItem(dbc.NavLink("Home", href="/apps/Home",
                    style=headerStyle)),
                     dbc.NavItem(dbc.NavLink("Companies", href="/apps/companies",
                     style=headerStyle)),
                     dbc.NavItem(dbc.NavLink("Realtime Chart", href="/apps/realtimeChart",
                     style=headerStyle)),
                     dbc.NavItem(dbc.NavLink("AI", href="/apps/modelsAI",
                     style=headerStyle)),
                     dbc.DropdownMenu(
                         children=[
                            dbc.DropdownMenuItem("Gold", href="/apps/gold"),
                            dbc.DropdownMenuItem("Oil", href="/apps/oil"),
                        ],
                        nav=True,
                        in_navbar=True,
                        label="International Market",
                        toggle_style={
                            "color": "#FFFFFF",
                        },
                     ),
                     dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("Portfolio Optimization", href="/apps/portfolio"),
                            dbc.DropdownMenuItem("Recommendation", href="/apps/recommendation"),
                        ],
                        nav=True,
                        in_navbar=True,
                        label="Advanced",
                        toggle_style={
                            "color": "#FFFFFF",
                        },
                        
                     ),
                    
                     dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("Sector", href="/apps/sector"),
                            dbc.DropdownMenuItem("Graphical View", href="/apps/graphicalView"),
                            dbc.DropdownMenuItem("Treemap", href="/apps/treemap"),
                        ],
                        nav=True,
                        in_navbar=True,
                        label="Sector Analysis",
                        toggle_style={
                            "color": "#FFFFFF",
                        },
                        
                     )
                    ],
                    className="ms-auto",
                    navbar=True,
                    
                ),
                id="url",
                navbar=True,
            ),
        ],
        fluid=False
    ),
    color="#0275D8",
    className="mb-2 container-fluid",
    
)
content=html.Div([
    dcc.Location(id='urlPage',refresh=False),
    dbc.Container(id='page_content')
])
footer=html.Footer([
    html.H5('All Copyrights© reserved',
    style={'color':'white','text-align': 'center'}),
    html.A(children='UET Taxila',href='https://web.uettaxila.edu.pk/',
    style={'color':'white','font-weight': 'bold','text-align': 'center'}),
    
],style={'background-color': '#000000'})
app.layout=html.Div([logo,content])

@app.callback(
    Output('page_content','children'),
    Input('urlPage','pathname')
)
def multpage(pathname):
    print(pathname)
    if pathname=='/apps/Home':
        return Home.layout
    elif pathname=='/apps/companies':
        return companies.layout
    elif pathname=='/apps/sector':
        return sector.layout
    elif pathname=='/apps/graphicalView':
        return graphicalView.layout
    elif pathname=='/apps/realtimeChart':
        return realtimeChart.layout
    elif pathname=='/apps/treemap':
        return treemap.layout
    elif pathname=='/apps/modelsAI':
        return modelsAI.layout
    elif pathname=='/apps/gold':
        return gold.layout
    elif pathname=='/apps/oil':
        return oil.layout
    elif pathname=='/apps/portfolio':
        return portfolio.layout
    elif pathname=='/apps/recommendation':
        return recommendation.layout
    else:
        return Home.layout

if __name__ == '__main__':
    app.run_server(debug=False)
