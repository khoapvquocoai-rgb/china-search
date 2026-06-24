# Usage Decision Template (v3.0)

When to use / when NOT to use china-search skill and its components.

**Version:** 3.0  
**Status:** Updated for multi-project support  

---

## When to Use china-search v3.0

### ✅ Ideal Scenarios

1. **Multi-Project Environments**
   - You manage multiple projects (data centers, factories, construction sites)
   - Need reusable workflows across different projects
   - Want to avoid code duplication for each project

2. **Diverse Document Types**
   - Your project involves HSYC, contracts, vendor datasheets, meeting minutes
   - Need domain-specific analysis per document type
   - Want automated routing to appropriate review branches

3. **Zero-Budget Research**
   - No budget for paid APIs or enterprise tools
   - Need China mainland research capabilities
   - Public sources are sufficient for your needs

4. **Quantitative Risk Assessment**
   - Need scored risk assessment (0-100) instead of binary pass/fail
   - Want evidence-backed Go/No-Go decisions
   - Require audit trail for compliance

5. **Enterprise Security Requirements**
   - Self-hosted deployment is mandatory
   - Sensitive data cannot go to cloud demos
   - Need prompt injection and RAG poisoning mitigation

### 🎯 Best Fit Projects

| Project Type | Document Volume | Complexity | Recommendation |
|--------------|-----------------|------------|----------------|
| Data Center | High (HSYC, specs) | High | ✅ Perfect fit |
| Manufacturing | Medium (drawings, BOMs) | Medium-High | ✅ Great fit |
| Construction | High (contracts, RFIs) | High | ✅ Perfect fit |
| Software Dev | Low-Medium | Low-Medium | ⚠️ Consider simpler tools |
| Single Document Review | Low | Low | ❌ Overkill |

---

## When NOT to Use china-search

### ❌ Avoid If

1. **Simple Use Cases**
   - Single document review only
   - No need for multi-branch workflows
   - Basic Q&A without risk scoring

2. **Cloud-Only Deployments**
   - Cannot self-host Dify or FastGPT
   - Must use SaaS-only solutions
   - Sensitive data must stay in approved clouds

3. **Real-Time Requirements**
   - Sub-second response times needed
   - Live collaboration with multiple users
   - Streaming updates required

4. **Non-Chinese Research**
   - Focus is entirely on Western markets
   - No China mainland sources needed
   - English-only documentation

5. **Budget Available for Enterprise Tools**
   - Can afford commercial RAG platforms
   - Need built-in SSO, RBAC, auditing
   - Prefer vendor support over open source

### 🔧 Better Alternatives

| Scenario | Recommended Alternative | Why |
|----------|------------------------|-----|
| Simple document Q&A | LangChain + vector DB | Less overhead, easier setup |
| Cloud-only deployment | Commercial RAG SaaS | Built-in security compliance |
| Real-time collaboration | Dedicated collaboration platform | Better UX for live editing |
| Enterprise features needed | Paid platform (e.g., Coveo) | SSO, RBAC, SLA included |
| Non-Chinese research | Generic search tools | No China-specific features needed |

---

## Component-Level Decisions

### generate_workflow_json.py

**Use when:**
- ✅ Need to generate Dify workflows programmatically
- ✅ Managing multiple projects with similar structures
- ✅ Want to version-control workflow configurations

**Avoid when:**
- ❌ Comfortable with manual Dify Studio UI
- ❌ Single project, one-time setup
- ❌ Need visual drag-and-drop editor

### generate_context_aware_recommendations.py

**Use when:**
- ✅ Evaluating multiple AI tools for your project
- ✅ Need structured comparison with metrics
- ✅ Want license risk analysis upfront

**Avoid when:**
- ❌ Already decided on tool stack
- ❌ Quick PoC without deep analysis
- ❌ Team already experts in selected tools

### build_search_matrix.py

**Use when:**
- ✅ Need systematic China search queries
- ✅ Researching vendors/products in Chinese market
- ✅ Want to ensure comprehensive coverage

**Avoid when:**
- ❌ English-only research sufficient
- ❌ Single query, ad-hoc search
- ❌ Familiar with Chinese search patterns already

### score_evidence.py

**Use when:**
- ✅ Need quantitative reliability scores
- ✅ Comparing multiple sources
- ✅ Audit trail required for decisions

**Avoid when:**
- ❌ Trust all sources equally
- ❌ Single authoritative source exists
- ❌ Speed more important than accuracy

---

## Industry-Specific Guidance

### Data Centers

**✅ Highly Recommended**
- Complex HSYC/HSMT reviews
- Multi-vendor comparisons
- Regulatory compliance (TIA-942, Uptime Tier)

