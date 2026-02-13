# src/aggregation.py
import os
import json
import numpy as np
from collections import Counter, defaultdict
from openai import OpenAI
from dotenv import load_dotenv
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_distances

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Embedding model (选择合适的 embedding 模型)
EMBED_MODEL = "text-embedding-3-small"  # or text-embedding-3-large

def get_embeddings(texts):
    # texts: list[str]
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    # 返回 list of vectors
    return [item.embedding for item in resp.data]

def cluster_texts(texts, eps=0.35, min_samples=1):
    """
    使用 DBSCAN 做语义聚类（cosine 距离）。
    eps 是距离阈值（需要根据模型与短文本调参）。
    """
    embs = np.array(get_embeddings(texts))
    # 使用 cosine distances；DBSCAN expects a distance matrix if metric='precomputed'
    dists = cosine_distances(embs)
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric="precomputed")
    labels = clustering.fit_predict(dists)
    return labels, embs

def canonical_label_for_cluster(texts_in_cluster, embs_in_cluster):
    """
    从簇内选代表：选择与簇中心最接近的短语作为 label。
    也可以在此处调用 LLM 将该短语润色为更友好的标签（可选）。
    """
    centroid = np.mean(embs_in_cluster, axis=0)
    # 计算距离，选最小距离项
    dists = np.linalg.norm(embs_in_cluster - centroid, axis=1)
    idx = int(np.argmin(dists))
    return texts_in_cluster[idx]

def aggregate_insights_with_clustering(group_results, eps=0.35):
    """
    group_results: list of dicts 每个dict含 audience_interest_themes / positive_content_drivers / recurring_pain_points
    返回 final_report: {top_audience_interest_themes: [(label,count),...], ...}
    """

    # 1) collect all candidate phrases with source info
    def collect(field):
        items = []
        for i, res in enumerate(group_results):
            for phrase in res.get(field, []):
                items.append({"text": phrase, "source_idx": i})
        return items

    themes = collect("audience_interest_themes")
    pos = collect("positive_content_drivers")
    pains = collect("recurring_pain_points")

    def process_collection(items):
        if not items:
            return []
        texts = [it["text"] for it in items]
        labels, embs = cluster_texts(texts, eps=eps)
        clusters = defaultdict(list)
        cluster_embs = defaultdict(list)
        cluster_sources = defaultdict(list)
        for i, lab in enumerate(labels):
            clusters[lab].append(texts[i])
            cluster_embs[lab].append(embs[i])
            cluster_sources[lab].append(items[i]["source_idx"])
        # build summary with representative label and frequency (count of unique source chunks)
        result = []
        for lab, texts_in in clusters.items():
            embs_in = np.array(cluster_embs[lab])
            label = canonical_label_for_cluster(texts_in, embs_in)
            # frequency: count how many unique chunk indices contributed to this cluster
            freq = len(set(cluster_sources[lab]))
            result.append((label, freq, texts_in))
        # sort by freq
        result.sort(key=lambda x: x[1], reverse=True)
        return result

    themes_agg = process_collection(themes)
    pos_agg = process_collection(pos)
    pains_agg = process_collection(pains)

    final_report = {
        "top_audience_interest_themes": [(t[0], t[1]) for t in themes_agg[:5]],
        "top_positive_content_drivers": [(t[0], t[1]) for t in pos_agg[:3]],
        "top_recurring_pain_points": [(t[0], t[1]) for t in pains_agg[:3]],
        # optionally include raw clusters for debugging/visualization
        "raw_clusters": {
            "themes": themes_agg,
            "positive_drivers": pos_agg,
            "pains": pains_agg
        }
    }
    return final_report
