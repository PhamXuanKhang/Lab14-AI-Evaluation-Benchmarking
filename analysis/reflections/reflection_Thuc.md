# Individual Reflection - Thức

**Role:** Data Engineer - SDG & Retrieval Evaluation
**Date:** 2026-04-21

---

## 1. Đóng góp cá nhân (Engineering Contribution)

### 1.1 Modules đã phát triển

#### data/synthetic_gen.py
- **Sample Corpus Creation**: Tạo 8 documents về AI/ML topics
- **generate_qa_from_text()**: Gọi GPT-4o-mini để sinh QA pairs
- **generate_adversarial_cases()**: 10 hard cases (prompt injection, out-of-context, etc.)
- **Main pipeline**: Orchestrate SDG để tạo 50+ test cases

#### engine/retrieval_eval.py
- **calculate_hit_rate()**: Hit Rate calculation với top-k
- **calculate_mrr()**: Mean Reciprocal Rank calculation
- **calculate_precision_at_k()**: Precision@K metric
- **calculate_recall_at_k()**: Recall@K metric
- **evaluate_batch()**: Batch evaluation với detailed results
- **get_failure_analysis()**: Automatic failure analysis và recommendations

#### agent/main_agent.py
- Cập nhật để trả về `retrieved_ids` field
- Implement keyword-based retrieval simulation

### 1.2 Dataset Statistics
| Category | Count |
|----------|-------|
| Total Cases | 58 |
| Normal Cases | 48 |
| Adversarial Cases | 10 |
| Documents in Corpus | 8 |

### 1.3 Git Commits
```
- "feat: Implement SDG with OpenAI API"
- "feat: Add 10 adversarial test cases"
- "feat: Implement retrieval metrics (Hit Rate, MRR, P@K, R@K)"
- "feat: Add failure analysis with recommendations"
```

---

## 2. Hiểu biết kỹ thuật (Technical Depth)

### 2.1 Retrieval Metrics Explained

#### Hit Rate (Binary Relevance)
```
Hit Rate = (# queries with at least 1 relevant doc in top-k) / (# total queries)
```

**Example:**
| Query | Expected | Retrieved (top-3) | Hit? |
|-------|----------|-------------------|------|
| Q1 | [doc_1] | [doc_1, doc_2, doc_3] | ✓ |
| Q2 | [doc_5] | [doc_2, doc_3, doc_4] | ✗ |
| Q3 | [doc_3] | [doc_1, doc_3, doc_5] | ✓ |

**Hit Rate = 2/3 = 0.67**

#### MRR (Mean Reciprocal Rank)
```
MRR = (1/N) * Σ(1/rank_i)
```

**Same example:**
| Query | First Relevant Position | Reciprocal Rank |
|-------|-------------------------|-----------------|
| Q1 | 1 | 1/1 = 1.0 |
| Q2 | Not found | 0 |
| Q3 | 2 | 1/2 = 0.5 |

**MRR = (1.0 + 0 + 0.5) / 3 = 0.5**

### 2.2 Hit Rate vs MRR Trade-offs

| Metric | Measures | Best For |
|--------|----------|----------|
| Hit Rate | "Did we find it?" | Coverage analysis |
| MRR | "How fast did we find it?" | Ranking quality |
| Precision@K | "How many correct in top-k?" | Precision-focused apps |
| Recall@K | "What % of relevant did we get?" | Recall-focused apps |

### 2.3 Synthetic Data Generation Pipeline

```
┌─────────────────┐
│  Source Corpus  │
│  (8 documents)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Chunking       │
│  (by document)  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  LLM Generation (GPT-4o-mini)   │
│  - Generate 6 QA per document   │
│  - Include difficulty levels    │
│  - Include question types       │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Ground Truth Assignment        │
│  - Map expected_retrieval_ids   │
│  - Add metadata                 │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Adversarial Augmentation       │
│  - Prompt injection (2 cases)   │
│  - Out-of-context (3 cases)     │
│  - Ambiguous (1 case)           │
│  - Conflicting info (1 case)    │
│  - Security (3 cases)           │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────┐
│  golden_set.jsonl │
│  (58 cases)       │
└───────────────────┘
```

### 2.4 Adversarial Test Case Design

| Type | Purpose | Detection Method |
|------|---------|------------------|
| Prompt Injection | Test guardrails | Check if agent follows malicious instruction |
| Out-of-Context | Test "I don't know" | Check if agent admits lack of knowledge |
| Ambiguous | Test clarification | Check if agent asks for clarification |
| Conflicting | Test reasoning | Check if agent handles contradictions |
| Security | Test data protection | Check if agent refuses sensitive requests |

---

## 3. Vấn đề gặp phải và cách giải quyết

### 3.1 Vấn đề: LLM sinh QA không đúng format

**Mô tả:** GPT đôi khi trả về text thay vì JSON array.

**Giải pháp:**
- Explicit instruction: "Chỉ trả về JSON, không có text khác"
- Post-processing để clean markdown
- Fallback với hardcoded placeholder nếu parsing fails

### 3.2 Vấn đề: Ground truth ID mapping

**Mô tả:** Làm sao biết expected_retrieval_ids nào đúng?

**Giải pháp:**
- Generate QA từ specific document → expected_id = document's id
- Manually verify một số cases
- Add metadata về source document

### 3.3 Vấn đề: Adversarial cases quá dễ hoặc quá khó

**Mô tả:** Cần balance để có meaningful evaluation.

**Giải pháp:**
- Design cases theo HARD_CASES_GUIDE.md
- Include variety: security, out-of-scope, ambiguous
- Test trước khi chạy full benchmark

---

## 4. Bài học rút ra

1. **Quality of ground truth = quality of evaluation** - Nếu expected_answer sai, evaluation vô nghĩa.

2. **Retrieval metrics cần ground truth IDs** - Không thể đánh giá retrieval mà không biết docs nào đúng.

3. **Adversarial testing reveals weaknesses** - Normal cases cho scores cao, adversarial cho insight.

4. **Synthetic data != real data** - SDG tiện lợi nhưng cần validate với real user queries.

---

## 5. Đề xuất cải tiến

1. **Thêm human validation** cho một số QA pairs.

2. **Diversify adversarial cases** - Thêm multi-turn, context carry-over.

3. **Implement automated ground truth generation** từ production logs.

4. **Add negative sampling** cho retrieval evaluation (hard negatives).

---

*Reflection by Thức - Data Engineer*
