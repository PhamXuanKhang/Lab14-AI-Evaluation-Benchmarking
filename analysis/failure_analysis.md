# Báo cáo Phân tích Thất bại (Failure Analysis Report)

**Ngày thực hiện:** 2026-04-21
**Nhóm thực hiện:** Khang, Duy, Thức, Thư

---

## 1. Tổng quan Benchmark

### 1.1 Thông tin chạy Benchmark
- **Agent Version:** Agent_V2_Optimized
- **Tổng số test cases:** 58
- **Thời gian chạy:** 85.33 giây
- **Estimated Cost:** $0.0588

### 1.2 Kết quả tổng hợp
| Metric | Giá trị |
|--------|---------|
| **Tỉ lệ Pass/Fail** | 53/5 |
| **Pass Rate** | 91.4% |
| **Điểm LLM-Judge trung bình** | 4.51 / 5.0 |
| **Agreement Rate (Multi-Judge)** | 0.95 |

### 1.3 Retrieval Metrics
| Metric | Giá trị | Đánh giá |
|--------|---------|----------|
| **Hit Rate** | 84.48% | Tốt |
| **MRR (Mean Reciprocal Rank)** | 0.8017 | Tốt |

### 1.4 RAGAS Metrics
| Metric | Giá trị |
|--------|---------|
| **Faithfulness** | 0.8930 |
| **Relevancy** | 0.9375 |

---

## 2. Phân nhóm lỗi (Failure Clustering)

### 2.1 Phân loại theo loại lỗi
| Nhóm lỗi | Số lượng | % | Nguyên nhân dự kiến |
|----------|----------|---|---------------------|
| **Hallucination** | 0 | 0.0% | Không ghi nhận trường hợp bịa thông tin khi đã có context phù hợp |
| **Incomplete Answer** | 1 | 1.7% | Câu hỏi mơ hồ, agent không hỏi lại mà tự suy đoán |
| **Wrong Retrieval** | 2 | 3.4% | Keyword map thiếu coverage, lấy sai policy |
| **Out of Scope** | 2 | 3.4% | Câu hỏi adversarial, judge đánh giá thấp dù agent đã từ chối |
| **Tone Mismatch** | 0 | 0.0% | Không có lỗi tone đáng kể |
| **Safety Violation** | 0 | 0.0% | Guardrails cơ bản hoạt động đúng |

### 2.2 Phân loại theo độ khó
| Độ khó | Tổng | Pass | Fail | Pass Rate |
|--------|------|------|------|-----------|
| Easy | 16 | 16 | 0 | 100.0% |
| Medium | 24 | 22 | 2 | 91.7% |
| Hard | 18 | 15 | 3 | 83.3% |

---

## 3. Phân tích 5 Whys (3 Case tệ nhất)

### Case #1: Wrong Retrieval - Báo cáo thiết bị bị mất/đánh cắp

**Question:** Quy trình báo cáo khi thiết bị bị mất hoặc đánh cắp là gì?

**Expected Answer:** Người sử dụng cần báo cáo ngay lập tức cho bộ phận IT trong vòng 1 giờ kể từ khi phát hiện thiết bị bị mất hoặc đánh cắp.

**Agent's Answer:** Không có thông tin trong tài liệu, đề nghị liên hệ bộ phận liên quan.

**Score:** 1.0/5.0

**5 Whys Analysis:**

| Level | Why? | Answer |
|-------|------|--------|
| **Symptom** | Agent không trả lời đúng quy trình báo cáo | Agent nói không có thông tin |
| **Why 1** | Tại sao Agent nói không có thông tin? | Context retrieved không chứa policy IT security |
| **Why 2** | Tại sao context sai? | Keyword map không bắt được cụm “thiết bị bị mất/đánh cắp” |
| **Why 3** | Tại sao keyword không cover? | Từ khóa chưa được mở rộng theo synonyms và phrase matching |
| **Why 4** | Tại sao chưa có mở rộng? | Retrieval đang dùng keyword-based đơn giản, chưa có scoring |
| **Root Cause** | Nguyên nhân gốc rễ | **Retrieval coverage yếu** (missing synonyms/phrases) |

