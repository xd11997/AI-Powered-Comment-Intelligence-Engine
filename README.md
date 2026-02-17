# AI-Powered Audience Insight Engine

## Overview

## Overview

This project builds a scalable AI pipeline for extracting structured insights from large-scale comment data.

The system converts unstructured user discussions into recurring, interpretable themes using LLM-based semantic abstraction and density-based clustering.

While the pipeline can operate on any comment dataset, a high-value use case is cross-video topic-level analysis within a platform, where distributed comment signals can be aggregated into audience-level intelligence.

---

## Problem

Large volumes of user comments contain valuable behavioral signals, but they are:

- Unstructured  
- Redundant  
- Difficult to aggregate systematically  

Manual review does not scale.  
Unsupervised aggregation methods can group similar expressions, but they often fail to resolve semantic noise and mixed signals within large-scale comment data.

The challenge is:

> How can we systematically extract recurring and meaningful content and audience signals from tens of thousands of comments in a robust and interpretable way?

---

## Dataset

- **Source:** Kaggle – YouTube Comments Dataset  
- **Raw Size:** ~28,000 comments  

### Preprocessing Steps
- Duplicate removal  
- Non-English comment filtering  
- Text normalization  

This ensures insights are derived from real engagement data while maintaining linguistic consistency.

---

## Methodology

### 1. Sampling & Chunking

- Comments are batched into manageable chunks  
- Chunk size is tuned to preserve contextual density  
- Processing is designed to scale across thousands of comments  

This stage ensures LLM efficiency while maintaining semantic coverage.

### 2. LLM-Based Insight Extraction (Pre-Clustering)

For each chunk:

- Extract structured insights in schema-constrained JSON format  
- Identify potential audience signals  
- Reduce noise through semantic abstraction  

This step converts unstructured comments into normalized, higher-level insight candidates.

### 3. Embedding & Clustering on Extracted Insights

- Sentence-transformer embeddings  
- DBSCAN for density-based grouping  
- Parameter exploration for stable semantic grouping  

Clustering at the insight level improves:

- Thematic coherence  
- Noise robustness  
- Interpretability  

### 4. Insight Aggregation & Ranking

Clustered insights are then:

- Deduplicated  
- Frequency-ranked  
- Organized into structured dimensions  

The final output reflects recurring audience intelligence grounded in aggregated engagement patterns.

---
## Core Design Principles

### 1. Preserve High-Resolution Semantic Signals

System design should avoid premature compression of complex user expressions.  
Processing stages must preserve semantically meaningful signals before irreversible aggregation occurs.

### 2. Ensure Bounded LLM Complexity

LLM with variable cost and stochastic behavior should operate under controlled and predictable task scopes.
Bounding workload variability supports scalable engineering, cost awareness, and consistent output behavior.

---

## Output Structure

The system generates structured audience intelligence including:

- Content Elements  
- Audience Sentiment Patterns  
- Engagement Drivers  
- Recurring Frustrations  

Each theme is grounded in clustered comment evidence.

---

## Product Demo

Below is a demonstration of the insight generation workflow:

![Product Demo](presentation/demo.png)

---

## Potential Extensions
 
- Temporal evolution of extracted insight patterns
- Multilingual clustering  
- Dashboard integration for interactive exploration  
