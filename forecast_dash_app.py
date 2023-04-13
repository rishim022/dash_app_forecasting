import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from dash.exceptions import PreventUpdate
import io
from datetime import datetime
from dash_extensions import Download

new_df=Gold_coin_prediction.join([Universal_prediction, NewHope_prediction,CPI_prediction,Japfa_prediction,QLFeed_prediction,QLAgrofood_prediction,WidodoMakmur_prediction,Farmsco_prediction,SabasDian_prediction,KertamulyaSari_prediction,Agrico_prediction,Wonokoyo_prediction,CibadakIndah_prediction,Gorontalo_prediction,NTB_prediction])
new_df_average=new_df.copy()
new_df_average.reset_index(inplace=True)
df_weekly_average = new_df_average.groupby(pd.Grouper(key='index', freq='W-SUN')).mean()[['PT. Gold Coin', 'yhat_PT. Gold Coin','PT. Universal','yhat_PT. Universal','PT. NEW HOPE INDONESIA','yhat_PT. NEW HOPE INDONESIA','CPI','yhat_CPI','Japfa','yhat_Japfa','QLFeed','yhat_QLFeed','QLAgrofood','yhat_QLAgrofood','WidodoMakmur','yhat_WidodoMakmur','Farmsco','yhat_Farmsco','SabasDian','yhat_SabasDian','KertamulyaSari','yhat_KertamulyaSari','Agrico','yhat_Agrico','Wonokoyo','yhat_Wonokoyo','CibadakIndah','yhat_CibadakIndah','Gorontalo','yhat_Gorontalo','NTB','yhat_NTB']]
df_weekly_average ['week_start'] = df_weekly_average.index

with open('Downloads/logo_jiva (1).jpg', 'rb') as f:
    img = f.read()

# Encode the image in base64
encoded_image = base64.b64encode(img).decode()

image_element = html.Img(src='data:image/png;base64,{}'.format(encoded_image),style={'position': 'absolute', 'top': '0', 'left': '0'})


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,suppress_callback_exceptions=True,external_stylesheets=external_stylesheets)
header_element = html.Div([
    image_element,
    html.Div([
        html.H1('Welcome to the Home Page!',id='header-1',style={'textAlign': 'center', 'fontWeight': 'bold'})
    ],style={'textAlign': 'center'}),
], style={'alignItems': 'center'})

index_page = html.Div([
    header_element,
    html.Div([
        html.A('Feedmill Price Forecasts', href='/page-1', id='page-1-link', className='hyperlink')
    ], style={'textAlign': 'center', 'fontWeight': 'bold'}),
    html.Br(),
    dcc.Store(id='header-text', data='Welcome to the Home Page!'),
    html.Div(id='page-content')
])


page_1_layout = html.Div([
    dcc.Link('Go back to Home Page', href='/', id='home-page-link',style={'textAlign': 'right','left': '1470px','bottom': '70px','position': 'relative'}),
    html.P("Select Feedmill:",style={'textAlign': 'center'}),
    dcc.Dropdown(
        id="ticker",
        options=["PT. Gold Coin","PT. Universal", "PT. NEW HOPE INDONESIA","CPI","Japfa","QLFeed","QLAgrofood","WidodoMakmur","Farmsco","SabasDian","KertamulyaSari","Agrico","Wonokoyo","CibadakIndah","Gorontalo","NTB"],
        value="PT. Gold Coin",
        clearable=False,
        style={'width': '50%', 'margin': 'auto'}
    ),
    html.Div([html.H2('Feedmill price forecasts(daily)')]),
    dcc.Graph(id="page-1-graph"),
    html.Br(),
    html.Div(html.Button('Download CSV(Daily)', id='export-csv-button', n_clicks=0),style={'textAlign': 'center'}),
    Download(id="download-dataframe-csv"),
    html.Br(),
    html.Div(id='mae-div', style={'textAlign': 'right',
                                 'position': 'absolute',
                                  'top': '730px',
                                  'bottom': '20px',
                                  'right': '150px'
                                     }),
    html.Br(),
    html.Div(id='mae-rolling-div', style={'textAlign': 'right',
                                 'position': 'absolute',
                                  'top': '750px',
                                  'bottom': '50px',
                                  'right': '150px'
                                     }),
    html.H2('Feedmill price forecasts(weekly)'),
    dcc.Graph(id="time-series-chart"),
    html.Br(),
    html.Div(html.Button('Download CSV(Weekly)',id='export-csv-button1', n_clicks=0),style={'textAlign': 'center'}),
    Download(id="download-dataframe1-csv"),
    html.Div(id='mae-div-weekly', style={'textAlign': 'right',
                                 'position': 'absolute',
                                  'top': '1370px',
                                  'bottom': '20px',
                                  'right': '150px'}),
    html.Br(),
    html.Div(id='mae-rolling-div-weekly', style={'textAlign': 'right',
                                 'position': 'absolute',
                                  'top': '1390px',
                                  'bottom': '50px',
                                  'right': '150px'})
])
    

