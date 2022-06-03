from dash import Dash, html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from datetime import datetime, date

import yfinance as yf
import pandas as pd
import plotly_express as px



# Create a dash instance
app = Dash(__name__, external_stylesheets=[
        # include google fonts
        "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap"
    ],)

server = app.server

# Line plots
line_plot = px.line(x=[1, 2, 3], y=[4,5,6], title="basic line plots")

stock_id = "AAPL"
start_date = "2017-01-01"
end_date = "2017-04-30"
stock_data = yf.download(stock_id, start=start_date, end=end_date)
stock_data.reset_index(inplace=True)
# fig = get_stock_price_fig(df)
# return # plot the graph of fig using DCC function



# Define the page layout
# Header section
header_section = html.Div([dmc.Header(
    height=70,
    fixed=False, 
    p="md",
    children=[
        dmc.Container(
            fluid=True,
            children=dmc.Group(
                position="apart",
                align="flex-start",
                children=[
                    dmc.Text(
                                'Stock Screener and Predictor',
                                size="xl",
                                color="gray",
                            ),
                    dmc.Group(
                        position="right",
                        align="center",
                        spacing="xl",
                        children=[
                            html.A(
                                dmc.Tooltip(
                                    dmc.ThemeIcon(
                                        DashIconify(
                                            icon="radix-icons:github-logo",
                                            width=22,
                                        ),
                                        radius=30,
                                        size=36,
                                        variant="outline",
                                        color="gray",
                                    ),
                                    label="Source Code",
                                    position="bottom",
                                ),
                                href="https://github.com/sanjivch/stocks-screener-and-predictor",
                            ),
                            
                        ],
                    ),
                ],
            ),
        )
    ],
)]) 

# Navigation bar
nav_container_style =  {
                            "width": "25vw",
                            "align-items": "center",
                            "display": "flex",
                            "flex-direction": "column",
                            "justify-content": "center",
                            "background-color": "rgb(255, 255, 255)"
}
nav_section= html.Div([
                       dmc.Container([
                           dmc.Navbar(
                        fixed=False, # uncomment this line if you are using this example in your app
                        width={"base": 300},
                        height=900,
                        children=[
                            dmc.ScrollArea(
                                offsetScrollbars=True,
                                type="scroll",
                                children=[
                                    dmc.Title(f"Choose from the options below", order=5),
                                    dmc.Divider(label="Stocks",style={"marginBottom": 10, "marginTop": 10}),
                                    dmc.Group(
                                        direction="column",
                                        children=[
                                                    dmc.Select(
                                                                label="Select Stock",
                                                                placeholder="Select a stocker ticker",
                                                                id="stock-select",
                                                                required=True,
                                                                clearable=True,
                                                                searchable=True,
                                                                nothingFound="No options found",
                                                                value="SBI",
                                                                data=['SBI','TCS'],
                                                                icon=[DashIconify(icon="radix-icons:magnifying-glass")],
                                                                style={"width": 200, "marginBottom": 10},
                                                            ),
                                                    dmc.Text(id="selected-value"),
                                                    dmc.DatePicker(
                                                                id="date-picker",
                                                                label="Start Date",
                                                                description="You can also provide a description",
                                                                required=True,
                                                                minDate=date(2020, 8, 5),
                                                                maxDate=date(2022, 9, 19),
                                                                value=datetime.now().date(),
                                                                style={"width": 200},
                                                                ),
                                                    dmc.Space(h=10),
                                                    dmc.Text(id="selected-date"),
                                                ],
                                            ),
                                    dmc.Group(
                                        direction="row",
                                        children=[
                                            dmc.Button("Stock Price",),
                                            dmc.Space(w=20),
                                            # Indicators button
                                            dmc.Button("Indicators",),
                                        ]
                                    ),
                                    
                                    # ant-design:stock-outlined
                                    dmc.Divider(label="Forecast",style={"marginBottom": 20, "marginTop": 20},),
                                    dmc.Group(
                                        direction="column",
                                        children=[
                                            
                                            # Number of days of forecast input
                                            dmc.NumberInput(
                                                label="Number of days",
                                                description="From 0 to infinity, in steps of 5",
                                                value=5,
                                                min=0,
                                                step=5,
                                                required=True,
                                                style={"width": 250},
                                            ),
                                            # Forecast button
                                            dmc.Button("Forecast"),
                                        ],
                                    ),
                                ],
                            )
                        ],
                    ),
                       ], style=nav_container_style) 
                    ], className="nav")

# Content section
content_section = html.Div([
                            html.Div([
                                # Logo
                                # Company name
                            ], className="header"),
                            html.Div([
                                # Description
                            ], id="description", className="description_ticker"),
                            html.Div([
                                # Stock price plot
                                dcc.Graph(id='stock-plot', figure=line_plot),
                            ], id="plot-content"),
                            html.Div([
                                # Indicator plot
                            ], id="main-content"),
                            html.Div([
                                # Forecast plot 
                            ], id="forecast-content"),
                        ], className="content")

# App layout
app.layout = html.Div([header_section, nav_section, content_section])


if __name__ == '__main__':
    app.run_server(debug=True)