# Food Pantry Route Optimizer — Plan

## Overview

A single HTML file that takes a CSV of addresses, clusters them geographically among N drivers, orders each cluster for efficient pickup, and outputs copy-paste lists with Google Maps links.

No server. No database. No login. Just CSV in → optimized routes out.

---

## Input

**CSV format:**
```csv
full_address,latitude,longitude
"123 Main St, Allentown PA",40.6084,-75.4902
"456 Oak Ave, Bethlehem PA",40.6259,-75.3705
```

Optional 4th column for notes:
```csv
full_address,latitude,longitude,notes
"123 Main St, Allentown PA",40.6084,-75.4902,"Ring doorbell"
```

**Requirements:**
- Latitude and longitude should be populated (rows with missing coords will be flagged/skipped)
- No limit on row count — tested for 10k

---

## User Interface

```
┌────────────────────────────────────────────────────────────┐
│  FOOD PANTRY ROUTE OPTIMIZER                               │
│                                                            │
│  Step 1: Upload CSV                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  [Choose File] or drag CSV here                      │  │
│  │                                                      │  │
│  │  ✓ Loaded: 10,234 addresses                          │  │
│  │  ⚠ Skipped: 47 (missing coordinates)                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  Step 2: Number of drivers                                 │
│  [ 20 ]                                                    │
│                                                            │
│  Step 3: Generate                                          │
│  [ Generate Routes ]                                       │
│                                                            │
│  ──────────────────────────────────────────────────────    │
│                                                            │
│  Results                                                   │
│                                                            │
│  ▼ Driver 1 — 487 stops                    [Copy] [Save]   │
│    1. 123 Main St, Allentown PA            [Maps]          │
│    2. 789 Elm Rd, Allentown PA             [Maps]          │
│    3. ...                                                  │
│                                                            │
│  ▼ Driver 2 — 512 stops                    [Copy] [Save]   │
│    ...                                                     │
│                                                            │
│  ▼ Driver 3 — 498 stops                    [Copy] [Save]   │
│    ...                                                     │
│                                                            │
│  [Download All as ZIP]                                     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## Output Formats

### Copy to Clipboard (per driver)

```
Driver 1 — 487 stops

1. 123 Main St, Allentown PA
   https://www.google.com/maps/search/?api=1&query=40.6084,-75.4902

2. 789 Elm Rd, Allentown PA
   https://www.google.com/maps/search/?api=1&query=40.6091,-75.4875

3. 456 Oak Ave, Allentown PA
   https://www.google.com/maps/search/?api=1&query=40.6103,-75.4901

...
```

### Save as File (per driver)

Text file: `driver-1.txt`

Same format as clipboard, easy to print or share.

### Download All

ZIP file containing:
- `driver-1.txt`
- `driver-2.txt`
- ...
- `driver-20.txt`
- `summary.txt` (driver names, stop counts)

---

## Algorithm

### Step 1: Parse CSV

- Use PapaParse library
- Validate lat/lng are present and numeric
- Flag/skip bad rows with warning count

### Step 2: K-Means Clustering

Divide addresses into N clusters (N = number of drivers).

```
Input:  10,000 addresses as [lat, lng] points
K:      20 (number of drivers)
Output: Each address tagged with cluster 0-19
```

Library: `ml-kmeans` via CDN, or simple custom implementation (~50 lines).

K-means naturally groups geographically close addresses together.

### Step 3: Nearest-Neighbor Ordering

For each cluster, order the stops to minimize backtracking.

```
1. Start with the northernmost address (or centroid)
2. Find the nearest unvisited address
3. Move there, mark visited
4. Repeat until all visited
```

This is a greedy TSP approximation — not perfect, but fast and good enough.

### Step 4: Generate Output

For each driver/cluster:
- Number the stops 1, 2, 3...
- Generate Google Maps link for each: `https://www.google.com/maps/search/?api=1&query={lat},{lng}`
- Format as copyable text

---

## Technical Details

### Libraries (CDN, no install)

| Library | Purpose | CDN |
|---------|---------|-----|
| PapaParse | CSV parsing | `https://unpkg.com/papaparse@5` |
| ml-kmeans | Clustering | `https://unpkg.com/ml-kmeans@6` |
| JSZip | ZIP download | `https://unpkg.com/jszip@3` |

### Browser Requirements

- Modern browser (Chrome, Firefox, Edge, Safari)
- JavaScript enabled
- Works offline after first load (libraries cached)

### Performance

| Addresses | Clustering | Ordering | Total |
|-----------|------------|----------|-------|
| 1,000 | <100ms | <200ms | <0.5s |
| 10,000 | ~500ms | ~2s | ~3s |
| 50,000 | ~2s | ~10s | ~15s |

All runs client-side in the browser.

---

## File Structure

```
food-pantry-optimizer.html    ← The entire application (single file)
```

That's it. One file. Open in browser. Done.

---

## Optional Enhancements (Phase 2)

If needed later, easy to add:

| Feature | Effort |
|---------|--------|
| Remember last driver count in localStorage | 5 min |
| Leaflet map preview showing clusters | 30 min |
| Batched Google Maps route links (10 stops each) | 20 min |
| KML export for Google My Maps | 20 min |
| Driver name labels instead of numbers | 10 min |
| Dark mode | 10 min |

---

## Not Included (Separate Tools)

- **Geocoding:** If CSV has bad/missing coords, fix externally or use a separate geocoding script
- **Pickup tracking:** Drivers checking off completed stops — use Google Sheets or separate app
- **Driver assignment history:** No persistence, just generates fresh each time

---

## How to Use

1. Open `food-pantry-optimizer.html` in Chrome
2. Drag your CSV onto the page (or click to browse)
3. Enter number of drivers (e.g., 20)
4. Click "Generate Routes"
5. Click "Copy" next to each driver to get their list
6. Paste into email, text, doc — share with driver
7. Driver clicks links to navigate to each pickup

---

## Next Step

Build the HTML file.