**Key Features to Use:**
- Technical branch for HSYC reviews
- Procurement branch for vendor comparisons
- Risk scoring for compliance gaps

### Manufacturing

**✅ Recommended**
- Drawing and BOM reviews
- Supplier qualification
- Quality standard compliance

**Key Features to Use:**
- Custom document types (DRAWING, BOM)
- Technical branch with industry context
- Meeting branch for production issues

### Construction

**✅ Highly Recommended**
- Contract reviews
- RFI management
- Multi-stakeholder coordination

**Key Features to Use:**
- Legal branch for contracts
- Meeting branch for RFIs
- Risk scoring for liability assessment

### Software Development

**⚠️ Conditional**
- Only if China market research needed
- Vendor evaluation for Chinese SaaS

**Consider Simpler Alternatives:**
- GitHub-based research tools
- Standard RAG for documentation Q&A

---

## Team Skill Level Guidance

### Business Users (Non-Technical)

**✅ Use:**
- Dify visual interface
- Pre-generated workflows from `generate_workflow_json.py`
- Interactive recommendations from `generate_context_aware_recommendations.py`

**❌ Avoid:**
- Direct Python script modifications
- Custom prompt engineering
- Manual KB management

### Technical Teams

**✅ Use:**
- All scripts with custom parameters
- Config file approach for multi-project
- Custom branch development

**🔧 Extend:**
- Modify prompts for industry specifics
- Add custom document type parsers
- Integrate with internal systems

### Mixed Teams

**✅ Strategy:**
- Technical team: Manage configs and KBs
- Business users: Use Dify/FastGPT UI
- Shared: Review outputs and risk scores

---

## Budget Considerations

### $0 Budget

**✅ Perfect Fit:**
- All tools are open source (Apache-2.0)
- Self-hosted deployment free
- Public China search sources free

**⚠️ Trade-offs:**
- Time investment for setup
- Self-maintenance responsibility
- No vendor support

### Low Budget (<$100/month)

**✅ Good Fit:**
- Host on cheap VPS ($5-20/month)
- Optional: Paid model API for better quality
- Still mostly free tools

**💰 Recommended Spending:**
- VPS hosting: $10-20/month
- Model API (optional): $50-80/month
- Domain/SSL: $10/year

### Enterprise Budget

**⚠️ Consider:**
- Commercial RAG platforms may offer better ROI
- Built-in enterprise features (SSO, RBAC)
- Vendor support and SLAs

**✅ Still Use china-search If:**
- China-specific features critical
- Multi-project reusability valuable
- Open source preference strong

---

## Timeline Considerations

### Quick Demo (<1 week)

**✅ Use:**
- Pre-configured templates
- Default document types
- Interactive recommendation generator

**⚡ Fast Path:**
```bash
python generate_context_aware_recommendations.py
# Answer questions, get instant workflow
```

### PoC (1-4 weeks)

**✅ Use:**
- Custom config files
- Industry-specific tuning
- Knowledge base population

**📋 Steps:**
1. Week 1: Setup and config
2. Week 2: KB population
3. Week 3: Testing and refinement
4. Week 4: Stakeholder demo

### Production (>1 month)

**✅ Use:**
- Full multi-project architecture
- Custom branch development
- Integration with internal systems

**🏗️ Consider:**
- CI/CD pipeline integration
- Monitoring and logging
- Backup and disaster recovery

---

## Decision Matrix

| Factor | Weight | china-search Score | Verdict |
|--------|--------|-------------------|---------|
| Multi-project support | High | 10/10 | ✅ Excellent |
| Zero-budget friendly | High | 10/10 | ✅ Excellent |
| China research focus | High | 10/10 | ✅ Excellent |
| Ease of setup | Medium | 6/10 | ⚠️ Moderate |
| Enterprise features | Medium | 5/10 | ⚠️ Limited |
| Real-time collaboration | Low | 3/10 | ❌ Not suitable |
| Cloud-only deployment | Low | 2/10 | ❌ Avoid |

**Overall:** Best for multi-project, zero-budget, China-focused research with self-hosted deployment.

---

## Related Documentation

- [SKILL.md](../SKILL.md) - Complete technical documentation
- [README.md](../README.md) - Quick start guide
- [multi-branch-workflow-template.md](multi-branch-workflow-template.md) - Workflow patterns
- [risk-assessment-checklist.md](risk-assessment-checklist.md) - Security considerations

---

**Version:** 3.0  
**Last Updated:** 2026-06-24  
**Next Review:** After first multi-project deployment
