
function renderScatterByYear(year, containerId = "viz2_scatter_container") {
  const CSV_FILE = "datasets/mashup/mashup2.csv";

  const container = document.getElementById(containerId);
  container.innerHTML = `<div id="scatter-${year}" style="width:100%;height:600px;"></div>`;

  d3.csv(CSV_FILE).then(data => {
    const filtered = data.filter(d => d.year === String(year));

    // NUTS and ISO mappings would ideally be stored externally or preprocessed
    const countryNames = {
  'AT': 'Austria','BE': 'Belgium','BG': 'Bulgaria','CY': 'Cyprus','CZ': 'Czech Republic','DE': 'Germany','DK': 'Denmark','EE': 'Estonia','EL': 'Greece','ES': 'Spain','FI': 'Finland','FR': 'France','HR': 'Croatia','HU': 'Hungary','IE': 'Ireland','IT': 'Italy','LT': 'Lithuania','LU': 'Luxembourg','LV': 'Latvia','MT': 'Malta','NL': 'Netherlands','PL': 'Poland','PT': 'Portugal','RO': 'Romania','SE': 'Sweden','SI': 'Slovenia','SK': 'Slovakia','CH': 'Switzerland','NO': 'Norway'
};

const regionNames = {
  "AT11": "Burgenland", "AT12": "Niederösterreich", "AT13": "Wien", "AT21": "Kärnten", "AT22": "Steiermark", "AT31": "Oberösterreich", "AT32": "Salzburg", "AT33": "Tirol", "AT34": "Vorarlberg",
  "BE10": "Région de Bruxelles-Capitale/Brussels Hoofdstedelijk Gewest", "BE21": "Prov. Antwerpen", "BE22": "Prov. Limburg (BE)", "BE23": "Prov. Oost-Vlaanderen", "BE24": "Prov. Vlaams-Brabant",
  "BE25": "Prov. West-Vlaanderen", "BE31": "Prov. Brabant Wallon", "BE32": "Prov. Hainaut", "BE33": "Prov. Liège", "BE34": "Prov. Luxembourg (BE)", "BE35": "Prov. Namur",
  "BG31": "Severozapaden", "BG32": "Severen tsentralen", "BG33": "Severoiztochen", "BG34": "Yugoiztochen", "BG41": "Yugozapaden", "BG42": "Yuzhen tsentralen", "CY00": "Kýpros",
  "CZ01": "Praha", "CZ02": "Střední Čechy", "CZ03": "Jihozápad", "CZ04": "Severozápad", "CZ05": "Severovýchod", "CZ06": "Jihovýchod", "CZ07": "Střední Morava", "CZ08": "Moravskoslezsko",
  "DE11": "Stuttgart", "DE12": "Karlsruhe", "DE13": "Freiburg", "DE14": "Tübingen", "DE21": "Oberbayern", "DE22": "Niederbayern", "DE23": "Oberpfalz", "DE24": "Oberfranken",
  "DE25": "Mittelfranken", "DE26": "Unterfranken", "DE27": "Schwaben", "DE30": "Berlin", "DE40": "Brandenburg", "DE50": "Bremen", "DE60": "Hamburg", "DE71": "Darmstadt",
  "DE72": "Gießen", "DE73": "Kassel", "DE80": "Mecklenburg-Vorpommern", "DE91": "Braunschweig", "DE92": "Hannover", "DE93": "Lüneburg", "DE94": "Weser-Ems", "DEA1": "Düsseldorf",
  "DEA2": "Köln", "DEA3": "Münster", "DEA4": "Detmold", "DEA5": "Arnsberg", "DEB1": "Koblenz", "DEB2": "Trier", "DEB3": "Rheinhessen-Pfalz", "DEC0": "Saarland",
  "DED2": "Dresden", "DED4": "Chemnitz", "DED5": "Leipzig", "DEE0": "Sachsen-Anhalt", "DEF0": "Schleswig-Holstein", "DEG0": "Thüringen", "DK01": "Hovedstaden", "DK02": "Sjælland",
  "DK03": "Syddanmark", "DK04": "Midtjylland", "DK05": "Nordjylland", "EE00": "Eesti", "EL30": "Attiki", "EL41": "Voreia Ellada", "EL42": "Kentriki Ellada", "EL43": "Nisia Aigaiou, Kriti",
  "ES11": "Galicia", "ES12": "Principado de Asturias", "ES13": "Cantabria", "ES21": "País Vasco", "ES22": "Comunidad Foral de Navarra", "ES23": "La Rioja", "ES24": "Aragón",
  "ES30": "Comunidad de Madrid", "ES41": "Castilla y León", "ES42": "Castilla-La Mancha", "ES43": "Extremadura", "ES51": "Cataluña", "ES52": "Comunidad Valenciana",
  "ES53": "Illes Balears", "ES61": "Andalucía", "ES62": "Región de Murcia", "ES63": "Ciudad Autónoma de Ceuta", "ES64": "Ciudad Autónoma de Melilla", "ES70": "Canarias"
};

    // Extract country code and region label
    filtered.forEach(d => {
      d.country = d.nuts2_code.slice(0, 2);
      d.country_name = countryNames[d.country] || d.country;
      d.region_label = d.region_name ? `${d.region_name} (${d.nuts2_code})` : d.nuts2_code;
      d.poverty = +d.poverty;
      d.fertility = +d.fertility;
      d.tertiary_educ = +d.tertiary_educ;
    });

    // Normalize education for bubble size
    const minEduc = d3.min(filtered, d => d.tertiary_educ);
    const maxEduc = d3.max(filtered, d => d.tertiary_educ);
    filtered.forEach(d => {
      d.educ_norm = (d.tertiary_educ - minEduc) / (maxEduc - minEduc);
    });

    const groups = d3.groups(filtered, d => d.country_name);
    const traces = groups.map(([country, values]) => {
      return {
        x: values.map(d => d.poverty),
        y: values.map(d => d.fertility),
        text: values.map(d => d.region_label),
        name: country,
        mode: "markers",
        type: "scatter",
        visible: country === "Italy" ? true : "legendonly",
        marker: {
          size: values.map(d => 10 + d.educ_norm * 30),
          sizemode: 'area',
          sizeref: 2.0 * Math.max(...values.map(d => 10 + d.educ_norm * 30)) / (40 ** 2),
          line: { width: 0.6, color: '#444' }
        },
        hovertemplate: "%{text}<br>Poverty: %{x:.1f}%<br>Fertility: %{y:.2f}<extra>%{name}</extra>"
      };
    });

    Plotly.newPlot(`scatter-${year}`, traces, {
      title: `Fertility vs Poverty (size = education) – NUTS2 (${year})`,
      xaxis: { title: "Poverty (%)" },
      yaxis: { title: "Fertility" },
      margin: {l: 60, r: 30, t: 90, b: 60},
      legend: { orientation: "h", yanchor: "bottom", y: 1.02, xanchor: "right", x: 1 },
      plot_bgcolor: "#f9f9f9",
      paper_bgcolor: "#ffffff"
    }, {responsive: true});
  }).catch(err => {
    container.innerHTML += `<p style='color:red'>Could not load CSV – see console.</p>`;
    console.error("CSV load error", err);
  });
}

