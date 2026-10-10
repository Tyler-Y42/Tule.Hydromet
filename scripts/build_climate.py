#!/usr/bin/env python3
"""Precompute the mid October rain climatology the page shows (static, so it loads offline).

PRISM daily precipitation (via the IEM IEMRE point service, 1991 to 2025, 20 Sep to 10 Nov)
at Painter Spring and Marjum Pass, plus Tule Valley SCAN 2163 daily gauge precipitation
(NRCS AWDB, 2011 to 2025). Writes climate.json next to index.html.
"""
import json, os, time, urllib.request, concurrent.futures as cf

POINTS = {"camp": (39.1873, -113.4430), "marjum": (39.2544, -113.3614)}
YEARS = range(1991, 2026)
UA = {"User-Agent": "Tule-Hydromet/1.0 (github.com/Tyler-Y42)"}


def get(url, tries=4):
    for k in range(tries):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90))
        except Exception:
            time.sleep(3 * (k + 1))
    raise RuntimeError(url)


def prism(key, y):
    la, lo = POINTS[key]
    d = get(f"https://mesonet.agron.iastate.edu/iemre/multiday/{y}-09-20/{y}-11-10/{la}/{lo}/json")
    return key, y, {r["date"][5:]: (None if r["prism_precip_in"] is None else round(r["prism_precip_in"] * 25.4, 2)) for r in d["data"]}


def main():
    out = {"source": {"prism": "PRISM daily via IEM IEMRE (https://mesonet.agron.iastate.edu/iemre/), mm",
                      "scan": "NRCS SCAN 2163 Tule Valley daily PRCP via AWDB, mm"},
           "points": POINTS, "prism": {k: {} for k in POINTS}, "scan": {}}
    with cf.ThreadPoolExecutor(4) as ex:
        for key, y, days in ex.map(lambda a: prism(*a), [(k, y) for k in POINTS for y in YEARS]):
            out["prism"][key][str(y)] = days
    d = get("https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/data?stationTriplets=2163:UT:SCAN&elements=PRCP&duration=DAILY&beginDate=2011-01-01&endDate=2025-12-31")
    for r in d[0]["data"][0]["values"]:
        if r["date"][5:7] in ("09", "10", "11") and r.get("value") is not None:
            out["scan"].setdefault(r["date"][:4], {})[r["date"][5:]] = round(r["value"] * 25.4, 2)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "climate.json")
    with open(path, "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
