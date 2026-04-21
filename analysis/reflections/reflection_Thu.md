# Individual Reflection - Thư

**Role:** QA / Analyst - Testing & Failure Analysis
**Date:** 2026-04-21
**MSSV:** 2A202600210
---

## 1. Đóng góp cá nhân (Engineering Contribution)

### 1.1 Responsibilities

#### Testing & Validation
- Chạy `check_lab.py` và verify output format
- Test end-to-end pipeline (SDG → Benchmark → Reports)
- Verify reports/summary.json có đầy đủ required fields
- Validate benchmark_results.json structure

#### Failure Analysis
- Điền số liệu thực vào `analysis/failure_analysis.md`
- Phân loại failures theo categories
- Thực hiện phân tích 5 Whys cho 3 worst cases
- Đề xuất Action Plan

#### Documentation
- Tổng hợp reflection files từ team members
- Review và format final documentation

### 1.2 Analysis Outputs
| Deliverable | Status |
|-------------|--------|
| failure_analysis.md | [Completed] |
| Failure categorization | [Completed] |
| 5 Whys for 3 cases | [Completed] |
| Action Plan | [Completed] |
| Cost analysis | [Completed] |

### 1.3 Git Commits
```
- "docs: Fill in failure_analysis.md with benchmark results"
- "docs: Add 5 Whys analysis for worst cases"
- "docs: Complete action plan with priorities"
```

---

## 2. Hiểu biết kỹ thuật (Technical Depth)

### 2.1 5 Whys Methodology

**Purpose:** Identify root cause, not just symptoms.

**Process:**
```
Symptom → Why? → Cause 1 → Why? → Cause 2 → ... → Root Cause
```

**Example from our lab:**
```
Symptom: Agent hallucinated về FAISS
    ↓ Why?
Cause 1: LLM không có correct context
    ↓ Why?
Cause 2: Vector search returned wrong documents
    ↓ Why?
Cause 3: Query embedding didn't match document embedding
    ↓ Why?
Cause 4: Chunking broke up the relevant information
    ↓ Why?
ROOT CAUSE: Fixed-size chunking (512 tokens) cut important paragraphs
```

### 2.2 Failure Categorization Framework

| Category | Description | Common Causes | Fix Priority |
|----------|-------------|---------------|--------------|
| Hallucination | Agent invents information | Bad retrieval, missing guardrails | High |
| Incomplete | Answer lacks detail | Short context, vague prompt | Medium |
| Wrong Retrieval | Got wrong docs | Embedding mismatch, poor chunking | High |
| Out of Scope | Should say "I don't know" | Missing topic boundaries | Medium |
| Tone Mismatch | Wrong communication style | System prompt issues | Low |
| Safety Violation | Should refuse but didn't | Weak guardrails | Critical |

### 2.3 Root Cause Categories

```
┌─────────────────────────────────────────────────────────┐
│                    RAG Pipeline                          │
├──────────┬──────────┬──────────┬──────────┬────────────┤
│ Ingestion│ Chunking │ Retrieval│ Prompting│ Generation │
├──────────┼──────────┼──────────┼──────────┼────────────┤
│ - Parser │ - Size   │ - Top-k  │ - System │ - Model    │
│   errors │ - Overlap│ - Embed  │   prompt │ - Temp     │
│ - Format │ - Strategy│ - Index │ - Few-shot│ - Max_tok │
│ - Missing│          │ - Ranking│          │ - Context  │
│   docs   │          │          │          │            │
└──────────┴──────────┴──────────┴──────────┴────────────┘
```

### 2.4 Quality Gates in Production

| Gate | Metric | Threshold | Action if Fail |
|------|--------|-----------|----------------|
| Retrieval | Hit Rate | ≥ 80% | Block release |
| Quality | Avg Score | ≥ 3.5/5 | Block release |
| Agreement | Agreement Rate | ≥ 0.7 | Review flagged cases |
| Cost | $ per query | ≤ $0.01 | Optimize before release |
| Latency | P95 latency | ≤ 2s | Performance tuning |

---

## 3. Vấn đề gặp phải và cách giải quyết

### 3.1 Vấn đề: Khó xác định root cause từ benchmark data

**Mô tả:** Benchmark results cho scores nhưng không explain tại sao.

**Giải pháp:**
- Add detailed logging trong runner
- Include retrieved_ids và expected_ids trong results
- Compare contexts để understand retrieval failures

### 3.2 Vấn đề: Too many failures to analyze

**Mô tả:** 20+ failed cases, không thể analyze hết.

**Giải pháp:**
- Prioritize by score (lowest first)
- Group by failure type
- Sample representative cases per category
- Focus on 3 worst for deep 5 Whys

### 3.3 Vấn đề: Action items không actionable

**Mô tả:** "Improve chunking" quá vague.

**Giải pháp:**
- Be specific: "Change from fixed-size 512 to semantic chunking"
- Include success criteria: "Target Hit Rate ≥ 85%"
- Assign owner and timeline

---

## 4. Bài học rút ra

1. **5 Whys cần depth** - Dừng ở "retrieval failed" không đủ. Phải đi đến chunking, embedding, etc.

2. **Categorization giúp prioritize** - Không thể fix tất cả. Focus on high-impact categories.

3. **Metrics tell story** - Hit Rate + MRR + Agreement Rate cùng nhau cho picture đầy đủ.

4. **Testing early saves time** - Chạy check_lab.py sớm để catch format issues.

---

## 5. Failure Analysis Summary

### 5.1 Key Findings
1. **Retrieval coverage**: Hit Rate 84.48% và có 2 lỗi do thiếu keyword coverage.
2. **Multi-judge reliability**: Agreement 0.95, Cohen's Kappa 0.6886, có 3 conflict cases.
3. **Hard cases yếu hơn**: Pass Rate nhóm hard 83.3%, đặc biệt câu hỏi mơ hồ.

### 5.2 Top Recommendations
1. **Mở rộng keyword map** cho policy_it_security và policy_performance.
2. **Thêm ambiguity handling**: câu hỏi ngắn/không match rõ → hỏi lại.
3. **Tinh chỉnh rubric out-of-scope** để giảm conflict giữa judges.

### 5.3 Next Iteration Targets
| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| Pass Rate | 91.4% | 93.0% | +1.6% |
| Hit Rate | 84.48% | 88.0% | +3.52% |
| Avg Score | 4.51 | 4.60 | +0.09 |

---

## 6. Đề xuất cải tiến

1. **Automate failure categorization** - Train classifier để auto-label failures.

2. **Build failure dashboard** - Visualize trends over time.

3. **Implement regression alerts** - Notify when metrics drop below threshold.

4. **Add tracing** - Link each eval to specific retrieval + generation calls.

---

*Reflection by Thư - QA/Analyst*
