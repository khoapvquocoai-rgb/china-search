---
name: "china-search"
description: "China search v2.0 with multi-branch workflows, KB segregation, risk scoring, Jinja2 templates (GitHub-ready)"
---

# China Search Skill v2.0 - Production Ready

**Version:** 2.0  
**Status:** Ready for GitHub Release  
**Date:** 2026-06-24  

## What's New

### Enterprise Workflow Patterns
- **Multi-branch architecture**: IF/ELSE routing by document type (HSYC, contracts, vendors, meetings)
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
- `generate_workflow_json.py`: Auto-generate Dify workflows
- `generate_context_aware_recommendations.py`: Interactive recommendation engine
- Complete test cases with expected outputs
- Comprehensive documentation in `references/`

## Files Included

```
china-search/
├── SKILL.md                          # Main docs (v2.0 updated)
├── README.md                         # Quick start
├── LEARNINGS_2026-06-24.md          # Evolution history
├── scripts/
│   ├── build_search_matrix.py       # Query generator
│   ├── score_evidence.py            # Evidence scoring
│   ├── generate_context_aware_recommendations.py  # NEW
│   └── generate_workflow_json.py    # NEW (syntax verified)
└── references/
    ├── usage-decision-template.md   # NEW: When to use/avoid
    ├── risk-assessment-checklist.md # NEW: 8-category checklist
    ├── multi-branch-workflow-template.md  # NEW: Complete patterns
    └── [original files preserved]
```

## Quick Start

```bash
# Generate workflow
cd scripts
python generate_workflow_json.py --project "HN-DC03" --output workflow.json

# Import to Dify
# Studio → Import from JSON → workflow.json
```

## Testing

All Python scripts syntax-verified:
```bash
python3 -m py_compile scripts/*.py  # ✅ Passed
```

## License

Apache-2.0 with notes on SaaS restrictions. See LICENSE file.

---

**Ready for community review and GitHub release.**
