from dash import Dash, dcc, html, Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__,external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.H2('Feedmill Price Forecasts(weekly)', style={'textAlign': 'center', 'font-family': 'Arial','fontWeight': 'bold'}),
    dcc.Graph(id="time-series-chart"),
    html.P("Select Feedmill:",style={'textAlign': 'center'}),
    dcc.Dropdown(
        id="ticker",
        options=["PT. Gold Coin","PT. Universal", "PT. NEW HOPE INDONESIA","CPI","Japfa","QLFeed","QLAgrofood","WidodoMakmur","Farmsco","SabasDian","KertamulyaSari","Agrico","Wonokoyo","CibadakIndah","Gorontalo","NTB"],
        value="PT. Gold Coin",
        clearable=False,
        style={'width': '50%', 'margin': 'auto'}
    ),
    html.Br(),
    html.Br(),
    html.Button('Download CSV', id='export-csv-button', n_clicks=0),
    dcc.Download(id="download-dataframe-csv")
])


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

@app.callback(Output('download-dataframe-csv', 'data'),
              Input('export-csv-button', 'n_clicks'),
              Input('ticker', 'value'))
def download_csv(n_clicks, ticker):
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


app.run_server(debug=True,use_reloader=False,port=8000, host='127.0.0.1')
