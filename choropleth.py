import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


GEOJSON_FILE = "USStates.geojson"
df = pd.read_csv("taxData2021.csv")

# Should change on button press
# 1 is left, 2 is right
title1 = 'title1'
title2 = 'title2'
view1 = 'T20'
view2 = 'T01'

fig = make_subplots(rows=1, cols=2,subplot_titles=[title1,title2],
                    specs=[[{'type':'choropleth'},{'type':'choropleth'}]])
fig.add_trace(
    go.Choropleth(locations=df['item'], z=df[view1], locationmode='USA-states', colorbar=dict(thickness=20, x=0.46) ), row=1, col=1)

fig.add_trace(
    go.Choropleth(locations=df['item'], z=df[view2], locationmode='USA-states', colorbar=dict(thickness=20, x=1.02)), row=1, col=2)

fig.update_geos(
    visible=False, resolution=110, scope="usa",
    showcountries=True, countrycolor="Black"
)
fig.update_layout(height=500, margin={"r":0,"t":100,"l":0,"b":0})
fig.show()