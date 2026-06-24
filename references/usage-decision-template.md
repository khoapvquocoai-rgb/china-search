# Usage Decision Template: Nên Dùng Khi / Không Nên Dùng Khi

## Mục Đích
Cung cấp hướng dẫn rõ ràng về khi nào NÊN và KHÔNG NÊN dùng từng công cụ, giúp người đọc tránh sai lầm.

---

## Template Cơ Bản

| Công cụ | Bản chất | Nên dùng khi... | Không nên dùng khi... | Nhận định |
|---------|----------|-----------------|----------------------|-----------|
| [Tên] | [Mô tả ngắn 1-2 dòng] | [Use case phù hợp] | [Khi nào tránh] | [Khuyến nghị ưu tiên] |

---

## Ví Dụ Thực Tế: Top 5 China AI Repos

| Công cụ | Bản chất | Nên dùng khi... | Không nên dùng khi... | Nhận định |
|---------|----------|-----------------|----------------------|-----------|
| **Dify** | Low-code/no-code LLM app platform, workflow + RAG + agent + model management. ~146k stars, license Apache 2.0-based có điều kiện bổ sung. | Cần dựng nhanh AI app nội bộ: hỏi đáp tài liệu, workflow phê duyệt, trợ lý nghiệp vụ, chatbot có RAG, tích hợp nhiều model. | Cần kiểm soát cực sâu từng bước agent bằng code hoặc muốn tránh license có điều kiện. | **Ưu tiên số 1 cho PoC nhanh và demo lãnh đạo.** |
| **FastGPT** | Knowledge-based LLM platform, data processing, RAG retrieval, visual workflow orchestration. License cho phép backend service thương mại nhưng KHÔNG cho SaaS nếu chưa có quyền phù hợp. | Cần hệ thống hỏi đáp tài liệu/knowledge base nhanh, trực quan, phục vụ phòng ban. | Muốn mở dịch vụ SaaS hoặc thương mại hóa ra ngoài mà chưa rà license. | **Ưu tiên số 1 cho RAG tài liệu nội bộ.** |
| **Qwen-Agent** | Framework phát triển LLM application dựa trên Qwen, tool usage, planning, memory; Function Calling, MCP, Code Interpreter, RAG, Chrome extension. Apache-2.0. | Đội kỹ thuật muốn viết agent tùy biến bằng code, ưu tiên Qwen/ModelScope/Alibaba ecosystem, cần MCP/tool calling/code interpreter. | Người dùng nghiệp vụ không code muốn tự kéo-thả workflow. | **Ưu tiên cho custom agent kỹ thuật.** |
| **MS-Agent** | Lightweight framework cho agentic execution, `ms-agent-skills`, Agent Skills v2, MCP, DeepResearch, DocResearch, CodeGenesis, WebUI. Apache-2.0. | Muốn nghiên cứu đúng "AI Skill 仓库", skill retrieval, skill orchestration, deep research, code generation, video workflow. | Cần nền tảng ổn định, mature, ít rủi ro để đưa thẳng vào production. | **Ưu tiên cho R&D AI Skill/MCP.** |
| **AgentScope** | Production-ready agent framework, event system, permission system, multi-tenancy/session isolation, workspace/sandbox. Apache-2.0, ~27.1k stars, release v2.0.2 ngày 16/06/2026. | Cần nghiên cứu multi-agent, agent service, permission control, sandbox, human-in-the-loop, agent team. | Cần dựng app nghiệp vụ nhanh cho người không code. | **Ưu tiên cho multi-agent có kiểm soát.** |

---

## Hướng Dẫn Điền Template

### Cột "Bản chất"
- Mô tả ngắn gọn (1-2 dòng) về công cụ
- Nhấn mạnh điểm khác biệt chính
- Ghi số stars/forks nếu có (để thể hiện community size)
- **Nhắc license type ngay từ đầu**

### Cột "Nên dùng khi..."
- Liệt kê 2-3 use cases cụ thể nhất
- Ưu tiên scenario thực tế thay vì generic description
- Nếu có context project, mention tên project (ví dụ: "HN-DC03 vendor review")

### Cột "Không nên dùng khi..."
- Cảnh báo rõ ràng về limitations
- Mention license restrictions nếu có (đặc biệt SaaS prohibition)
- Chỉ ra khi nào công cụ này là overkill hoặc underpowered
- Warn về technical debt hoặc security risks

### Cột "Nhận định"
- Khuyến nghị ngắn gọn, actionable
- Sử dụng format: "**Ưu tiên cho [mục đích]**."
- Nếu có ranking, ghi rõ (số 1, runner-up, specialized pick)

---

## Best Practices

1. **Luôn mention license risk** trong "Không nên dùng khi" nếu có restrictions
2. **Cụ thể hóa use cases** thay vì nói chung chung ("enterprise use" → "dựng workflow phê duyệt hợp đồng")
3. **Warn about community sources** - CSDN/Zhihu chỉ là leads, không phải final proof
4. **Đề xuất hybrid approach** khi phù hợp (không bắt buộc chọn 1 công cụ duy nhất)
5. **Define metrics rõ ràng** cho evaluation (accuracy, speed, control level, audit quality)

---

## Example: Risk-Specific Warnings

### License Risks
```markdown
⚠️ FastGPT: License cho phép self-hosted backend service NHƯNG cấm cung cấp SaaS 
   trừ khi có written permission từ maintainers. Check LICENSE file trước khi deploy commercial.

⚠️ Dify: Dựa trên Apache 2.0 nhưng có additional terms cho commercial use. 
   Review "COMMERCIAL" file trong repo.
```

### Security Risks
```markdown
⚠️ Qwen-Agent/MS-Agent: Có khả năng chạy code arbitrary (Code Interpreter). 
   PHẢI setup sandbox với:
   - File system isolation
   - Network access control
   - API key protection
   - Timeout limits

⚠️ All RAG platforms: Risk of prompt injection qua uploaded documents. 
   Mitigation: Document validation, input sanitization, system prompt hardening.
```

### Data Privacy
```markdown
⚠️ Never upload sensitive data (contracts, bids, internal reports) to cloud demos 
   without explicit approval from legal/security teams.

✅ Prefer self-hosted deployment for sensitive workloads.
```

---

## Checklist Before Finalizing Recommendation

- [ ] Checked license terms thoroughly (especially SaaS/commercial restrictions)
- [ ] Identified specific use cases with project context if available
- [ ] Listed concrete "when NOT to use" scenarios
- [ ] Warned about security risks (prompt injection, tool execution, data leakage)
- [ ] Distinguished between official sources và community leads
- [ ] Proposed hybrid architecture if multiple tools fit different needs
- [ ] Defined clear metrics for evaluation
- [ ] Named specific skills/use cases instead of generic descriptions

---

**Template Version:** 1.0  
**Last Updated:** 2026-06-24  
**Based on Learnings From:** ChatGPT comparison analysis
