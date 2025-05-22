import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

# Carica i dati
data = pd.read_csv("datasets/mashup/mashup2.csv")  # Modifica con il tuo path

# Filtra solo l'anno 2017
df = data[data["year"] == 2017].copy()

# Estrai codice paese (es. IT, DE, FR...)
df["country_code"] = df["nuts2_code"].str[:2]

# Calcola media per paese
country_avg = df.groupby("country_code")[["fertility", "poverty", "tertiary_educ"]].mean().reset_index()

# Normalizza i valori (Min-Max)
scaler = MinMaxScaler()
country_avg_scaled = country_avg.copy()
country_avg_scaled[["fertility", "poverty", "tertiary_educ"]] = scaler.fit_transform(
    country_avg[["fertility", "poverty", "tertiary_educ"]]
)

# Rinomina colonne per il grafico
country_avg_scaled = country_avg_scaled.rename(columns={
    "fertility": "Fertilità (norm.)",
    "poverty": "Povertà (norm.)",
    "tertiary_educ": "Educazione terziaria (norm.)"
})

# Porta in formato long per plotly
long_df = country_avg_scaled.melt(
    id_vars="country_code",
    var_name="Indicatore",
    value_name="Valore normalizzato"
)

# Crea grafico
fig = px.bar(
    long_df,
    x="country_code",
    y="Valore normalizzato",
    color="Indicatore",
    barmode="group",
    title="Confronto Normalizzato di Fertilità, Povertà ed Educazione per Paese (2017)",
    labels={"country_code": "Paese"},
    height=600
)

fig.write_html("visualizations/viz2/viz2_grafico_normalizzato_per_paese.html")
fig.show()
