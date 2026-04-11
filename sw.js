const CACHE = 'mm-v20';
const FILES = ['./index.html', './manifest.json', './icons/icon-192.png', './icons/icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)));
  self.skipWaiting(); // activate immediately
});

self.addEventListener('activate', e => {
  // delete all old caches that aren't mm-v5
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(cached => {
      // network-first for index.html so updates land; cache-first for assets
      if (e.request.url.endsWith('index.html') || e.request.url.endsWith('/')) {
        return fetch(e.request).then(res => {
          caches.open(CACHE).then(c => c.put(e.request, res.clone()));
          return res;
        }).catch(() => cached);
      }
      return cached || fetch(e.request);
    })
  );
});
