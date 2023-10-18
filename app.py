from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np
import pycountry_convert as pc

europe_growth = pd.read_csv('./data/europe_growth.csv',index_col=0)

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

mendeley_grouped = mendeley.groupby(by = "location").agg(np.mean)
mendeley_grouped.reset_index(inplace=True)

mendeley_grouped["continent"] = continent_code
mendeley_grouped = mendeley_grouped.replace({'AS':'Asia', 'EU':'Europe', 'AF':'Africa', 'AN':'Antarctica', 'NA':'North America', 'SA':'South America', 'OC':'Oceania'})

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

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
    dcc.Graph(figure=fig4)
])

if __name__ == '__main__':
    app.run(debug=True)
