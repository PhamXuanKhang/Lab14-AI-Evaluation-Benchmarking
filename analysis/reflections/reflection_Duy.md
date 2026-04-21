# Individual Reflection - Duy

**Role:** AI Engineer - Multi-Judge Consensus Engine
**Date:** 2026-04-21

---

## 1. Đóng góp cá nhân (Engineering Contribution)

### 1.1 Modules đã phát triển
- **engine/llm_judge.py**: Implement Multi-Judge Consensus Engine
  - `_call_single_judge()`: Gọi individual LLM judge với rubric
  - `evaluate_multi_judge()`: Orchestrate 2 judges (GPT-4o + GPT-4o-mini)
  - `check_position_bias()`: Phát hiện position bias
  - `calculate_cohens_kappa()`: Tính inter-rater agreement
  - `evaluate_all_criteria()`: Evaluate trên 3 criteria (accuracy, professionalism, safety)

### 1.2 Rubrics Design
Thiết kế chi tiết rubrics cho 3 criteria:
- **Accuracy (50% weight)**: 5-point scale dựa trên factual correctness
- **Professionalism (30% weight)**: Đánh giá clarity và structure
- **Safety (20% weight)**: Kiểm tra harmful content và appropriate responses

### 1.3 Conflict Resolution Logic
Implement weighted average strategy:
- GPT-4o weight: 0.6 (model mạnh hơn)
- GPT-4o-mini weight: 0.4
- Trigger khi score difference > 1.0

### 1.4 Git Commits
```
[Liệt kê các commits]
- "feat: Implement multi-judge evaluation with 2 OpenAI models"
- "feat: Add position bias detection"
- "feat: Add Cohen's Kappa calculation"
- "fix: Handle JSON parsing errors from LLM responses"
```

---

## 2. Hiểu biết kỹ thuật (Technical Depth)

### 2.1 LLM-as-Judge Architecture

```
                    ┌─────────────────┐
                    │   Test Case     │
                    │ (Q, A, GT)      │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                              ▼
    ┌─────────────────┐            ┌─────────────────┐
    │   GPT-4o        │            │  GPT-4o-mini    │
    │   Judge         │            │  Judge          │
    │   (weight=0.6)  │            │  (weight=0.4)   │
    └────────┬────────┘            └────────┬────────┘
             │                              │
             │  Score: 4.0                  │  Score: 3.5
             │                              │
             └──────────────┬───────────────┘
                            ▼
                   ┌─────────────────┐
                   │ Consensus Logic │
                   │ diff = |4-3.5|  │
                   │ = 0.5 < 1.0     │
                   │ → No conflict   │
                   └────────┬────────┘
                            │
                            ▼
                   Final Score: 3.75
                   Agreement: 0.875
```

### 2.2 Tại sao cần Multi-Judge?

| Single Judge | Multi-Judge |
|--------------|-------------|
| Bias của 1 model | Balanced perspectives |
| Không có validation | Cross-validation |
| Single point of failure | Redundancy |
| Không đo agreement | Agreement metrics |

### 2.3 Position Bias Deep Dive

**Experiment Design:**
```python
# Test 1: A first, B second
result_ab = judge("Which is better?", response_a, response_b)

# Test 2: B first, A second (swap positions)
result_ba = judge("Which is better?", response_b, response_a)

# Analysis
if result_ab.winner == "A" and result_ba.winner == "A":
    # Consistent - A always wins regardless of position
    has_bias = False
elif result_ab.winner == "A" and result_ba.winner == "A":
    # Wait, this means position matters!
    # In test 2, original B is now in A position
    has_bias = True
```

**Findings từ lab:** Agreement Rate 0.95, Cohen's Kappa 0.6886 (substantial), 3 conflict cases (3/58). Position bias chưa chạy trong lần benchmark này.

### 2.4 Agreement Metrics Comparison

| Metric | Pros | Cons |
|--------|------|------|
| Simple Agreement | Easy to compute | Doesn't account for chance |
| Cohen's Kappa | Chance-corrected | Only for 2 raters |
| Fleiss' Kappa | Multi-rater | More complex |
| Krippendorff's Alpha | Most robust | Computationally expensive |

---

## 3. Vấn đề gặp phải và cách giải quyết

### 3.1 Vấn đề: Inconsistent JSON output từ LLM

**Mô tả:** GPT đôi khi trả về:
```
Here's my evaluation:
```json
{"score": 4, "reasoning": "..."}
```
```

**Giải pháp:**
```python
# Clean markdown artifacts
content = response.choices[0].message.content.strip()
for prefix in ["```json", "```"]:
    if content.startswith(prefix):
        content = content[len(prefix):]
for suffix in ["```"]:
    if content.endswith(suffix):
        content = content[:-len(suffix)]
```

### 3.2 Vấn đề: Temperature setting cho Judge

**Mô tả:** Temperature cao → inconsistent scores
**Giải pháp:** Set temperature=0.0 cho deterministic evaluation

### 3.3 Vấn đề: Rubric interpretation khác nhau giữa models

**Mô tả:** GPT-4o và GPT-4o-mini interpret "score 3" khác nhau
**Giải pháp:** 
- Detailed rubric với examples
- Calibration qua test set nhỏ

---

## 4. Bài học rút ra

1. **Prompt engineering cho judges quan trọng** - Rubric rõ ràng = scores consistent hơn.

2. **Multi-judge không chỉ về reliability** - Còn giúp identify cases khó (high disagreement).

3. **Position bias là real problem** - Đặc biệt với weaker models.

4. **Error handling cần thorough** - LLM output không predictable 100%.

---

## 5. Đề xuất cải tiến

1. **Thêm Claude làm judge thứ 3** cho diversity (nếu có API key).

2. **Implement self-consistency** - Chạy cùng query nhiều lần, vote majority.

3. **Fine-tune rubrics** dựa trên failure analysis.

4. **Add confidence scores** từ judges (không chỉ final score).

---

*Reflection by Duy - AI Engineer*
