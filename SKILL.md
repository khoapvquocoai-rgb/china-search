---
name: "china-search"
description: "China search v3.0 - Generic multi-project support with dynamic configuration, multi-branch workflows, KB segregation, risk scoring, Jinja2 templates (GitHub-ready)"
version: "3.0.0"
configurable: true
---

# China Search Skill v3.0 - Multi-Project Production Ready

**Version:** 3.0.0  
**Status:** Ready for GitHub Release  
**Date:** 2026-06-24  
**Breaking Change:** ✅ Project-agnostic design with dynamic configuration  

## What's New in v3.0

### 🎯 Multi-Project Support
- **Dynamic project configuration**: Replace hardcoded project names with CLI parameters and config files
- **Template-based prompts**: All examples use `[PROJECT_NAME]` placeholder
- **Reusable workflows**: Generate workflows for any project without code changes
- **Backward compatible**: Still works with HN-DC03 via `--project` flag

### Enterprise Workflow Patterns (v2.0 features retained)
- **Multi-branch architecture**: IF/ELSE routing by document type (configurable types)
- **Knowledge base segregation**: Separate KBs per domain (Technical/Legal/Procurement/Meeting)
- **Quantitative risk scoring**: 0-100 scale with Go/No-Go decisions
- **Jinja2 template outputs**: Structured formatting, not LLM-generated
- **Domain-specific prompts**: Specialized reasoning per branch

### Security & Compliance
- License risk analysis (SaaS restrictions, commercial terms)
- Prompt injection mitigation strategies
- RAG poisoning prevention
- Tool execution sandboxing guide
- CAC regulation compliance checklist

### Developer Tools
- `generate_workflow_json.py`: Auto-generate Dify workflows with `--project` parameter
- `generate_context_aware_recommendations.py`: Interactive recommendation engine
- `config/project-template.json`: Reusable project configuration template
- Complete test cases with expected outputs
- Comprehensive documentation in `references/`

## Files Included

```
china-search/
├── SKILL.md                          # Main docs (v3.0 updated)
├── README.md                         # Quick start
├── CHANGELOG.md                      # Version history
├── config/
│   ├── project-template.json         # NEW: Project configuration template
│   └── document-types-default.json   # NEW: Default document type mappings
├── scripts/
│   ├── build_search_matrix.py       # Query generator
│   ├── score_evidence.py            # Evidence scoring
│   ├── generate_context_aware_recommendations.py  # Updated v3.0
│   └── generate_workflow_json.py    # Updated v3.0 (dynamic project support)
└── references/
    ├── usage-decision-template.md   # When to use/avoid
    ├── risk-assessment-checklist.md # 8-category checklist
    ├── multi-branch-workflow-template.md  # Complete patterns (generic)
    └── [original files preserved]
```

## Quick Start

### Option 1: Interactive Mode (Recommended for First Time)

```bash
cd scripts
python generate_context_aware_recommendations.py
# Answer prompts about your project context
# Generates customized workflow automatically
```

### Option 2: Command Line (Quick Setup)

```bash
cd scripts

# Generate workflow for any project
python generate_workflow_json.py --project "YOUR_PROJECT_NAME" --output workflow.json

# With custom document types
python generate_workflow_json.py \
  --project "MyDataCenter" \
  --doc-types "SPECIFICATION,CONTRACT,VENDOR_DATABOOK,MEETING_MINUTES" \
  --output workflow.json

# Import to Dify:
# 1. Open Dify → Studio → Create from JSON
# 2. Select workflow.json
# 3. Configure Knowledge Bases
# 4. Test with sample documents
```

### Option 3: Configuration File (Enterprise)

```bash
# Create project config
cp config/project-template.json my-project.json

# Edit with your settings
vim my-project.json

# Generate workflow from config
python generate_workflow_json.py --config my-project.json --output workflow.json
```

## Configuration

### Project Config Template (`config/project-template.json`)

```json
{
  "project": {
    "name": "PROJECT_NAME",
    "description": "Brief project description",
    "industry": "data-center|construction|manufacturing|other",
    "location": "Vietnam|China|other"
  },
  "document_types": {
    "technical": ["HSYC", "HSMT", "SPECIFICATION", "STANDARD"],
    "legal": ["CONTRACT", "AGREEMENT", "MOU"],
    "procurement": ["VENDOR_DATABOOK", "DATASHEET", "QUOTE"],
    "meeting": ["MINUTES", "RFI", "ACTION_LOG"]
  },
  "knowledge_bases": {
    "technical": "KB-Technical",
    "legal": "KB-Legal",
    "procurement": "KB-Procurement",
    "meeting": "KB-Meeting"
  },
  "risk_thresholds": {
    "low": 30,
    "medium": 60,
    "high": 80,
    "critical": 100
  },
  "output_templates": {
    "executive_brief": "templates/executive-brief.jinja2",
    "issue_log": "templates/issue-log.jinja2",
    "rfi_list": "templates/rfi-list.jinja2"
  }
}
```

### Document Type Mappings

Default Vietnamese ↔ English mappings:

| Category | Vietnamese | English |
|----------|-----------|---------|
| Technical | HSYC, HSMT, tiêu chuẩn | SPECIFICATION, STANDARD |
| Legal | hợp đồng, thỏa thuận | CONTRACT, AGREEMENT |
| Procurement | hồ sơ nhà cung cấp, datasheet | VENDOR_DATABOOK, DATASHEET |
| Meeting | biên bản họp, RFI | MINUTES, RFI |

Customize in `config/document-types-default.json`.

## Testing

All Python scripts syntax-verified:

```bash
python3 -m py_compile scripts/*.py  # ✅ Passed

# Run with different projects
python scripts/generate_workflow_json.py --project "TestProject-Alpha" --output test.json
python scripts/generate_workflow_json.py --project "HN-DC03" --output dc03.json  # Backward compat
```

## Migration Guide (v2.0 → v3.0)

### Breaking Changes

1. **Hardcoded project names removed**: All `HN-DC03`, `DC03` replaced with `[PROJECT_NAME]`
2. **CLI required**: Must pass `--project` parameter or use config file
3. **Document types configurable**: No longer fixed to HSYC/HSMT only

### Migration Steps

```bash
# v2.0 users: Add --project flag to existing commands
OLD: python generate_workflow_json.py --output workflow.json
NEW: python generate_workflow_json.py --project "YourProject" --output workflow.json

# Or create config file for repeated use
cp config/project-template.json myproject.json
# Edit myproject.json
python generate_workflow_json.py --config myproject.json --output workflow.json
```

### Backward Compatibility

v3.0 maintains backward compatibility with HN-DC03:

```bash
# This still works exactly as v2.0
python generate_workflow_json.py --project "HN-DC03" --output workflow.json
```

## License

Apache-2.0 with notes on SaaS restrictions. See LICENSE file.

---

**Ready for community review and GitHub release.**

**Key Improvement:** This skill is now truly reusable across multiple projects without code changes! 🚀
