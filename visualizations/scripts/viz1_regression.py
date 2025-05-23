import pandas as pd
import plotly.express as px

# 1. Carica il CSV
df = pd.read_csv("Linear regression learner.csv")

# 2. Filtra solo i tre inquinanti
pollutants = ['NO2+Mean(pollutant_av)', 'O3+Mean(pollutant_av)', 'PM2.5+Mean(pollutant_av)']
df_filtered = df[df['Variable'].isin(pollutants)].copy()

# 3. Rinomina per leggibilità
rename_map = {
    'NO2+Mean(pollutant_av)': 'NO₂',
    'O3+Mean(pollutant_av)': 'O₃',
    'PM2.5+Mean(pollutant_av)': 'PM2.5'
}
df_filtered['Pollutant'] = df_filtered['Variable'].map(rename_map)

# 4. Aggiungi colonna per significatività
df_filtered['Significance'] = df_filtered['P>|t|'].apply(lambda p: 'Significant (p < 0.05)' if p < 0.05 else 'Not significant')

# 5. Crea il bar chart
fig = px.bar(
    df_filtered,
    x='Pollutant',
    y='Coeff.',
    color='Significance',
    text='Coeff.',
    color_discrete_map={
        'Significant (p < 0.05)': 'crimson',
        'Not significant': 'lightgray'
    },
    title='Estimated Impact of Air Pollutants on Fertility (Linear Regression Coefficients)',
    labels={'Coeff.': 'Regression Coefficient'}
)

# 6. Migliora etichette e layout
fig.update_traces(texttemplate='%{text:.4f}', textposition='outside')
fig.update_layout(
    xaxis_title='Pollutant',
    yaxis_title='Regression Coefficient',
    yaxis=dict(zeroline=True, zerolinecolor='black'),
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

# 7. Mostra il grafico
fig.show()

# (Opzionale) Salva il grafico in HTML
#fig.write_html("linear_regression_coefficients.html")


# Esporta il grafico come HTML parziale (solo il grafico)
plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
# Crea il file HTML finale
with open("visualizations/viz1_regression.html", "w", encoding="utf-8") as f:
    f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pollution and Fertility Correlations</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px auto;
            max-width: 950px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            text-align: center;
            font-size: 28px;
            margin-bottom: 0;
        }}
        h2 {{
            font-size: 20px;
            margin-top: 40px;
        }}
        .subtitle {{
            text-align: center;
            font-size: 16px;
            margin-bottom: 40px;
            color: #555;
        }}
        .plot-container {{
            margin-bottom: 30px;
            width:100%;
        }}
    </style>
</head>
<body>

<h1>Is There a Relationship Between Pollutants and Fertility?</h1>
<div class="subtitle">
    This chart explores which pollutant has the strongest estimated impact on fertility (2017–2019).
</div>

<div class="plot-container">
{plot_html}
</div>

<h2>Multiple linear regression. What Does it Mean?</h2>
<p>
When you use linear regression (e.g. KNIME Linear Regression Learner), you are building a model:
<br>
fertility = Intercept + (a × NO₂) + (b × O₃) + (c × PM2.5) + (d × density)</p>
<p>This model:
</p>
<ul>
  <li>Takes all variables together (controls for confounding effects).</li>
  <li>Estimates which variable best predicts fertility, all else being equal.</li>
  <li>Tells which variable has the greatest impact in a multivariate realistic model.</li>
</ul>

<h2>The Results</h2>
<ul>
  <li>📉 More pollution → lower fertility</li>
  <li>NO2: strongly negative -0.0067, is the pollutant with the strongest and most significant impact on fertility in your model.</li>
  <li>O3: negative, also negatively correlated and significant.</li>
  <li>PM2.5: negative but not significant: although the hypothesis seemed plausible, the data do not support it in this model.</li>
</ul>
<p>
While ozone (O₃) shows the strongest negative correlation with fertility when considered alone (r = –0.301), the regression model reveals that nitrogen dioxide (NO₂) has the greatest negative impact on fertility when controlling for other variables, including density and other pollutants. This suggests that NO₂ may play a more dominant role in driving fertility decline in polluted areas.
</p>

<h2>What Are NO₂, O₃, and PM2.5?</h2>
<ul>
  <li><strong>NO₂ – Nitrogen Dioxide:</strong> A gas mainly from cars and industry. It irritates the lungs and may affect fertility.</li>
  <li><strong>O₃ – Ground-Level Ozone:</strong> Formed when sunlight reacts with other pollutants. It harms the respiratory and cardiovascular systems.</li>
  <li><strong>PM2.5 – Fine Particulate Matter:</strong> Tiny particles from combustion and chemical reactions. They enter the lungs and blood, causing serious health risks and possibly reducing fertility.</li>
</ul>

</body>
</html>
""")
