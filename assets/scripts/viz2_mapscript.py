import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

# Carica i dati
data = pd.read_csv("datasets/mashup/mashup2.csv")
data_2018 = data[data["year"] == 2018]

# GeoJSON completo
with open("assets/js/nuts2_simplified.geojson") as f:
    geojson = json.load(f)

# Estrai tutti i codici e nomi delle regioni
all_nuts_codes = [f['properties']['NUTS_ID'] for f in geojson['features']]
region_names = {f['properties']['NUTS_ID']: f['properties']['NAME_LATN'] for f in geojson['features']}

region_names = {
    f["properties"]["NUTS_ID"]: f["properties"]["NAME_LATN"]
    for f in geojson["features"]
}

data['region_name'] = data['nuts2_code'].map(region_names)

# Crea DataFrame base e unisci con i dati
full_df = pd.DataFrame({'nuts2_code': all_nuts_codes})
full_df['region_name'] = full_df['nuts2_code'].map(region_names)
merged_df = full_df.merge(data_2018, on='nuts2_code', how='left')

# Crea l'array customdata manualmente
customdata = merged_df[['region_name', 'poverty', 'tertiary_educ']].to_numpy()

# Crea il choropleth con Plotly Express
fig = px.choropleth(
    data_frame=merged_df,    
    geojson=geojson,
    locations='nuts2_code',
    featureidkey='properties.NUTS_ID',
    color='fertility',
    color_continuous_scale="Magma",
    labels={'fertility': 'Fertility'},
    hover_name='region_name'
)


# Assegna il customdata **solo al primo trace**
fig.data[0].customdata = customdata

# Applica l'hovertemplate solo al primo trace
fig.data[0].hovertemplate = (
    "<b>%{customdata[0]}</b><br>" +
    "Fertility: %{z:.2f}<br>" +
    "Poverty: %{customdata[1]:.1f}%<br>" +
    "Education: %{customdata[2]:.1f}%<extra></extra>"
)

# Layer contorni
fig.add_trace(go.Choropleth(
    geojson=geojson,
    locations=all_nuts_codes,
    z=[1]*len(all_nuts_codes),
    featureidkey='properties.NUTS_ID',
    showscale=False,
    colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(0,0,0,0)']],
    marker_line_width=0.8,
    marker_line_color='rgba(80,80,80,0.5)',
    hoverinfo='skip'
))


fig.update_geos(
    showcountries=False,
    showcoastlines=False,
    showland=False,
    visible=False,
    center={"lat": 50, "lon": 10},  # centro approssimativo dell'Europa
    projection_scale=3  # Aumenta per zoomare
)


fig.update_layout(
    title_text='Map Fertility NUTS2 (2018)',
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    coloraxis_colorbar=dict(title="Fertility", thickness=15, len=0.75)
)

fig.write_html("visualizations/viz2_map2018.html")
fig.show()
