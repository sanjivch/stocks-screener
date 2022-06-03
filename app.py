from dash import Dash, html, dcc, callback, Output, html, Input, State, no_update
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from datetime import datetime, date

import yfinance as yf
import pandas as pd
import plotly_express as px

from stocks import stock_list



# Create a dash instance
app = Dash(__name__, external_stylesheets=[
        # include google fonts
        "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap"
    ],)

server = app.server

#print(stock_list)
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

    #fig.update_traces(mode= # appropriate mode)


# Define the page layout
# Header section
header_section = html.Div([dmc.Header(
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
                                    dmc.Title(f"Choose from the options below", order=6),
                                    dmc.Divider(label=[
                                                        DashIconify(
                                                            icon="ant-design:stock-outlined", width=15, style={"marginRight": 10}
                                                        ),
                                                        "Stocks",
                                                    ],style={"marginBottom": 10, "marginTop": 10}),
                                    
                                    
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
                                                                value="SBI",
                                                                data=stock_list,
                                                                icon=[DashIconify(icon="radix-icons:magnifying-glass")],
                                                                style={"width": 200,},
                                                            ),
                                                    dmc.Text(id="selected-value"),
                                                    dmc.Group(
                                                        direction="row",
                                                        children= [
                                                            dmc.DatePicker(
                                                                id="start-date-picker",
                                                                label="Start Date",
                                                                required=True,
                                                                minDate=date(2012, 8, 5),
                                                                maxDate=datetime.today(),
                                                                value=datetime.now().date(),
                                                                style={"width": 125},
                                                                ),
                                                            dmc.DatePicker(
                                                                        id="end-date-picker",
                                                                        label="End Date",
                                                                        required=True,
                                                                        minDate=date(2012, 8, 5),
                                                                        maxDate=datetime.today(),
                                                                        value=datetime.now().date(),
                                                                        style={"width": 125},
                                                                        ),
                                                        ],
                                                    ),
                                                    dmc.Space(h=10),
                                
                                                ],
                                            ),
                                    dmc.Group(
                                        direction="row",
                                        children=[
                                            dmc.Button("Data",leftIcon=[DashIconify(icon="bx:data")],id="btn-show-data"),# 
                                            dmc.Space(w=10),
                                            # Indicators button
                                            dmc.Button("Indicators", leftIcon=[DashIconify(icon="carbon:summary-kpi")],), #carbon:summary-kpi
                                        ]
                                    ),
                                    
                                    # ant-design:stock-outlined
                                    dmc.Divider(label=[DashIconify(
                        icon="wpf:future", width=15, style={"marginRight": 10}
                    ),"Forecast"],style={"marginBottom": 20, "marginTop": 20},),
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
                                            dmc.Button("Forecast",leftIcon=[DashIconify(icon="carbon:forecast-lightning")],),#
                                        ],
                                    ),
                                ],
                            )
                        ],
                    ),
                       ], style=nav_container_style) 
                    ], className="nav")

# Content section
content_section = html.Div([dmc.Space(h=50),                        
                            dmc.Group(direction="row",
                                        children=[
                                            dmc.Space(h=20),
                                            # dmc.Image(src=stock_dict['logo_url'], 
                                            #           alt=stock_dict['shortName'], 
                                            #           caption=stock_dict['sector'], 
                                            #           width=75
                                            #           ),
                                            dmc.Space(w=500),                                                
                                            # dmc.Text(stock_dict['longName'], size="lg"),
                                                ]), 
                                dmc.Text(id='display-stock-info'),                               
                                # Stock price plot
                                dcc.Graph(id='stock-plot',),# figure=line_plot),
                                dcc.Graph(id='indicator-plot',),# figure=scatter_plot),
                            
                            
                                # Indicator plot
                           
                            
                                # Forecast plot 
                            
                        ], className="content")

# App layout
app.layout = html.Div([
                        header_section,
                        dmc.Group(direction="row",
                                  children = [nav_section, content_section]
                                  )
                    ])



@app.callback(Output('display-stock-info', 'children'),
                [Input('btn-show-data', 'n_clicks')],
                [State('stock-select', 'value'),State('start-date-picker', 'value'), State('end-date-picker', 'value')])

def update_output(clicked, input1, input2, input3):
    if clicked:
        stock_id = input1+".NS"
        start_time = input2
        end_time = input3
        return 'Data: ' + stock_id + start_time + end_time

@app.callback(Output('stock-plot', 'figure'),
                [Input('btn-show-data', 'n_clicks')],
                [State('stock-select', 'value'),State('start-date-picker', 'value'), State('end-date-picker', 'value')])

def update_line_plot(clicked, stock_id, start_date, end_date):
    if clicked:
        if stock_id == '':
            stock_id = 'SBIN.NS'
        else:
            stock_id = stock_id+".NS"
        stock_data = yf.download(stock_id, start=start_date, end=end_date)
        stock_data.reset_index(inplace=True)
        
        return px.line(x=stock_data['Date'], y=stock_data['High'], title="basic line plots")


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

if __name__ == '__main__':
    app.run_server(debug=True)

    