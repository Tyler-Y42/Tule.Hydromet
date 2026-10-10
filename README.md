# Tule Valley Hydromet

Rain forecast, radar and gauge rain history and soil moisture for
Painter Spring (camp, 5,408 ft) and Marjum Pass (6,238 ft), House Range, Utah.

Live: https://tyler-y42.github.io/Tule.Hydromet/

- Forecast: NWS gridded forecast (SLC 38,112 and 41,114).
- Radar history: IEM IEMRE point service (NCEP Stage IV hourly, NOAA MRMS daily). Radar now: IEM NEXRAD mosaic tiles.
- Gauges: NRCS SCAN 2163 Tule Valley (AWDB, hourly, MST stamps), MesoWest TVWU1, KCWU1, NSNA.
- Offline: the last load is saved in localStorage; `sw.js` caches the page, libraries and viewed map tiles.
- The trip dates are `TRIP` near the top of the script in `index.html`.
