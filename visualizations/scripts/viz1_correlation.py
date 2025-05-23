import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Carica il dataset
df = pd.read_csv("correlation_result.csv", encoding='utf-8-sig')

# Filtra solo le righe dove compare "fertility"
df_filtered = df[df['First column name'].str.contains('fertility') | df['Second column name'].str.contains('fertility')].copy()

# Crea una colonna con il nome della coppia per l'asse X
df_filtered['pair'] = df_filtered['First column name'] + " vs " + df_filtered['Second column name']

# Rinomina gli inquinanti per leggibilità
df_filtered['pair'] = df_filtered['pair'].str.replace(r'NO2\+Mean\(pollutant_av\)', 'NO₂ (pollutant)', regex=True)
df_filtered['pair'] = df_filtered['pair'].str.replace(r'O3\+Mean\(pollutant_av\)', 'O₃ (pollutant)', regex=True)
df_filtered['pair'] = df_filtered['pair'].str.replace(r'PM2.5\+Mean\(pollutant_av\)', 'PM2.5 (pollutant)', regex=True)

# Crea una colonna per colorare in base alla significatività
df_filtered['Significant'] = df_filtered['p value'] < 0.05

# Classifica l'intensità della correlazione
def interpret_corr(corr):
    if abs(corr) >= 0.5:
        return 'Strong correlation'
    elif abs(corr) >= 0.3:
        return 'Moderate correlation'
    elif abs(corr) >= 0.1:
        return 'Weak correlation'
    else:
        return 'Very weak / None'

df_filtered['Interpretation'] = df_filtered['Correlation value'].apply(interpret_corr)


# Ordina per valore di correlazione
df_filtered = df_filtered.sort_values(by='Correlation value')

# Crea una colonna testuale arrotondata per le etichette
df_filtered['Correlation text'] = df_filtered['Correlation value'].round(3)

# Crea il bar plot interattivo
fig = px.bar(
    df_filtered,
    x='pair',
    y='Correlation value',
    color='Interpretation',
    text='Correlation text',
    color_discrete_map={
        'Strong correlation': 'darkred',
        'Moderate correlation': 'orange',
        'Weak correlation': 'steelblue',
        'Very weak / None': 'lightgray'
    },
    title='Is Reproduction Environmentally Discouraged? Correlation with Fertility (2017–2019)',
    labels={'pair': 'Variabile Pair', 'Correlation value': 'Correlation Coefficient'}
)




# Ruota le etichette dell'asse X
fig.update_layout(xaxis_tickangle=-45)

# Aggiungi annotazioni
fig.add_annotation(
    text="All correlations are negative: higher pollution levels tend to be associated with lower fertility rates.",
    xref="paper", yref="paper",
    x=0.5, y=1.10, showarrow=False
)

# Personalizza i tooltip
fig.update_traces(hovertemplate=
    '<b>%{x}</b><br>' +
    'Correlation: %{y:.3f}<br>' +
    '<extra></extra>'
)

# Mostra il grafico
fig.show()

# Salva il grafico come file HTML
#fig.write_html("correlation_plot2.html")

# Esporta il grafico come HTML parziale (solo il grafico)
plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
# Crea il file HTML finale
with open("visualizations/viz1_correlation.html", "w", encoding="utf-8") as f:
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
    This chart explores whether different types of air pollutants are statistically correlated with fertility rates across Europe (2017–2019).
</div>

<div class="plot-container">
{plot_html}
</div>

<h2>What Does “Calculating Correlation” Mean?</h2>
<p>
Correlation measures how much two variables move together. In this case, we want to understand if there is a linear relationship between fertility rates and the presence of air pollutants. 
The Pearson correlation coefficient ranges from -1 to 1:
</p>
<ul>
  <li>+1 means a perfect positive linear relationship</li>
  <li>0 means no linear relationship</li>
  <li>-1 means a perfect negative linear relationship</li>
</ul>

<h2>The Results</h2>
<p>
All three pollutants show <strong>negative correlations</strong> with fertility:
</p>
<ul>
  <li>📉 More pollution → lower fertility</li>
  <li>O₃ (Ozone): shows the strongest negative correlation at –0.301, which is moderately strong.</li>
  <li>NO₂ (Nitrogen Dioxide): is close behind with –0.166.</li>
  <li>PM2.5 (Particulate Matter): follows with a correlation of –0.137</li>
</ul>
<p>
These correlations support the hypothesis that air pollution is associated with reduced fertility, although none of the correlations is particularly strong. Still, the consistent negative direction is meaningful.
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

