# Bài Học Từ So Sánh với ChatGPT - 2026-06-24

## Tổng Quan
Ngày 24/06/2026, skill `china-search` đã được cập nhật với **7 bài học quan trọng** từ việc so sánh câu trả lời giữa OpenClaw và ChatGPT cho cùng một yêu cầu shortlist.

---

## Priority 1: Critical Learnings (Đã Áp Dụng)

### ✅ 1. Phân Nhóm Theo Mục Đích Sử Dụng

**Trước đây:**
- Liệt kê 6 scenarios riêng lẻ
- Không có phân loại chiến lược rõ ràng
- Người đọc khó quyết định "bắt đầu từ đâu"

**Bây giờ:**
```markdown
Nhóm 1: Dùng NGAY cho PoC Nghiệp Vụ
├─ Dify: Nền tảng workflow tổng hợp
└─ FastGPT: Nền tảng RAG/hỏi đáp tài liệu

Nhóm 2: Dùng cho R&D Kỹ Thuật
├─ Qwen-Agent: Custom agent framework
├─ MS-Agent: Nghiên cứu "AI Skill" đúng nghĩa
└─ AgentScope: Multi-agent có kiểm soát
```

**File Updated:** `SKILL.md` → Section "Default output formats"

---

### ✅ 2. Bảng "Nên Dùng Khi / Không Nên Dùng Khi"

**Trước đây:**
- Chỉ có "Best For" một chiều
- Thiếu cảnh báo rủi ro
- Không nói rõ khi nào TRÁNH dùng tool

**Bây giờ:**
```markdown
| Công cụ | Nên dùng khi... | Không nên dùng khi... |
|---------|-----------------|----------------------|
| FastGPT | Hỏi đáp KB nhanh | Muốn mở SaaS (license restriction!) |
| Dify    | PoC nhanh demo lãnh đạo | Cần kiểm soát sâu bằng code |
```

**File Created:** `references/usage-decision-template.md` (5.7KB)

---

### ✅ 3. Chi Tiết License Risk

**Trước đây:**
- Ghi chung chung "check commercial terms"
- Không mention specific restrictions

**Bây giờ:**
```markdown
⚠️ FastGPT: Apache-2.0 nhưng KHÔNG cho phép SaaS 
   trừ khi có written permission từ maintainers.

⚠️ Dify: Dựa trên Apache 2.0 nhưng có additional terms.
   Review COMMERCIAL.md trước enterprise deployment.
```

**File Updated:** `SKILL.md` → New section "Risk Assessment Best Practices"

---

### ✅ 4. Specific Security Risks

**Trước đây:**
- Generic risks: "Security Vulnerabilities", "Data Privacy"
- Không mention attack vectors cụ thể

**Bây giờ:**
```markdown
Specific attack vectors:
├─ Prompt Injection (malicious instructions in input)
├─ RAG Poisoning (toxic documents corrupting KB)
├─ Tool Execution (arbitrary code/files in sandbox)
├─ Data Leakage (sensitive info via API/logs)
└─ Model Jailbreak (bypassing safety filters)

Mitigation strategies for each included.
```

**File Created:** `references/risk-assessment-checklist.md` (9.4KB)

---

## Priority 2: Important Learnings (Đã Áp Dụng)

### ✅ 5. Context-Aware Recommendations

**Trước đây:**
- Generic use cases: "Enterprise app development", "Customer service bots"
- Không gắn với real-world project context

**Bây giờ:**
```python
# Script tự động hỏi context trước khi recommend
context = {
    "project_name": "HN-DC03",
    "business_need": "vendor review, document Q&A",
    "team_skills": "technical",
    "deployment_type": "self-hosted",
    "budget": "$0 API",
    "timeline": "PoC (2-3 weeks)",
    "data_sensitivity": "contracts, internal reports"
}

# Generate recommendations based on context
```

**File Created:** `scripts/generate_context_aware_recommendations.py` (16KB)

---

### ✅ 6. Named Use Cases với Metrics

**Trước đây:**
- Generic: "Test with document processing"
- No measurable success criteria

**Bây giờ:**
```markdown
Use Case: `review_hndc03_vendor_matrix`
- Description: Review vendor datasheets, compare specs, flag risks
- Tool: FastGPT or Dify
- Metrics:
  ✓ accuracy_rate > 90%
  ✓ response_time < 5s
  ✓ false_positive_rate < 5%
```

