import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

new_df=Gold_coin_prediction.join([Universal_prediction, NewHope_prediction,CPI_prediction,Japfa_prediction,QLFeed_prediction,QLAgrofood_prediction,WidodoMakmur_prediction,Farmsco_prediction,SabasDian_prediction,KertamulyaSari_prediction,Agrico_prediction,Wonokoyo_prediction,CibadakIndah_prediction,Gorontalo_prediction,NTB_prediction])
df_weekly_average = new_df_average.groupby(pd.Grouper(key='index', freq='W-SUN')).mean()[['PT. Gold Coin', 'yhat_PT. Gold Coin','PT. Universal','yhat_PT. Universal','PT. NEW HOPE INDONESIA','yhat_PT. NEW HOPE INDONESIA','CPI','yhat_CPI','Japfa','yhat_Japfa','QLFeed','yhat_QLFeed','QLAgrofood','yhat_QLAgrofood','WidodoMakmur','yhat_WidodoMakmur','Farmsco','yhat_Farmsco','SabasDian','yhat_SabasDian','KertamulyaSari','yhat_KertamulyaSari','Agrico','yhat_Agrico','Wonokoyo','yhat_Wonokoyo','CibadakIndah','yhat_CibadakIndah','Gorontalo','yhat_Gorontalo','NTB','yhat_NTB']]
df_weekly_average ['week_start'] = df_weekly_average.index

app = dash.Dash(__name__,suppress_callback_exceptions=True,external_stylesheets=external_stylesheets)

index_page = html.Div([
    html.H1('Welcome to the Home Page!'),
    dcc.Link('Feedmill Price Forecasts(daily)', href='/page-1'),
    html.Br(),
    dcc.Link('Feedmill Price Forecasts(weekly)', href='/page-2'),
    html.Div(id='page-content')
])

page_1_layout = html.Div([
    html.H1('Welcome to Page 1!'),
    html.H2('Feedmill price forecasting'),
    dcc.Graph(id="time-series-chart"),
    dcc.Graph(id="page-1-graph"),
    html.P("Select Feedmill:"),
    dcc.Dropdown(
        id="ticker",
        options=["PT. Gold Coin","PT. Universal", "PT. NEW HOPE INDONESIA","CPI","Japfa","QLFeed","QLAgrofood","WidodoMakmur","Farmsco","SabasDian","KertamulyaSari","Agrico","Wonokoyo","CibadakIndah","Gorontalo","NTB"],
        value="PT. Gold Coin",
        clearable=False,
    ),
    dcc.Interval(id='interval-component', interval=24*60*60*1000, n_intervals=0),
])
page_2_layout = html.Div([
    html.H1('Welcome to Page 2!'),
    html.H2('Feedmill price forecasting'),
    dcc.Graph(id="time-series-chart"),
    dcc.Graph(id="page-2-graph"),
    html.P("Select Feedmill:"),
    dcc.Dropdown(
        id="ticker-2",
        options=["PT. Gold Coin","PT. Universal", "PT. NEW HOPE INDONESIA","CPI","Japfa","QLFeed","QLAgrofood","WidodoMakmur","Farmsco","SabasDian","KertamulyaSari","Agrico","Wonokoyo","CibadakIndah","Gorontalo","NTB"],
        value="PT. Gold Coin",
        clearable=False,
    ),
])

app.layout = html.Div([
    dcc.Location(id='url'),
    index_page])

def display_time_series(ticker, pathname):
    if pathname == '/page-1':
        filtered_df = new_df.loc[:, [ticker, f"yhat_{ticker}", f"y_lower_{ticker}", f"y_upper_{ticker}"]]
        filtered_df[f"yhat_{ticker}"] = filtered_df[f"yhat_{ticker}"].iloc[-8:]
        filtered_df[f"y_lower_{ticker}"] = filtered_df[f"y_lower_{ticker}"].iloc[-8:]
        filtered_df[f"y_upper_{ticker}"] = filtered_df[f"y_upper_{ticker}"].iloc[-8:]

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
                        fill=None,
                        mode='lines',
                        name="lower bound"))
        fig.add_trace(go.Scattergl(x=filtered_df.index, y=filtered_df[f"y_upper_{ticker}"],
                        fill='tonexty',
                        mode='lines',
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
              Input('interval-component', 'n_intervals'),
              Input('ticker', 'value'),
              prevent_initial_call=True)
def update_graph(n, ticker):
    fig = display_time_series(ticker, '/page-1')
    return fig

@app.callback(
    Output('page-2-graph', 'figure'),
    [Input('url', 'pathname'),
     Input('ticker-2', 'value')])
def update_page_2(pathname, ticker):
    fig = display_time_series(ticker, '/page-2')
    return fig

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return html.Div()
    elif pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return html.Div([
            html.H1('404 Error: Page not found'),
            dcc.Link('Go back to home', href='/')
        ])
# Run the app
if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False, port=8000, host='127.0.0.1')
