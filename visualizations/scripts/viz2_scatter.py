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
    'CH': 'Switzerland',
    'NO': 'Norway'
}

nuts2_mapping = {
    'AT11': 'Burgenland', 'AT12': 'Niederösterreich', 'AT13': 'Wien',
    'AT21': 'Kärnten', 'AT22': 'Steiermark', 'AT31': 'Oberösterreich',
    'AT32': 'Salzburg', 'AT33': 'Tirol', 'AT34': 'Vorarlberg',
    'BE10': 'Région de Bruxelles-Capitale/Brussels Hoofdstedelijk Gewest',
    'BE21': 'Prov. Antwerpen', 'BE22': 'Prov. Limburg (BE)',
    'BE23': 'Prov. Oost-Vlaanderen', 'BE24': 'Prov. Vlaams-Brabant',
    'BE25': 'Prov. West-Vlaanderen', 'BE31': 'Prov. Brabant Wallon',
    'BE32': 'Prov. Hainaut', 'BE33': 'Prov. Liège', 'BE34': 'Prov. Luxembourg (BE)',
    'BE35': 'Prov. Namur', 'BG31': 'Severozapaden', 'BG32': 'Severen tsentralen',
    'BG33': 'Severoiztochen', 'BG34': 'Yugoiztochen', 'BG41': 'Yugozapaden',
    'BG42': 'Yuzhen tsentralen', 'CY00': 'Kýpros', 'CZ01': 'Praha',
    'CZ02': 'Střední Čechy', 'CZ03': 'Jihozápad', 'CZ04': 'Severozápad',
    'CZ05': 'Severovýchod', 'CZ06': 'Jihovýchod', 'CZ07': 'Střední Morava',
    'CZ08': 'Moravskoslezsko', 'DE11': 'Stuttgart', 'DE12': 'Karlsruhe',
    'DE13': 'Freiburg', 'DE14': 'Tübingen', 'DE21': 'Oberbayern',
    'DE22': 'Niederbayern', 'DE23': 'Oberpfalz', 'DE24': 'Oberfranken',
    'DE25': 'Mittelfranken', 'DE26': 'Unterfranken', 'DE27': 'Schwaben',
    'DE30': 'Berlin', 'DE40': 'Brandenburg', 'DE50': 'Bremen',
    'DE60': 'Hamburg', 'DE71': 'Darmstadt', 'DE72': 'Gießen',
    'DE73': 'Kassel', 'DE80': 'Mecklenburg-Vorpommern', 'DE91': 'Braunschweig',
    'DE92': 'Hannover', 'DE93': 'Lüneburg', 'DE94': 'Weser-Ems',
    'DEA1': 'Düsseldorf', 'DEA2': 'Köln', 'DEA3': 'Münster',
    'DEA4': 'Detmold', 'DEA5': 'Arnsberg', 'DEB1': 'Koblenz',
    'DEB2': 'Trier', 'DEB3': 'Rheinhessen-Pfalz', 'DEC0': 'Saarland',
    'DED2': 'Dresden', 'DED4': 'Chemnitz', 'DED5': 'Leipzig',
    'DEE0': 'Sachsen-Anhalt', 'DEF0': 'Schleswig-Holstein', 'DEG0': 'Thüringen',
    'DK01': 'Hovedstaden', 'DK02': 'Sjælland', 'DK03': 'Syddanmark',
    'DK04': 'Midtjylland', 'DK05': 'Nordjylland', 'EE00': 'Eesti',
    'EL30': 'Attiki', 'EL41': 'Voreia Ellada', 'EL42': 'Kentriki Ellada',
    'EL43': 'Nisia Aigaiou, Kriti', 'ES11': 'Galicia', 'ES12': 'Principado de Asturias',
    'ES13': 'Cantabria', 'ES21': 'País Vasco', 'ES22': 'Comunidad Foral de Navarra',
    'ES23': 'La Rioja', 'ES24': 'Aragón', 'ES30': 'Comunidad de Madrid',
    'ES41': 'Castilla y León', 'ES42': 'Castilla-La Mancha', 'ES43': 'Extremadura',
    'ES51': 'Cataluña', 'ES52': 'Comunidad Valenciana', 'ES53': 'Illes Balears',
    'ES61': 'Andalucía', 'ES62': 'Región de Murcia', 'ES63': 'Ciudad Autónoma de Ceuta',
    'ES64': 'Ciudad Autónoma de Melilla', 'ES70': 'Canarias',
    'FI19': 'Länsi-Suomi', 'FI1B': 'Etelä-Suomi', 'FI1C': 'Pohjois- ja Itä-Suomi',
    'FI20': 'Åland', 'FRB0': 'Bretagne', 'FRC1': 'Bourgogne', 'FRC2': 'Franche-Comté',
    'FRD1': 'Basse-Normandie', 'FRD2': 'Haute-Normandie', 'FRE1': 'Nord-Pas-de-Calais',
    'FRE2': 'Picardie', 'FRF1': 'Alsace', 'FRF2': 'Champagne-Ardenne', 'FRF3': 'Lorraine',
    'FRG0': 'Île-de-France', 'FRH0': 'Centre-Val de Loire', 'FRI1': 'Auvergne',
    'FRI2': 'Limousin', 'FRI3': 'Poitou-Charentes', 'FRJ1': 'Aquitaine',
    'FRJ2': 'Midi-Pyrénées', 'FRJ3': 'Languedoc-Roussillon', 'FRK1': 'Rhône-Alpes',
    'FRK2': 'Auvergne-Rhône-Alpes', 'FRL0': 'Provence-Alpes-Côte d’Azur',
    'FRM0': 'Corse', 'FRY1': 'Guadeloupe', 'FRY2': 'Martinique',
    'FRY3': 'Guyane', 'FRY4': 'La Réunion', 'FRY5': 'Mayotte',
    'HR03': 'Jadranska Hrvatska', 'HR04': 'Kontinentalna Hrvatska',
    'HU10': 'Közép-Magyarország', 'HU21': 'Közép-Dunántúl', 'HU22': 'Nyugat-Dunántúl',
    'HU23': 'Dél-Dunántúl', 'HU31': 'Észak-Magyarország', 'HU32': 'Észak-Alföld',
    'HU33': 'Dél-Alföld', 'IE04': 'Northern and Western', 'IE05': 'Southern',
    'IE06': 'Eastern and Midland', 'ITC1': 'Piemonte', 'ITC2': "Valle d'Aosta",
    'ITC3': 'Liguria', 'ITC4': 'Lombardia', 'ITF1': 'Abruzzo', 'ITF2': 'Molise',
    'ITF3': 'Campania', 'ITF4': 'Puglia', 'ITF5': 'Basilicata', 'ITF6': 'Calabria',
    'ITG1': 'Sicilia', 'ITG2': 'Sardegna', 'ITE1': 'Toscana', 'ITE2': 'Umbria',
    'ITE3': 'Marche', 'ITE4': 'Lazio', 'ITH1': 'P.A. Bolzano', 'ITH2': 'P.A. Trento',
    'ITH3': 'Veneto', 'ITH4': 'Friuli-Venezia Giulia', 'ITH5': 'Emilia-Romagna',
    'LT00': 'Lietuva', 'LU00': 'Luxembourg', 'LV00': 'Latvija',
    'MT00': 'Malta', 'NL11': 'Groningen', 'NL12': 'Friesland',
    'NL13': 'Drenthe', 'NL21': 'Overijssel', 'NL22': 'Gelderland',
    'NL23': 'Flevoland', 'NL31': 'Utrecht', 'NL32': 'Noord-Holland',
    'NL33': 'Zuid-Holland', 'NL34': 'Zeeland', 'NL41': 'Noord-Brabant',
    'NL42': 'Limburg (NL)', 'PL21': 'Małopolskie', 'PL22': 'Śląskie',
    'PL41': 'Wielkopolskie', 'PL42': 'Zachodniopomorskie', 'PL43': 'Lubuskie',
    'PL51': 'Dolnośląskie', 'PL52': 'Opolskie', 'PL61': 'Kujawsko-pomorskie',
    'PL62': 'Warmińsko-mazurskie', 'PL63': 'Pomorskie', 'PL71': 'Łódzkie',
    'PL72': 'Świętokrzyskie', 'PL81': 'Lubelskie', 'PL82': 'Podkarpackie',
    'PL84': 'Podlaskie', 'PT11': 'Norte', 'PT15': 'Algarve',
    'PT16': 'Centro (PT)', 'PT17': 'Área Metropolitana de Lisboa',
    'PT18': 'Alentejo', 'PT20': 'Região Autónoma dos Açores',
    'PT30': 'Região Autónoma da Madeira', 'RO11': 'Nord-Vest',
    'RO12': 'Centru', 'RO21': 'Nord-Est', 'RO22': 'Sud-Est',
    'RO31': 'Sud-Muntenia', 'RO32': 'București-Ilfov', 'RO41': 'Sud-Vest Oltenia',
    'RO42': 'Vest', 'SE11': 'Stockholm', 'SE12': 'Östra Mellansverige',
    'SE21': 'Småland med öarna', 'SE22': 'Sydsverige', 'SE23': 'Västsverige',
    'SE31': 'Norra Mellansverige', 'SE32': 'Mellersta Norrland',
    'SE33': 'Övre Norrland', 'SI03': 'Vzhodna Slovenija', 'SI04': 'Zahodna Slovenija',
    'SK01': 'Bratislavský kraj', 'SK02': 'Západné Slovensko',
    'SK03': 'Stredné Slovensko', 'SK04': 'Východné Slovensko',
    'CH01': 'Région lémanique', 'CH02': 'Espace Mittelland', 'CH03': 'Nordwestschweiz',
    'CH04': 'Zürich', 'CH05': 'Ostschweiz', 'CH06': 'Zentralschweiz', 'CH07': 'Ticino',
    'EL51': 'Anatoliki Makedonia, Thraki', 'EL52': 'Kentriki Makedonia', 'EL53': 'Dytiki Makedonia',
    'EL54': 'Thessalia', 'EL61': 'Ipeiros', 'EL62': 'Ionioi Nisoi', 'EL63': 'Dytiki Ellada',
    'EL64': 'Sterea Ellada', 'EL65': 'Peloponnisos',
    'FI1D': 'Uusimaa',
    'HU11': 'Budapest', 'HU12': 'Pest',
    'ITI1': 'Toscana', 'ITI2': 'Umbria', 'ITI3': 'Marche', 'ITI4': 'Lazio',
    'LT01': 'Sostinės regionas', 'LT02': 'Vidurio ir vakarų Lietuvos regionas',
    'NO02': 'Innlandet', 'NO06': 'Trøndelag', 'NO07': 'Nord-Norge',
    'PL91': 'Łódzkie i Świętokrzyskie', 'PL92': 'Lubelskie, Podkarpackie i Podlaskie'
}

# Estrai il codice paese dai codici NUTS2
data['country_code'] = data['nuts2_code'].str[:2]

# Mappa i codici ai nomi dei paesi
data['country_name'] = data['country_code'].map(iso_country_mapping)

# Mappa i codici NUTS2 ai nomi delle regioni
data['region_name'] = data['nuts2_code'].map(nuts2_mapping)

# Filtra per anno 2018
df = data[data["year"] == 2019].copy()
df["country"] = df["nuts2_code"].str[:2]
df["region_label"] = df["region_name"] + " (" + df["nuts2_code"] + ")"

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
    hover_name="region_name",
    labels={
        "poverty": "Poverty (%)",
        "fertility": "Fertility",
        "educ_norm": "Tertiary Education Normalized",
        "country_name": "Country",
        "region_name": "NUTS2 Region"
    },
    title="Fertility vs Poverty (dimension = education) – NUTS2 (2018)",
    height=600
)


# Imposta solo Italia come visibile inizialmente
for trace in fig.data:
    trace.visible = 'legendonly'  # Imposta tutti come nascosti
    if trace.name == 'Italy':
        trace.visible = True  # Mostra solo l'Italia

fig.write_html("visualizations/viz2_scatter2019.html")
fig.show()

