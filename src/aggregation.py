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
    选择更长的一条显示。
    """
    texts_in_cluster = sorted(texts_in_cluster, key=len, reverse=True)
    return texts_in_cluster[0]

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

    themes = collect("content_elements")
    audience = collect("audience_identity_signals")
    pos = collect("engagement_drivers")
    pains = collect("audience_painpoints")

    def process_collection(items):
        if not items:
            return []

        cleaned_items = []
        for it in items:
            text = str(it["text"]).strip()
            if not text:
                continue
            if text.upper() in ["N/A", "NA", "NONE"]:
                continue
            if text in ["N", "/", "A"]:
                continue
            cleaned_items.append({"text": text, "source_idx": it["source_idx"]})

        if not cleaned_items:
            return []

        texts = [it["text"] for it in cleaned_items]

        labels, embs = cluster_texts(texts, eps=eps)

        clusters = defaultdict(list)
        cluster_embs = defaultdict(list)
        cluster_sources = defaultdict(list)

        for i, lab in enumerate(labels):
            clusters[lab].append(texts[i])
            cluster_embs[lab].append(embs[i])
            cluster_sources[lab].append(cleaned_items[i]["source_idx"])

        result = []
        for lab, texts_in in clusters.items():
            embs_in = np.array(cluster_embs[lab])
            label = canonical_label_for_cluster(texts_in, embs_in)
            freq = len(set(cluster_sources[lab]))
            result.append((label, freq, texts_in))

        result.sort(key=lambda x: x[1], reverse=True)
        return result


    themes_agg = process_collection(themes)
    audience_agg = process_collection(audience)
    pos_agg = process_collection(pos)
    pains_agg = process_collection(pains)

    final_report = {
        "top_content_elements": [(t[0], t[1]) for t in themes_agg[:5]] if themes_agg else None,
        "top_audience_insights": [(t[0], t[1]) for t in audience_agg[:3]] if audience_agg else None,
        "top_engagement_drivers": [(t[0], t[1]) for t in pos_agg[:3]] if pos_agg else None,
        "top_audience_pain_points": [(t[0], t[1]) for t in pains_agg[:3]] if pains_agg else None,
    }
    return final_report
