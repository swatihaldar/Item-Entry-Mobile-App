
const CACHE_NAME = "erp-mobile-cache-v1";
const urlsToCache = [
  "/",
  "/erp_mobile",
  "/index.html",
  "/src/main.js",
  "/assets/erp_mobile/frontend/manifest.webmanifest",
  "/favicon.png"
];

// Install Service Worker
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("✅ Caching files...");
      return cache.addAll(urlsToCache);
    })
  );
});

// Fetch Cached Resources
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});

// Activate and Remove Old Caches
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            console.log("🗑 Deleting old cache:", cache);
            return caches.delete(cache);
          }
        })
      );
    })
  );
});