app.layout = html.Div([
    dcc.Location(id='url',refresh=False),
    index_page])

def display_time_series_2(ticker, pathname):
    if pathname == '/page-1':
        filtered_df = new_df.loc[:, [ticker, f"yhat_{ticker}", f"y_lower_{ticker}", f"y_upper_{ticker}"]]
        filtered_df[f"yhat_{ticker}"] = filtered_df[f"yhat_{ticker}"].iloc[-7:]
        filtered_df[f"y_lower_{ticker}"] = filtered_df[f"y_lower_{ticker}"].iloc[-7:]
        filtered_df[f"y_upper_{ticker}"] = filtered_df[f"y_upper_{ticker}"].iloc[-7:]

        # Add rolling mean line
        rolling_mean = filtered_df[ticker].rolling(window=7, min_periods=1).mean().shift(7)
        fig = go.Figure()
        fig.add_trace(go.Scattergl(x=filtered_df.index, y=filtered_df[ticker],
                        mode='lines',
                        name='Actual'))
        fig.add_trace(go.Scattergl(x=filtered_df.index, y=rolling_mean,
                        mode='lines',
                        name='Rolling Mean'))
        fig.add_trace(go.Scattergl(x=filtered_df.index, y=filtered_df[f"yhat_{ticker}"],
                        mode='lines',
                        name="Predicted"))
        fig.add_trace(go.Scattergl(x=filtered_df.index, y=filtered_df[f"y_lower_{ticker}"],
                    fill='tonexty',
                    mode='lines',
                    fillcolor='rgba(255, 0, 0, 0.2)',
                    line=dict(color='blue'),
                    name="lower bound"))
        fig.add_trace(go.Scattergl(x=filtered_df.index, y=filtered_df[f"y_upper_{ticker}"],
                    fill='tonexty',
                    mode='lines',
                    fillcolor='rgba(255, 0, 0, 0.2)',
                    line=dict(color='red'),
                    name="upper bound"))
        fig.update_xaxes(title_text='Date',
        title_font=dict(
            family="Arial, sans-serif",
            size=18,
            color="black"))
        fig.update_yaxes(
        title_text='Feedmill Price',
        title_font=dict(
            family="Arial, sans-serif",
            size=18,
            color="black"))
        fig.update_layout(legend=dict(title="Legend", orientation="v", y=1.1, x=1.05, xanchor="center", bgcolor='rgba(0,0,0,0)'),
                         margin=dict(l=20, r=20, t=80, b=30)
                         )
        fig.update_traces(marker=dict(size=1.5))      
    elif pathname == '/page-2':
        filtered_df = df_weekly_average.loc[:, [ticker, f"yhat_{ticker}"]]
        filtered_df[f"yhat_{ticker}"] = filtered_df[f"yhat_{ticker}"].iloc[-2:]
        fig = px.line(filtered_df)
        fig.update_xaxes(title_text='Week_start')
        fig.update_yaxes(title_text='Feedmill Price')
    else:
        fig = {}
    return fig

@app.callback(Output('page-1-graph', 'figure'),
              Input('url', 'pathname'),
              Input('ticker', 'value'))
def update_graph(pathname, ticker):
    fig = display_time_series_2(ticker, '/page-1')
    return fig        



@app.callback(
    Output("time-series-chart", "figure"), 
    Input("ticker", "value"))

def display_time_series(ticker):
    filtered_df = df_weekly_average.loc[:, [ticker, f"yhat_{ticker}"]]
    filtered_df[f"yhat_{ticker}"] = filtered_df[f"yhat_{ticker}"].iloc[-2:]
    
    rolling_mean = filtered_df[ticker].rolling(window=7, min_periods=1).mean().shift(1)
    fig = go.Figure()
    fig.add_trace(go.Scattergl(x=filtered_df.index, y=filtered_df[ticker],
                    mode='lines',
                    name='Actual'))
    fig.add_trace(go.Scattergl(x=filtered_df.index, y=rolling_mean,
                    mode='lines',
                    name='Rolling Mean'))
    fig.add_trace(go.Scattergl(x=filtered_df.index, y=filtered_df[f"yhat_{ticker}"],
                    mode='lines',
                    name="Predicted"))
    
    fig.update_xaxes(title_text='Date',
    title_font=dict(
        family="Arial, sans-serif",
        size=18,
        color="black"))
    fig.update_yaxes(
    title_text='Feedmill Price',
    title_font=dict(
        family="Arial, sans-serif",
        size=18,
        color="black"))
    fig.update_layout(legend=dict(title="Legend", orientation="v", y=1.1, x=1.05, xanchor="center", bgcolor='rgba(0,0,0,0)'),
                     margin=dict(l=20, r=20, t=80, b=30)
                     )
    fig.update_traces(marker=dict(size=1.5))
    return fig


