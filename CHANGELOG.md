# Changelog

All notable changes to china-search skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0] - 2026-06-24

### 🎉 Added

- **Multi-project support**: Dynamic configuration via CLI parameters and config files
- **Template-based prompts**: All hardcoded project names replaced with `[PROJECT_NAME]` placeholders
- **Config file support**: `project-template.json` for complex multi-project setups
- **Customizable document types**: No longer fixed to HSYC/HSMT only
- **Industry-specific tuning**: Manufacturing, construction, data-center presets
- **Location-aware compliance**: Vietnam/China/others regulatory context
- **Knowledge base isolation**: Per-project KB naming (`KB-{PROJECT_ID}-*`)

### 🔧 Changed

- `generate_workflow_json.py`: Now requires `--project` parameter or `--config` file
- `generate_context_aware_recommendations.py`: Updated to include multi-project features
- All reference documents: Replaced HN-DC03/DC03 examples with generic placeholders
- Risk scoring prompts: Include industry and location context

### ✅ Fixed

- Hardcoded project name references throughout codebase
- Document type inflexibility (now fully configurable)
- Knowledge base pollution across projects

### ⚠️ Breaking Changes

- **CLI required**: Must pass `--project` parameter or use `--config` file (no more defaults)
- **Document types**: No longer fixed to HSYC/HSMT (use config to customize)
- **KB naming**: Changed from `KB-DC03-*` to `KB-{PROJECT_ID}-*`

### 🔄 Migration Guide

#### v2.0 → v3.0

```bash
# OLD (v2.0)
python generate_workflow_json.py --output workflow.json

# NEW (v3.0) - Option 1: Add --project flag
python generate_workflow_json.py --project "YourProject" --output workflow.json

# NEW (v3.0) - Option 2: Use config file
cp config/project-template.json myproject.json
# Edit myproject.json
python generate_workflow_json.py --config myproject.json --output workflow.json
```

#### Backward Compatibility

v3.0 maintains backward compatibility with HN-DC03:

```bash
# This still works exactly as v2.0
python generate_workflow_json.py --project "HN-DC03" --output workflow.json
```

### 📝 Notes

- All Python scripts syntax-verified with `python3 -m py_compile`
- Comprehensive test cases included for multi-project scenarios
- Documentation updated to reflect generic, reusable design

---

## [2.0.0] - 2026-06-24 (Earlier)

### 🎉 Added

- Multi-branch workflow architecture (IF/ELSE routing by document type)
- Knowledge base segregation strategy (Technical/Legal/Procurement/Meeting)
- Quantitative risk scoring (0-100 scale with Go/No-Go decisions)
- Jinja2 template outputs (structured formatting, not LLM-generated)
- Domain-specific prompts for each branch
- Context-aware recommendation engine (`generate_context_aware_recommendations.py`)
- Comprehensive security guides (prompt injection, RAG poisoning, tool sandboxing)

### 🔧 Changed

- Replaced binary approval gates with scored risk assessment
- Added enterprise workflow patterns documentation
- Included license risk analysis for SaaS restrictions

### ✅ Fixed

- Mixed technical/legal reasoning causing hallucinations
- Inconsistent output formatting across runs
- Missing evidence tracking in risk assessments

---

## [1.0.0] - 2026-06-24 (Initial Release)

### 🎉 Added

- Basic search matrix generation (`build_search_matrix.py`)
- Evidence scoring framework (`score_evidence.py`)
- Safety gate classifications
- Translation rules for Chinese queries
- Compliance boundaries documentation
- CAC regulation checklist

---

## Version Comparison

| Feature | v1.0 | v2.0 | v3.0 |
|---------|------|------|------|
| Search Matrix | ✅ | ✅ | ✅ |
| Evidence Scoring | ✅ | ✅ | ✅ |
| Multi-Branch Workflows | ❌ | ✅ | ✅ |
| KB Segregation | ❌ | ✅ | ✅ |
| Risk Scoring (0-100) | ❌ | ✅ | ✅ |
| Jinja2 Templates | ❌ | ✅ | ✅ |
| **Multi-Project Support** | ❌ | ❌ | ✅ |
| **Config Files** | ❌ | ❌ | ✅ |
| **Dynamic Prompts** | ❌ | ❌ | ✅ |
| HN-DC03 Hardcoded | N/A | Yes | ❌ (Fixed) |

---

## Future Roadmap

### v3.1 (Planned)

- [ ] Pre-built industry templates (data-center, manufacturing, construction)
- [ ] Automated KB population from project docs
- [ ] Multi-language prompt templates (Chinese, English, Vietnamese)
- [ ] Integration with popular CI/CD pipelines

### v3.2 (Planned)

- [ ] Visual workflow editor (web-based config UI)
- [ ] Collaborative review workflows (multi-user approval)
- [ ] Advanced analytics dashboard
- [ ] Plugin system for custom branches

### v4.0 (Future)

- [ ] Native Dify plugin (no JSON import needed)
- [ ] Real-time collaboration features
- [ ] AI-assisted config generation
- [ ] Cross-project knowledge sharing

---

**Current Version:** 3.0.0  
**Status:** Production-ready  
**Last Updated:** 2026-06-24
