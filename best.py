import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('./static/data/all_2.csv')
country_df = df[df['Country Name'] == 'Denmark']
variable_1_df = country_df[country_df['Indicator Name'] == 'GDP (current US$)']
variable_2_df = country_df[country_df['Indicator Name'] == 'CO2 emissions (kt)']
variable_3_df = country_df[country_df['Indicator Name'] == 'Renewable energy consumption (% of total final energy consumption)']

app.layout = html.Div([
    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Scatter(
                    x=variable_1_df['Year'],
                    y=variable_1_df['Value'],
                    name='GDP per capita (current US$)',
                    mode='lines+markers'
                ), 
                go.Scatter(
                    x=variable_2_df['Year'],
                    y=variable_2_df['Value'],
                    name='CO2 emissions (kt)',
                    mode='lines+markers', 
                    yaxis='y2', 
                ), 
                go.Scatter(
                    x=variable_3_df['Year'],
                    y=variable_3_df['Value'],
                    mode='lines+markers', 
                    name='Renewable energy consumption (% of total energy consumption)',
                    yaxis='y3', 
                ), 
            ],
        layout=go.Layout(
            title='Denmark', 
            xaxis={'type': 'linear', 'title': 'Year'},
            yaxis=dict(
                title= 'GDP per capita (current US$)',
                position=0.03,
                titlefont=dict(
                    color='#1f77b4'
                ), 
                tickfont=dict(
                    color='#1f77b4'
                )
            ),
            yaxis2=dict(
                title='CO2 emissions (kt)', 
                overlaying='y', 
                side='left',
                anchor='free', 
                position=0.08, 
                showgrid=False,
                titlefont=dict(
                    color='#ff7f0e'
                 ),
                tickfont=dict(
                    color='#ff7f0e'
                ),
            ), 
            yaxis3=dict(
                title='Renewable energy consumption (% of total energy consumption)',
                overlaying='y', 
                side='right', 
                anchor='x', 
                showgrid=False,
                titlefont=dict(
                    color='#228b22'
                 ),
                tickfont=dict(
                    color='#228b22'
                ),
            ), 
            margin={'l': 20, 'b': 40, 't': 40, 'r': 40},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    ),
    style={'height': 600},
    id='my-graph'
)])

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)