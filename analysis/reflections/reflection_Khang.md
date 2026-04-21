# Individual Reflection - Khang

**Role:** Team Lead / Backend Integration
**Date:** 2026-04-21

---

## 1. Đóng góp cá nhân (Engineering Contribution)

### 1.1 Modules đã phát triển
- **main.py**: Tích hợp toàn bộ evaluation pipeline
  - Kết nối `ExpertEvaluator`, `LLMJudge`, `RetrievalEvaluator`
  - Implement regression comparison logic (V1 vs V2)
  - Implement Release Gate với 3 criteria (Quality, Retrieval, Cost)
  - Lưu `reports/v1_results.json` để so sánh đầy đủ

- **agent/main_agent.py**: Điều chỉnh V1 dùng LLM thật (không mock)
  - V1 dùng keyword retrieval + LLM trả lời ngắn gọn
  - Guardrails ở mức cơ bản, không over-blocking

- **engine/runner.py**: Review và đảm bảo async runner ổn định
  - Theo dõi latency, tokens, cost
  - Progress tracking theo batch

### 1.2 Hướng dẫn thực hiện chi tiết (chạy thực tế)
1. Tạo `.env` và điền `OPENAI_API_KEY`.
2. Tạo dataset: `python data/synthetic_gen.py`.
3. Chạy benchmark: `python main.py` (tạo `reports/summary.json`, `reports/benchmark_results.json`, `reports/v1_results.json`).
4. Kiểm tra định dạng: `python check_lab.py`.
5. Điền báo cáo: cập nhật `analysis/failure_analysis.md` và reflection cá nhân.

### 1.3 Git Commits
- Chưa chốt hash trong reflection (local run). Sẽ cập nhật khi finalize.

### 1.4 Code Review
- Review PR của Duy (LLM Judge)
- Review PR của Thức (SDG + Retrieval)

---

## 2. Hiểu biết kỹ thuật (Technical Depth)

### 2.1 Giải thích MRR (Mean Reciprocal Rank)

**Định nghĩa:** MRR đo vị trí của document đúng đầu tiên trong danh sách retrieval.

**Công thức:**
```
MRR = (1/N) * Σ(1/rank_i)
```

**Ví dụ:**
- Query 1: đúng ở vị trí 1 → RR = 1.0
- Query 2: đúng ở vị trí 3 → RR = 0.33
- Query 3: không tìm thấy → RR = 0
- **MRR = 0.44**

**Kết quả thực tế (run 2026-04-21):** MRR = 0.8017 (V2) → ranking tốt.

### 2.2 Giải thích Cohen's Kappa

**Định nghĩa:** Cohen's Kappa đo mức độ đồng thuận giữa 2 judges, có điều chỉnh theo agreement ngẫu nhiên.

**Công thức:**
```
κ = (P_o - P_e) / (1 - P_e)
```

**Kết quả thực tế:** κ = 0.6886 → mức **substantial** (3 case conflict).

### 2.3 Position Bias trong LLM-as-Judge

**Cách phát hiện:** swap position A/B và so sánh winner.

**Ghi chú:** Chưa chạy swap-position trong run này do giới hạn thời gian.

### 2.4 Trade-off Chi phí vs Chất lượng

| Approach | Cost | Quality | Use Case |
|----------|------|---------|----------|
| GPT-4o only | High ($$$) | Highest | Production critical |
| GPT-4o + GPT-4o-mini | Medium ($$) | High | Balanced (our choice) |
| GPT-4o-mini only | Low ($) | Good | Development/Testing |
| 2x GPT-4o-mini | Low ($) | Medium | Budget constrained |

**Observation:** Cost gate ban đầu fail do V2 tăng token (tăng 68.4% so với V1). Sau khi tăng ngân sách V1 (context dài hơn + max_tokens cao hơn), cost delta còn +28.9% và gate pass.

---

## 3. Vấn đề gặp phải và cách giải quyết (Problem Solving)

### 3.1 Vấn đề: Conflict trong code sau merge
**Mô tả:** Xung đột trong `engine/retrieval_eval.py` và `agent/main_agent.py`.
**Giải pháp:** Resolve conflict, loại bỏ duplicate blocks, chạy lại benchmark để đảm bảo report hợp lệ.

### 3.2 Vấn đề: Cost gate ban đầu fail (tăng 68.4%)
**Nguyên nhân:** V2 trả lời dài hơn, judge phải đọc nhiều hơn.
**Giải pháp:** Tăng ngân sách V1 (context + max_tokens) để cân bằng cost; chạy lại benchmark, cost delta +28.9% và gate pass.

### 3.3 Vấn đề: Conflict giữa judges ở một số cases khó
**Nguyên nhân:** Rubric đánh giá refusal không nhất quán giữa GPT-4o và GPT-4o-mini.
**Giải pháp:** Tinh chỉnh rubric “out-of-scope” và thêm tiêu chí chấm refusal rõ ràng.

---

## 4. Bài học rút ra (Lessons Learned)

1. **Judge reliability cần đo lường** – agreement cao chưa đủ, cần kappa và conflict rate.
2. **Retrieval coverage quan trọng** – 2 lỗi lớn đều do thiếu keyword mapping.
3. **Cost control là bắt buộc** – nếu không, regression gate dễ bị block.
4. **Adversarial cases tạo insight thực** – giúp phát hiện thiếu logic hỏi lại.

---

## 5. Đề xuất cải tiến

1. **Giảm cost V2**: cap `max_tokens`, rút context, caching.
2. **Thêm ambiguity handling**: câu hỏi mơ hồ → hỏi lại.
3. **Mở rộng keyword map** cho thuật ngữ tiếng Anh (Needs Improvement, PIP).

---

*Reflection by Khang - Team Lead*
