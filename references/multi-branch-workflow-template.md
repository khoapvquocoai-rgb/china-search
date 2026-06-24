# Multi-Branch Workflow Template (v3.0 - Generic)

This template provides a complete multi-branch workflow architecture for reviewing diverse document types with domain-specific analysis and risk scoring.

**Version:** 3.0  
**Status:** Project-agnostic, reusable across multiple projects  
**Last Updated:** 2026-06-24  

---

## Architecture Overview

```
User Input → Doc Extractor → Parameter Extractor (JSON)
    ↓
IF/ELSE Router (by document type):
├─ IF "technical" → Technical Review Branch
├─ IF "legal" → Legal Review Branch  
├─ IF "procurement" → Procurement Review Branch
├─ IF "meeting" → Meeting/RFI Review Branch
└─ ELSE → General Executive Brief

Each branch has:
• Domain-specific prompt
• Dedicated Knowledge Base
• Custom output template
• Branch-specific risk scoring
    ↓
Risk Scoring Node (unified assessment)
    ↓
Jinja2 Template Output
    ↓
End (formatted report)
```

---

## Configuration

### Document Type Classification

Define document types per category in your project config:

```json
{
  "document_types": {
    "technical": ["SPECIFICATION", "STANDARD", "DRAWING"],
    "legal": ["CONTRACT", "AGREEMENT"],
    "procurement": ["VENDOR_DATABOOK", "DATASHEET"],
    "meeting": ["MINUTES", "RFI"]
  }
}
```

### Dynamic Project Context

All prompts use `[PROJECT_NAME]` placeholder, replaced at runtime:

```python
project_name = config["project"]["name"]  # e.g., "MyDataCenter"
prompt = f"You are a reviewer for {project_name} project..."
```

---

## Branch Templates

### Technical Review Branch

**Trigger Condition:** Document type contains technical keywords (configurable)

**Knowledge Base ID:** `KB-{PROJECT_ID}-Technical`

**Prompt Template:**

```
You are a technical expert reviewer for [PROJECT_NAME] project.
Industry: [INDUSTRY]
Location: [LOCATION]

Analyze the document based on technical considerations specific to 
[INDUSTRY] projects in [LOCATION].

Consider:
- Industry-specific standards and best practices
- Local regulations and compliance requirements
- Project-specific constraints mentioned in the document

Return structured analysis with:
1. Key findings
2. Technical risk assessment
3. Recommendations
4. Action items

Input: {{#param_extractor.output#}}
Retrieved knowledge: {{#technical_rag.context#}}
```

**Output Template (Jinja2):**

```jinja2
## Technical Review - {{ project_name }}

### Key Findings
{{ technical_findings }}

### Risk Assessment
{% for risk in technical_risks %}
- **{{ risk.severity }}:** {{ risk.description }}
  - Evidence: {{ risk.evidence }}
  - Mitigation: {{ risk.mitigation }}
{% endfor %}

### Recommendations
{{ technical_recommendations }}

### Action Items
{% for item in action_items %}
- [ ] {{ item.task }} (Owner: {{ item.owner }}, Deadline: {{ item.deadline }})
{% endfor %}
```

---

### Legal Review Branch

**Trigger Condition:** Document type contains legal keywords

**Knowledge Base ID:** `KB-{PROJECT_ID}-Legal`

**Prompt Template:**

```
You are a legal expert reviewer for [PROJECT_NAME] project.
Industry: [INDUSTRY]
Location: [LOCATION]

Analyze the document based on legal considerations:
- Contract terms and conditions
- Liability clauses
- Compliance with [LOCATION] laws
- Intellectual property rights
- Dispute resolution mechanisms

Return structured analysis with:
1. Key legal findings
2. Risk assessment
3. Recommendations
4. Required actions

Input: {{#param_extractor.output#}}
Retrieved knowledge: {{#legal_rag.context#}}
```

---

### Procurement Review Branch

**Trigger Condition:** Document type contains procurement/vendor keywords

**Knowledge Base ID:** `KB-{PROJECT_ID}-Procurement`

**Prompt Template:**

```
You are a procurement expert reviewer for [PROJECT_NAME] project.

Analyze vendor documents for:
- Technical compliance with specifications
- Commercial terms and pricing
- Delivery timelines
- Warranty and support commitments
- Vendor lock-in risks

Return structured analysis with:
1. Vendor comparison (if multiple)
2. Risk assessment
3. Go/No-Go recommendation
4. Negotiation points

Input: {{#param_extractor.output#}}
Retrieved knowledge: {{#procurement_rag.context#}}
```

---

### Meeting/RFI Review Branch

**Trigger Condition:** Document type contains meeting/RFI keywords

**Knowledge Base ID:** `KB-{PROJECT_ID}-Meeting`

**Prompt Template:**

```
You are a meeting/RFI analyst for [PROJECT_NAME] project.

Extract from meeting minutes or RFI:
- Key decisions made
- Action items with owners and deadlines
- Open questions requiring follow-up
- Risks identified
- Next steps

Return structured log with:
1. Decision log
2. Action item tracker
3. RFI response draft (if applicable)
4. Risk register updates

Input: {{#param_extractor.output#}}
Retrieved knowledge: {{#meeting_rag.context#}}
```

