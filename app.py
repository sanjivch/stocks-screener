import time
from dash import Dash, html, dcc, callback, Output, html, Input, State, no_update
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from datetime import datetime, date, timedelta

import yfinance as yf
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go

from stocks import stock_list


# Create a dash instance
app = Dash(
    __name__,
    external_stylesheets=[
        # include google fonts
        "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap"
    ],
)

server = app.server

# print(stock_list)
# def get_stock_data(stock_id, start_date, end_date):
#     # stock_id = "UNIONBANK.NS"
#     # start_date = "2017-01-01"
#     # end_date = "2017-04-30"
#     stock_data = yf.download(stock_id, start=start_date, end=end_date)
#     stock_data.reset_index(inplace=True)
#     return stock_data

# def get_stock_info(stock_id):
#     return  yf.Ticker(stock_id).info

# def get_line_plot(stock_data):
#     return px.line(x=stock_data['Date'], y=stock_data['High'], title="basic line plots")

# def get_scatter_plot(stock_data):
#     stock_data['EWA_20'] = stock_data['Close'].ewm(span=20, adjust=False).mean()
#     return px.scatter(stock_data,
#                     x= stock_data['Date'],
#                     y= stock_data['EWA_20'],
#                     title="Exponential Moving Average vs Date")

# fig.update_traces(mode= # appropriate mode)


