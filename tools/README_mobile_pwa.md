## Chance Mobile Web App - Add to Home Screen

The mobile app now supports PWA install flow.

### What changed

- Added a dynamic `manifest.webmanifest` endpoint.
- Added a dynamic `sw.js` service worker endpoint.
- Added an **"Add to Home Screen"** button in the app UI.
- Added a fallback instruction for browsers that don't expose the install prompt.

### Start server

```bash
python3 tools/chance_mobile_webapp.py --host 0.0.0.0 --port 8787 --agency-profiles-dir /workspace/external/agency-agents
```

### Use from phone

1. Open the app URL in Chrome (Android) or Safari (iOS).
2. Press **Add to Home Screen**.
3. If native install prompt appears, confirm install.
4. If no prompt appears, follow browser menu instructions shown in the app.

### Notes

- For best install behavior, access over HTTPS (for example via your tunnel URL).
- Service worker is intentionally minimal for now and focuses on shell caching.
