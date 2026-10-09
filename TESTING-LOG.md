# Amazon Movie Recommender — Testing Log

**Recorded:** 2026-10-09 (UTC+05:30)  
**Application:** `app.py`  
**Purpose:** Record runtime testing, 50-user recommendation results, issues, and how test status changed during this chat.

## Current test status

**PASS** for application startup, data loading, and the recommendation flow for every user in the top-50 selector.

The Streamlit app was run through its test runner and as a live local web app. Each of the 50 selector choices was selected and submitted with **Find Movies**. Every run completed without an app exception and showed a recommendation table.

| Check | Result |
|---|---|
| Startup and data loading | PASS — “Data loaded successfully!” displayed |
| User selector | PASS — 50 users available |
| Recommendation action | PASS — all 50 users produced a table |
| Recommendation count | 117 total: 30 users received 3, 7 received 2, 13 received 1 |
| Empty recommendation results | 0 users |
| Positive match scores | PASS — all returned scores were positive |
| Popularity fallback | Used for 18 users |
| Live health endpoint | PASS — `/_stcore/health` returned `ok` |
| Live homepage | PASS — HTTP 200 |
| Browser smoke test | PASS — app rendered and User 1 recommendations appeared |
| App exceptions during 50-user run | 0 |

The test server used `http://localhost:8765` and was stopped after the checks.

## Per-user recommendation results

These are the movie IDs returned during the 50-user evaluation. The list records recommendation identifiers, rather than movie names, so recommendations with missing metadata remain identifiable. A dagger (†) marks an ID that did not resolve to a title in the metadata file.

| User | Reviewed items in sampled data | Recommendations | Popularity fallback | Recommended movie IDs |
|---|---:|---:|:---:|---|
| User 1 | 24 | 3 | No | 0767882938, 0780021045†, 0767027329 |
| User 2 | 19 | 3 | No | 0767088247, 0783226896, 0780623614 |
| User 3 | 17 | 3 | No | 0783114729, 0767805712, 0767818105 |
| User 4 | 16 | 2 | No | 078322687X, 0780622383 |
| User 5 | 16 | 3 | No | 0783230427, 0780623614, 0767817648 |
| User 6 | 21 | 3 | No | 0767802799, 0767809254, 0767817664 |
| User 7 | 16 | 2 | No | 0783227272, 0780622537 |
| User 8 | 12 | 3 | Yes | 0783225857, 078322687X, 076780192X |
| User 9 | 12 | 1 | No | 0780621832 |
| User 10 | 13 | 3 | Yes | 0783225857, 078322687X, 0767805712 |
| User 11 | 11 | 2 | No | 0767830555, 0780021088 |
| User 12 | 13 | 3 | Yes | 0783225857, 0767824571, 078322687X |
| User 13 | 10 | 3 | Yes | 0782010792†, 0783225857, 0767824571 |
| User 14 | 11 | 3 | No | 0783225857, 0767824571, 0767827759† |
| User 15 | 10 | 3 | Yes | 0783225857, 0767824571, 078322687X |
| User 16 | 10 | 3 | Yes | 0782010792†, 0783225857, 0767824571 |
| User 17 | 10 | 3 | Yes | 0782010792†, 0783225857, 0767824571 |
| User 18 | 12 | 3 | Yes | 0783225857, 0767824571, 078322687X |
| User 19 | 9 | 3 | Yes | 0782010792†, 0783225857, 0767824571 |
| User 20 | 9 | 3 | Yes | 0782010792†, 0767824571, 076780192X |
| User 21 | 9 | 3 | Yes | 0782010792†, 0783225857, 0767824571 |
| User 22 | 9 | 3 | Yes | 0782010792†, 0783225857, 0767824571 |
| User 23 | 9 | 1 | No | 0767830555 |
| User 24 | 10 | 3 | Yes | 0782010792†, 0767824571, 078322687X |
| User 25 | 9 | 3 | No | 0783239955, 0767817486, 0767834739† |
| User 26 | 8 | 1 | No | 0780622383 |
| User 27 | 10 | 3 | No | 0780615573, 0767818105, 0780020715 |
| User 28 | 8 | 3 | Yes | 0783225857, 0767824571, 078322687X |
| User 29 | 9 | 3 | No | 0783225911†, 078322687X, 0767802799 |
| User 30 | 8 | 3 | Yes | 0782010792†, 0783225857, 0767824571 |
| User 31 | 8 | 3 | Yes | 0782010792†, 0783225857, 0767824571 |
| User 32 | 8 | 3 | Yes | 0782010792†, 0783225857, 0767824571 |
| User 33 | 8 | 1 | No | 0767830555 |
| User 34 | 8 | 3 | No | 0783227361, 0783114907, 0780622383 |
| User 35 | 10 | 2 | No | 0783112750, 076780192X |
| User 36 | 8 | 3 | Yes | 0782010792†, 0767824571, 078322687X |
| User 37 | 8 | 1 | No | 0767830555 |
| User 38 | 8 | 1 | No | 0780622383 |
| User 39 | 8 | 1 | No | 0767824571 |
| User 40 | 9 | 1 | No | 0783226799 |
| User 41 | 8 | 1 | No | 0767817664 |
| User 42 | 7 | 1 | No | 0782008372 |
| User 43 | 8 | 1 | No | 0783225857 |
| User 44 | 7 | 1 | No | 076780192X |
| User 45 | 7 | 3 | No | 0767824555, 0307142493, 0783226535 |
| User 46 | 9 | 2 | No | 0767830555, 0780630866 |
| User 47 | 7 | 1 | No | 0780022319 |
| User 48 | 8 | 2 | No | 0767817664, 0767830555 |
| User 49 | 7 | 2 | No | 0783114729, 0780635299 |
| User 50 | 7 | 3 | No | 0767830555, 078062582X, 0767001311 |

