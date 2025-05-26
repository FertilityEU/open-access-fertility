
window.renderViz3_1 = function(containerId = "viz3_1-container") {
  const CSV_FILE = "datasets/mashup/mashup3_for_viz.csv";
  const COLORS = {
    "High fertility, low investment" : "#FFCF00",
    "Balanced investment"            : "#00916E",
    "Low investment, low fertility"  : "#373737",
    "High investment, low fertility" : "#ED7D3A"
  };

  // Clear the container before rendering (if reloading)
  const container = document.getElementById(containerId);
  container.innerHTML = `
    <h2>Fertility vs. National Family-Spending</h2>
    <div id="viz3-1-wrap" style="display:flex;flex-wrap:wrap;gap:32px">
      <div id="viz3-1-scatter" style="flex:1 1 640px;min-width:420px;height:640px"></div>
      <div id="viz3-1-pie" style="flex:0 0 420px;height:420px"></div>
    </div>
  `;

  // Use d3 to load the CSV and Plotly to draw the charts (as in original code)
  d3.csv(CSV_FILE).then(fullRows => {

    const jitter = v => v + (Math.random()*2 - 1) * v * 0.03;

    const reps = [];
    d3.group(fullRows, d=>d.Mismatch).forEach(rows=>{
      rows.sort((a,b)=> +a.dist_to_median - +b.dist_to_median);
      reps.push(...rows.slice(0,10));
    });

    function makeTraces(rows, opacity, showLegend=true){
      return Object.keys(COLORS).map(cat=>{
        const sub = rows.filter(r=>r.Mismatch===cat);
        return {
          x: sub.map(r=> jitter(+r.family_exp)),
          y: sub.map(r=> +r.fertility),
          text: sub.map(r=> r.nuts2_code),
          name: cat,
          showlegend: showLegend,
          marker:{
            size : sub.map(r=> 6 + (+r.poverty)*0.35),
            color: COLORS[cat],
            opacity,
            line : {width:0.6,color:"#222"}
          },
          type:"scatter",
          mode:"markers",
          hovertemplate:
            "%{text}<br>fertility %{y:.2f}<br>spend %{x:.0f}% GDP"+
            "<br>poverty %{marker.size:.1f}%<extra>"+cat+"</extra>"
        };
      });
    }

const repTr = makeTraces(reps, 0.9, true);
const fullTr = makeTraces(fullRows, 0.25, false);
const traces = [...repTr, ...fullTr];
traces.slice(4).forEach(t=> t.visible=false);      

    /* ---- median lines ---- */
    const fertAll  = fullRows.map(r=> +r.fertility);
    const spendAll = fullRows.map(r=> +r.family_exp);
    const median = a => {const s=a.slice().sort((x,y)=>x-y);const m=Math.floor(s.length/2);return s.length&1?s[m]:(s[m-1]+s[m])/2;};
    const medF = median(fertAll), medS = median(spendAll);

    /* ---- scatter layout & dropdown ---- */
    const vis = fn => traces.map((_,i)=> fn(i));
    const buttons = [
      {label:"representative",method:"restyle",args:[{visible:vis(i=>i<4)}],execute:true},
      {label:"all regions",   method:"restyle",args:[{visible:vis(()=>true)}],execute:true},
      ...Object.keys(COLORS).map((cat,i)=>({
          label:cat,method:"restyle",
          args:[{visible:vis(idx=>idx===i||idx===i+4)}],execute:true}))
    ];

    Plotly.newPlot(container.querySelector("#viz3-1-scatter"), traces, {
      title:"Representative sample",
      xaxis:{title:"Family spending (% GDP)",type:"linear",tickformat:".0f",showgrid:false},
      yaxis:{title:"Total fertility rate",showgrid:false},
      shapes:[
        {type:"line",x0:medS,x1:medS,y0:Math.min(...fertAll),y1:Math.max(...fertAll),line:{dash:"dot",color:"#666"}},
        {type:"line",y0:medF,y1:medF,x0:Math.min(...spendAll),x1:Math.max(...spendAll),line:{dash:"dot",color:"#666"}}
      ],
      plot_bgcolor:"#fafafa",
      updatemenus:[{x:1.05,y:1,yanchor:"top",buttons,direction:"down",showactive:true}],
      margin:{l:60,r:90,t:60,b:60},
      hovermode:"closest",
      legend:{orientation:"h",x:0,y:-0.24}
    },{responsive:true});

    /* --------------- pie chart --------------- */
    const counts = d3.rollup(fullRows,v=>v.length,d=>d.Mismatch);
    const labels = Object.keys(COLORS);
    const values = labels.map(l => counts.get(l) || 0);

    Plotly.newPlot(container.querySelector("#viz3-1-pie"),[{
      labels, values, type:"pie",
      marker:{colors:labels.map(l=>COLORS[l])},
      textinfo:"percent",           
      textposition:"outside",       
      hovertemplate:"%{label}<br>%{value} regions<extra></extra>"
    }],{
      title:"Share of regions by mismatch type",
      margin:{t:50,b:30,l:50,r:20},
      plot_bgcolor:"#fafafa",
      showlegend:true               
    },{responsive:true});

  }).catch(err=>{
    container.innerHTML += `<p style='color:red'>Could not load CSV – see console.</p>`;
    console.error("CSV load error", err);
  });
}