window.renderViz2_scatter_2017 = () => renderScatterByYear(2017, "viz2_scatter_2017-container");
window.renderViz2_scatter_2018 = () => renderScatterByYear(2018, "viz2_scatter_2018-container");
window.renderViz2_scatter_2019 = () => renderScatterByYear(2019, "viz2_scatter_2019-container");


function renderScatterByYear(year, containerId = "viz2_scatter_container") {
  const CSV_FILE = "datasets/mashup/mashup2.csv";

  const container = document.getElementById(containerId);
  container.innerHTML = `<div id="scatter-${year}" style="width:100%;height:600px;"></div>`;

  d3.csv(CSV_FILE).then(data => {
    const filtered = data.filter(d => d.year === String(year));

    const countryNames = {
  'AT': 'Austria','BE': 'Belgium','BG': 'Bulgaria','CY': 'Cyprus','CZ': 'Czech Republic','DE': 'Germany','DK': 'Denmark','EE': 'Estonia','EL': 'Greece','ES': 'Spain','FI': 'Finland','FR': 'France','HR': 'Croatia','HU': 'Hungary','IE': 'Ireland','IT': 'Italy','LT': 'Lithuania','LU': 'Luxembourg','LV': 'Latvia','MT': 'Malta','NL': 'Netherlands','PL': 'Poland','PT': 'Portugal','RO': 'Romania','SE': 'Sweden','SI': 'Slovenia','SK': 'Slovakia','CH': 'Switzerland','NO': 'Norway'
};

const regionNames = {
  "AT11": "Burgenland", "AT12": "Niederösterreich", "AT13": "Wien", "AT21": "Kärnten", "AT22": "Steiermark", "AT31": "Oberösterreich", "AT32": "Salzburg", "AT33": "Tirol", "AT34": "Vorarlberg",
  "BE10": "Région de Bruxelles-Capitale/Brussels Hoofdstedelijk Gewest", "BE21": "Prov. Antwerpen", "BE22": "Prov. Limburg (BE)", "BE23": "Prov. Oost-Vlaanderen", "BE24": "Prov. Vlaams-Brabant",
  "BE25": "Prov. West-Vlaanderen", "BE31": "Prov. Brabant Wallon", "BE32": "Prov. Hainaut", "BE33": "Prov. Liège", "BE34": "Prov. Luxembourg (BE)", "BE35": "Prov. Namur",
  "BG31": "Severozapaden", "BG32": "Severen tsentralen", "BG33": "Severoiztochen", "BG34": "Yugoiztochen", "BG41": "Yugozapaden", "BG42": "Yuzhen tsentralen", "CY00": "Kýpros",
  "CZ01": "Praha", "CZ02": "Střední Čechy", "CZ03": "Jihozápad", "CZ04": "Severozápad", "CZ05": "Severovýchod", "CZ06": "Jihovýchod", "CZ07": "Střední Morava", "CZ08": "Moravskoslezsko",
  "DE11": "Stuttgart", "DE12": "Karlsruhe", "DE13": "Freiburg", "DE14": "Tübingen", "DE21": "Oberbayern", "DE22": "Niederbayern", "DE23": "Oberpfalz", "DE24": "Oberfranken",
  "DE25": "Mittelfranken", "DE26": "Unterfranken", "DE27": "Schwaben", "DE30": "Berlin", "DE40": "Brandenburg", "DE50": "Bremen", "DE60": "Hamburg", "DE71": "Darmstadt",
  "DE72": "Gießen", "DE73": "Kassel", "DE80": "Mecklenburg-Vorpommern", "DE91": "Braunschweig", "DE92": "Hannover", "DE93": "Lüneburg", "DE94": "Weser-Ems", "DEA1": "Düsseldorf",
  "DEA2": "Köln", "DEA3": "Münster", "DEA4": "Detmold", "DEA5": "Arnsberg", "DEB1": "Koblenz", "DEB2": "Trier", "DEB3": "Rheinhessen-Pfalz", "DEC0": "Saarland",
  "DED2": "Dresden", "DED4": "Chemnitz", "DED5": "Leipzig", "DEE0": "Sachsen-Anhalt", "DEF0": "Schleswig-Holstein", "DEG0": "Thüringen", "DK01": "Hovedstaden", "DK02": "Sjælland",
  "DK03": "Syddanmark", "DK04": "Midtjylland", "DK05": "Nordjylland", "EE00": "Eesti", "EL30": "Attiki", "EL41": "Voreia Ellada", "EL42": "Kentriki Ellada", "EL43": "Nisia Aigaiou, Kriti",
  "ES11": "Galicia", "ES12": "Principado de Asturias", "ES13": "Cantabria", "ES21": "País Vasco", "ES22": "Comunidad Foral de Navarra", "ES23": "La Rioja", "ES24": "Aragón",
  "ES30": "Comunidad de Madrid", "ES41": "Castilla y León", "ES42": "Castilla-La Mancha", "ES43": "Extremadura", "ES51": "Cataluña", "ES52": "Comunidad Valenciana",
  "ES53": "Illes Balears", "ES61": "Andalucía", "ES62": "Región de Murcia", "ES63": "Ciudad Autónoma de Ceuta", "ES64": "Ciudad Autónoma de Melilla", "ES70": "Canarias"
};

    filtered.forEach(d => {
      d.country = d.nuts2_code.slice(0, 2);
      d.country_name = countryNames[d.country] || d.country;
      d.region_label = d.region_name ? `${d.region_name} (${d.nuts2_code})` : d.nuts2_code;
      d.poverty = +d.poverty;
      d.fertility = +d.fertility;
      d.tertiary_educ = +d.tertiary_educ;
    });

    const minEduc = d3.min(filtered, d => d.tertiary_educ);
    const maxEduc = d3.max(filtered, d => d.tertiary_educ);
    filtered.forEach(d => {
      d.educ_norm = (d.tertiary_educ - minEduc) / (maxEduc - minEduc);
    });

    const groups = d3.groups(filtered, d => d.country_name);
    const traces = groups.map(([country, values]) => ({
      x: values.map(d => d.poverty),
      y: values.map(d => d.fertility),
      text: values.map(d => d.region_label),
      name: country,
      mode: "markers",
      type: "scatter",
      visible: country === "Italy" ? true : "legendonly",
      marker: {
        size: values.map(d => 10 + d.educ_norm * 30),
        sizemode: 'area',
        sizeref: 2.0 * Math.max(...values.map(d => 10 + d.educ_norm * 30)) / (40 ** 2),
        line: { width: 0.6, color: '#444' }
      },
      hovertemplate: "%{text}<br>Poverty: %{x:.1f}%<br>Fertility: %{y:.2f}<extra>%{name}</extra>"
    }));

    Plotly.newPlot(`scatter-${year}`, traces, {
      title: `Fertility vs Poverty (size = education) – NUTS2 (${year})`,
      xaxis: { title: "Poverty (%)" },
      yaxis: { title: "Fertility" },
      height: 700,
      legend: { orientation: "h", yanchor: "bottom", y: 1.02, xanchor: "right", x: 1 },
      plot_bgcolor: "#f9f9f9",
      paper_bgcolor: "#ffffff"
    }, {responsive: true});
  }).catch(err => {
    container.innerHTML += `<p style='color:red'>Could not load CSV – see console.</p>`;
    console.error("CSV load error", err);
  });
}

// Unified renderer
window.renderViz2_scatter = function(year, containerId = "viz2_scatter_container") {
  renderScatterByYear(year, containerId);
};
