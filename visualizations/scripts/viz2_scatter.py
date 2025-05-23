import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

# Carica il tuo dataset
data = pd.read_csv("datasets/mashup/mashup2.csv")

# Dizionario di mappatura dei codici ISO alpha-2 ai nomi dei paesi
iso_country_mapping = {
    'AT': 'Austria',
    'BE': 'Belgium',
    'BG': 'Bulgaria',
    'CY': 'Cyprus',
    'CZ': 'Czech Republic',
    'DE': 'Germany',
    'DK': 'Denmark',
    'EE': 'Estonia',
    'EL': 'Greece',
    'ES': 'Spain',
    'FI': 'Finland',
    'FR': 'France',
    'HR': 'Croatia',
    'HU': 'Hungary',
    'IE': 'Ireland',
    'IT': 'Italy',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'LV': 'Latvia',
    'MT': 'Malta',
    'NL': 'Netherlands',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'SE': 'Sweden',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
}

# Estrai il codice paese dai codici NUTS2
data['country_code'] = data['nuts2_code'].str[:2]

# Mappa i codici ai nomi dei paesi
data['country_name'] = data['country_code'].map(iso_country_mapping)

# Filtra per anno 2018
df = data[data["year"] == 2018].copy()
df["country"] = df["nuts2_code"].str[:2]

# Normalizza educazione per evitare ridimensionamento dinamico
scaler = MinMaxScaler()
df["educ_norm"] = scaler.fit_transform(df[["tertiary_educ"]])

# Scatterplot con size normalizzato
fig = px.scatter(
    df,
    x="poverty",
    y="fertility",
    color="country_name",
    size="educ_norm",
    size_max=40,
    hover_name="nuts2_code",
    labels={
        "poverty": "Povertà (%)",
        "fertility": "Fertilità",
        "educ_norm": "Educazione Terziaria (normalizzata)",
        "country_name": "Country"
    },
    title="Fertilità vs Povertà (dimensione = Educazione) – NUTS2 (2018)",
    height=600
)

# Imposta solo Italia come visibile inizialmente
for trace in fig.data:
    trace.visible = 'legendonly'  # Imposta tutti come nascosti
    if trace.name == 'Italy':
        trace.visible = True  # Mostra solo l'Italia

fig.write_html("visualizations/viz2_scatter2018.html")
fig.show()