"""
Shared knowledge base used by BOTH synthetic_gen.py (for QA generation)
and agent/main_agent.py (for retrieval simulation).
Keeping both in sync ensures expected_retrieval_ids actually match
what the agent can retrieve.
"""

KNOWLEDGE_BASE = [
    {
        "doc_id": "policy_it_security",
        "title": "Chính sách Bảo mật Công nghệ Thông tin",
        "content": """
Chính sách Bảo mật Công nghệ Thông tin - VinTech Company

1. MỤC ĐÍCH
Chính sách này quy định các yêu cầu bảo mật CNTT nhằm bảo vệ tài sản thông tin của công ty khỏi các rủi ro như truy cập trái phép, rò rỉ dữ liệu và tấn công mạng.

2. QUẢN LÝ MẬT KHẨU
- Mật khẩu phải có ít nhất 12 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt.
- Mật khẩu phải được thay đổi 90 ngày một lần.
- Không được chia sẻ mật khẩu với bất kỳ ai, kể cả cấp trên hay bộ phận IT.
- Sử dụng trình quản lý mật khẩu được công ty phê duyệt (LastPass Enterprise).
- Bật xác thực hai yếu tố (2FA) bắt buộc cho tất cả tài khoản công ty.

3. SỬ DỤNG THIẾT BỊ
- Chỉ sử dụng thiết bị được công ty phê duyệt để truy cập hệ thống nội bộ.
- Không cài đặt phần mềm không được phép lên thiết bị công ty.
- Kích hoạt mã hóa ổ đĩa (BitLocker/FileVault) trên tất cả laptop.
- Báo cáo ngay lập tức nếu thiết bị bị mất hoặc đánh cắp cho bộ phận IT trong vòng 1 giờ.
- Khóa màn hình khi rời khỏi máy tính, kể cả trong thời gian ngắn.

4. SỬ DỤNG MẠNG
- Không kết nối vào mạng Wi-Fi công cộng khi làm việc với dữ liệu nhạy cảm.
- Sử dụng VPN công ty khi làm việc từ xa hoặc mạng không tin cậy.
- Báo cáo ngay các hoạt động mạng đáng ngờ cho bộ phận IT.
- Không sử dụng phần mềm chia sẻ file P2P trên mạng công ty.

5. XỬ LÝ DỮ LIỆU
- Dữ liệu khách hàng được phân loại là "Bí mật" và không được lưu trên thiết bị cá nhân.
- Chỉ chia sẻ dữ liệu nội bộ qua các kênh được phê duyệt (Google Workspace, SharePoint).
- Xóa dữ liệu nhạy cảm khỏi email sau khi xử lý xong.
- Mã hóa tất cả file chứa dữ liệu cá nhân trước khi gửi qua email.

6. VI PHẠM VÀ HẬU QUẢ
Vi phạm chính sách bảo mật có thể dẫn đến kỷ luật từ cảnh cáo đến chấm dứt hợp đồng tùy mức độ nghiêm trọng. Vi phạm gây thiệt hại cho công ty có thể bị xử lý theo pháp luật.
        """.strip()
    },
    {
        "doc_id": "policy_remote_work",
        "title": "Chính sách Làm việc Từ xa",
        "content": """
Chính sách Làm việc Từ xa (Remote Work Policy) - VinTech Company

1. ĐIỀU KIỆN ĐƯỢC PHÉP LÀM VIỆC TỪ XA
- Nhân viên đã qua thời gian thử việc 3 tháng.
- Đánh giá hiệu suất 6 tháng gần nhất đạt mức "Đáp ứng kỳ vọng" trở lên.
- Có không gian làm việc riêng, yên tĩnh tại nhà với kết nối internet ổn định (tối thiểu 20 Mbps).
- Được quản lý trực tiếp phê duyệt bằng văn bản.

2. SỐ NGÀY LÀM VIỆC TỪ XA
- Nhân viên cấp Staff: tối đa 2 ngày/tuần.
- Nhân viên cấp Senior/Lead: tối đa 3 ngày/tuần.
- Nhân viên cấp Manager trở lên: linh hoạt theo thỏa thuận với cấp trên.
- Toàn bộ nhân viên phải có mặt tại văn phòng ít nhất 2 ngày/tuần (thường là thứ Ba và thứ Năm).

3. GIỜ LÀM VIỆC VÀ TÍNH SẴN SÀNG
- Duy trì giờ làm việc cốt lõi từ 9:00 - 17:00 (theo giờ Việt Nam).
- Phản hồi email/Slack trong vòng 30 phút trong giờ làm việc cốt lõi.
- Bật camera trong tất cả các cuộc họp video.
- Cập nhật trạng thái trên Slack trong suốt giờ làm việc.

4. THIẾT BỊ VÀ HỖ TRỢ KỸ THUẬT
- Công ty cung cấp laptop và màn hình thứ hai cho nhân viên làm việc từ xa thường xuyên.
- Hỗ trợ chi phí internet tối đa 300.000 VNĐ/tháng sau khi nộp hóa đơn.
- Bộ phận IT hỗ trợ từ xa qua Zoom từ 8:00 - 20:00 các ngày làm việc.
- Nhân viên tự chịu trách nhiệm đảm bảo môi trường làm việc an toàn và ergonomic.

5. BẢO MẬT KHI LÀM VIỆC TỪ XA
- Bắt buộc sử dụng VPN công ty khi truy cập hệ thống nội bộ.
- Không làm việc tại quán cà phê hay nơi công cộng khi xử lý thông tin mật.
- Không để người khác nhìn vào màn hình khi làm việc với dữ liệu nhạy cảm.

6. ĐÁNH GIÁ VÀ THU HỒI QUYỀN LÀM VIỆC TỪ XA
Quyền làm việc từ xa có thể bị thu hồi nếu hiệu suất giảm sút hoặc vi phạm chính sách. Đánh giá lại mỗi 6 tháng.
        """.strip()
    },
    {
        "doc_id": "policy_leave",
        "title": "Chính sách Nghỉ phép và Nghỉ lễ",
        "content": """
Chính sách Nghỉ phép và Nghỉ lễ - VinTech Company

1. NGHỈ PHÉP NĂM
- Nhân viên dưới 1 năm: 12 ngày phép/năm (1 ngày/tháng, tính từ tháng thứ 6).
- Nhân viên từ 1-3 năm: 14 ngày phép/năm.
- Nhân viên từ 3-5 năm: 16 ngày phép/năm.
- Nhân viên trên 5 năm: 18 ngày phép/năm.
- Phép năm không dùng hết có thể chuyển sang năm sau tối đa 5 ngày, phần còn lại sẽ mất.

2. NGHỈ LỄ QUỐC GIA
Nhân viên được nghỉ đủ các ngày lễ quốc gia theo quy định của Bộ Luật Lao động Việt Nam, bao gồm: Tết Dương lịch, Tết Nguyên đán (5 ngày), Giỗ Tổ Hùng Vương, Ngày Giải phóng miền Nam, Ngày Quốc tế Lao động, và Ngày Quốc khánh.

3. NGHỈ BỆNH
- 10 ngày nghỉ bệnh có lương mỗi năm, không cần giấy tờ y tế cho 1-2 ngày liên tiếp.
- Nghỉ bệnh từ 3 ngày trở lên phải nộp giấy xác nhận của cơ sở y tế trong vòng 5 ngày làm việc.
- Nghỉ bệnh không sử dụng hết không được chuyển sang năm sau và không được quy đổi thành tiền.

4. NGHỈ THAI SẢN
- Lao động nữ: 6 tháng nghỉ thai sản theo Luật Bảo hiểm xã hội, hưởng 100% lương bình quân 6 tháng đóng BHXH.
- Lao động nam: 5-14 ngày nghỉ sinh con có hưởng BHXH tùy số con và phương thức sinh.
- Công ty bổ sung thêm 1 tháng hỗ trợ sau nghỉ thai sản cho nhân viên có thâm niên từ 2 năm trở lên.

5. NGHỈ KHẨN CẤP VÀ SỰ KIỆN GIA ĐÌNH
- Đám cưới bản thân: 3 ngày có lương.
- Đám cưới con: 1 ngày có lương.
- Tang cha mẹ, vợ/chồng, con: 3 ngày có lương.
- Tang ông bà, anh chị em ruột: 1 ngày có lương.

6. QUY TRÌNH XIN PHÉP
- Nghỉ phép thông thường: nộp đơn trên hệ thống HR trước ít nhất 3 ngày làm việc.
- Nghỉ từ 5 ngày trở lên: nộp trước 2 tuần và cần phê duyệt của quản lý cấp 2.
- Nghỉ khẩn cấp: thông báo cho quản lý trực tiếp qua điện thoại/nhắn tin trước 8:30 sáng ngày nghỉ.
        """.strip()
    },
    {
        "doc_id": "policy_data_privacy",
        "title": "Chính sách Bảo vệ Dữ liệu Cá nhân",
        "content": """
Chính sách Bảo vệ Dữ liệu Cá nhân (PDPA Compliance) - VinTech Company

1. PHẠM VI ÁP DỤNG
Chính sách này áp dụng cho tất cả nhân viên, nhà thầu và đối tác xử lý dữ liệu cá nhân của khách hàng, nhân viên hoặc đối tác kinh doanh của VinTech Company.

2. PHÂN LOẠI DỮ LIỆU CÁ NHÂN
- Thông tin nhận dạng: họ tên, ngày sinh, CMND/CCCD, địa chỉ, số điện thoại, email.
- Dữ liệu tài chính: tài khoản ngân hàng, lịch sử giao dịch, thông tin tín dụng.
- Dữ liệu nhạy cảm: tình trạng sức khỏe, dữ liệu sinh trắc học, quan điểm chính trị.
- Dữ liệu hành vi: lịch sử duyệt web, dữ liệu vị trí, thói quen sử dụng.

3. NGUYÊN TẮC XỬ LÝ DỮ LIỆU
- Chỉ thu thập dữ liệu cần thiết cho mục đích đã xác định (Data Minimization).
- Phải có cơ sở pháp lý hợp lệ: đồng ý, hợp đồng, nghĩa vụ pháp lý hoặc lợi ích hợp pháp.
- Thông báo rõ ràng cho chủ thể dữ liệu về mục đích và cách thức xử lý.
- Không chia sẻ dữ liệu cá nhân với bên thứ ba khi chưa có sự đồng ý hoặc cơ sở pháp lý.

4. QUYỀN CỦA CHỦ THỂ DỮ LIỆU
- Quyền truy cập: được xem dữ liệu cá nhân của mình đang được lưu trữ.
- Quyền chỉnh sửa: yêu cầu sửa đổi dữ liệu không chính xác.
- Quyền xóa: yêu cầu xóa dữ liệu trong một số trường hợp nhất định.
- Quyền phản đối: từ chối việc xử lý dữ liệu cho mục đích tiếp thị.
- Phản hồi các yêu cầu trong vòng 30 ngày làm việc.

5. BẢO MẬT DỮ LIỆU
- Mã hóa tất cả dữ liệu cá nhân khi lưu trữ (AES-256) và truyền tải (TLS 1.3).
- Kiểm soát truy cập theo nguyên tắc đặc quyền tối thiểu (Least Privilege).
- Lưu nhật ký truy cập vào hệ thống chứa dữ liệu cá nhân tối thiểu 1 năm.
- Thực hiện đánh giá tác động bảo vệ dữ liệu (DPIA) trước các dự án mới.

6. SỰ CỐ RÒ RỈ DỮ LIỆU
Trong trường hợp rò rỉ dữ liệu, phải thông báo cho bộ phận DPO trong vòng 24 giờ. Thông báo cho cơ quan quản lý trong vòng 72 giờ nếu có nguy cơ ảnh hưởng đến chủ thể dữ liệu.
        """.strip()
    },
    {
        "doc_id": "policy_ai_usage",
        "title": "Chính sách Sử dụng Công cụ AI",
        "content": """
Chính sách Sử dụng Công cụ Trí tuệ Nhân tạo (AI) - VinTech Company

1. MỤC ĐÍCH
Chính sách này hướng dẫn việc sử dụng các công cụ AI (ChatGPT, Copilot, Gemini, Claude, v.v.) một cách có trách nhiệm và hiệu quả trong môi trường làm việc.

2. CÔNG CỤ AI ĐƯỢC PHÊ DUYỆT
- ChatGPT Enterprise (có gói bảo mật dữ liệu): được dùng cho tất cả bộ phận.
- Microsoft 365 Copilot: được dùng cho bộ phận kỹ thuật và quản lý.
- GitHub Copilot: được dùng cho bộ phận Engineering.
- Công cụ khác phải được bộ phận IT và Bảo mật phê duyệt trước khi sử dụng.

3. NHỮNG GÌ ĐƯỢC PHÉP
- Soạn thảo email, báo cáo, tài liệu không chứa thông tin mật.
- Viết và review code cho các dự án nội bộ không liên quan đến dữ liệu khách hàng.
- Tóm tắt tài liệu công khai, nghiên cứu thị trường.
- Dịch thuật tài liệu không chứa thông tin bí mật kinh doanh.
- Brainstorming ý tưởng sản phẩm, marketing.

4. NHỮNG GÌ KHÔNG ĐƯỢC PHÉP
- Nhập dữ liệu cá nhân của khách hàng (tên, email, số điện thoại, v.v.) vào bất kỳ công cụ AI nào.
- Chia sẻ mã nguồn proprietary, bí quyết kinh doanh hoặc chiến lược công ty chưa công bố.
- Nhập thông tin tài chính nội bộ, kế hoạch M&A hoặc thông tin nhạy cảm về nhân sự.
- Sử dụng AI để tạo nội dung gây hiểu lầm hoặc vi phạm bản quyền.
- Sử dụng AI để thay thế hoàn toàn quá trình đánh giá của con người trong quyết định quan trọng.

5. TRÁCH NHIỆM KHI SỬ DỤNG AI
- Luôn xem xét và kiểm tra kỹ lưỡng output của AI trước khi sử dụng.
- Ghi rõ "Được hỗ trợ bởi AI" trong tài liệu quan trọng được tạo với sự hỗ trợ đáng kể của AI.
- Không dựa hoàn toàn vào AI cho các quyết định có ảnh hưởng đến con người.
- Báo cáo ngay các sự cố liên quan đến AI (output có hại, rò rỉ dữ liệu) cho bộ phận IT.

6. ĐÀO TẠO VÀ TUÂN THỦ
Tất cả nhân viên phải hoàn thành khóa đào tạo "AI Responsible Use" trực tuyến trong vòng 30 ngày kể từ ngày ban hành chính sách hoặc ngày onboarding.
        """.strip()
    },
    {
        "doc_id": "policy_performance",
        "title": "Chính sách Đánh giá Hiệu suất",
        "content": """
Chính sách Đánh giá Hiệu suất (Performance Review Policy) - VinTech Company

1. CHU KỲ ĐÁNH GIÁ
- Đánh giá giữa năm (Mid-year Review): tháng 6-7, mang tính định hướng và phản hồi.
- Đánh giá cuối năm (Annual Review): tháng 11-12, quyết định thăng tiến và điều chỉnh lương.
- Đánh giá thử việc: cuối tháng thứ 3 để quyết định chính thức hóa hợp đồng.

2. CÁC MỨC ĐÁNH GIÁ
- Exceptional (5): Vượt xa mong đợi, đóng góp đặc biệt cho công ty (dưới 5% nhân viên).
- Exceeds Expectations (4): Thường xuyên vượt KPI và tiêu chuẩn đề ra.
- Meets Expectations (3): Đáp ứng đầy đủ và ổn định các yêu cầu công việc.
- Needs Improvement (2): Chưa đáp ứng một số tiêu chí quan trọng, cần có kế hoạch cải thiện.
- Unsatisfactory (1): Không đáp ứng yêu cầu công việc, có nguy cơ chấm dứt hợp đồng.

3. TIÊU CHÍ ĐÁNH GIÁ
- KPI và kết quả công việc (50%): hoàn thành mục tiêu đã cam kết đầu kỳ.
- Năng lực chuyên môn (20%): kỹ năng kỹ thuật và kiến thức lĩnh vực.
- Kỹ năng mềm và teamwork (15%): giao tiếp, hợp tác, giải quyết vấn đề.
- Phát triển và học hỏi (15%): chủ động học kỹ năng mới, chia sẻ kiến thức.

4. QUY TRÌNH ĐÁNH GIÁ
Bước 1: Nhân viên tự đánh giá (Self-assessment) trên hệ thống HR trước ngày 5 của tháng đánh giá.
Bước 2: Quản lý trực tiếp đánh giá và thêm nhận xét trong vòng 1 tuần.
Bước 3: Cuộc họp 1-1 giữa nhân viên và quản lý để thảo luận kết quả (tối đa 60 phút).
Bước 4: Nhân viên ký xác nhận kết quả (không đồng ý có quyền khiếu nại lên HR).
Bước 5: HR tổng hợp và phê duyệt điều chỉnh lương/thăng tiến.

5. ĐIỀU CHỈNH LƯƠNG VÀ THĂNG TIẾN
- Exceptional: tăng lương 15-20% + xem xét thăng tiến.
- Exceeds Expectations: tăng lương 8-12%.
- Meets Expectations: tăng lương 3-5% (theo lạm phát).
- Needs Improvement: không tăng lương + Performance Improvement Plan (PIP) 90 ngày.
- Unsatisfactory: không tăng lương + PIP 60 ngày, có thể chấm dứt hợp đồng.

6. KHIẾU NẠI
Nhân viên không đồng ý với kết quả đánh giá có thể nộp đơn khiếu nại lên HR trong vòng 10 ngày làm việc kể từ ngày nhận kết quả.
        """.strip()
    },
    {
        "doc_id": "policy_onboarding",
        "title": "Chính sách Hội nhập Nhân viên Mới",
        "content": """
Chính sách Hội nhập Nhân viên Mới (Onboarding Policy) - VinTech Company

1. TRƯỚC NGÀY LÀM VIỆC ĐẦU TIÊN
- HR gửi Welcome Package qua email chứa: lịch trình tuần đầu, danh sách tài liệu cần mang theo, thông tin về chỗ đậu xe và ăn trưa.
- Bộ phận IT chuẩn bị laptop, tài khoản email, Slack, Jira và các hệ thống liên quan.
- Buddy (người hướng dẫn) được chỉ định là đồng nghiệp cùng team, có thâm niên từ 6 tháng trở lên.

2. TUẦN ĐẦU TIÊN
Ngày 1: Lễ chào mừng với HR, tour văn phòng, nhận thiết bị, setup tài khoản, gặp team.
Ngày 2-3: Training bắt buộc gồm: chính sách công ty, bảo mật thông tin, quy trình làm việc.
Ngày 4-5: Gặp gỡ các stakeholder chính, tìm hiểu sản phẩm/dịch vụ công ty.

3. THÁNG ĐẦU TIÊN
- Hoàn thành tất cả khóa đào tạo bắt buộc trên hệ thống LMS (khoảng 8-10 khóa).
- Thiết lập mục tiêu 30-60-90 ngày cùng với quản lý trực tiếp trong tuần đầu tiên.
- Tham gia ít nhất 3 cuộc họp team và 2 cuộc họp all-hands.
- Buddy check-in hàng tuần trong tháng đầu.

4. THÁNG THỨ 2-3 (THỜI GIAN THỬ VIỆC)
- Bắt đầu nhận nhiệm vụ độc lập theo mức độ tăng dần.
- Nhận phản hồi không chính thức từ quản lý hàng tuần.
- Đánh giá thử việc chính thức vào cuối tháng thứ 3.
- Tỷ lệ thông qua thử việc của công ty là 85%, nhân viên không đạt được hỗ trợ tìm việc mới.

5. TÀI LIỆU VÀ QUYỀN LỢI
- Handbook nhân viên có trên cổng thông tin nội bộ (intranet).
- Thẻ y tế bảo hiểm sức khỏe cá nhân được kích hoạt từ tháng đầu tiên.
- Phụ cấp ăn trưa 50.000 VNĐ/ngày làm việc tại văn phòng.
- Đăng ký tài khoản học trực tuyến (Coursera, LinkedIn Learning) từ tháng thứ 2.

6. PHẢN HỒI VỀ ONBOARDING
Nhân viên mới điền khảo sát onboarding sau 30 ngày và 90 ngày để giúp công ty liên tục cải thiện quy trình hội nhập.
        """.strip()
    },
    {
        "doc_id": "policy_expense",
        "title": "Chính sách Thanh toán Chi phí Công tác",
        "content": """
Chính sách Thanh toán Chi phí Công tác và Chi phí Kinh doanh - VinTech Company

1. PHẠM VI ÁP DỤNG
Chính sách này áp dụng cho tất cả chi phí phát sinh khi thực hiện công việc vì lợi ích của công ty, bao gồm công tác trong nước, quốc tế và các chi phí kinh doanh khác.

2. GIỚI HẠN CHI PHÍ KHÁCH SẠN
- Hà Nội, TP.HCM: tối đa 1.500.000 VNĐ/đêm.
- Các tỉnh thành khác trong nước: tối đa 1.000.000 VNĐ/đêm.
- Châu Á (Nhật, Singapore, Hàn Quốc): tối đa 150 USD/đêm.
- Châu Âu, Bắc Mỹ: tối đa 200 USD/đêm.

3. PHỤ CẤP ĂN UỐNG HÀNG NGÀY (PER DIEM)
- Công tác trong nước: 300.000 VNĐ/ngày.
- Công tác khu vực Đông Nam Á: 50 USD/ngày.
- Công tác Nhật Bản, Hàn Quốc, Úc: 80 USD/ngày.
- Công tác Châu Âu, Bắc Mỹ: 100 USD/ngày.

4. DI CHUYỂN
- Vé máy bay đặt trước ít nhất 2 tuần qua bộ phận Admin để được giá tốt nhất.
- Hạng ghế Economy cho chuyến bay dưới 8 tiếng, Business class cho từ 8 tiếng trở lên với chức vụ từ Manager.
- Taxi/Grab đến/từ sân bay được hoàn tiền với hóa đơn.
- Không hoàn tiền thuê xe tự lái nếu chưa được phê duyệt trước.

5. QUY TRÌNH HOÀN TIỀN
- Nộp expense report trên hệ thống Concur trong vòng 10 ngày làm việc sau khi kết thúc công tác.
- Đính kèm hóa đơn/chứng từ gốc cho tất cả chi phí từ 200.000 VNĐ trở lên.
- Quản lý phê duyệt trong vòng 3 ngày làm việc; Finance xử lý trong vòng 5 ngày làm việc tiếp theo.
- Thanh toán vào ngày 15 hoặc 30 của tháng, tùy ngày nào gần hơn sau khi phê duyệt.

6. CHI PHÍ KHÔNG ĐƯỢC HOÀN TRẢ
Rượu/bia và đồ uống có cồn (trừ khi trong bữa tiếp khách có phê duyệt), phim/giải trí cá nhân, chi phí gia đình đi kèm, tiền phạt giao thông, và tiền tip vượt quá 15%.
        """.strip()
    }
]

# Flat dict for quick lookup by doc_id (used by agent for retrieval simulation)
KNOWLEDGE_BASE_DICT = {doc["doc_id"]: doc["content"] for doc in KNOWLEDGE_BASE}
KNOWLEDGE_BASE_IDS = [doc["doc_id"] for doc in KNOWLEDGE_BASE]
