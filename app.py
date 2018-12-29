import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('./data/GDP_growth.csv')
rows = [df.iloc[i] for i in range(len(df))]
rows = [el[el.notnull()] for el in rows]


app.layout = html.Div([
    dcc.Graph(
        id='gdp-per-year',
        figure={
            'data': [
                go.Scatter(
                    y=list(row[4:-1]),
                    x=list(row.index[4:-1]),
                    text=row[0],
                    mode='lines+markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=row[0]
                ) for row in rows
            ],
            'layout': go.Layout(
                xaxis={'type': 'linear', 'title': 'Year'},
                yaxis={'title': 'GDP Per Capita'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)