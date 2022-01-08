import dash
import dash_core_components as dcc
import dash_html_components as html
from aufgabenblatt_10 import main as main10


# Necessary for deployment
# app --> for the app to run the server
# server --> for heroku to start the server (Procfile)
app, server = main10()
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
