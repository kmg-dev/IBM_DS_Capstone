# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Create a dash application
app = dash.Dash(__name__)

launch_sites = spacex_df["Launch Site"].unique()
dropdown_options = [{"label": "All Sites", "value": "ALL"}]
for site in launch_sites:
    dropdown_options.append({"label": site, "value": site})

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
            id="site-dropdown",
            options=dropdown_options,
            value="ALL",
            placeholder="Select a Launch Site here",
            searchable=True,
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            marks={0: "0", 2500: "2500", 5000: "5000", 7500: "7500", 10000: "10000"},
            value=[min_payload, max_payload],
        ),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == "ALL":
        data = filtered_df.groupby(["Launch Site"]).sum()
        data = data.reset_index()

        fig = px.pie(
            data,
            values="class",
            names=launch_sites,
            title="Total Success Launches by Site",
        )
        return fig
    else:
        data = (
            filtered_df[filtered_df["Launch Site"] == entered_site]
            .groupby(["class"])
            .count()
        )
        fig = px.pie(
            data,
            values="Launch Site",
            names=spacex_df["class"].unique(),
            title="Total Success Launches for site " + entered_site,
        )
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")],
)
def get_scatter_chart(entered_site, entered_payload):
    filtered_df = spacex_df
    data_pay_load_filtered = filtered_df[(filtered_df["Payload Mass (kg)"] >= entered_payload[0]) & (filtered_df["Payload Mass (kg)"] <= entered_payload[1])]
    if entered_site == "ALL":
        x  = data_pay_load_filtered["Payload Mass (kg)"]
        y = data_pay_load_filtered["class"]
        fig = px.scatter(data_pay_load_filtered, x=x, y=y, color="Booster Version Category")
        return fig
    else:
        data = data_pay_load_filtered[data_pay_load_filtered["Launch Site"] == entered_site]
        x  = data["Payload Mass (kg)"]
        y = data["class"]
        fig = px.scatter(data, x=x, y=y, color="Booster Version Category")
        return fig
    
    


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
