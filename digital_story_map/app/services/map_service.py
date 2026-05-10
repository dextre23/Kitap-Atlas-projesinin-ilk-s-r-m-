import json


def build_map_html(entries: list[dict], lang: str = "tr") -> str:
    markers_json = json.dumps(entries, ensure_ascii=False)
    lang_js = "tr" if lang.lower().startswith("tr") else "en"

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Kitap Atlası</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css"/>
  <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css"/>
  <style>
    html, body, #map {{
      width: 100%;
      height: 100%;
      margin: 0;
      background-color: #11151b;
    }}
    .leaflet-popup-content-wrapper {{
      border-radius: 14px;
      padding: 0;
      overflow: hidden;
      box-shadow: 0 14px 44px rgba(0, 0, 0, 0.38), 0 2px 10px rgba(0, 0, 0, 0.18);
      border: 1px solid rgba(255, 255, 255, 0.35);
      background: linear-gradient(165deg, #fafbfd 0%, #eef1f6 100%);
    }}
    .leaflet-popup-tip {{
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.22);
    }}
    .leaflet-popup-content {{
      margin: 0;
      min-width: 268px;
      max-width: 320px;
      font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
      font-size: 13px;
      line-height: 1.5;
      color: #1c2430;
    }}
    .kitap-popup-inner {{
      padding: 16px 18px 14px 18px;
    }}
    .kitap-popup-title {{
      font-weight: 700;
      font-size: 15px;
      letter-spacing: 0.01em;
      margin: 0 0 6px 0;
      color: #121820;
    }}
    .kitap-popup-meta {{
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #5a6575;
      margin-bottom: 12px;
    }}
    .kitap-popup-row {{
      margin-bottom: 8px;
      font-size: 13px;
    }}
    .kitap-popup-row b {{
      color: #2c3544;
      font-weight: 600;
    }}
    .kitap-popup-quote {{
      font-style: italic;
      color: #3d4a5c;
      margin: 12px 0;
      padding: 10px 12px;
      border-left: 3px solid #3d6ec4;
      background: rgba(61, 110, 196, 0.08);
      border-radius: 0 8px 8px 0;
    }}
    .kitap-popup-context {{
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid rgba(0, 0, 0, 0.08);
      font-size: 12px;
      color: #3d4a5c;
    }}
    .smart-label {{
      color: #e8ebf2;
      font-size: 12px;
      font-weight: 600;
      text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.85);
      white-space: nowrap;
      pointer-events: none;
      transform: translate(10px, -6px);
    }}
  </style>
