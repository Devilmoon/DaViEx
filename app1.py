import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import math

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('./static/data/all_5.csv')
df = df.dropna(subset=['Region'])
available_indicators = df['Indicator Name'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=''
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=''
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),  

        html.Div([
            dcc.Checklist(
                id='crossfilter-bubble-size',
                options=[
                    {'label': 'resize bubbles', 'value': 'show'}
                ],
                labelStyle={'display': 'inline-block'},
                values=[]
            )
        ])
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Japan'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(
        id='crossfilter-year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()}
    ), style={'width': '98%', 'padding': '0px 20px 20px 20px'})
])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-bubble-size', 'values'), 
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type, apply_bubble_size, 
                 year_value):
    dff = df[df['Year'] == year_value]
    traces = []
    for i in dff.Region.unique():
        df_by_region = dff[dff['Region'] == i]
        bubble_size_variable = 'Population, total'
        t = df_by_region[df_by_region['Indicator Name'] == bubble_size_variable].fillna(100000)
        if apply_bubble_size:
            '''
            t = df_by_region[df_by_region['Indicator Name'] == bubble_size_variable]
            x = df_by_region[df_by_region['Indicator Name'] == xaxis_column_name]
            x_list = df_by_region[df_by_region['Indicator Name'] == xaxis_column_name]["Country Name"].unique()
            y = df_by_region[df_by_region['Indicator Name'] == yaxis_column_name]
            y_list = df_by_region[df_by_region['Indicator Name'] == yaxis_column_name]["Country Name"].unique()
            for c in x_list:
                if x[x["Country Name"] == c ]["Value"] ==  or y[y["Country Name"] == c ]["Value"] == 'nan':
            bubble_size = []'''
            bubble_size = []
            [bubble_size.append(a/100000) for a in t['Value']]
        else: 
            bubble_size = 15
       # print(len(df_by_region[df_by_region['Indicator Name'] == yaxis_column_name]['Country Name']))
        traces.append(go.Scatter(
            x=df_by_region[df_by_region['Indicator Name'] == xaxis_column_name]['Value'],
            y=df_by_region[df_by_region['Indicator Name'] == yaxis_column_name]['Value'],
            text=df_by_region[df_by_region['Indicator Name'] == yaxis_column_name]['Country Name'],
            customdata=df_by_region[df_by_region['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'sizemode': 'area', 
                'opacity': 0.5,
                'sizemin': 10,
                'size': bubble_size,
                'line': {'width': 0.5, 'color': 'white'}
            }, name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


def create_time_series(dff, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dff['Year'],
            y=dff['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 240,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)

if __name__ == '__main__':
    app.run_server(debug=True, port=8053)