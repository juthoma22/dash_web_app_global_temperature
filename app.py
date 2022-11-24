import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html

import data_handler as dh


DataHandler = dh.DataHandler()

df_country, years, countries = DataHandler.read_files()

# Layout used later for the graph
layout = dict(
    title="Use slider to move through years",
    geo=dict(
        showframe=False,
        showocean=True,
        oceancolor="rgb(0,255,255)",
        type="equirectangular",
    ),
)

app = dash.Dash("Gloabal Temperature")

# server called in Dockerfile
server = app.server

# HTML Layout of the web app
app.layout = html.Div(
    children=[
        html.H1(children="Average Temperature per year in each country"),
        dcc.Graph(
            id="average-temp-year",
        ),
        html.Div(
            dcc.Slider(
                int(years.min()),
                int(years.max()),
                step=1,
                id="year-slider",
                value=int(years.max()),
                marks={
                    str(year): str(year)
                    for year in [1750, 1800, 1850, 1900, 1950, 2000]
                },
            ),
            style={"width": "95%", "padding": "0px 20px 20px 20px"},
        ),
    ]
)


@app.callback(Output("average-temp-year", "figure"), Input("year-slider", "value"))
def update_graph(year):
    """
    update_graph(year) -> Dict

    Calculating the mean temperature for each country for a given year.
    Returning the data and layout for a graph based on the year

    year -- The year to calculate the temperatures for -> Int
    """
    # changing the timestamp ('dt') to just the years
    dff = df_country[df_country["dt"].apply(lambda x: x[:4]) == str(year)]

    # calculating the mean temperature per year for each country
    mean_temp = []
    for country in countries:
        mean_temp.append(dff[dff["Country"] == country]["AverageTemperature"].mean())

    # creating a graph of a map, using the calculated mean temperature for each country
    data = [
        dict(
            type="choropleth",
            locations=countries,
            z=mean_temp,
            locationmode="country names",
            text=countries,
            marker=dict(line=dict(color="rgb(0,0,0)", width=1)),
            colorbar=dict(
                autotick=True, tickprefix="", title="Average\nTemperature,\n°C"
            ),
        )
    ]

    fig = dict(data=data, layout=layout)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