</head>
<body>
  <div id="map"></div>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
  <script>
    const uiLang = "{lang_js}";

    const turkeyBounds = L.latLngBounds([34.0, 25.0], [43.0, 46.0]);

    const map = L.map("map", {{
      zoomControl: true,
      maxBounds: turkeyBounds,
      maxBoundsViscosity: 1.0,
      minZoom: 6
    }});

    map.fitBounds(turkeyBounds);
    map.setMinZoom(6);

    window.__kitapUx = {{ z: map.getZoom(), markerT: 0, emptyT: 0 }};

    L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png", {{
      maxZoom: 19,
      minZoom: 6,
      noWrap: true,
      attribution: "&copy; OpenStreetMap contributors"
    }}).addTo(map);

    const markers = L.markerClusterGroup();
    const labelLayer = L.layerGroup();
    const records = {markers_json};
    const markerLookup = {{}};

    function escapeHtml(value) {{
      return (value ?? "").toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
    }}

    function buildPopup(item) {{
      const title = escapeHtml(item.title);
      const author = escapeHtml(item.author);
      const year = escapeHtml(item.publication_year);
      const genre = escapeHtml(item.genre);
      const loc = escapeHtml(item.location_name);
      const spatial = escapeHtml(item.spatial_type);
      const sentiment = escapeHtml(item.sentiment);
      const quote = escapeHtml(item.quote);

      if (uiLang === "tr") {{
        const desc = escapeHtml(item.description_tr || item.description || "");
        const ctxRaw = (item.historical_context || item.donem || "").toString();
        const ctx = escapeHtml(ctxRaw);
        const ctxBlock = ctxRaw.trim()
          ? `<div class="kitap-popup-context"><b>Tarihsel bağlam:</b> ${{ctx}}</div>`
          : "";
        return `
          <div class="kitap-popup-inner">
            <div class="kitap-popup-title">${{title}}</div>
            <div class="kitap-popup-meta">${{author}} · ${{year}}</div>
            <div class="kitap-popup-row"><b>Konum:</b> ${{loc}}</div>
            <div class="kitap-popup-row"><b>Tema:</b> ${{genre}}</div>
            <div class="kitap-popup-row"><b>Mekân türü:</b> ${{spatial}}</div>
            <div class="kitap-popup-row"><b>Duygu:</b> ${{sentiment}}</div>
            <div class="kitap-popup-quote">“${{quote}}”</div>
            <div class="kitap-popup-row"><b>Açıklama:</b> ${{desc}}</div>
            ${{ctxBlock}}
          </div>`;
      }}

      const descEn = escapeHtml(item.description_en || "");
      const ctxEnRaw = (item.historical_context_en || "").toString();
      const ctxEn = escapeHtml(ctxEnRaw);
      const ctxBlockEn = ctxEnRaw.trim()
        ? `<div class="kitap-popup-context"><b>Historical context:</b> ${{ctxEn}}</div>`
        : "";
      return `
        <div class="kitap-popup-inner">
          <div class="kitap-popup-title">${{title}}</div>
          <div class="kitap-popup-meta">${{author}} · ${{year}}</div>
          <div class="kitap-popup-row"><b>Location:</b> ${{loc}}</div>
          <div class="kitap-popup-row"><b>Theme:</b> ${{genre}}</div>
          <div class="kitap-popup-row"><b>Spatial type:</b> ${{spatial}}</div>
          <div class="kitap-popup-row"><b>Sentiment:</b> ${{sentiment}}</div>
          <div class="kitap-popup-quote">“${{quote}}”</div>
          <div class="kitap-popup-row"><b>Description:</b> ${{descEn}}</div>
          ${{ctxBlockEn}}
        </div>`;
    }}

    records.forEach((item) => {{
      if (!item.coordinates || item.coordinates.length < 2) return;
      const lat = item.coordinates[0];
      const lng = item.coordinates[1];

      const popup = buildPopup(item);

      const marker = L.marker([lat, lng], {{ title: item.title }});
      marker.bindPopup(popup, {{ maxWidth: 340, className: "kitap-leaflet-popup" }});
      marker.on("click", function () {{
        window.__kitapUx.markerT = Date.now();
        const latLng = marker.getLatLng();
        const targetZoom = Math.max(map.getZoom(), 13);
        map.flyTo(latLng, targetZoom, {{ duration: 1.15, easeLinearity: 0.22 }});
        setTimeout(function () {{ marker.openPopup(); }}, 420);
      }});
      markers.addLayer(marker);
      markerLookup[item.id] = marker;

      const labelMarker = L.marker([lat, lng], {{
        icon: L.divIcon({{
          className: "smart-label",
          html: `${{escapeHtml(item.title)}} - ${{escapeHtml(item.author)}}`,
        }}),
        interactive: false,
      }});
      labelLayer.addLayer(labelMarker);
    }});

    map.addLayer(markers);

    map.on("click", function () {{
      window.__kitapUx.emptyT = Date.now();
    }});

    markers.on("clusterclick", function (a) {{
      if (a.layer && typeof a.layer.spiderfy === "function") {{
        a.layer.spiderfy();
      }}
    }});

    function syncLabelVisibility() {{
      if (map.getZoom() > 8) {{
        if (!map.hasLayer(labelLayer)) {{
          map.addLayer(labelLayer);
        }}
      }} else if (map.hasLayer(labelLayer)) {{
        map.removeLayer(labelLayer);
      }}
    }}

    map.on("zoomend", function () {{
      window.__kitapUx.z = map.getZoom();
      syncLabelVisibility();
    }});
    syncLabelVisibility();

    window.flyToBook = function(bookId) {{
      window.__kitapUx.markerT = Date.now();
      const marker = markerLookup[bookId];
      if (!marker) return;
      const latLng = marker.getLatLng();
      const targetZoom = Math.max(map.getZoom(), 13);
      map.flyTo(latLng, targetZoom, {{ duration: 1.25, easeLinearity: 0.22 }});
      setTimeout(function () {{ marker.openPopup(); }}, 450);
    }};
  </script>
</body>
</html>
"""
