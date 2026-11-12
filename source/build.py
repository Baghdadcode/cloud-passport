"""Assemble the single-file Windows app and the PWA folder."""
import pathlib, sys, json, hashlib
from PIL import Image, ImageDraw, ImageFont

B = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
data = (pathlib.Path(sys.argv[2])).read_text(encoding="utf-8")
html = (B / "app.html").read_text(encoding="utf-8").replace("/*DATA*/", data.replace("</", "<\\/"))

# 1) Single file for Windows: double-click to open, works offline.
(OUT / "CloudPassport.html").write_text(html.replace("<!--PWA-->", "").replace("/*SW*/", ""), encoding="utf-8")

# 2) PWA folder for iPhone (needs to be served once over https, then works offline).
pwa = OUT / "iphone-web-app"; pwa.mkdir(exist_ok=True)
ver = hashlib.sha1(html.encode()).hexdigest()[:8]
(pwa / "index.html").write_text(
    html.replace("<!--PWA-->", '<link rel="manifest" href="manifest.webmanifest"><link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="icon" href="icon-192.png">')
        .replace("/*SW*/", 'if ("serviceWorker" in navigator && location.protocol === "https:") navigator.serviceWorker.register("sw.js").catch(() => {});'),
    encoding="utf-8")
(pwa / "manifest.webmanifest").write_text(json.dumps({
    "name": "Cloud Passport", "short_name": "Cloud Passport", "start_url": "./", "scope": "./",
    "display": "standalone", "background_color": "#EEF1E5", "theme_color": "#5A1424",
    "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1))
(pwa / "sw.js").write_text(f"""const C="cp-{ver}";
const CORE=["./","index.html","manifest.webmanifest","icon-192.png","icon-512.png","apple-touch-icon.png"];
self.addEventListener("install",e=>{{e.waitUntil(caches.open(C).then(c=>c.addAll(CORE)));self.skipWaiting();}});
self.addEventListener("activate",e=>{{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))));self.clients.claim();}});
self.addEventListener("fetch",e=>{{if(e.request.method!=="GET")return;e.respondWith(caches.match(e.request,{{ignoreSearch:true}}).then(r=>r||fetch(e.request).then(res=>{{if(res.ok||res.type==="opaque"){{const cl=res.clone();caches.open(C).then(c=>c.put(e.request,cl));}}return res;}}).catch(()=>caches.match("index.html"))));}});
""")

def icon(size, path):
    im = Image.new("RGB", (size, size), "#5A1424"); d = ImageDraw.Draw(im)
    s = size / 512
    d.rounded_rectangle([96*s, 64*s, 416*s, 448*s], radius=28*s, outline="#D9B45C", width=int(10*s))
    d.ellipse([176*s, 150*s, 336*s, 310*s], outline="#D9B45C", width=int(10*s))
    # cloud-ish arcs inside the emblem
    d.arc([200*s, 200*s, 312*s, 300*s], 180, 360, fill="#F0DCA6", width=int(10*s))
    d.line([206*s, 262*s, 306*s, 262*s], fill="#F0DCA6", width=int(10*s))
    d.line([170*s, 370*s, 342*s, 370*s], fill="#D9B45C", width=int(10*s))
    d.line([200*s, 400*s, 312*s, 400*s], fill="#D9B45C", width=int(6*s))
    im.save(path)
icon(192, pwa / "icon-192.png"); icon(512, pwa / "icon-512.png"); icon(180, pwa / "apple-touch-icon.png")
print("built", ver)
