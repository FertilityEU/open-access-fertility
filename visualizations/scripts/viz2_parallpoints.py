import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv("datasets/mashup/mashup2.csv")
df = data[data["year"] == 2017].copy()
df["country_code"] = df["nuts2_code"].str[:2]

country_avg = df.groupby("country_code")[["fertility", "poverty", "tertiary_educ"]].mean().reset_index()
scaler = MinMaxScaler()
norm_values = scaler.fit_transform(country_avg[["fertility", "poverty", "tertiary_educ"]])
country_avg_norm = pd.DataFrame(norm_values, columns=["Fertilità", "Povertà", "Educazione"])
country_avg_norm["Paese"] = country_avg["country_code"]

fig = px.parallel_coordinates(
    country_avg_norm,
    dimensions=["Fertilità", "Povertà", "Educazione"],
    color="Fertilità",
    labels={
        "Fertilità": "Fertilità (norm.)",
        "Povertà": "Povertà (norm.)",
        "Educazione": "Educazione terziaria (norm.)"
    },
    color_continuous_scale=px.colors.sequential.Magma
)

fig.update_layout(title="Relazione tra Fertilità, Povertà ed Educazione nei Paesi Europei (2017)")
fig.write_html("visualizations/viz2_grafico_parallel_coordinates.html")
fig.show()
