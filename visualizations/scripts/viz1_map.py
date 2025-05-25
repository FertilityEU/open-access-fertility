import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

# Carica i dati
data = pd.read_csv("datasets/mashup/mashup1.csv", sep=",")
print(data.columns.tolist())

# Filtra anno 2018
data_2019 = data[data["year"] == 2019]

# Trasforma in formato largo (una riga per inquinante)
pivoted = data_2019.pivot_table(
    index=["nuts2_code", "fertility"],
    columns="air_pollutant",
    values="pollutant_av",
    aggfunc="mean"
).reset_index()

# Rinomina colonne
pivoted.columns.name = None
pivoted = pivoted.rename(columns={
    "NO2": "NO2_mean",
    "O3": "O3_mean",
    "PM2.5": "PM25_mean"
})

# Carica il GeoJSON
with open("assets/js/nuts2_simplified.geojson") as f:
    geojson = json.load(f)

# Mappa codici NUTS2 → nome regione
region_names = {f["properties"]["NUTS_ID"]: f["properties"]["NAME_LATN"] for f in geojson["features"]}

# Codici per layer contorni
all_nuts_codes = [f['properties']['NUTS_ID'] for f in geojson['features']]
full_df = pd.DataFrame({'nuts2_code': all_nuts_codes})

# Merge e assegna region name
merged_df = full_df.merge(pivoted, on='nuts2_code', how='left')
merged_df['region_name'] = merged_df['nuts2_code'].map(region_names)

# Hover data
customdata = merged_df[[
    'region_name', 'fertility', 'O3_mean', 'PM25_mean'
]].to_numpy()

# Mappa cloropletica colorata per NO₂
fig = px.choropleth(
    data_frame=merged_df,
    geojson=geojson,
    locations='nuts2_code',
    featureidkey='properties.NUTS_ID',
    color='NO2_mean',
    color_continuous_scale="Inferno",
    labels={'NO2_mean': 'NO₂ (µg/m³)'},
    hover_name='region_name'
)

# Hover personalizzato
fig.data[0].customdata = customdata
fig.data[0].hovertemplate = (
    "<b>%{customdata[0]}</b><br>" +
    "NO₂: %{z:.1f} µg/m³<br>" +
    "Fertility: %{customdata[1]:.2f}<br>" +
    "O₃: %{customdata[2]:.1f} µg/m³<br>" +
    "PM2.5: %{customdata[3]:.1f} µg/m³<extra></extra>"
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

# Layout geografico
fig.update_geos(
    showcountries=False,
    showcoastlines=False,
    showland=False,
    visible=False,
    center={"lat": 50, "lon": 10},
    projection_scale=3
)

# Layout finale
fig.update_layout(
    title_text='NO₂ & Reproductive Indicators in Europe (2019)',
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    coloraxis_colorbar=dict(title="NO₂ (µg/m³)", thickness=15, len=0.75)
)

# Salva e mostra
fig.write_html("visualizations/viz1_map.html", full_html=False, include_plotlyjs='cdn')
fig.show()
