


import pandas as pd
import gzip 
import json
import math
import numpy as np
import random
from sklearn.metrics.pairwise import cosine_similarity
pa_th='C:/Users/anish/Desktop/MRS/Movies_and_TV_5.json.gz'


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

df=getdf(pa_th)
# print(df)
user_matrix=pd.pivot_table(df,values="adjusted_rating",index=["reviewerID"],columns=["asin"],fill_value=0)
# print(user_matrix.shape)
# print(user_matrix.info())

sim_array=cosine_similarity(user_matrix)
user_similarity_df=pd.DataFrame(sim_array,index=user_matrix.index,columns=user_matrix.index)
# print(user_similarity_df.shape)
# print(user_similarity_df.head())
# print(user_similarity_df.iloc[:5,:5])



# print(user_id)
user_id = "A16CZRQL23NOIW"
neighbors=user_similarity_df.loc[user_id].sort_values(ascending=False).head(5)

r_ow=user_similarity_df.loc[user_id]
neighbors=r_ow.drop(user_id)
neighbors=neighbors[neighbors > 0]
top_neighbor_ids=neighbors.sort_values(ascending=False).head(5).index
neighbor_movies=user_matrix.loc[top_neighbor_ids]
movies=neighbor_movies.mean(axis=0).sort_values(ascending=False)

target_history=user_matrix.loc[user_id]
unseen_movies=movies[target_history==0]
final_recommendations=unseen_movies[unseen_movies>0].head(3)
print(final_recommendations)