**Proposed Fix:** Bổ sung keyword cho “mất thiết bị”, “đánh cắp”, “báo cáo sự cố”; thêm scoring theo TF-IDF nhẹ.

---

### Case #2: Wrong Retrieval - “Needs Improvement”

**Question:** Nhân viên đạt mức "Needs Improvement" sẽ gặp phải những hậu quả nào?

**Expected Answer:** Nhân viên đạt mức "Needs Improvement" sẽ không được tăng lương và sẽ phải thực hiện Performance Improvement Plan (PIP) trong 90 ngày.

**Agent's Answer:** Không có thông tin trong tài liệu.

**Score:** 1.5/5.0

**5 Whys Analysis:**

| Level | Why? | Answer |
|-------|------|--------|
| **Symptom** | Agent không nêu hậu quả của “Needs Improvement” | Agent từ chối vì thiếu thông tin |
| **Why 1** | Tại sao thiếu thông tin? | Retrieved docs không phải policy_performance |
| **Why 2** | Tại sao retrieval sai? | Từ khóa “Needs Improvement” và “PIP” chưa được map |
| **Why 3** | Tại sao thiếu keyword? | Keyword map tập trung tiếng Việt, bỏ sót thuật ngữ tiếng Anh |
| **Why 4** | Tại sao không có fallback? | Không có synonym expansion theo domain glossary |
| **Root Cause** | Nguyên nhân gốc rễ | **Keyword map thiếu thuật ngữ tiếng Anh** |

**Proposed Fix:** Thêm keywords “needs improvement”, “PIP”, “performance improvement plan” vào map; ưu tiên policy_performance khi gặp cụm “review”.

---

### Case #3: Ambiguous Query - “Quy định là bao nhiêu ngày?”

**Question:** Quy định là bao nhiêu ngày?

**Expected Answer:** Câu hỏi chưa rõ ràng. Bạn muốn hỏi về số ngày nghỉ phép, số ngày thử việc, hay quy định ngày công tác?

**Agent's Answer:** Trả lời luôn về chính sách nghỉ phép.

**Score:** 2.0/5.0

**5 Whys Analysis:**

| Level | Why? | Answer |
|-------|------|--------|
| **Symptom** | Agent tự suy đoán nội dung câu hỏi | Không hỏi làm rõ |
| **Why 1** | Tại sao không hỏi lại? | Prompt V2 chưa có rule cho câu hỏi mơ hồ |
| **Why 2** | Tại sao prompt thiếu rule? | Guardrails tập trung safety, chưa có ambiguity handling |
| **Why 3** | Tại sao không detect ambiguity? | Không có check độ đặc hiệu (length/keyword coverage) |
| **Why 4** | Tại sao chưa có check? | Chưa ưu tiên trong phiên bản hiện tại |
| **Root Cause** | Nguyên nhân gốc rễ | **Thiếu logic xử lý câu hỏi mơ hồ** |

**Proposed Fix:** Thêm rule: nếu câu hỏi ngắn và không match keyword rõ ràng → hỏi lại 1 câu để làm rõ.

---

## 4. Multi-Judge Agreement Analysis

### 4.1 Agreement Statistics
| Metric | Giá trị |
|--------|---------|
| **Overall Agreement Rate** | 0.95 |
| **Cases with Conflict (diff > 1)** | 3 / 58 (5.2%) |
| **Cohen's Kappa** | 0.6886 (substantial) |

### 4.2 Conflict Cases Analysis
| Case # | GPT-4o Score | GPT-4o-mini Score | Diff | Resolution |
|--------|--------------|-------------------|------|------------|
| 36 | 4.0 | 2.0 | 2.0 | Weighted Average (3.2) |
| 48 | 3.0 | 1.0 | 2.0 | Weighted Average (2.2) |
| 51 | 4.0 | 1.0 | 3.0 | Weighted Average (2.8) |

### 4.3 Position Bias Check
- **Has Position Bias:** Not evaluated in this run
- **Details:** Chưa chạy swap-position test do giới hạn thời gian

---

## 5. Retrieval Quality Deep Dive

