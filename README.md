# Amazon Movie Recommender

A local Streamlit application that recommends movies and TV products from Amazon review data. Select one of the 50 most active reviewers in the loaded sample and request up to three recommendations based on similar reviewers. If collaborative recommendations are unavailable, the app falls back to popular unseen products.

## Project links

- **GitHub repository:** [ANISHAKHADE/amazon-movie-recommender](https://github.com/ANISHAKHADE/amazon-movie-recommender)
- **Live Streamlit app:** [Amazon Movie Recommender](https://amazon-movie-recommender-zgeeintsbmzfxrevz66jzx.streamlit.app/)

## Features

- Builds a reviewer-by-product ratings matrix from the review dataset.
- Uses cosine similarity to find similar reviewers and ranks unseen products from their ratings.
- Stores the matrix as a SciPy CSR sparse matrix and calculates similarities for the selected reviewer on demand.
- Falls back to overall product popularity when similar reviewers cannot provide positive recommendations.
- Displays product titles from the metadata dataset and match scores.

## How recommendations are calculated

For each review, the app derives an adjusted rating using the original star rating, review length, and vote count:

```text
adjusted_rating =
    (overall_rating - 3)
    * min(review_word_count, 20) / 20
    * (1 + ln(vote_count + 1))
```

The app pivots these values into a reviewer-by-product matrix. It selects the 50 reviewers with the most positive matrix entries. For the selected reviewer, it finds positive-similarity neighbors, considers the top 15, and calculates similarity-weighted scores for products the reviewer has not seen. Up to three products with positive scores are returned.

If that step produces no recommendations, the app ranks unseen products by the sum of their adjusted ratings across reviewers and returns up to three positive results. Product identifiers are mapped to titles using `parent_asin`, falling back to `asin`. If no metadata match exists, the UI displays `Title Not Found`.

## Project structure

| Path | Role |
|---|---|
| `app.py` | Streamlit entry point; reads datasets, constructs the ratings matrix, performs recommendations, and renders the UI. |
| `demo_reviews.json.gz` | Compressed line-delimited review sample used by the application. |
| `demo_meta.jsonl` | Product metadata sample used to map product IDs to titles. |
| `Untitled-1.py` | Earlier standalone experimentation script. It uses a hard-coded Windows path and computes a dense similarity matrix; use `app.py` to run the current app. |
| `shrinker.py` | Utility for generating the demo datasets from the full source datasets. |
| `requirements.txt` | Pinned Python dependencies for the application. |
| `TESTING-LOG.md` | Detailed test history and results, including all 50 users' recommendations. |
| `.gitignore` | Excludes the local virtual environment and Python bytecode cache. |

The application is a **single-page Python/Streamlit web app**. There is no separate frontend, API server, database, authentication layer, or external service integration. The UI, data loading, and recommendation logic currently live together in `app.py`.

## Requirements

- Python 3.11 is the tested runtime (tested with Python 3.11.9).
- The two demo dataset files listed above must be present in the project root, beside `app.py`. They are included in the GitHub repository.
- Dependency versions are pinned in `requirements.txt`; install them with the command below.

The versions in the environment used for the successful app test were:

| Package | Tested version |
|---|---:|
| pandas | 3.0.5 |
| numpy | 2.4.6 |
| scipy | 1.17.1 |
| scikit-learn | 1.9.0 |
| streamlit | 1.63.0 |

## Setup and run (Windows PowerShell)

Open PowerShell in the project root (the directory containing `app.py` and the datasets), then run:

```powershell
py -3.11 -m venv myyenv
.\myyenv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If PowerShell prevents virtual-environment activation, invoke the environment's Python directly:

```powershell
.\myyenv\Scripts\python.exe -m pip install -r requirements.txt
.\myyenv\Scripts\python.exe -m streamlit run app.py
```

Streamlit prints the local URL after startup (normally `http://localhost:8501`). The app uses relative dataset paths, so launch it with the project root as the working directory. It reports an error if a dataset is absent or the working directory is incorrect.

## Data and runtime notes

- Review data is read from `demo_reviews.json.gz`; the app processes up to **25,000 reviews**.
- In the tested sample, those rows contained **20,424 reviewers** and **191 product IDs**. The UI selector shows the 50 reviewers with the most positive adjusted-rating entries in that sample, labeled `User 1` through `User 50`.
- The demo files are reduced samples intended to keep the repository and hosted app practical to run. The full source datasets (`Movies_and_TV_5.json.gz` and `meta_Movies_and_TV.jsonl`) are not included in the repository.
- `shrinker.py` reads those full source datasets from the project root and generates the demo files. Run it only when both source datasets are available.
- The metadata loader reads the demo JSONL file and stores title mappings in memory during app startup.
- Sparse, on-demand cosine similarity avoids building a dense all-reviewer similarity matrix.
- Some recommended product IDs may not have titles in the supplied metadata; these appear as `Title Not Found`.
- Streamlit currently reports that `use_container_width` is deprecated. This is a warning, not a runtime failure.

## Validation

On 2026-10-09, the app was started and exercised using Streamlit's app test runner for all 50 selector users. Every selection produced a recommendation table without an app exception:

- **117** recommendations total: 30 users received 3, 7 received 2, and 13 received 1.
- The popularity fallback was used for 18 users.
- All returned match scores were positive.
- A live HTTP smoke test returned `ok` from `/_stcore/health` and HTTP 200 from the homepage. A browser smoke test confirmed the page and User 1's results rendered.
- The deployed Streamlit URL was also opened and tested: data loaded, the 50-user selector appeared, and User 1's recommendation table rendered after clicking **Find Movies**.
- In the 50-user run, 16 recommendation rows showed `Title Not Found`.

For the per-user IDs and chronological record of earlier path/startup blockers, see [TESTING-LOG.md](./TESTING-LOG.md).

## Known limitations

- Results are based only on the first 25,000 reviews, not the full review file.
- The repository includes reduced demo datasets, not the complete source datasets.
- The recommendation method is neighborhood-based collaborative filtering with a popularity fallback; it does not use movie content, genres, or external services.
- Missing title records reduce the readability of some results, although recommendations still return.
- Dependency versions are pinned in `requirements.txt`; changing those pins should be followed by a fresh environment and app test.
