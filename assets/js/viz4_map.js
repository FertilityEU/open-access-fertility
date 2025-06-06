
window.renderViz4_map = function(containerId = "viz4_map-container") {
  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = `
    <h2>Zones of compromised reproduction</h2>
    <div id="frame-viz4" style="display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:0 12px 12px;">
      <div id="map-viz4" style="height:600px;width:100%"></div>
      <div id="scatter-viz4" style="height:600px;width:100%"></div>
    </div>
  `;

  // Cluster meta
  const CLUSTERS = {
    A: { label: "A — Toxic × Poor", color: "#0A090C" },
    B: { label: "B — Toxic × Rich", color: "#8A716A" },
    C: { label: "C — Clean × Poor", color: "#FABC3C" },
    D: { label: "D — Clean × Rich", color: "#D6F7A3" }
  };

  Promise.all([
    d3.json("assets/js/nuts2_simplified.geojson"),
    d3.csv("datasets/mashup/mashup4.csv")
  ]).then(([shapes, rows]) => {
    
    // ---------- MAP ----------
    const clusterByID = new Map(rows.map(r => [r.nuts2_code, r.Clusters]));
    const map = L.map("map-viz4").setView([53, 10], 4);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      { attribution: "© OSM" }).addTo(map);

    L.geoJSON(shapes, {
      style: f => ({
        fillColor: CLUSTERS[clusterByID.get(f.properties.NUTS_ID)]?.color || "#ccc",
        fillOpacity: 0.8, weight: 0.3, color: "#555"
      }),
      onEachFeature: (f, l) => {
        const id = f.properties.NUTS_ID;
        const c = clusterByID.get(id) ?? "?";
        l.bindTooltip(`<b>${id}</b><br>${CLUSTERS[c]?.label || "unknown"}`);
      }
    }).addTo(map);

    // ---------- SCATTERGL ----------
    const traces = Object.entries(CLUSTERS).map(([key, { label, color }]) => {
      const sub = rows.filter(r => r.Clusters === key);
      return {
        x: sub.map(r => +r.EBI),
        y: sub.map(r => +r.EPI),
        name: label,
        type: "scattergl",
        mode: "markers",
        marker: { color, size: 4, opacity: 0.7, line: { width: 0 } },
        text: sub.map(r => r.nuts2_code),
        hovertemplate: `%{text}<br>${label}<br>EBI %{x:.2f}<br>EPI %{y:.2f}<extra></extra>`
      };
    });

    Plotly.newPlot("scatter-viz4", traces, {
      margin: { t: 20, l: 60, r: 20, b: 60 },
      xaxis: { title: "Environmental Burden Index" },
      yaxis: { title: "Economic Precarity Index" },
      plot_bgcolor: "#fafafa",
      legend: { orientation: "h", x: 0, y: 1.08 }
    }, { responsive: true });
  });
};
