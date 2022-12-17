from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.stattools import acf
import plotly.graph_objects as go
import numpy as np
import math


app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

# df = pd.read_csv('preprocessed_data.csv')
# freqs = pd.read_csv('freqs.csv')
# psd = pd.read_csv('psd.csv')
# tpreds = pd.read_csv('tpreds.csv')
# y_test = pd.read_csv('y_test.csv')
# tpreds.index = y_test['InvoiceDate']
# mapes = pd.read_csv('mapes.csv')
# mapes = mapes['0'].tolist()

# IMPORT DATASETS
df = pd.read_csv('df_day_head.csv')
merged = pd.read_csv('merged.csv') # ARIMA
prophet_mapes = pd.read_csv('prophet_mapes.csv')


# Derived Lists
users = list(set(df['user'].tolist()))
users.sort()

user_focus = None

models = ['ARIMA', 'Prophet', 'DeepAR']


@app.callback(
    [Output('graph-court', 'figure')],
    [Input('user-dropdown', 'value')]
)

def update_graph(linedropval):
    #global df_filtered
    subset = df.loc[df['user'] == linedropval]
    subset.sort_values('date', inplace=True)

    global user_focus
    user_focus = linedropval
    
    line_chart = px.line(
            data_frame=subset,
            x='date',
            y='sum_per_day',
            labels={'Rate':'rate', 'Datetime':'date'},
            )
    line_chart.update_layout()

    return [line_chart]


@app.callback(Output('final_table', 'children'),
            Input('model-dropdown', 'value'))
def print_MAPE(value):
	# return user_focus

	if value == 'ARIMA':
		subset = merged.loc[merged['Unnamed: 0'] == user_focus]
		vals = subset[['first_3', 'middle_3', 'last_3']].values.tolist()
		vals = vals[0]
		vals = [round(a, 2) * 100 for a in vals]
		retstr = "First 3 Months " + str(vals[0]) + "% | Second 3 Months " + str(vals[1]) + "% | Last 3 Months " + str(vals[2]) + "%"
		retstr = retstr + "\nModel = " + subset['model']

		return retstr
	elif value == 'Prophet':
		subset = prophet_mapes.loc[prophet_mapes['user'] == user_focus]
		vals = subset[['1st_90', '2nd_90', '3rd_90']].values.tolist()
		print(vals)
		vals = vals[0]
		vals = [round(a, 2) * 100 for a in vals]
		retstr = "First 3 Months " + str(vals[0]) + "% | Second 3 Months " + str(vals[1]) + "% | Last 3 Months " + str(vals[2]) + "%"

		return retstr
	else:
		return ""
	


app.layout = html.Div(children=[
    html.H1(children='Electricity Usage Forecast'),
    html.H2(children='Time Series of Electricity Consumption'),
    
    html.Div([
	html.H3(children='Select User:'),
    dcc.Dropdown(users, id='user-dropdown', value=users[0]),
    dcc.Graph(id='graph-court'),
    html.Div(children="Select Model:"),
    dcc.Dropdown(models, id='model-dropdown'),
    html.H3(children="MAPE Breakdowns:"),
    html.Div(id='final_table')
	])





    # html.Div(children=[
    # # fig.show()
    # html.H2(children='Autocorrelation Plot & PSD'),
    # dcc.Graph(id='pacf', figure=fig2, style={'display': 'inline-block'}),

    # dcc.Graph(id='psd', figure=fig3, style={'display': 'inline-block'})
    # ]),

    # html.H2(children='Forecast with best ARIMA Model'),

    # dcc.Graph(
    #     id='finalForecast',
    #     figure=fig4,
    # ),

    # html.H2(children='Model Performance on Test Data - Section-wise Horizon'),
    # html.Div(children=[
        
    #     dcc.Graph(id='chunk1', figure=figs[0], style={'display': 'inline-block','width':'300'}),
    #     dcc.Graph(id='chunk2', figure=figs[1], style={'display': 'inline-block','width':'300'}),
    #     dcc.Graph(id='chunk3', figure=figs[2], style={'display': 'inline-block','width':'300'}),
    #     dcc.Graph(id='chunk4', figure=figs[3], style={'display': 'inline-block','width':'300'}),
    # ])



   
])



if __name__ == '__main__':
    app.run_server(debug=True)