**Integrated into:** `generate_context_aware_recommendations.py`

---

### ✅ 7. Hybrid Architecture Recommendations

**Trước đây:**
- Khuyến nghị chọn 1 repo cho mỗi scenario
- Không đề cập đến multi-tool approach

**Bây giờ:**
```markdown
✅ Hybrid Architecture:

Production Layer (Quick PoC):
├─ Dify: Workflow orchestration, enterprise features
└─ FastGPT: RAG/knowledge base specialist

Research Layer (Custom Development):
├─ Qwen-Agent: Custom agent framework with MCP
├─ MS-Agent: Skill-based agents, DeepResearch
└─ AgentScope: Multi-agent orchestration with governance

Integration: Use Dify/FastGPT APIs as entry points,
            call Qwen-Agent/MS-Agent for complex tasks
```

**Updated in:** `SKILL.md` → "Hybrid Architecture Recommendations" subsection

---

## Files Modified/Created

### Modified
1. **`SKILL.md`** (+3 sections, ~800 lines added)
   - Updated "Default output formats"
   - Added "Risk Assessment Best Practices"
   - Enhanced "Evidence capture" fields

### Created
2. **`references/usage-decision-template.md`** (5.7KB)
   - Template cho "Nên dùng khi/Không nên dùng khi" tables
   - Best practices và examples

3. **`references/risk-assessment-checklist.md`** (9.4KB)
   - Comprehensive risk assessment checklist
   - 8 categories: License, Security, Injection, Execution, etc.
   - Scoring system (0-100)

4. **`scripts/generate_context_aware_recommendations.py`** (16KB)
   - Interactive script asking for project context
   - Auto-generates grouped recommendations
   - Creates named use cases with metrics
   - Proposes hybrid architecture

---

## Impact Summary

### Before Update
- ❌ Generic recommendations without context
- ❌ Missing "when NOT to use" guidance
- ❌ Vague license warnings
- ❌ No specific security attack vectors
- ❌ Single-tool focus

### After Update
- ✅ Context-aware, project-specific recommendations
- ✅ Clear "use when / avoid when" decision matrix
- ✅ Detailed license risk analysis (SaaS restrictions, commercial terms)
- ✅ Specific security mitigations (prompt injection, RAG poisoning, sandbox)
- ✅ Hybrid architecture proposals (multiple tools for different layers)
- ✅ Named use cases with measurable metrics
- ✅ Automated recommendation generation script

---

## Testing Results

### Test Case: HN-DC03 Project

**Input Context:**
- Project: HN-DC03 (data center construction)
- Need: Vendor review, document Q&A, executive reports
- Team: Mixed (technical + business users)
- Budget: $0 API preferred
- Timeline: 2-week PoC

**Output Quality:**
- ✅ Correctly grouped tools into Production vs R&D
- ✅ Warned about FastGPT SaaS restriction
- ✅ Proposed Dify+FastGPT for quick PoC
- ✅ Named use case: `review_hndc03_vendor_matrix`
- ✅ Defined metrics: accuracy >90%, latency <5s
- ✅ Security warning: Don't upload contracts to cloud demos

**Result:** Significantly more actionable than previous version!

---

## Next Steps (Future Improvements)

### Priority 3 (Nice to Have)
1. **Community source warnings automation** - Auto-detect and flag CSDN/Zhihu as "leads only"
2. **License checker integration** - Parse LICENSE files automatically
3. **Security scanner** - Test for prompt injection vulnerabilities
4. **Multi-language support** - Generate reports in Vietnamese/English/Chinese

### Long-term Vision
- Integrate with GitHub API for real-time star/commit data
- Build knowledge base of known license restrictions
- Create interactive CLI wizard for context gathering
- Add benchmarking suite for performance comparison

---

## Acknowledgments

**Learnings from:** ChatGPT comparison analysis on 2026-06-24  
**Key insight:** Practical, context-aware guidance beats comprehensive but generic coverage  
**Philosophy shift:** From "list everything" to "help user decide what to use when"

---

**Last Updated:** 2026-06-24 21:25 GMT+7  
**Version:** 1.1 (Priority 1 & 2 learnings integrated)  
**Status:** ✅ Ready for production use
