function renderCountryBarChart(year, containerId = "viz2_country_container") {
  const CSV_FILE = "/datasets/mashup/mashup2.csv";
  const container = document.getElementById(containerId);
  container.innerHTML = `<div id="bar-chart-${year}" style="width:100%;height:600px;"></div>`;

  d3.csv(CSV_FILE).then(data => {
    const df = data.filter(d => d.year === String(year));
    const countries = Array.from(new Set(df.map(d => d.nuts2_code.slice(0, 2)))).sort();

    const agg = {};
    countries.forEach(cc => {
      const sub = df.filter(d => d.nuts2_code.startsWith(cc));
      const mean = (arr, key) => d3.mean(arr, d => +d[key]);
      agg[cc] = {
        Fertility: mean(sub, "fertility"),
        "Poverty (%)": mean(sub, "poverty"),
        "Tertiary Education (%)": mean(sub, "tertiary_educ")
      };
    });

    const indicators = ["Fertility", "Poverty (%)", "Tertiary Education (%)"];
    const traces = indicators.map(ind => ({
      x: countries,
      y: countries.map(cc => agg[cc][ind]),
      name: ind,
      type: "bar"
    }));

    Plotly.newPlot(`bar-chart-${year}`, traces, {
      barmode: "group",
      title: `<b>Average Fertility, Poverty and Education by Country (${year})</b>`,
      xaxis: {title: "Country"},
      yaxis: {title: "Value"},
      legend: {orientation: "h", yanchor: "bottom", y: 1.02, xanchor: "right", x: 1},
      font: {size: 14},
      plot_bgcolor: "#f9f9f9",
      paper_bgcolor: "#ffffff",
      margin: {l: 60, r: 30, t: 90, b: 60}
    }, {responsive: true});
  }).catch(err => {
    container.innerHTML += `<p style='color:red'>Could not load CSV – see console.</p>`;
    console.error("CSV load error", err);
  });
}

// Unified renderer
window.renderViz2_country = function(year, containerId = "viz2_country_container") {
  renderCountryBarChart(year, containerId);
};
