// Offline support: the page shell, libraries and climatology are cached; the page itself
// keeps its last data load in localStorage. Map tiles are cached as you view them.
const CACHE = 'tule-v1';
const CORE = ['./', './index.html', './keys.js', './climate.json', './manifest.webmanifest',
  'https://cdn.jsdelivr.net/npm/chart.js@4.5.1/dist/chart.umd.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE && k !== 'tule-tiles').map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET') return;
  if (u.origin === location.origin) { // network first, so updates show; cache when offline
    e.respondWith(fetch(e.request).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r; }).catch(() => caches.match(e.request, { ignoreSearch: true })));
  } else if (/cdn\.jsdelivr\.net|cdnjs\.cloudflare\.com/.test(u.host)) {
    e.respondWith(caches.match(e.request).then(m => m || fetch(e.request)));
  } else if (/server\.arcgisonline\.com/.test(u.host)) { // map tiles: cache as viewed
    e.respondWith(caches.open('tule-tiles').then(c => c.match(e.request).then(m => m || fetch(e.request).then(r => { c.put(e.request, r.clone()); return r; }))));
  }
});
