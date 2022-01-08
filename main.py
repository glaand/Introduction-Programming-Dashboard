import dash
import dash_bootstrap_components as dbc
import dash_table as dt
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

df = pd.read_csv('./datasets/data.csv')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "color": "grey"
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.Img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Olympic_rings_without_rims.svg/2560px-Olympic_rings_without_rims.svg.png", style={"width": "100%"}),
        html.Hr(),
        html.P("FHGR CDS-201 (Alex & André)"),
        dbc.Nav(
            [
                dbc.NavLink("Startseite", href="/", active="exact"),
                dbc.NavLink("Datensatz", href="/datensatz", active="exact"),
                dbc.NavLink("Aufgabe 36", href="/a-36", active="exact"),
                dbc.NavLink("Aufgabe 37", href="/a-37", active="exact"),
                dbc.NavLink("Aufgabe 38", href="/a-38", active="exact"),
                dbc.NavLink("Aufgabe 39", href="/a-39", active="exact"),
                dbc.NavLink("Aufgabe 40", href="/a-40", active="exact"),
                dbc.NavLink("Aufgabe 41", href="/a-41", active="exact"),
                dbc.NavLink("Aufgabe 42", href="/a-42", active="exact"),
                dbc.NavLink("Aufgabe 43", href="/a-43", active="exact"),
                dbc.NavLink("Aufgabe 44", href="/a-44", active="exact"),
                dbc.NavLink("Aufgabe 45", href="/a-45", active="exact"),
                dbc.NavLink("Aufgabe 46", href="/a-46", active="exact"),
                dbc.NavLink("Aufgabe 47", href="/a-47", active="exact"),
                dbc.NavLink("Aufgabe 48", href="/a-48", active="exact"),
                dbc.NavLink("Aufgabe 49", href="/a-49", active="exact"),
                dbc.NavLink("Aufgabe 50", href="/a-50", active="exact")
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
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
                html.H1('Startseite',style={'textAlign':'center'})
            ]
    elif pathname == "/datensatz":
        return [
            html.H1('Datensatz', style={'textAlign':'center'}),
            dt.DataTable(
                id='tbl', data=df.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df.columns],
                style_header={
                    'backgroundColor': 'rgb(30, 30, 30)',
                    'color': 'white'
                },
                style_data={
                    'backgroundColor': 'rgb(50, 50, 50)',
                    'color': 'white'
                },
            ),
        ]
    elif pathname == "/a-36":
        return [
                html.H1('Aufgabe 36', style={'textAlign':'center'}),
            ]
    return html.Div(
        dbc.Container(
            [
                html.H1("404: not found", className="display-3"),
                html.Hr(className="my-2"),
                html.P(f"The pathname {pathname} was not recognised...",
                    className="lead",
                ),
            ],
            fluid=True,
            className="py-3",
        ),
        className="p-3 bg-light rounded-3",
    )



if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
