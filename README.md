# Amazon Movie Recommender

A local Streamlit application that recommends movies and TV products from Amazon review data. Select one of the 50 most active reviewers in the loaded sample and request up to three recommendations based on similar reviewers. If collaborative recommendations are unavailable, the app falls back to popular unseen products.

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
| `Movies_and_TV_5.json.gz` | Compressed line-delimited review data used by the application. |
| `meta_Movies_and_TV.jsonl` | Line-delimited product metadata used to map product IDs to titles. |
| `Untitled-1.py` | Earlier standalone experimentation script. It uses a hard-coded Windows path and computes a dense similarity matrix; use `app.py` to run the current app. |
| `TESTING-LOG.md` | Detailed test history and results, including all 50 users' recommendations. |
| `.gitignore` | Excludes the local virtual environment and Python bytecode cache. |

The application is a **single-page Python/Streamlit web app**. There is no separate frontend, API server, database, authentication layer, or external service integration. The UI, data loading, and recommendation logic currently live together in `app.py`.

## Requirements

- Python 3.11 is the tested runtime (tested with Python 3.11.9).
- The two dataset files listed above must be present in the project root, beside `app.py`.
- Python packages: `pandas`, `numpy`, `scipy`, `scikit-learn`, and `streamlit`.
- The repository currently has no `requirements.txt`, `pyproject.toml`, or other dependency lock/manifest file.

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
python -m pip install pandas numpy scipy scikit-learn streamlit
python -m streamlit run app.py
```

If PowerShell prevents virtual-environment activation, invoke the environment's Python directly:

```powershell
.\myyenv\Scripts\python.exe -m pip install pandas numpy scipy scikit-learn streamlit
.\myyenv\Scripts\python.exe -m streamlit run app.py
```

Streamlit prints the local URL after startup (normally `http://localhost:8501`). The app uses relative dataset paths, so launch it with the project root as the working directory. It reports an error if a dataset is absent or the working directory is incorrect.

## Data and runtime notes

- Review data is read from the beginning of `Movies_and_TV_5.json.gz`; processing stops after **25,000 reviews**.
- In the tested sample, those rows contained **20,424 reviewers** and **191 product IDs**. The UI selector shows the 50 reviewers with the most positive adjusted-rating entries in that sample, labeled `User 1` through `User 50`.
- The supplied review and metadata files are large (approximately **791 MB** compressed reviews and **1.29 GB** metadata in the tested project copy). The metadata loader reads the JSONL file and stores title mappings in memory. Initial startup may therefore take time and use substantial memory.
- Sparse, on-demand cosine similarity avoids building a dense all-reviewer similarity matrix, but startup still loads the review sample and metadata.
- Some recommended product IDs may not have titles in the supplied metadata; these appear as `Title Not Found`.
- Streamlit currently reports that `use_container_width` is deprecated. This is a warning, not a runtime failure.

## Validation

On 2026-10-09, the app was started and exercised using Streamlit's app test runner for all 50 selector users. Every selection produced a recommendation table without an app exception:

- **117** recommendations total: 30 users received 3, 7 received 2, and 13 received 1.
- The popularity fallback was used for 18 users.
- All returned match scores were positive.
- A live HTTP smoke test returned `ok` from `/_stcore/health` and HTTP 200 from the homepage. A browser smoke test confirmed the page and User 1's results rendered.
- In the 50-user run, 16 recommendation rows showed `Title Not Found`.

For the per-user IDs and chronological record of earlier path/startup blockers, see [TESTING-LOG.md](./TESTING-LOG.md).

## Known limitations

- Results are based only on the first 25,000 reviews, not the full review file.
- The recommendation method is neighborhood-based collaborative filtering with a popularity fallback; it does not use movie content, genres, or external services.
- Missing title records reduce the readability of some results, although recommendations still return.
- Dependencies are not pinned in a project manifest, so fresh installs may resolve different package versions.
