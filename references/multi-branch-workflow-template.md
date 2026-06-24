# Multi-Branch Workflow Template for Enterprise Document Review

## Overview

This template provides a complete multi-branch workflow architecture for reviewing diverse document types (HSYC, contracts, vendor datasheets, meeting minutes) with domain-specific analysis and risk scoring.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User Input Node                          │
│  - question (paragraph)                                     │
│  - dossier_type (select: HSYC/contract/vendor/meeting/etc)  │
│  - uploaded_files (file list)                               │
│  - output_type (select: brief/issue-log/checklist/full)     │
│  - risk_focus (multi-select)                                │
│  - decision_needed (paragraph)                              │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
           ┌─────────────────────────┐
           │   Doc Extractor Node    │
           │  (PDF/DOCX → text)      │
           └─────────────┬───────────┘
                         ↓
           ┌─────────────────────────┐
           │ Parameter Extractor     │
           │ (JSON Schema Output)    │
           └─────────────┬───────────┘
                         ↓
           ┌─────────────────────────┐
           │   IF/ELSE Router        │
           │  (Branch by Type)       │
           └─────────────┬───────────┘
          ┌──────┼──────┼──────┼──────┐
          ↓      ↓      ↓      ↓      ↓
    ┌────────┐ ┌──────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐
    │Technical│ │ Legal│ │Procurement│ │Meeting/RFI│ │  General    │
    │Review  │ │Review│ │  Review   │ │  Review   │ │  Executive   │
    └────┬───┘ └──┬───┘ └────┬─────┘ └─────┬────┘ └─────┬──────┘
         │        │          │            │             │
         ↓        ↓          ↓            ↓             ↓
    ┌──────────────────────────────────────────────────────────┐
    │              Knowledge Retrieval (RAG)                   │
    │  (Route to appropriate KB per branch)                    │
    └──────────────┬───────────────────────────────────────────┘
                   ↓
    ┌──────────────────────────────────────────────────────────┐
    │              Domain-Specific LLM Analysis                │
    │  (Specialized prompts per branch)                        │
    └──────────────┬───────────────────────────────────────────┘
                   ↓
    ┌──────────────────────────────────────────────────────────┐
    │                  Risk Scoring Node                       │
    │  (0-100 score + Go/No-Go decision)                       │
    └──────────────┬───────────────────────────────────────────┘
                   ↓
    ┌──────────────────────────────────────────────────────────┐
    │              Jinja2 Template Formatter                   │
    │  (Structured output, not LLM-generated)                  │
    └──────────────┬───────────────────────────────────────────┘
                   ↓
    ┌──────────────────────────────────────────────────────────┐
    │                    End Node                              │
    │  (Return formatted report)                               │
    └──────────────────────────────────────────────────────────┘
```

---

## Node-by-Node Implementation

### Node 1: User Input

**Type:** `start`  
**Variables:**

```json
{
  "question": {
    "type": "paragraph",
    "required": true,
    "description": "Câu hỏi/yêu cầu của người dùng"
  },
  "dossier_type": {
    "type": "select",
    "required": true,
    "options": [
      "HSYC", "HSMT", "hợp đồng", "vendor datasheet", 
      "biên bản họp", "RFI", "tiêu chuẩn", "báo cáo", "khác"
    ],
    "default": "HSYC"
  },
  "uploaded_files": {
    "type": "file_list",
    "required": false,
    "allowed_file_types": ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"],
    "max_file_size": 15
  },
  "output_type": {
    "type": "select",
    "required": true,
    "options": [
      "Executive brief", 
      "Issue log", 
      "RFI list", 
      "Checklist", 
      "Full review"
    ],
    "default": "Executive brief"
  },
  "risk_focus": {
    "type": "multi_select",
    "required": false,
    "options": [
      "kỹ thuật", "pháp lý", "thương mại", 
      "vendor lock-in", "vận hành", "tuân thủ"
    ]
  },
  "decision_needed": {
    "type": "paragraph",
    "required": false,
    "description": "Việc cần lãnh đạo quyết định"
  }
}
```

---

### Node 2: Doc Extractor

**Type:** `document-extractor`  
**Name:** `Extract Uploaded Dossier`

**Configuration:**
```json
{
  "input_variable": "{{#start_node.uploaded_files#}}",
  "output_format": "text",
  "chunk_strategy": "fixed_size",
  "chunk_size": 500,
  "chunk_overlap": 50,
  "cleaning_strategy": "basic_clean"
}
```

**Output:** `extracted_text`

---

### Node 3: Parameter Extractor

**Type:** `llm`  
**Name:** `Classify & Normalize Input`

**Prompt:**
```text
Bạn là trợ lý phân loại hồ sơ dự án data center HN-DC03.

