---
title: ""
layout: default
---
## Totals
{% assign total_miles = 0 %}
{% assign total_hours = 0 %}
{% assign total_tours = 0 %}
{% for post in site.posts %}
  {% assign total_miles = total_miles | plus: post.distance_traveld_NM %}
  {% assign total_hours = total_hours | plus: post.duration_h %}
  {% assign total_tours = total_tours | plus: 1 %}
{% endfor %}

| ---            | --:                          | --              |
| total distance | {{ total_miles }}            | nautical miles  |
| total time     | {{ total_hours | round: 0 }} | hours           |
| total #        | {{ total_tours }}            | logbook entries |

## Passage Index

<div id="passage-index-controls" style="margin: 0 0 0.75rem 0;">
  <input id="passage-index-search" type="search" placeholder="Filter…" style="padding: 0.4rem 0.5rem; max-width: 22rem; width: 100%;" />
</div>

<div id="passage-index-table"></div>

<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
(() => {
  // Build data from Jekyll posts at build-time (Liquid), render at runtime (D3).
  const rows = [
    {% for post in site.posts %}
      {
        date: "{{ post.date | date: "%Y-%m-%d" }}",
        url: "{{ post.url | relative_url }}",
        from: {{ post.origin_locn | default: "" | jsonify }},
        via: {{ post.via | default: "" | jsonify }},
        to: {{ post.terminus_locn | default: "" | jsonify }},
        distNm: {{ post.distance_traveld_NM | default: "" | jsonify }},
        hours: {{ post.duration_h | default: "" | jsonify }},
        avgKn: {{ post.distance_traveld_NM | times: 1.0 | divided_by: post.duration_h | round: 1 | default: "" | jsonify }},
        crew: {% if post.crew %}{{ post.crew | jsonify }}{% else %}""{% endif %},
        skipper: {{ post.skipper | default: "" | jsonify }},
        vessel: {{ post.tags[0] | split: '_' | last | default: "" | jsonify }},
        track: {{ post.gps_track | default: "" | jsonify }},
        photos: {{ post.photos | default: "" | jsonify }},
      },
    {% endfor %}
  ];

  const columns = [
    { key: "date", label: "Date", type: "date", render: d => `<a href="${d.url}">${d.date}</a>` },
    { key: "from", label: "from", type: "string" },
    { key: "via", label: "via", type: "string" },
    { key: "to", label: "to", type: "string" },
    { key: "distNm", label: "dist (NM)", type: "number" },
    { key: "hours", label: "time (hours)", type: "number" },
    { key: "avgKn", label: "avg speed (kn)", type: "number" },
    { key: "crew", label: "Crew", type: "string" },
    { key: "skipper", label: "Skipper", type: "string" },
    { key: "vessel", label: "Vessel", type: "string" },
    {
      key: "links",
      label: "hyper-links",
      type: "string",
      render: d => {
        const parts = [];
        if (d.track) parts.push(`<a href="${d.track}">track</a>`);
        if (d.photos) parts.push(`<a href="${d.photos}">photos</a>`);
        return parts.join(" ");
      }
    },
  ];

  const root = d3.select("#passage-index-table");

  // Minimal styling (no Jekyll layout changes). Ensure full-width scroll container.
  const style = document.createElement("style");
  style.textContent = `
    #passage-index-controls,
    #passage-index-table {
      width: 100vw;
      position: relative;
      left: 50%;
      margin-left: -50vw;
      box-sizing: border-box;
      padding: 0 1rem;
    }

    #passage-index-table { overflow-x: auto; }

    #passage-index-table table {
      border-collapse: collapse;
      width: max-content;
      min-width: 1100px;
      margin: 0 auto;
    }

    #passage-index-table th,
    #passage-index-table td {
      border: 1px solid rgba(0,0,0,0.15);
      padding: 0.35rem 0.5rem;
      white-space: nowrap;
      vertical-align: top;
    }

    #passage-index-table th {
      cursor: pointer;
      user-select: none;
      position: sticky;
      top: 0;
      background: #fff;
      z-index: 1;
    }

    #passage-index-table td.num {
      text-align: right;
      font-variant-numeric: tabular-nums;
    }

    #passage-index-table th .sort-indicator { opacity: 0.7; margin-left: 0.25rem; }
  `;
  document.head.appendChild(style);

  let sortKey = "date";
  let sortAsc = false;

  const normalize = (v) => String(v ?? "").toLowerCase();
  const parseNumber = (v) => {
    const s = String(v ?? "").trim();
    if (!s) return null;
    const n = Number(s);
    return Number.isFinite(n) ? n : null;
  };
  const parseDate = (v) => {
    const s = String(v ?? "").trim();
    if (!s) return null;
    const d = new Date(s + "T00:00:00Z");
    return Number.isNaN(d.getTime()) ? null : d;
  };

  const compare = (a, b, type) => {
    const dir = sortAsc ? 1 : -1;

    if (type === "number") {
      const av = parseNumber(a);
      const bv = parseNumber(b);
      if (av === null && bv === null) return 0;
      if (av === null) return 1;
      if (bv === null) return -1;
      return dir * (av - bv);
    }

    if (type === "date") {
      const ad = parseDate(a);
      const bd = parseDate(b);
      if (ad === null && bd === null) return 0;
      if (ad === null) return 1;
      if (bd === null) return -1;
      return dir * (ad - bd);
    }

    const as = String(a ?? "").toLowerCase();
    const bs = String(b ?? "").toLowerCase();
    if (as === bs) return 0;
    return dir * (as < bs ? -1 : 1);
  };

  function render(filterText = "") {
    const ft = normalize(filterText);

    const filtered = ft
      ? rows.filter(r => columns.some(c => normalize(r[c.key]).includes(ft)) || normalize(r.date).includes(ft))
      : rows.slice();

    const col = columns.find(c => c.key === sortKey) || columns[0];
    const data = filtered.sort((r1, r2) => compare(r1[col.key], r2[col.key], col.type));

    root.selectAll("*").remove();

    const table = root.append("table");
    const thead = table.append("thead");
    const tbody = table.append("tbody");

    const headerRow = thead.append("tr");
    headerRow.selectAll("th")
      .data(columns)
      .enter()
      .append("th")
      .attr("title", d => `Sort by ${d.label}`)
      .html(d => {
        const indicator = (d.key === sortKey) ? `<span class="sort-indicator">${sortAsc ? "▲" : "▼"}</span>` : "";
        return `${d.label}${indicator}`;
      })
      .on("click", (event, d) => {
        if (sortKey === d.key) {
          sortAsc = !sortAsc;
        } else {
          sortKey = d.key;
          sortAsc = d.type === "date" ? false : true; // dates desc by default
        }
        render(document.getElementById("passage-index-search").value);
      });

    const tr = tbody.selectAll("tr")
      .data(data)
      .enter()
      .append("tr");

    tr.selectAll("td")
      .data(row => columns.map(c => ({ col: c, row })))
      .enter()
      .append("td")
      .attr("class", d => (d.col.type === "number" ? "num" : null))
      .html(d => {
        if (d.col.render) return d.col.render(d.row);
        const val = d.row[d.col.key];
        return (val === null || val === undefined) ? "" : String(val);
      });
  }

  const search = document.getElementById("passage-index-search");
  search.addEventListener("input", () => render(search.value));

  render();
})();
</script>
