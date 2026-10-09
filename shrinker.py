import gzip
import json

print("Shrinking datasets for GitHub...")

# 1. Extract the first 25,000 reviews and track their ASINs (Movie IDs)
asins = set()
with gzip.open('Movies_and_TV_5.json.gz', 'rt', encoding='utf-8') as f_in:
    with gzip.open('demo_reviews.json.gz', 'wt', encoding='utf-8') as f_out:
        for i, line in enumerate(f_in):
            if i >= 25000: break
            f_out.write(line)
            asins.add(json.loads(line).get("asin"))

# 2. Extract only the metadata for those specific movies
with open('meta_Movies_and_TV.jsonl', 'r', encoding='utf-8') as f_in:
    with open('demo_meta.jsonl', 'w', encoding='utf-8') as f_out:
        for line in f_in:
            d = json.loads(line)
            item_id = d.get("parent_asin", d.get("asin"))
            if item_id in asins:
                f_out.write(line)

print("Done! Your demo files are ready.")