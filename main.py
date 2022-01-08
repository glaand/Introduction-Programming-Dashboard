import dash
import dash_core_components as dcc
import dash_html_components as html


def main():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div([
        html.H2('Hello World'),
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
            value='LA'
        ),
        html.Div(id='display-value')
    ])

    @app.callback(dash.dependencies.Output('display-value', 'children'),
                  [dash.dependencies.Input('dropdown', 'value')])
    def display_value(value):
        return 'You have selected "{}"'.format(value)

    return app, app.server


# Necessary for deployment
# app --> for the app to run the server
# server --> for heroku to start the server (Procfile)
app, server = main()
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