## Outstanding observations

### Missing movie titles

The metadata scan found titles for 40 of the 45 distinct recommended movie IDs. These five IDs had no matching title record and are rendered by the app as **“Title Not Found”**:

- `0767827759`
- `0767834739`
- `0780021045`
- `0782010792`
- `0783225911`

Across the 50 displayed users, this resulted in **16 recommendation rows** showing “Title Not Found”. Recommendation scoring still completed for these rows.

### Streamlit deprecation warning

During a successful recommendation run, Streamlit warned that `use_container_width` is deprecated and will be removed after 2025-12-31. The current usage should be changed to `width="stretch"` when convenient. This warning did not cause test failures.

## Test history and resolved blockers

1. **Initial recommendation-only test:** The then-current implementation created a dense similarity matrix for approximately 20,424 users. This was not suitable for a full UI run on the available machine, which had about 1 GB free RAM. To evaluate recommendations, similarity rows for the selected users were calculated without materializing the full matrix. The 50-user recommendation checks passed.
2. **Earlier path failures:** Subsequent app versions temporarily failed startup because relative paths referenced files under `MRS/` when the files were directly in the project folder. One run stopped while opening the metadata file; another stopped while opening the compressed review file. In those runs, the selector and browser recommendation flow could not be tested.
3. **Sparse-matrix version:** The app was updated to use a CSR sparse matrix and calculate similarities on demand. This allowed the recommendation algorithm to be evaluated for all 50 users without building the full dense user-to-user matrix.
4. **Current successful run:** The current app loaded its data and title metadata, exposed all 50 users, and passed the recommendation flow for each selection. The live app health check and homepage also returned successfully.

## Scope and limitations

- The app loads the first **25,000 review records** from `Movies_and_TV_5.json.gz`; the outcomes above apply to that sample and the top 50 users derived from it.
- The final 50-user check exercised Streamlit’s app flow. A separate browser smoke test confirmed that the live page rendered and User 1’s recommendation table appeared.
- Missing title metadata and the deprecation warning remain observations; they did not prevent recommendation generation.