Nhiệm vụ:
1. Đọc yêu cầu người dùng và nội dung file đã trích xuất.
2. Nhận diện loại hồ sơ, chuyên ngành, bên liên quan, quyết định cần đưa ra.
3. Không suy đoán khi thiếu dữ liệu.
4. Trả về JSON đúng schema dưới đây.

Schema:
{
  "project": "string",
  "document_type": "string",
  "discipline": "string",
  "main_entities": ["string"],
  "decision_required": "string",
  "risk_categories": ["technical", "legal", "commercial", "procurement", "operation", "compliance"],
  "urgency": "low|medium|high",
  "missing_information": ["string"]
}

Quy tắc:
- Nếu không chắc chắn về bất kỳ trường nào, ghi vào missing_information.
- Không kết luận đạt/không đạt ở bước này.
- Chỉ phân loại và chuẩn hóa đầu vào.
- Giữ nguyên ngôn ngữ tiếng Việt cho các giá trị string.

Input từ user:
{{#start_node.question#}}

Nội dung file (nếu có):
{{#doc_extractor.extracted_text#}}

Trả về CHỈ JSON, không giải thích thêm.
```

**Output:** `classified_params` (JSON)

---

### Node 4: IF/ELSE Router

**Type:** `if-else`  
**Name:** `Route by Document Type`

**Conditions:**

```javascript
// Branch 1: Technical Review
{{#parameter_extractor.classified_params.document_type#}} contains "HSYC" or "HSMT" or "tiêu chuẩn"

// Branch 2: Legal Review  
{{#parameter_extractor.classified_params.document_type#}} contains "hợp đồng" or "phụ lục"

// Branch 3: Procurement Review
{{#parameter_extractor.classified_params.document_type#}} contains "vendor" or "datasheet" or "HSYC"

// Branch 4: Meeting/RFI Review
{{#parameter_extractor.classified_params.document_type#}} contains "biên bản" or "RFI" or "issue"

// Default: General Executive Brief
ELSE
```

---

### Branch A: Technical Review

#### Step A1: Knowledge Retrieval
**Type:** `knowledge-retrieval`  
**Knowledge ID:** `KB-DC03-Technical`  
**Query:** `{{#parameter_extractor.classified_params.discipline#}} requirements for {{#parameter_extractor.classified_params.project#}}`  
**Top-K:** 5  
**Score Threshold:** 0.7

#### Step A2: LLM Analysis
**Type:** `llm`  
**Prompt:**
```text
Bạn là chuyên gia rà soát kỹ thuật data center phía chủ đầu tư.

Hồ sơ cần rà soát:
{{#doc_extractor.extracted_text#}}

Tiêu chuẩn áp dụng (từ RAG):
{{#rag_retrieval.context#}}

Phân tích theo cấu trúc:
1. Kết luận ngắn (2-3 câu)
2. Các yêu cầu kỹ thuật chính đã thấy
3. Điểm có căn cứ (trích dẫn cụ thể)
4. Điểm thiếu căn cứ
5. Rủi ro kỹ thuật, vận hành, nghiệm thu, bảo trì
6. Rủi ro vendor lock-in hoặc tiêu chí hạn chế cạnh tranh
7. Câu hỏi RFI cần gửi tư vấn/NCC
8. Checklist hành động

Nguyên tắc:
- Tách rõ sự thật trong hồ sơ, giả định và suy luận.
- Không kết luận PASS nếu thiếu model/datasheet/thông số định lượng.
- Không dùng brand name làm bằng chứng kỹ thuật.
- Nếu thiếu tiêu chuẩn áp dụng, ghi rõ cần xác minh.
- Trích dẫn trang/đoạn cụ thể khi có thể.
```

**Output:** `technical_analysis`

---

### Branch B: Legal Review

#### Step B1: Knowledge Retrieval
**Type:** `knowledge-retrieval`  
**Knowledge ID:** `KB-DC03-Legal-Contract`  
**Query:** `hợp đồng {{#parameter_extractor.classified_params.project#}} điều khoản nghiệm thu thanh toán`

#### Step B2: LLM Analysis
**Type:** `llm`  
**Prompt:**
```text
Bạn là trợ lý rà soát pháp lý/hợp đồng phía chủ đầu tư.

Nội dung hợp đồng:
{{#doc_extractor.extracted_text#}}

Quy định áp dụng (từ RAG):
{{#rag_retrieval.context#}}

Hãy kiểm tra:
1. Phạm vi nghĩa vụ hai bên
2. Điều kiện thanh toán/nghiệm thu
3. Điều kiện phạt, bồi thường, chấm dứt hợp đồng
4. Quyền phê duyệt/thẩm quyền ký
5. Rủi ro thiếu căn cứ pháp lý
6. Điều khoản bất lợi hoặc mơ hồ
7. Điểm cần xin ý kiến pháp chế
8. Kiến nghị sửa đổi

Không đưa kết luận pháp lý chắc chắn nếu chưa có đầy đủ hợp đồng, phụ lục, phê duyệt và quy định nội bộ.

Kết quả trả về dạng JSON:
{
  "conclusion": "string",
  "key_clauses": ["string"],
  "risks": [{"clause": "string", "risk": "string", "severity": "low|medium|high"}],
  "recommendations": ["string"],
  "needs_legal_review": boolean
}
```

---

### Branch C: Procurement/Vendor Review

#### Step C1: Knowledge Retrieval
**Type:** `knowledge-retrieval`  
**Knowledge ID:** `KB-DC03-Procurement-Vendor`  
**Query:** `vendor matrix {{#parameter_extractor.classified_params.main_entities[0]#}} tiêu chí đánh giá`

#### Step C2: LLM Analysis
**Type:** `llm`  
**Prompt:**
```text
Bạn là chuyên gia kiểm soát HSYC/HSMT, vendor và vật tư.

Datasheet/Hồ sơ vendor:
{{#doc_extractor.extracted_text#}}

Tiêu chí đánh giá (từ RAG):
{{#rag_retrieval.context#}}

Hãy rà soát:
1. Tiêu chí có tạo khóa hãng không? (brand-specific requirements)
2. Có tối thiểu 3 OEM/3 supplier tiềm năng không?
3. Datasheet có đúng model, đúng loại thiết bị không?
4. Có thiếu thông số định lượng không? (PUE, efficiency, capacity, v.v.)
5. Có chi phí ẩn/license/maintenance/consumable không?
6. Có rủi ro nghiệm thu, CO/CQ, bảo hành, tương thích BMS/DCIM không?
7. Bảng vendor evidence cần bổ sung
8. Kiến nghị chỉnh tiêu chí để đảm bảo cạnh tranh và nghiệm thu được

Trả về JSON:
{
  "competitiveness_assessment": "competitive|limited|locked_in",
  "missing_evidence": ["string"],
  "hidden_costs": ["string"],
  "acceptance_risks": ["string"],
  "recommendations": ["string"]
}
```

---

### Branch D: Meeting/RFI Review

#### Step D1: Knowledge Retrieval
**Type:** `knowledge-retrieval`  
**Knowledge ID:** `KB-DC03-Meeting-RFI`  
**Query:** `issue log action items {{#parameter_extractor.classified_params.project#}}`

#### Step D2: LLM Analysis
**Type:** `llm`  
**Prompt:**
```text
Bạn là thư ký kiểm soát issue/action dự án.

Biên bản họp/RFI:
{{#doc_extractor.extracted_text#}}

Lịch sử issues (từ RAG):
{{#rag_retrieval.context#}}

Hãy trích xuất:
1. Vấn đề được nêu (clear statement)
2. Người/bên nêu vấn đề nếu có
3. Người/bên chịu trách nhiệm giải quyết
4. Deadline nếu có
5. Trạng thái: open/closed/pending/reopened
6. Bằng chứng close (nếu đã đóng)
7. Điểm mâu thuẫn hoặc thiếu xác nhận
8. Action tiếp theo

Trả về JSON array:
[
  {
    "issue_id": "string",
    "description": "string",
    "raised_by": "string",
    "owner": "string",
    "deadline": "string|null",
    "status": "open|closed|pending|reopened",
    "close_evidence": "string|null",
    "next_action": "string"
  }
]
```

---

### Node 5: Risk Scoring (Common for All Branches)

**Type:** `llm`  
**Name:** `Quantitative Risk Assessment`

**Prompt:**
```text
Bạn là risk controller của chủ đầu tư HN-DC03.

Phân tích từ nhánh trước:
{{#branch_output#}}

Thông tin phân loại:
{{#parameter_extractor.classified_params#}}

Hãy chấm rủi ro dựa trên nội dung phân tích.

Thang điểm:
- 0-30: low (tiếp tục với giám sát thông thường)
- 31-60: medium (cần xem xét bổ sung)
- 61-80: high (cần phê duyệt cấp cao)
- 81-100: critical (dừng ngay, hành động khẩn cấp)

Nguyên tắc:
- Thiếu bằng chứng quan trọng → tối thiểu medium (31+)
- Rủi ro pháp lý, khóa hãng, không nghiệm thu được, sai loại thiết bị → high/critical (61+)
- Không đủ dữ liệu → go_no_go = "need_more_info", không đoán

Trả về JSON:
{
  "overall_risk": "low|medium|high|critical",
  "risk_score": <integer 0-100>,
  "top_risks": [
    {
      "risk": "string",
      "reason": "string",
      "evidence": "string",
      "owner_action": "string",
      "score_impact": <integer>
    }
  ],
  "go_no_go": "go|conditional_go|no_go|need_more_info",
  "conditions_for_go": ["string"]
}
```

**Output:** `risk_assessment`

---

### Node 6: Jinja2 Template Formatter

**Type:** `template-transform`  
**Name:** `Format Final Report`

**Template:**
```jinja2
# Báo Cáo Rà Soi Hồ Sơ - {{ classified_params.project }}

**Ngày:** {{ current_time }}  
**Loại hồ sơ:** {{ classified_params.document_type }}  
**Mức độ khẩn cấp:** {{ classified_params.urgency }}  
**Điểm rủi ro:** {{ risk_assessment.risk_score }}/100 ({{ risk_assessment.overall_risk }})  
**Quyết định:** {{ risk_assessment.go_no_go }}

---

## 📋 Kết Luận
{{ analysis_summary.conclusion }}

## 🎯 Việc Cần Quyết Định
{{ start_node.decision_needed }}

{% if risk_assessment.go_no_go == "no_go" %}
## 🚨 CẢNH BÁO: KHÔNG ĐẠT
{% elif risk_assessment.go_no_go == "conditional_go" %}
## ⚠️ ĐIỀU KIỆN ĐỂ TIẾP TỤC
{% else %}
## ✅ ĐÁNH GIÁ TỔNG THỂ
{% endif %}

{{ analysis_summary.key_findings }}

## 📊 Bằng Chứng Chính
{{ evidence_summary }}

## ⚠️ Rủi Ro
{% for item in risk_assessment.top_risks %}
- **{{ item.risk }}** (Impact: {{ item.score_impact }} pts)
  - Nguyên nhân: {{ item.reason }}
  - Căn cứ: {{ item.evidence }}
  - Hành động: {{ item.owner_action }}
{% endfor %}

## 💡 Kiến Nghị
{% for item in recommendations %}
- {{ item }}
{% endfor %}

## ✅ Checklist Hành Động
{% for item in action_checklist %}
- [ ] {{ item }}
{% endfor %}

## ❓ Điểm Thiếu Căn Cứ Cần Xác Minh
{% if classified_params.missing_information|length > 0 %}
{% for item in classified_params.missing_information %}
- {{ item }}
{% endfor %}
{% else %}
- Không có
{% endif %}

---

*Report generated by Dify AI Assistant. Please verify all findings with domain experts before making decisions.*

**Confidence Level:** {{ confidence_score }}/10  
**Reviewer:** {{ assigned_reviewer or "AI System" }}
```

---

## Testing the Workflow

### Test Case 1: HSYC Technical Review
**Input:**
- dossier_type: "HSYC"
- uploaded_files: [UPS_specification.pdf]
- risk_focus: ["kỹ thuật", "vendor lock-in"]

**Expected:** Routes to Technical branch, checks for missing model numbers, battery autonomy specs, CO/CQ requirements.

### Test Case 2: Contract Review
**Input:**
- dossier_type: "hợp đồng"
- uploaded_files: [contract_draft.docx]
- output_type: "Full review"

**Expected:** Routes to Legal branch, identifies payment terms risks, acceptance criteria gaps.

### Test Case 3: Vendor Matrix
**Input:**
- dossier_type: "vendor datasheet"
- uploaded_files: [vendor_comparison.xlsx]
- risk_focus: ["thương mại", "vendor lock-in"]

**Expected:** Routes to Procurement branch, detects brand-locking criteria, missing competitive options.

---

## Best Practices

1. **Always extract parameters first** before routing
2. **Use separate KBs per domain** to improve retrieval accuracy
3. **Score risks quantitatively** instead of binary approval
4. **Template outputs** rather than letting LLM format
5. **Track missing information** explicitly instead of guessing
6. **Test each branch independently** before integrating
7. **Log all decisions** for audit trails

---

**Version:** 2.0  
**Last Updated:** 2026-06-24  
**Compatible with:** Dify 0.6.0+
