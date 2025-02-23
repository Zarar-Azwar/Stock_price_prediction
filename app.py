import dash
import dash_bootstrap_components as dbc
FA="https://use.fontawesome.com/releases/v5.12.1/css/all.css"
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
# Connect to your app pages

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                            external_stylesheets=[dbc.themes.BOOTSTRAP,FA]
                )
server = app.server