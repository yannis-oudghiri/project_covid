from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import numpy as np
import pycountry_convert as pc

europe_growth = pd.read_csv('./data/europe_growth.csv',index_col=0)

growth = pd.read_csv('./data/growth.csv', index_col=1).drop(columns = ['Unnamed: 0']).stack()\
    .reset_index().rename(columns = {'Real GDP growth (Annual percent change)' : 'Country'})

animation = pd.read_csv('./data/animation.csv')

#Ajinkya
mendeley = pd.read_excel("data/mendeley_data.xlsx")
mendeley.drop(columns= ["Unnamed: 9", "Unnamed: 10", "Unnamed: 11", "Unnamed: 12", "Unnamed: 13"], inplace=True)

country_codes = mendeley.iso_code.unique().tolist()
continent_code = []
alpha2 = []

for c in country_codes:
    try:
        alpha2.append(pc.country_alpha3_to_country_alpha2(c))
    except:
        alpha2.append("Unknown")


for a in alpha2:
    try:
        continent_code.append(pc.country_alpha2_to_continent_code(a))
    except:
        continent_code.append("Unknown")

mendeley_grouped = mendeley_grouped = mendeley.groupby(by = "location")[['human_development_index','gdp_per_capita','population','total_cases']].agg(np.mean)
mendeley_grouped.reset_index(inplace=True)

mendeley_grouped["continent"] = continent_code
df2_grouped = mendeley_grouped.replace({'AS':'Asia', 'EU':'Europe', 'AF':'Africa', 'AN':'Antarctica', 'NA':'North America', 'SA':'South America', 'OC':'Oceania'})

europe_growth_stack = europe_growth.stack().reset_index().rename(columns = {'level_0' : 'date','level_1' : 'Country', 0 : 'growth'})

fig1 = px.line(europe_growth_stack, x='date', y='growth', color='Country', title='GROWTH')

fig2 = px.scatter(mendeley_grouped, x="human_development_index", y="gdp_per_capita", size="population", hover_name="location", color='location', template='simple_white', size_max=70)
fig2.update_layout(
    height=500,
    title_text="Comparison between a Country's GDP per Capita and HDI"
)

fig3 = px.scatter(mendeley_grouped, x="gdp_per_capita", y="total_cases", color="location" ,size="population", hover_name="location", template='simple_white', size_max=70)
fig3.update_layout(
    height=500,
    title_text="COVID-19 Cases (mean) vs GDP per Capita (per Country)"
)

fig4 = px.bar(mendeley_grouped, x='continent', y='total_cases', hover_name='location', color='continent', template="simple_white")
fig4.update_layout(
    height=500,
    title_text='COVID-19 Cases per Continent'
)
fig4.update_xaxes(showticklabels=False)

fig5 = px.choropleth(animation, locations="iso_code",
                    color='new_cases_smoothed_per_million', 
                    hover_name="location",
                    animation_frame="date",
                    range_color=[0,10000],
                    color_continuous_scale=px.colors.sequential.Greens)

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    dcc.Link('Graphic 1', href='/page-1'),
    html.Br(),
    dcc.Link('Graphic 2', href='/page-2'),
])

page_1_layout = html.Div([
    html.H1('Page 1'),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig5),
    dcc.Dropdown(growth.Country.unique(), 'France', id='dropdown-selection'),
    dcc.Graph(id='graph-content'),
    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])


@callback(Output('page-1-content', 'children'),
          Input('page-1-dropdown', 'value'))
def page_1_dropdown(value):
    return f'You have selected {value}'


page_2_layout = html.Div([
    html.H1('Page 2'),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
    dcc.Graph(figure=fig4),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])


@callback(Output('page-2-content', 'children'), Input('page-2-radios', 'value'))
def page_2_radios(value):
    return f'You have selected {value}'


# Update the index
@callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)

def update_graph(value):
    dff = growth[growth.Country==value].rename(columns={'level_1' : 'date',0 : 'growth'})
    dff['growth'] = dff['growth'].replace(',','.',regex=True).astype(float)
    return px.line(dff, x='date', y='growth')


if __name__ == '__main__':
    app.run(debug=True)
