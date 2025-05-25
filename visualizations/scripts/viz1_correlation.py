import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Carica il dataset
df = pd.read_csv("datasets/mashup/correlation_result.csv", encoding='utf-8-sig')

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
fig.write_html("visualizations/viz1_correlation.html", full_html=False, include_plotlyjs='cdn')
fig.show()


