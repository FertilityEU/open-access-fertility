const map = L.map('map').setView([51, 10], 4);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap'
}).addTo(map);

Promise.all([
  fetch('assets/data/mashup/mashup2.csv').then(res => res.text()),
  fetch('assets/data/nuts2.geojson').then(res => res.json())
]).then(([csvText, geojson]) => {
  const csv = Papa.parse(csvText, { header: true }).data;
  const data = Object.fromEntries(csv
    .filter(d => d.year === "2019")
    .map(d => [d.nuts2_code, {
      fertility: +d.fertility,
      poverty: +d.poverty,
      education: +d.tertiary_educ,
      density: +d.density
    }])
  );

  function getColor(f) {
    return f > 2 ? '#800026' :
           f > 1.8 ? '#BD0026' :
           f > 1.6 ? '#E31A1C' :
           f > 1.4 ? '#FC4E2A' :
           f > 1.2 ? '#FD8D3C' :
           f > 1.0 ? '#FEB24C' :
                     '#FFEDA0';
  }

  geojson.features.forEach(f => {
    const props = data[f.properties.NUTS_ID];
    if (props) {
      f.properties = { ...f.properties, ...props };
    }
  });

  L.geoJson(geojson, {
    style: f => ({
      fillColor: getColor(f.properties.fertility),
      weight: 1,
      opacity: 1,
      color: '#ccc',
      dashArray: '1',
      fillOpacity: 0.8
    }),
    onEachFeature: (feature, layer) => {
      const p = feature.properties;
      if (p.fertility) {
        layer.bindPopup(`
          <strong>${p.NUTS_NAME}</strong><br>
          Fertility: ${p.fertility.toFixed(2)}<br>
          Poverty: ${p.poverty}%<br>
          Education: ${p.education}%<br>
          Density: ${p.density} people/km²
        `);
      }
    }
  }).addTo(map);
});