---

## Risk Scoring Framework

### Unified Risk Assessment

After all branches complete, aggregate scores:

```json
{
  "overall_risk": "low|medium|high|critical",
  "risk_score": 0-100,
  "category_scores": {
    "technical": 45,
    "legal": 62,
    "commercial": 38,
    "operational": 25
  },
  "top_risks": [
    {
      "category": "technical",
      "risk": "Specification gap identified",
      "reason": "Missing performance criteria",
      "evidence": "Section 3.2 incomplete",
      "owner_action": "Request clarification from designer"
    }
  ],
  "go_no_go": "go|conditional_go|no_go|need_more_info"
}
```

### Scoring Scale

| Score Range | Risk Level | Action Required |
|-------------|------------|-----------------|
| 0-30 | Low | Proceed with monitoring |
| 31-60 | Medium | Additional review needed |
| 61-80 | High | Executive approval required |
| 81-100 | Critical | Stop, immediate action |

---

## Implementation Example

### Generate Workflow for Any Project

```bash
# Simple: Just provide project name
python generate_workflow_json.py --project "MyDataCenter" --output workflow.json

# Advanced: With custom config
python generate_workflow_json.py --config my-project.json --output workflow.json
```

### Project Config Example (`my-project.json`)

```json
{
  "project": {
    "name": "HCMC-Manufacturing-Plant",
    "industry": "manufacturing",
    "location": "Vietnam"
  },
  "document_types": {
    "technical": ["DRAWING", "BILL_OF_MATERIALS", "STANDARD"],
    "legal": ["SUPPLY_CONTRACT", "MOU"],
    "procurement": ["VENDOR_QUOTE", "DATASHEET"],
    "meeting": ["PRODUCTION_MINUTES", "QUALITY_RFI"]
  },
  "branches": {
    "enabled": ["technical", "procurement", "meeting"]
  }
}
```

---

## Best Practices

### 1. Knowledge Base Segregation

**DO:**
- Create separate KBs per domain (`KB-{Project}-Technical`, `KB-{Project}-Legal`)
- Index only relevant documents in each KB
- Use consistent naming conventions

**DON'T:**
- Mix technical and legal documents in same KB
- Use single KB for all projects (causes context pollution)
- Forget to update KB when project scope changes

### 2. Prompt Engineering

**DO:**
- Include project context (`[PROJECT_NAME]`, `[INDUSTRY]`, `[LOCATION]`)
- Specify output format explicitly
- Provide examples for complex tasks

**DON'T:**
- Hardcode project names in prompts
- Assume LLM knows project specifics
- Skip validation of extracted parameters

### 3. Risk Scoring

**DO:**
- Use quantitative scores (0-100)
- Provide evidence for each risk
- Include actionable mitigation steps

**DON'T:**
- Use binary pass/fail gates
- Skip risk categorization
- Forget to update thresholds per project

---

## Migration from v2.0

### Breaking Changes

| v2.0 | v3.0 |
|------|------|
| Hardcoded `HN-DC03` | Dynamic `[PROJECT_NAME]` |
| Fixed HSYC/HSMT types | Configurable document types |
| Single KB per domain | Per-project KB isolation |

### Migration Steps

```bash
# v2.0 command
python generate_workflow_json.py --output workflow.json

# v3.0 equivalent (backward compatible)
python generate_workflow_json.py --project "HN-DC03" --output workflow.json

# Or use config file for full control
python generate_workflow_json.py --config hn-dc03-config.json --output workflow.json
```

---

## Test Cases

### Test Case 1: Technical Specification Review

**Input:**
- Project: `TestProject-Alpha`
- Document Type: `SPECIFICATION`
- Content: HVAC system technical spec

**Expected Flow:**
1. Router → Technical branch
2. RAG from `KB-TestProject_Alpha-Technical`
3. Analysis with industry-specific prompts
4. Risk score: 45 (medium)
5. Output: Executive brief with action items

### Test Case 2: Contract Review

**Input:**
- Project: `TestProject-Alpha`
- Document Type: `CONTRACT`
- Content: Vendor agreement

**Expected Flow:**
1. Router → Legal branch
2. RAG from `KB-TestProject_Alpha-Legal`
3. Analysis of terms and liabilities
4. Risk score: 62 (medium-high)
5. Output: Legal review checklist

### Test Case 3: Multi-Project Reuse

**Scenario:** Same workflow logic for different projects

**Steps:**
```bash
# Project A
python generate_workflow_json.py --project "DataCenter-A" --output dc-a.json

# Project B (zero code changes)
python generate_workflow_json.py --project "Factory-B" --output factory-b.json

# Verify differences
diff <jq '.project_context' dc-a.json factory-b.json>
# Should show only project name/industry/location differences
```

---

## Related Documentation

- [SKILL.md](../SKILL.md) - Complete skill documentation
- [README.md](../README.md) - Quick start guide
- [generate_workflow_json.py](../scripts/generate_workflow_json.py) - Workflow generator
- [project-template.json](../config/project-template.json) - Configuration template

---

**Version:** 3.0  
**Status:** Production-ready, multi-project support  
**Last Updated:** 2026-06-24
