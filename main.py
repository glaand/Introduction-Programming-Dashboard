import dash
import dash_bootstrap_components as dbc
from dash import dash_table as dt, html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from aufgabenblatt_8 import load_data, get_axis, exercise39, exercise40
import plotly.graph_objects as go
from aufgabenblatt_8 import exercise38
from aufgabenblatt_9 import aufgabe45, aufgabe44, getSortedListByColumnName, aufgabe43, getCountriesByDiscipline
from aufgabenblatt_10 import filter_data, filter_data2, group_medals_by_country, aufgabe50, aufgabe49

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "Olympics Dashboard - FHGR CDS-201 (Alex & André)"

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "color": "grey",
    "overflow": "auto"
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "color": "grey"
}

sidebar = html.Div(
    [
        html.Img(
            src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Olympic_rings_without_rims.svg/2560px-Olympic_rings_without_rims.svg.png",
            style={"width": "100%"}),
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


# Aufgabe 48
@app.callback(
    Output(component_id='48tbl', component_property='data'),
    Output(component_id="medals_per_country", component_property="figure"),
    Input(component_id='country-dropdown', component_property='value')
)
def update_country_stats(country):
    medalCount = group_medals_by_country(load_data().dropna(), country)
    return medalCount.to_dict("records"), go.Figure(data=[go.Bar(
        x=medalCount.columns,
        y=medalCount.iloc[0].to_numpy(),
        text=medalCount.iloc[0].to_numpy(),
        textposition='auto',
        marker_color=["#CD7F32", "#C0C0C0", "#FFD700"],
    )])


# Aufgabe 47
@app.callback(
    Output(component_id='47tbl', component_property='data'),
    Input(component_id='search_input', component_property='value')
)
def search_athlethe(searchString):
    if searchString is None:
        searchString = ""
    df = load_data().dropna()
    return filter_data2(df, searchString).to_dict("records")


# Aufgabe 46
@app.callback(
    Output(component_id='46tbl', component_property='data'),
    [Input(component_id='country-dropdown', component_property='value'),
     Input(component_id='year-dropdown', component_property='value'),
     Input(component_id='sport-dropdown', component_property='value')]
)
def search_dropdown(country, year, sport):
    if country == "No Country":
        country = None
    if year == "No Year":
        year = None
    if sport == "No Sport":
        sport = None
    df = load_data().dropna()
    return filter_data(df, country, year, sport).to_dict('records')


# Aufgabe 40
@app.callback(
    Output(component_id='line-chart', component_property='figure'),
    Input(component_id='country', component_property='value'),
)
def update_graph(country):
    df = load_data()
    df2 = df.groupby(["Country", "Year", "Medal"]).size().reset_index(name="count")
    dff = df2.copy()
    dff2 = dff[dff["Country"] == country]
    for y in range(1976, 2012, 4):
        a_row = pd.Series({"Country": country, "Year": y, "Medal": "Bronze", "count": 0})
        row_df = pd.DataFrame([a_row])
        dff2 = pd.concat([row_df, dff2], ignore_index=True)
    dff2 = dff2.loc[dff2.reset_index().groupby(["Country", "Year", "Medal"])["count"].idxmax()]
    bronze_x = get_axis(dff2, "Bronze", "Year")
    bronze_y = get_axis(dff2, "Bronze", "count").to_numpy()
    silver_x = get_axis(dff2, "Silver", "Year")
    silver_y = get_axis(dff2, "Silver", "count").to_numpy()
    gold_x = get_axis(dff2, "Gold", "Year")
    gold_y = get_axis(dff2, "Gold", "count").to_numpy()

    fig = go.Figure(data=[
        go.Bar(
            name='Bronze',
            x=bronze_x,
            y=bronze_y,
            marker={"color": "#CD7F32"},
        ),
        go.Bar(
            name='Silver',
            x=silver_x,
            y=silver_y,
            marker={"color": "#C0C0C0"},
        ),
        go.Bar(
            name='Gold',
            x=gold_x,
            y=gold_y,
            marker={"color": "#FFD700"}
        ),
    ])
    fig.update_xaxes(title="Olympic year", type="category")
    fig.update_yaxes(title="Medal count", dtick=1, type="log")

    # Change the bar mode
    fig.update_layout(
        barmode='stack'
    )
    return fig


# Aufgabe 45
@app.callback(
    [Output("bar", "figure")],
    [Input("gender_dropdown", "value"),
     Input("year_slider", "value")]
)
def updateBarGraph(gender, year_value):
    df = load_data()
    # Dataframe should contain, men/women and their respective medal count per year
    dff = df.groupby(["Year", "Gender"]).size().reset_index(name="Count")
    # select either male or female (men/women)
    dff = dff[dff["Gender"] == gender]
    # dataframe drops the years which arent needed
    dff = dff.drop(dff[dff.Year > year_value].index)
    fig = px.bar(dff,
                 x="Year",
                 y="Count",
                 title=f"Anzahl Medaillen der {'Männer' if gender == 'Men' else 'Frauen'}", )
    fig.update_xaxes(type='category')
    return fig,


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def render_page_content(pathname):
    global app
    df = pd.read_csv('./datasets/data.csv', encoding="utf-8")
    if pathname == "/":
        return [
            html.H1('Startseite', style={'textAlign': 'center'}),
            html.Br(),
            html.H2("Willkommen zum Dashboard von Alex und André!"),
            html.H3("Dieses Dashboard wurde im Jahr 2021/2022 im Modul Einführung in die Programmierung."),
            html.H4("Wir befinden uns im Herbstsemester des Bachelor Studiengang Computational und Data Science."),
            html.P("Der Datensatz wurde uns von den Dozenten vorgegeben. Es werden die Olympiadaten vom Jahr 1976 bis 2008 dargestellt."),
            html.P("Hier ein Meme, welches mich zum lachen gebracht hat während dem Programmieren: "),
            html.Img(src=app.get_asset_url('meme.jpg'))
        ]
    elif pathname == "/datensatz":
        return [
            html.H1('Datensatz', style={'textAlign': 'center'}),
            dt.DataTable(
                id='tbl', data=df.to_dict('records'),
                columns=[{"name": i, "id": i} for i in df.columns],
                filter_action='native',
            ),
        ]
    elif pathname == "/a-36":
        return [
            html.H1('Aufgabe 36', style={'textAlign': 'center'}),
            html.P("""
                    Für unser Dashboard-Projekt auf den letzten 3 Aufgabenblättern sollen Sie sich eine(n)
                    Studentin/Studenten aus der Vorlesung suchen, mit der/dem Sie diese Projektaufgaben zusammen
                    bearbeiten. Geben Sie den Namen der beiden Studierenden aus Ihrer Projektgruppe an. (1 P.)
                """),
            html.Hr(),
            dcc.Markdown('''
                ```
                Die Projektgruppe besteht aus André Glatzl und Alexandru Schneider.
                ```
                ''')
        ]
    elif pathname == "/a-37":
        return [
            html.H1('Aufgabe 37', style={'textAlign': 'center'}),
            html.P("""
                    Der erste Schritt bei einem Visualisierungsproblem ist es immer, sich die Daten genauer anzuschauen, um
                    zum Beispiel deren Struktur und Grösse zu verstehen, aber auch mögliche Fehler in den Daten ausfindig
                    zu machen. 
                    Nachdem Sie die Olympia-Daten näher (ohne Programmierung) untersucht haben, sollen Sie:
                """),
            html.P("""
                    (a) diese einlesen und einen Teil davon ausgeben (am Besten verwenden Sie ein Pandas Dataframe
                    für das Einlesen der Daten). (2 P.)
                """),
            html.P("""
                    (b) die Anzahl der Spalten und Zeilen bestimmen. (2 P.)
                """),
            html.Hr(),
            dcc.Markdown('''
                ```
                       City    Year     Sport Discipline           Event                   Athlete Gender Country_Code        Country Event_gender   Medal
                    0  Montreal  1976.0  Aquatics     Diving  3m springboard           KÖHLER, Christa  Women          GDR   East Germany            W  Silver
                    1  Montreal  1976.0  Aquatics     Diving  3m springboard       KOSENKOV, Aleksandr    Men          URS   Soviet Union            M  Bronze
                    2  Montreal  1976.0  Aquatics     Diving  3m springboard      BOGGS, Philip George    Men          USA  United States            M    Gold
                    3  Montreal  1976.0  Aquatics     Diving  3m springboard  CAGNOTTO, Giorgio Franco    Men          ITA          Italy            M  Silver
                    4  Montreal  1976.0  Aquatics     Diving    10m platform    WILSON, Deborah Keplar  Women          USA  United States            W  Bronze
                    
                    15316 Datensätze mit 11 Spalten.
                ```
                ''')
        ]
    elif pathname == "/a-38":
        tmpApp = exercise38(False)
        layout = tmpApp[0].layout
        return [
            html.H1('Aufgabe 38', style={'textAlign': 'center'}),
            html.P("""
                    Schreiben Sie Python-Code, der die Olympia-Daten filtert:
                """),
            html.P("""
                    (a) nach Land (2 P.)
                """),
            html.P("""
                    (b) nach Sportart (2 P.)
                """),
            html.P("""
                    (c) Gibt es einen Zusammenhang zwischen Ländern und Sportarten? (Diskutieren Sie dies kurz oder
                        erzeugen Sie ein entsprechendes Plotly-Diagramm, in dem man direkt einen Zusammenhang
                        erkennt) (1 P.)
                """),
            html.Hr(),
            layout
        ]
    elif pathname == "/a-39":
        tmpApp = exercise39()
        layout = tmpApp[0].layout
        return [
            html.H1('Aufgabe 39', style={'textAlign': 'center'}),
            html.P("""
                    Auf https://plotly.com/python/plotly-express/ finden Sie zahlreiche Beispiele für interaktive Diagramme.
                    Zusätzlich gibt es dort Beispielquellcode, den Sie kopieren und ausführen können. Erzeugen Sie ein
                """),
            html.P("""
                        (a) Streudiagramm (scatter) (2 P.)
                """),
            html.P("""
                        (b) Histogramm (histogram) (2 P.)
                """),
            html.P("""
                        (c) Liniendiagramm (line) (2 P.)
                """),
            html.P("""
                    Sie können einen beliebigen Datensatz nehmen (Sie müssen nicht die Olympia-Daten nehmen, Sie dürfen
                    es aber gerne). In dieser Aufgabe geht es nur darum, dass Sie sich mit den Diagrammtypen vertraut
                    machen. Machen Sie Screenshots von Ihren Diagrammen und fügen Sie diese in Ihr Lösungs-pdf ein.
                """),
            html.Hr(),
            layout
        ]
    elif pathname == "/a-40":
        layout = exercise40().layout
        prepareLayout = [
            html.H1('Aufgabe 40', style={'textAlign': 'center'}),
            html.P("""
                    Modifizieren Sie das Dashboard-Beispiel aus der Vorlesung, so dass Sie in einem Drop-Down-Menü ein
                    Land auswählen können und die Summe der Medaillengewinne über die Jahre visuell als Liniendiagramm
                    (oder gestapeltes Balkendiagramm, falls Sie zwischen Bronze/Silber/Gold über die Zeit unterscheiden
                    wollen) dargestellt bekommen. Sie können gerne weitere Features implementieren. Es geht nicht darum,
                    das perfekte Dashboard zu bauen, sondern eher darum, dass Sie sicherer beim Python-Programmieren
                    werden, z.B. indem Sie einen gegebene Datenstruktur verarbeiten. (4 P.)
                """),
            html.Hr(),
            layout
        ]

        return prepareLayout
    elif pathname == "/a-41":
        df = load_data()
        laender = getSortedListByColumnName(df, "Country")
        gewinner = getSortedListByColumnName(df, "Athlete")
        sportarten = getSortedListByColumnName(df, "Discipline")
        res1 = f"Es gibt {len(laender)} Länder."
        res2 = f"Es gibt {len(gewinner)} Medaillengewinner."
        res3 = f"Es gibt {len(sportarten)} Disziplinen."
        prepareLayout = [
            html.H1('Aufgabe 41', style={'textAlign': 'center'}),
            html.P("""
                    Lesen Sie den Olympia-Datensatz ein (haben Sie eigentlich schon auf Aufgabenblatt 8 gelöst). Berechnen
                    Sie drei Listen – eine Liste für alle Sportarten/Disziplinen/Events, eine Liste für alle
                    Medaillengewinner/innen und eine Liste für alle Länder. Sortieren Sie die drei Listen alphabetisch und
                    geben Sie diese aus. (3 P.)
                """),
            html.Hr(),
            dcc.Markdown("""
                {}
                {}
                {}
                """.format(res1, res2, res3))
        ]
        return prepareLayout
    elif pathname == "/a-42":
        df = load_data()
        countriesByMedalSum = df.groupby(["Country"]).size().reset_index(name="Count")
        countriesByMedalSum = countriesByMedalSum.sort_values(by=["Count"], ascending=False)
        prepareLayout = [
            html.H1('Aufgabe 42', style={'textAlign': 'center'}),
            html.P("""
                    Für die Liste der Länder sollen Sie zusätzlich die Anzahl der gewonnenen Medaillen berechnen und zwar
                    über alle Jahre aufsummiert. Sortieren Sie jetzt die Länder nach ihrem Erfolg, also wie viele Medaillen von
                    jedem Land gewonnen wurden. Geben Sie die Top Ten Liste aus. (4 P.)
                """),
            html.Hr(),
            html.P(countriesByMedalSum.head(10).to_string(), style={"white-space": "pre-line"})
        ]
        return prepareLayout
    elif pathname == "/a-43":
        df = load_data()
        matrix = aufgabe43(getCountriesByDiscipline(df))
        prepareLayout = [
            html.H1('Aufgabe 43', style={'textAlign': 'center'}),
            html.P("""
                    Für jedes Land und jede Sportart (olympische Disziplin) sollen Sie eine Übersicht generieren. Erzeugen Sie
                    eine Matrix (Liste von Listen), die für jedes Land die Anzahl der gewonnen Medaillen in einer bestimmten
                    Sportart/Disziplin/Event berechnet. Wenn Sie also 10 Länder und 20 Sportarten hätten, dann hätte Ihre
                    Matrix 200 Einträge. (4 P.)
                """),
            html.Hr(),
            dcc.Markdown(matrix.to_string())
        ]
        return prepareLayout
    elif pathname == "/a-44":
        df = load_data()
        tmpApp = aufgabe44(df)
        prepareLayout = [
            html.H1('Aufgabe 44', style={'textAlign': 'center'}),
            html.P("""
                    Normalisieren Sie die in Aufgabe 43 berechnete Matrix, indem Sie jeden Wert durch die Gesamtanzahl der
                    gewonnenen Medaillen eines entsprechenden Landes dividieren. Dies generiert Werte zwischen 0.0 und
                    1.0. (2 P.) Nutzen Sie Plotly Express, um eine farbkodierte Matrixvisualisierung (als density_heatmap) zu
                    erzeugen. (2 P.) Machen Sie einen Screenshot von Ihrem Ergebnis. Welche Sportarten sind in welchen
                    Ländern am erfolgreichsten? (1 P.)
                """),
            html.Hr(),
            tmpApp[0][0].layout
        ]
        return prepareLayout
    elif pathname == "/a-45":
        df = load_data()
        app2, fig, matrix = aufgabe44(df)
        tmpApp = aufgabe45(df, fig)
        prepareLayout = [
            html.H1('Aufgabe 45', style={'textAlign': 'center'}),
            html.P("""
                    Erweitern Sie Ihr Dashboard aus Aufgabe 40 um (mindestens) zwei weitere Plotly Diagramme und um
                    (mindestens) eine weitere Eingabemöglichkeit (zum Beispiel einem Slider, einem Date Picker oder einem
                    Textfeld). Zeigen Sie beispielsweise die Ergebnisse aus Aufgabe 44 im Dashboard an (eventuell können Sie
                    diese nach männlichen und weiblichen Medaillengewinner/innen aufsplitten oder den Verlauf über die
                    Zeit anzeigen lassen). Es gibt sehr viele Möglichkeiten, das Dashboard zu erweitern und kreativ
                    umzugestalten. In dieser Aufgabe haben Sie viele Freiheiten. (4 P.)
                """),
            html.Hr(),
            tmpApp.layout
        ]

        return prepareLayout
    elif pathname == "/a-46":
        country_options = [{"label": i, "value": i} for i in df["Country"].dropna().unique()]
        year_options = [{"label": i, "value": i} for i in df["Year"].dropna().unique()]
        sport_options = [{"label": i, "value": i} for i in df["Sport"].dropna().unique()]
        country_options.insert(0, {"label": "No Country", "value": "No Country"})
        year_options.insert(0, {"label": "No Year", "value": "No Year"})
        sport_options.insert(0, {"label": "No Sport", "value": "No Sport"})
        prepareLayout = [
            html.H1('Aufgabe 46 - Filtern ', style={'textAlign': 'center'}),
            html.P("""
                    Implementieren Sie einen Filter als Python-Funktion, die drei Parameter als Eingabe akzeptiert, die
                    Olympia-Daten nach Land, Jahr und Sportart filtert und das gefilterte DataFrame zurückliefert. Gibt der
                    Nutzer kein Land, kein Jahr oder keine Sportart an, so wird auf dieser der drei Datendimensionen nicht
                    gefiltert. (4 P.)
                """),
            html.Hr(),
            html.Div(children=[
                dcc.Dropdown(
                    id='country-dropdown',
                    options=country_options,
                    value="Switzerland"
                ),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=year_options,
                    value=2008
                ),
                dcc.Dropdown(
                    id='sport-dropdown',
                    options=sport_options,
                    value="Cycling"
                ),
            ], className="responsive-dropdowns"),
            html.Br(),
            dt.DataTable(
                id='46tbl', data=[],
                columns=[{"name": i, "id": i} for i in df.columns],
            ),
        ]
        return prepareLayout
    elif pathname == "/a-47":
        prepareLayout = [
            html.H1('Aufgabe 47 - Filtern 2', style={'textAlign': 'center'}),
            html.P("""
                            Sie sollen einen weiteren Filter als Python-Funktion implementieren, der eine beliebige Zeichenkette als
                            Argument annimmt und alle Sportlernamen ausgibt, in denen die Zeichen in der angegebenen
                            Zeichenkette in beliebiger Reihenfolge vorkommen. Wenn man also nach „imch“ filtert, so ist der Name
                            „Michael“ ein gültiges Filterergebnis. Die Funktion soll entsprechend wieder das gefilterte DataFrame
                            zurückliefern (2 P.)
                        """),
            html.Hr(),
            dcc.Input(
                id="search_input",
                type="text",
                placeholder="Search Athlete",
            ),
            dt.DataTable(
                id="47tbl",
                data=[],
                columns=[{"name": "Athlete", "id": "Athlete"}],
            )
        ]
        return prepareLayout
    if pathname == "/a-48":
        country_options = [{"label": i, "value": i} for i in df["Country"].dropna().unique()]
        medalCount = group_medals_by_country(df.dropna(), "Switzerland")
        prepareLayout = [
            html.H1('Aufgabe 48 - Aggregation', style={'textAlign': 'center'}),
            html.P("""
                                    Sie sollen einen weiteren Filter als Python-Funktion implementieren, der eine beliebige Zeichenkette als
                                    Argument annimmt und alle Sportlernamen ausgibt, in denen die Zeichen in der angegebenen
                                    Zeichenkette in beliebiger Reihenfolge vorkommen. Wenn man also nach „imch“ filtert, so ist der Name
                                    „Michael“ ein gültiges Filterergebnis. Die Funktion soll entsprechend wieder das gefilterte DataFrame
                                    zurückliefern (2 P.)
                                """),
            html.Hr(),
            dcc.Dropdown(
                id='country-dropdown',
                options=country_options,
                value=country_options[0]["value"]
            ),
            html.Br(),
            dt.DataTable(
                id="48tbl",
                data=medalCount.to_dict("records"),
                columns=[{"name": "Bronze", "id": "Bronze"},
                         {"name": "Silver", "id": "Silver"},
                         {"name": "Gold", "id": "Gold"}],
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="medals_per_country",
                    )
                ]
            ),
        ]
        return prepareLayout
    if pathname == "/a-49":
        app, _ = aufgabe49(df.dropna())
        layout = app.layout
        prepareLayout = [
            html.H1('Aufgabe 49 - Anwendungsbeispiele', style={'textAlign': 'center'}),
            html.P("""
                Laden Sie den Olympia-Datensatz in Ihr Dashboard. Nutzen Sie die implementierten Filter und
                Aggregationen, sowie die interaktiven Visualisierungen, um den Datensatz zu explorieren. Beschreiben Sie
                5 Muster oder Anomalien in dem Olympia-Datensatz, die Sie mit Ihrem Dashboard herausgefunden haben.
                Bei den visuellen Mustern oder Anomalien sollten Sie auch Screenshots ins Lösungs-pdf hinzufügen. (5 P.)
            """),
            html.Hr(),
            html.Div(children=[graph for graph in layout.children[1:]]),
        ]
        return prepareLayout
    if pathname == "/a-50":
        app, _ = aufgabe50(df.dropna())
        layout = app.layout
        prepareLayout = [
            html.H1('Aufgabe 50 - Sortierung der Matrix aus Aufgaben 43 und 44', style={'textAlign': 'center'}),
            html.P("""
                Implementieren Sie eine Sortierung auf zwei Dimensionen (Spalten und Zeilen). Hierzu gibt es zahlreiche
                Möglichkeiten, aber um Ihnen die Aufgabe zu erleichtern, können Sie sich selbst ein Sortierkriterium
                überlegen und die 2D Datenstruktur sortieren. Dennoch finden Sie in einem Forschungspapier auf Moodle
                technisch ausgereifte algorithmische Lösungen (für den Fall, dass Sie eine effektive Lösung implementieren
                möchten). Binden Sie einen Screenshot in das Lösungs-pdf ein, welches die Matrix vor und nach der
                Sortierung zeigt. Ein Sortierbeispiel einer Matrix finden Sie oben in den beiden Abbildungen! (5 P.)
            """),
            html.Hr(),
            html.Div(children=[graph for graph in layout.children[1].children[1:]]),
        ]
        return prepareLayout
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


server = app.server
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
