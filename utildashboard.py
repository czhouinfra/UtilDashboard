import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas_datareader.data as pdr
from datetime import datetime
import os
import yfinance as yf
import dash_auth
import dashtools

yf.pdr_override()

USERNAME_PASSWORD_PAIRS = [['username','password'],['gcinfra','gcinfra']]

app = dash.Dash()
server = app.server

auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

app.layout = html.Div([
                html.H1('New Stock Chart'),
                html.Div([
                    html.H3('Enter a new stock symbol',style={'paddingRight':'30px'}),
                    dcc.Input(id='stock_ticker_input',
                                value='AAPL',
                              style={'fontSize':24, 'width': 75}),
                    ], style={'display': 'inline-block','verticalAlign':'top'}),
                html.Div([
                    html.H3('Select a start date and end date:'),
                    dcc.DatePickerRange(id='date_picker_input',
                                        min_date_allowed=datetime(2019,1,1),
                                        max_date_allowed=datetime.today(),
                                        start_date=datetime(2020,1,1),
                                        end_date=datetime.today()
                                        )
                ], style={'display': 'inline-block'}),
                html.Button(id='submit_button',
                            n_clicks=0,
                            children='Submit',
                            style={'fontSize':24, 'marginLeft':'30px'}),
                dcc.Graph(
                    id='stock_chart',
                    figure={
                        'data': [],
                        'layout': {'title': 'name'}
                    }
                )
])

@app.callback(Output('stock_chart','figure'),
              [Input('submit_button','n_clicks')],
              [State('stock_ticker_input','value'),
               State('date_picker_input','start_date'),
               State('date_picker_input','end_date')],
              )

def generate_output(n_clicks, stock_ticker, start_date, end_date):
    start = start_date
    end = end_date
    df = pdr.get_data_yahoo(stock_ticker, start, end)

    fig = {
        'data': [
            {'x': df.index,
            'y': df['Close']}
        ],
        'layout': {'title': stock_ticker}
    }
    return  fig


if __name__ == '__main__':
    app.run_server()