@app.callback(Output('download-dataframe1-csv', 'data'),
              Input('export-csv-button1', 'n_clicks'),
              Input('ticker', 'value'))
def download_csv_1(n_clicks, ticker):
    if n_clicks == 0:
        raise PreventUpdate
    filtered_df_weekly = df_weekly_average.loc[:, [ticker, f"yhat_{ticker}"]]
    filtered_df_weekly[f"{ticker}_rolling_mean"] = filtered_df_weekly[ticker].rolling(window=7, min_periods=1).mean().shift(1)
    filtered_df_weekly.reset_index(inplace=True)
    csv_string = io.StringIO()
    filtered_df_weekly.to_csv(csv_string, index=False, encoding='utf8')
    csv_string.seek(0)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{ticker}_weekly_price_forecasts_{timestamp}.csv"
    return dict(filename=filename, content=csv_string.getvalue())


@app.callback(Output('download-dataframe-csv', 'data'),
              Input('export-csv-button', 'n_clicks'),
              Input('ticker', 'value'))
def download_csv(n_clicks, ticker):
    if n_clicks == 0:
        raise PreventUpdate
    filtered_df = new_df.loc[:, [ticker, f"yhat_{ticker}",f"y_lower_{ticker}",f"y_upper_{ticker}"]]
    filtered_df[f"{ticker}_rolling_mean"] = filtered_df[ticker].rolling(window=7, min_periods=1).mean().shift(7)
    filtered_df.reset_index(inplace=True)
    csv_string = io.StringIO()
    filtered_df.to_csv(csv_string, index=False, encoding='utf8')
    csv_string.seek(0)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{ticker}_daily_price_forecasts_{timestamp}.csv"
    return dict(filename=filename, content=csv_string.getvalue())


@app.callback(Output('mae-div', 'children'),
              Input('ticker', 'value'))
def display_mae(ticker):
    filtered_df = new_df.loc[:, [ticker, f"yhat_{ticker}"]]
    mae = np.mean(np.abs(filtered_df[ticker] - filtered_df[f"yhat_{ticker}"]))
    return html.Div([
        html.Div(f"Mean Absolute Error: {mae:.2f}"),
    ])


@app.callback(Output('mae-rolling-div', 'children'),
              Input('ticker', 'value'))
def display_rolling_mae(ticker):
    filtered_df = new_df.loc[:, [ticker, f"yhat_{ticker}"]]
    filtered_df[f"{ticker}_rolling_mean"] = filtered_df[ticker].rolling(window=7, min_periods=1).mean().shift(7) # change window size as per your requirement
    mae_rolling = np.mean(np.abs(filtered_df[f"{ticker}_rolling_mean"] - filtered_df[f"yhat_{ticker}"]))
    return html.Div([
        html.Div(f"Mean Absolute Error of Rolling Mean: {mae_rolling:.2f}")
    ])

@app.callback(Output('mae-rolling-div-weekly', 'children'),
              Input('ticker', 'value'))
def display_rolling_mae(ticker):
    filtered_df = df_weekly_average.loc[:, [ticker, f"yhat_{ticker}"]]
    filtered_df[f"{ticker}_rolling_mean"] = filtered_df[ticker].rolling(window=7, min_periods=1).mean().shift(1) # change window size as per your requirement
    mae_rolling = np.mean(np.abs(filtered_df[f"{ticker}_rolling_mean"] - filtered_df[f"yhat_{ticker}"]))
    return html.Div([
        html.Div(f"Mean Absolute Error of Rolling Mean: {mae_rolling:.2f}")
    ])

@app.callback(Output('mae-div-weekly', 'children'),
              Input('ticker', 'value'))
def display_mae(ticker):
    filtered_df = df_weekly_average.loc[:, [ticker, f"yhat_{ticker}"]]
    mae = np.mean(np.abs(filtered_df[ticker] - filtered_df[f"yhat_{ticker}"]))
    return html.Div([
        html.Div(f"Mean Absolute Error: {mae:.2f}"),
    ])


@app.callback(
    Output('page-content', 'children'),
    Output('header-1', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/':
        header_text = 'Welcome to the Home Page!'
        page_content = html.Div()
    elif pathname == '/page-1':
        header_text = 'Feedmill Price Forecasting (Main Page)'
        page_content = page_1_layout
    else:
        header_text = '404 Error: Page not found'
        page_content = html.Div([
            html.H1(header_text),
            dcc.Link('Go back to home', href='/')
        ])
    return page_content, header_text
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False, port=8000, host='127.0.0.1')
