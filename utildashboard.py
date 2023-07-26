import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas_datareader.data as pdr
from datetime import datetime
import dash_auth

USERNAME_PASSWORD_PAIRS = [['username','password'],['gcinfra','gcinfra']]

df = pd.read_excel('https://github.com/czhouinfra/UtilDashboard/blob/main/Dashboard.xlsm', engine='openpyxl', sheet='Contract')
contract_buyer = df['Column1.buyer'].unique()
contract_sign_date = df['Column1.original_signing']
contract_volume = df['Column1.contract_volume_mmt']


app = dash.Dash()

auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

app.layout = html.Div([
                html.H1('China (Mainland) LNG Contract Dashboard'),
                html.Div([
                    html.H3('Select Buyer',style={'paddingRight':'30px'}),
                    dcc.Dropdown(contract_buyer, id='contract_buyer_dropdown',
                              style={'fontSize':18, 'width': 400}),
                    ], style={'display': 'inline-block','verticalAlign':'top','paddingRight':'30px'}),
                html.Div([
                    html.H3('Select a start date and end date:'),
                    dcc.DatePickerRange(id='date_picker_input',
                                        min_date_allowed=datetime(2005,1,1),
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
                    id='chart1',
                    figure={
                        'data': [],
                        'layout': {'title': 'name'}
                    }
                )
])

@app.callback(Output('chart1','figure'),
              [Input('submit_button','n_clicks')],
              [State('contract_buyer_dropdown','value'),
               State('date_picker_input','start_date'),
               State('date_picker_input','end_date')],
              )

def generate_contract_buyer(n_clicks, contract_buyer, start_date, end_date):

    selected_df = df[(df['Column1.buyer']==contract_buyer)
                    &(df['Column1.original_signing']>=start_date)
                    &(df['Column1.original_signing']<=end_date)]
    fig = {
        'data': [
            go.Bar(x=selected_df['Column1.original_signing'],
                   y=selected_df['Column1.contract_volume_mmt'])
        ],
        'layout': {'title': 'Buyer and Signed Date',
                   'xaxis': {'range': [start_date, end_date]}}
    }
    return  fig


if __name__ == '__main__':
    app.run_server()