### 5.1 Hit Rate Analysis
- **Perfect Retrieval (Hit Rate = 1.0):** 49 cases
- **Partial Retrieval:** 0 cases
- **Zero Retrieval (Hit Rate = 0.0):** 9 cases

### 5.2 Common Retrieval Failures
| Question Pattern | Expected Doc | Retrieved Docs | Issue |
|------------------|--------------|----------------|-------|
| “thiết bị bị mất/đánh cắp” | policy_it_security | policy_performance | Thiếu keyword liên quan sự cố thiết bị |
| “Needs Improvement / PIP” | policy_performance | policy_data_privacy, policy_onboarding | Thiếu keyword tiếng Anh |

### 5.3 Recommendations for Retrieval
1. Mở rộng keyword map với synonyms và thuật ngữ tiếng Anh trong policy.
2. Thêm scoring nhẹ (TF-IDF/BM25) để ưu tiên docs có nhiều overlap.
3. Thêm rule fallback theo doc title khi câu hỏi có từ khóa mơ hồ.

---

## 6. Kế hoạch cải tiến (Action Plan)

### 6.1 Short-term Fixes (Có thể làm ngay)
- [ ] **Keyword Map:** Bổ sung từ khóa “mất thiết bị”, “đánh cắp”, “Needs Improvement”, “PIP”.
- [ ] **Ambiguity Handling:** Nếu câu hỏi ngắn và không match rõ → hỏi lại.
- [ ] **Guardrails:** Giữ rule cơ bản, thêm log trường hợp adversarial bị judge chấm thấp.
- [ ] **Answer Length:** Giới hạn độ dài để kiểm soát cost.

### 6.2 Medium-term Improvements (1-2 tuần)
- [ ] **Hybrid Retrieval:** Keyword + BM25 để tăng coverage mà không cần embedding.
- [ ] **Judge Calibration:** Fine-tune rubric cho adversarial/out-of-scope để giảm conflict.

### 6.3 Long-term Enhancements (1+ tháng)
- [ ] **ChromaDB** (nếu có thời gian): Vector search + rerank nhẹ.
- [ ] **Continuous Evaluation:** Lập cron chạy benchmark định kỳ và alert khi score drop.

---

## 7. Cost-Quality Trade-off Analysis

### 7.1 Current Costs (ước tính theo tổng token)
| Component | Tokens | Est. Cost |
|-----------|--------|-----------|
| Agent (GPT-4o-mini) | 91,087 | $0.0364 |
| Judge (GPT-4o + GPT-4o-mini) | 55,932 | $0.0224 |
| **Total** | 147,019 | $0.0588 |

### 7.2 Optimization Opportunities
| Strategy | Potential Savings | Quality Impact |
|----------|-------------------|----------------|
| Cap max_tokens (V2) | 10-20% | Low-Medium |
| Shorter context (top-2) | 10-15% | Low |
| Judge easy cases 1-model | 15-25% | Medium |
| Cache repeated queries | 20-30% | None |

---

## 8. Conclusion

### 8.1 Key Findings
1. Retrieval đã ổn định (Hit Rate 84.48%, MRR 0.8017) nhưng vẫn có 2 lỗi do thiếu keyword coverage.
2. Multi-judge có agreement cao (0.95) với kappa ở mức substantial (0.6886) và có 3 conflict cases.
3. Hard questions vẫn là điểm yếu (pass 83.3%), đặc biệt với câu hỏi mơ hồ.

### 8.2 Priority Actions
1. **Highest Priority:** Bổ sung keyword coverage cho policy_it_security và policy_performance.
2. **High Priority:** Thêm logic hỏi lại cho câu hỏi mơ hồ.
3. **Medium Priority:** Tinh chỉnh rubric/judge cho out-of-scope để giảm conflict.

### 8.3 Success Metrics for Next Iteration
| Metric | Current | Target |
|--------|---------|--------|
| Pass Rate | 91.4% | 93.0% |
| Hit Rate | 84.48% | 88.0% |
| Avg Score | 4.51 | 4.60 |
| Cost per Eval | $0.001014 | $0.0009 |

---

*Report generated by AI Evaluation Factory - Lab Day 14*
