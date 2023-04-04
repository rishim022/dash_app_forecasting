import dash
from dash import dcc, html, Input, Output
import pandas as pd
import io
from dash.exceptions import PreventUpdate
import base64
import csv

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

new_df=Gold_coin_prediction.join([Universal_prediction, NewHope_prediction,CPI_prediction,Japfa_prediction,QLFeed_prediction,QLAgrofood_prediction,WidodoMakmur_prediction,Farmsco_prediction,SabasDian_prediction,KertamulyaSari_prediction,Agrico_prediction,Wonokoyo_prediction,CibadakIndah_prediction,Gorontalo_prediction,NTB_prediction])

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.layout = html.Div([
        html.H2('Feedmill Price Forecasts(daily)', style={'textAlign': 'center', 'font-family': 'Arial','fontWeight': 'bold'}),
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
        dcc.Download(id="download-dataframe-csv"),
        html.Br(),
        html.Div(id='mae-div', style={'textAlign': 'center',
                                 'position': 'absolute',
                                  'bottom': '250px',
                                  'right': '70px'
                                     }),
        html.Br(),
        html.Div(id='mae-rolling-div', style={'textAlign': 'center',
                                 'position': 'absolute',
                                  'bottom': '220px',
                                  'right': '70px'
                                     })
        
    ])
    

@app.callback(
    Output("time-series-chart", "figure"), 
    Input("ticker", "value"))
def display_time_series(ticker):
    filtered_df = new_df.loc[:, [ticker, f"yhat_{ticker}", f"y_lower_{ticker}", f"y_upper_{ticker}"]]
    filtered_df[f"yhat_{ticker}"] = filtered_df[f"yhat_{ticker}"].iloc[-7:]
    filtered_df[f"y_lower_{ticker}"] = filtered_df[f"y_lower_{ticker}"].iloc[-7:]
    filtered_df[f"y_upper_{ticker}"] = filtered_df[f"y_upper_{ticker}"].iloc[-7:]
    
    # Add rolling mean line
    rolling_mean = filtered_df[ticker].rolling(window=7, min_periods=1).mean().shift(7)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[ticker],
                mode='lines',
                name='Actual'))
    fig.add_trace(go.Scatter(x=filtered_df.index, y=rolling_mean,
                mode='lines',
                name='Rolling Mean'))
    fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[f"yhat_{ticker}"],
                mode='lines',
                name="Predicted"))
    fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[f"y_lower_{ticker}"],
                fill='tonexty',
                mode='lines',
                fillcolor='rgba(255, 0, 0, 0.2)',
                name="lower bound"))
    fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[f"y_upper_{ticker}"],
                fill='tonexty',
                mode='lines',
                fillcolor='rgba(0, 255, 0, 0.2)',
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

    return fig

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


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False, port=8000, host='127.0.0.1')
    
    
    
