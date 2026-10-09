
import pandas as pd
import gzip 
import json
import math
import numpy as np
import random
import scipy.sparse as sp
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

st.title("Amazon Movie Recommender")

def parse(path):
    g=gzip.open(path,'r')
    for l in g:
        yield json.loads(l)

        
def getdf(path):
        i=0
        master_directory={}
        target=20
        for d in parse(path):
            cur_row={}    
            cur_row["reviewerID"]=d["reviewerID"]
            cur_row["asin"]=d["asin"]
            cur_row["overall"]=d["overall"]
            cur_row["reviewText"]=len((d.get("reviewText","").split()))
            word_count=cur_row["reviewText"]
            wei_ght=min(word_count,target)/target
            cur_row["unixReviewTime"]=d["unixReviewTime"]
            cur_row["vote"]=d.get("vote",0)
            clean_vote = int(str(cur_row["vote"]).replace(",", ""))
            vote_modifier=1+math.log(clean_vote+1)
            adjusted_rat=(cur_row["overall"]-3)*wei_ght*vote_modifier
            cur_row["adjusted_rating"]=adjusted_rat
            master_directory[i]=cur_row
            i+=1
            if i==25000:
                break
        return pd.DataFrame.from_dict(master_directory,orient="index")

@st.cache_data
def load_data():
    df = getdf("Movies_and_TV_5.json.gz")

    user_matrix = df.pivot_table(index="reviewerID", columns="asin", values="adjusted_rating", fill_value=0)
    sparse_matrix = sp.csr_matrix(user_matrix.values)    
   
    return user_matrix, sparse_matrix

@st.cache_data
def load_titles():
    title_dict = {}
    path = "meta_Movies_and_TV.jsonl"
    
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            d = json.loads(line)

            item_id = d.get("parent_asin", d.get("asin"))
            if item_id:
                title_dict[item_id] = d.get("title", "Unknown Title")
                
    return title_dict


title_mapping = load_titles()
def get_recommendations(user_id, user_matrix, sparse_matrix):
    
    # ENTERPRISE FIX: Lazy Evaluation
    # 1. Find the row index (number) of the target user
    user_idx = user_matrix.index.get_loc(user_id)
    
    # 2. Extract just their single 1D vector from the compressed matrix
    target_vector = sparse_matrix[user_idx]
    
    # 3. Calculate similarity ONLY for this one vector against the rest of the sparse matrix
    sim_scores = cosine_similarity(target_vector, sparse_matrix).flatten()
    
    # 4. Convert the 1D results back into a Pandas Series with the proper reviewerIDs
    r_ow = pd.Series(sim_scores, index=user_matrix.index)
    neighbors = r_ow.drop(user_id)
    neighbors = neighbors[neighbors > 0]
    target_history = user_matrix.loc[user_id]

    final_recommendations=pd.Series(dtype=float)
    used_fallback=False

    if not neighbors.empty:
        top_neighbors = neighbors.sort_values(ascending=False).head(15)
        top_neighbor_ids = top_neighbors.index
        neighbor_movies = user_matrix.loc[top_neighbor_ids]
        sim_weights = top_neighbors.values.reshape(-1, 1)
        weighted_ratings = neighbor_movies.values * sim_weights
        weight_sum = sim_weights.sum()
        consensus_scores = weighted_ratings.sum(axis=0) / (weight_sum if weight_sum > 0 else 1)
        movies = pd.Series(consensus_scores, index=neighbor_movies.columns).sort_values(ascending=False)       
        unseen_movies = movies[target_history == 0]
        final_recommendations = unseen_movies[unseen_movies > 0].head(3)

    if final_recommendations.empty:
        used_fallback = True
        overall_popularity = user_matrix.sum(axis=0).sort_values(ascending=False)
        unseen_popular = overall_popularity[target_history == 0]  
        final_recommendations = unseen_popular[unseen_popular > 0].head(3)

    return final_recommendations, used_fallback

st.write("Loading 25,000 rows of Amazon data... (This will only take a moment on the first run)")
user_matrix, sparse_matrix = load_data()

st.success("Data loaded successfully!")
st.header("Get Recommendations")

# Dynamically find the Top 50 most active users
top_users = (user_matrix > 0).sum(axis=1).sort_values(ascending=False).head(50).index.tolist()

# Create a dictionary mapping ugly IDs to normal names (e.g., "User 1", "User 2")
friendly_names = {user: f"User {i+1}" for i, user in enumerate(top_users)}

# Use format_func to display the friendly name, but keep the real ID for the math
user_id = st.selectbox(
    "Select a Target User:", 
    options=top_users,
    format_func=lambda x: friendly_names[x]
)
 


if st.button("Find Movies"):    
    final_recommendations, used_fallback = get_recommendations(user_id, user_matrix, sparse_matrix)

    if used_fallback:
        st.info("Taste twins had no new movies to offer. Switching to Popularity Fallback!")
    if final_recommendations.empty:
        st.error("The dataset is too small to find any unwatched movies for this user.")
    else:
        st.subheader(f"Top 3 Movie Matches for {friendly_names.get(user_id, user_id)}")
        
        final_df = final_recommendations.to_frame(name="Match Score")
        final_df["Movie Title"] = final_df.index.map(lambda x: title_mapping.get(x, "Title Not Found"))
        final_df = final_df[["Movie Title", "Match Score"]]
        
        st.dataframe(final_df, use_container_width=True)

