import pandas as pd
import plotly.express as px

# 1. Carica il CSV
df = pd.read_csv("datasets/mashup/Linear regression learner.csv")

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

# Mostra il grafico
fig.write_html("visualizations/viz1_regression.html", full_html=False, include_plotlyjs='cdn')
fig.show()
