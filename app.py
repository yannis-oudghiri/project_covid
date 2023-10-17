from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

europe_growth = pd.read_csv('./data/europe_growth.csv',index_col=0)

europe_growth_stack = europe_growth.stack().reset_index().rename(columns = {'level_0' : 'date','level_1' : 'Country', 0 : 'growth'})

fig1 = px.line(europe_growth_stack, x='date', y='growth', color='Country', title='GROWTH')

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Graph(figure=fig1)
])

if __name__ == '__main__':
    app.run(debug=True)