# Define the page layout
# Header section
header_section = html.Div(
    [
        dmc.Header(
            height=60,
            fixed=True,
            p="md",
            children=[
                dmc.Container(
                    fluid=True,
                    children=dmc.Group(
                        position="apart",
                        align="flex-start",
                        children=[
                            dmc.Text(
                                "Stock screener",
                                variant="gradient",
                                gradient={"from": "blue", "to": "cyan", "deg": 45},
                                size="xl",
                                weight="bold",
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
                                                color="blue",
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
        )
    ]
)

# Navigation bar
nav_container_style = {
    "width": "25vw",
    "align-items": "center",
    "display": "flex",
    "flex-direction": "column",
    "justify-content": "center",
    "background-color": "rgb(255, 255, 255)",
}
nav_section = html.Div(
    [
        dmc.Container(
            [
                dmc.Navbar(
                    fixed=True,
                    width={"base": 300},
                    # height=900,
                    position={"top": 60},
                    children=[
                        dmc.ScrollArea(
                            offsetScrollbars=True,
                            type="scroll",
                            children=[
                                html.Br(),
                                dmc.Title(
                                    f"Choose from the options below",
                                    order=6,
                                    style={"color": "gray"},
                                ),
                                dmc.Divider(
                                    label=[
                                        DashIconify(
                                            icon="ant-design:stock-outlined",
                                            width=15,
                                            style={"marginRight": 10},
                                        ),
                                        "Stocks",
                                    ],
                                    style={"marginBottom": 10, "marginTop": 10},
                                ),
                                dmc.Group(
                                    direction="column",
                                    children=[
                                        dmc.Select(
                                            label="Select Stock",
                                            placeholder="Select a stock ticker",
                                            id="stock-select",
                                            # required=True,
                                            clearable=True,
                                            searchable=True,
                                            nothingFound="No options found",
                                            data=stock_list,
                                            value="ABB",
                                            icon=[
                                                DashIconify(
                                                    icon="radix-icons:magnifying-glass"
                                                )
                                            ],
                                            style={
                                                "width": 250,
                                            },
                                        ),
                                        dmc.Group(
                                            direction="row",
                                            children=[
                                                
                                                dmc.DateRangePicker(
                                                    id="date-range-picker",
                                                    label="Date Range",
                                                    # description="You can also provide a description",
                                                    minDate=date(2020, 8, 5),
                                                    maxDate=datetime.today(),
                                                    value=[
                                                        datetime.now().date()
                                                        - timedelta(days=5),
                                                        datetime.now().date(),
                                                    ],
                                                    style={"width": 250},
                                                ),
                                            ],
                                        ),
                                        dmc.Space(h=10),
                                    ],
                                ),
                                dmc.Group(
                                    direction="row",
                                    id='loading-data',
                                    children=[
                                        dmc.LoadingOverlay(dmc.Button(
                                            "Fetch Data",
                                            leftIcon=[DashIconify(icon="bx:data")],
                                            id="btn-fetch-data",
                                            variant="gradient",
                                            gradient={"from": "indigo", "to": "cyan"},
                                        ), loaderProps={'size':"xs"}), #
                                        dmc.Space(w=10),
                                        # Indicators button
                                        # dmc.Button("Indicators", leftIcon=[DashIconify(icon="carbon:summary-kpi")],), #carbon:summary-kpi
                                    ],
                                ),
                                # ant-design:stock-outlined
                                #                 dmc.Divider(label=[DashIconify(
                                #     icon="wpf:future", width=15, style={"marginRight": 10}
                                # ),"Forecast"],style={"marginBottom": 20, "marginTop": 20},),
                                #                 dmc.Group(
                                #                     direction="column",
                                #                     children=[
                                #                         # Number of days of forecast input
                                #                         dmc.NumberInput(
                                #                             label="Number of days",
                                #                             description="From 0 to infinity, in steps of 5",
                                #                             value=5,
                                #                             min=0,
                                #                             step=5,
                                #                             required=True,
                                #                             style={"width": 250},
                                #                         ),
                                #                         # Forecast button
                                #                         dmc.Button("Forecast",leftIcon=[DashIconify(icon="carbon:forecast-lightning")],),#
                                #                     ],
                                #                 ),
                            ],
                        )
                    ],
                ),
            ],
            style=nav_container_style,
        )
    ],
    className="nav",
)

# Content section
content_section = html.Div(style={"width": 900},

    children=[
        dmc.Space(h=50),
        dmc.Group(
            direction="row",
            children=[
                dmc.Space(h=30),
                dmc.Image(
                    id="stock-img-url",
                    # src=stock_dict['logo_url'],
                    # alt=stock_dict['shortName'],
                    # caption=stock_dict['sector'],
                    width=75,
                ),
                dmc.Space(w=400),
                dmc.Text(
                    id="stock-name",
                    size="lg",
                ),
                dmc.Badge(id="stock-recommendation", variant="filled",),
            ],
        ),
        dmc.Accordion(
            children=[
                dmc.AccordionItem([
                    dmc.Text(id="pe-ratio", size="xs",),
                    dmc.Text(id="peg-ratio", size="xs",),],
                    label=[
                        DashIconify(
                            icon="icon-park-solid:analysis",
                            width=15,
                            style={"marginRight": 10},
                        ),
                        "Fundamental Analysis",
                        
                    ],
                ),
                dmc.AccordionItem(
                    "Configure temp appearance and behavior with vast amount of settings or overwrite any part of component "
                    "styles",
                    label="Flexibility",
                ),
            ],
        ),
        # Stock price plot
        dcc.Graph(
            id="stock-plot", config={"displayModeBar": False}
        ),  # figure=line_plot),
        dcc.Graph(
            id="indicator-plot", config={"displayModeBar": False}
        ),  # figure=scatter_plot),
        # Indicator plot
        # Forecast plot
    ],
    className="content",
)

# App layout
app.layout = html.Div(
    [
        header_section,
        dmc.Group(direction="row", children=[nav_section, content_section]),
    ]
)



@app.callback(
    [   
        Output("btn-fetch-data", "children"),
        Output("stock-img-url", "src"),
        Output("stock-img-url", "caption"),
        Output("stock-name", "children"),
        Output("stock-recommendation", "children"),
        Output("stock-recommendation", "color"),
        Output("pe-ratio", "children"),
        Output("peg-ratio", "children"),
        Output("stock-plot", "figure"),
        Output("indicator-plot", "figure"),
    ],
    [Input("btn-fetch-data", "n_clicks")],
    [
        State("stock-select", "value"),
        State("date-range-picker", "value"),
    ],
)
def update_stock_info(btn_data_clicked, stock_id, date_range):
    if btn_data_clicked:
        time.sleep(2)
        stock_id = stock_id + ".NS"
        start_date = date_range[0]
        end_date = date_range[1]
        stock_info = yf.Ticker(stock_id).info
        stock_recommendation = stock_info["recommendationKey"]
        recommendation_color = {"none":"gray","hold":"orange", "buy":"green", "sell":"red"}
        print(stock_info)
        stock_data = yf.download(stock_id, start=start_date, end=end_date)
        stock_data.reset_index(inplace=True)

        stock_ohlc_plot = go.Figure(
            data=go.Ohlc(
                x=stock_data["Date"],
                open=stock_data["Open"],
                high=stock_data["High"],
                low=stock_data["Low"],
                close=stock_data["Close"],
            )
        )
        stock_ohlc_plot.update(layout_xaxis_rangeslider_visible=False)

        stock_line_plot = px.line(
            x=stock_data["Date"],
            y=stock_data["High"],
            title=f"{stock_info['shortName']}",
        )
        stock_data["EWA_20"] = stock_data["Close"].ewm(span=20, adjust=False).mean()
        stock_scatter_plot = px.scatter(
            stock_data,
            x=stock_data["Date"],
            y=stock_data["EWA_20"],
            title="Exponential Moving Average vs Date",
        )

        return (
            no_update,
            stock_info["logo_url"],
            stock_info["sector"],
            stock_info["longName"],
            stock_recommendation,
            recommendation_color[stock_recommendation],
            f"PE Ratio  : {stock_info['forwardPE']}",
            f"PEG Ratio : {stock_info['pegRatio']}",
            stock_ohlc_plot,
            stock_scatter_plot,
        )


# @app.callback(Output('stock-plot', 'figure'),
#                 [Input('btn-show-data', 'n_clicks')],
#                 [State('stock-select', 'value'),State('start-date-picker', 'value'), State('end-date-picker', 'value')])

# def update_line_plot(clicked, stock_id, start_date, end_date):
#     if clicked:
#         if stock_id == '':
#             stock_id = 'SBIN.NS'
#         else:
#             stock_id = stock_id+".NS"
#         stock_data = yf.download(stock_id, start=start_date, end=end_date)
#         stock_data.reset_index(inplace=True)

#         return px.line(x=stock_data['Date'], y=stock_data['High'], title="basic line plots")


# @app.callback(Output('indicator-plot', 'figure'),
#                 [Input('btn-show-data', 'n_clicks')],
#                 [State('stock-select', 'value'),State('start-date-picker', 'value'), State('end-date-picker', 'value')])

# def get_stock_data(stock_id, start_date, end_date):
#     # stock_id = "UNIONBANK.NS"
#     # start_date = "2017-01-01"
#     # end_date = "2017-04-30"
#     stock_data = yf.download(stock_id, start=start_date, end=end_date)
#     stock_data.reset_index(inplace=True)
#     return stock_data

# def get_stock_info(stock_id):
#     return  yf.Ticker(stock_id).info


# def get_scatter_plot(stock_data):
#     stock_data['EWA_20'] = stock_data['Close'].ewm(span=20, adjust=False).mean()
#     return px.scatter(stock_data,
#                     x= stock_data['Date'],
#                     y= stock_data['EWA_20'],
#                     title="Exponential Moving Average vs Date")


# def update_line_plot(clicked, input1, input2, input3):
#     if clicked:
#         stock_id = input1+".NS"
#         start_time = input2
#         end_time = input3
#         print(stock_id, start_time, end_time)
#         df = get_stock_data(stock_id, start_time, end_time)

#         return get_line_plot(df)

# def update_scatter_plot(clicked, input1, input2, input3):
#     if clicked:
#         stock_id = input1+".NS"
#         start_time = input2
#         end_time = input3
#         stock_data = get_stock_data(stock_id, start_time, end_time)


#         return get_scatter_plot(stock_data)

if __name__ == "__main__":
    app.run_server(debug=True)
