import pandas as pd
import plotly.express as px

# Carica i dati
data = pd.read_csv("datasets/mashup/mashup2.csv")  # Usa il tuo percorso locale

# Filtra solo l'anno 2017
df = data[data["year"] == 2017].copy()

# Estrai codice paese (es. IT, DE, FR...)
df["country_code"] = df["nuts2_code"].str[:2]

# Calcola media per paese
country_avg = df.groupby("country_code")[["fertility", "poverty", "tertiary_educ"]].mean().reset_index()

# Rinomina per leggibilità
country_avg = country_avg.rename(columns={
    "fertility": "Fertilità",
    "poverty": "Povertà (%)",
    "tertiary_educ": "Educazione terziaria (%)"
})

# Trasforma per visualizzazione
long_df = country_avg.melt(id_vars="country_code", var_name="Indicatore", value_name="Valore")

# Crea il grafico
fig = px.bar(
    long_df,
    x="country_code",
    y="Valore",
    color="Indicatore",
    barmode="group",
    title="Media Fertilità, Povertà ed Educazione per Paese (2017)",
    labels={"country_code": "Paese"},
    height=600
)

fig.write_html("visualizations/viz2_grafico_media_per_paese_2017.html")
fig.show()
