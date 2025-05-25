import pandas as pd
import plotly.express as px

# Load the data
data = pd.read_csv("datasets/mashup/mashup2.csv")

# Filter for year 2017
df = data[data["year"] == 2019].copy()

# Extract country code (e.g. IT, DE, FR...)
df["country_code"] = df["nuts2_code"].str[:2]

# Compute average values per country
country_avg = df.groupby("country_code")[["fertility", "poverty", "tertiary_educ"]].mean().reset_index()

# Rename for clarity
country_avg = country_avg.rename(columns={
    "fertility": "Fertility",
    "poverty": "Poverty (%)",
    "tertiary_educ": "Tertiary Education (%)"
})

# Sort countries alphabetically
country_avg = country_avg.sort_values("country_code")

# Reshape for visualization
long_df = country_avg.melt(
    id_vars="country_code",
    var_name="Indicator",
    value_name="Value"
)

fig = px.bar(
    long_df,
    x="country_code",
    y="Value",
    color="Indicator",
    barmode="group",
    title="<b>Average Fertility, Poverty and Education by Country (2019" \
    ")</b>",
    labels={"country_code": "Country", "Value": "Value"},
    height=600
)

# Style adjustments
fig.update_layout(
    font=dict(size=14),
    title_font_size=20,
    legend_title_text="Indicator",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor="#f9f9f9",
    paper_bgcolor="#ffffff"
)

fig.write_html("visualizations/viz2_bar_chart_country_2019.html")
fig.show()
