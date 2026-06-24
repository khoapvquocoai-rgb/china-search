#!/usr/bin/env python3
"""Generate context-aware recommendations with Priority 1 & 2 learnings.

This script creates recommendations based on:
1. Clear grouping by purpose (PoC vs R&D)
2. "When to use / When NOT to use" tables
3. Specific license risk warnings
4. Security risk mitigation strategies
5. Hybrid architecture proposals
6. Named use cases with metrics
7. Multi-project support (v3.0)
"""

import json
from datetime import datetime
from typing import Dict, List, Optional


def get_project_context() -> Dict:
    """Ask user for project context or use defaults."""
    
    context_questions = {
        "project_name": "Tên project/dự án? (ví dụ: MyDataCenter)",
        "industry": "Ngành nghề? (data-center|construction|manufacturing|other)",
        "business_need": "Nhu cầu kinh doanh cụ thể? (ví dụ: vendor review, document Q&A)",
        "team_skills": "Đội ngũ kỹ thuật hay nghiệp vụ? (technical/business)",
        "deployment_type": "Cloud, self-hosted, hay hybrid?",
        "budget": "Budget API: $0, thấp (<$100/mo), hay enterprise?",
        "timeline": "Timeline: Quick demo (<1 tuần), PoC (1-4 tuần), hay Production (>1 tháng)?",
        "data_sensitivity": "Dữ liệu nhạy cảm? (contracts/bids/internal reports)",
        "document_types": "Loại tài liệu chính? (HSYC/contract/vendor datasheet/meeting minutes)",
    }
    
    print("\n📋 Vui lòng cung cấp context project:")
    print("=" * 60)
    
    context = {}
    for key, question in context_questions.items():
        answer = input(f"{question} [Enter để skip]: ").strip()
        context[key] = answer if answer else "Not specified"
    
    return context


def categorize_tools_by_purpose() -> Dict[str, List[Dict]]:
    """Group tools into clear categories based on purpose."""
    
    return {
        "production_poc": {
            "name": "Nhóm 1: Dùng NGAY cho PoC Nghiệp Vụ",
            "description": "Công cụ production-ready, setup nhanh, phù hợp business users",
            "tools": [
                {
                    "name": "Dify",
                    "role": "Nền tảng workflow tổng hợp",
                    "stars": 146429,
                    "license": "Apache 2.0-based (check commercial terms)",
                    "saas_restriction": False,
                    "use_when": [
                        "Cần dựng nhanh AI app nội bộ (workflow phê duyệt, chatbot RAG)",
                        "Demo cho lãnh đạo trong thời gian ngắn",
                        "Tích hợp nhiều models và tools qua visual interface",
                        "Multi-project support với config files"
                    ],
                    "avoid_when": [
                        "Cần kiểm soát cực sâu từng bước agent bằng code",
                        "Muốn tránh license có điều kiện bổ sung",
                        "Team chỉ có technical experts, không cần no-code"
                    ],
                    "priority": "Ưu tiên số 1 cho PoC nhanh"
                },
                {
                    "name": "FastGPT",
                    "role": "Nền tảng RAG/hỏi đáp tài liệu",
                    "stars": 28614,
                    "license": "Apache-2.0 (KHÔNG cho SaaS without permission)",
                    "saas_restriction": True,
                    "use_when": [
                        "Hệ thống hỏi đáp knowledge base/tài liệu nội bộ",
                        "Phòng ban cần tool trực quan, ít coding",
                        "Tối ưu RAG retrieval cho documents lớn",
                        "Document types đa dạng (HSYC, contracts, specs)"
                    ],
                    "avoid_when": [
                        "Muốn mở dịch vụ SaaS thương mại (license restriction!)",
                        "Cần multi-agent orchestration phức tạp",
                        "Customization sâu vượt quá visual workflow builder"
                    ],
                    "priority": "Ưu tiên số 1 cho RAG tài liệu"
                }
            ]
        },
        
        "research_rd": {
            "name": "Nhóm 2: Dùng cho R&D Kỹ Thuật",
            "description": "Frameworks cho custom development, research, advanced features",
            "tools": [
                {
                    "name": "Qwen-Agent",
                    "role": "Framework custom agent với MCP/tool calling",
                    "stars": 16600,
                    "license": "Apache-2.0 (clean)",
                    "saas_restriction": False,
                    "use_when": [
                        "Đội kỹ thuật Python muốn viết agent tùy biến",
                        "Ưu tiên Qwen/ModelScope ecosystem",
                        "Cần MCP, Code Interpreter, Browser Assistant",
                        "Multi-project với dynamic configuration"
                    ],
                    "avoid_when": [
                        "Người dùng nghiệp vụ không code muốn drag-and-drop",
                        "Cần enterprise features built-in (SSO, RBAC)",
                        "Multi-model support ngoài Qwen là priority"
                    ],
                    "priority": "Ưu tiên cho custom agent kỹ thuật"
                },
                {
                    "name": "MS-Agent",
                    "role": "Nghiên cứu 'AI Skill 仓库' đúng nghĩa",
                    "stars": 4300,
                    "license": "Apache-2.0 (clean)",
                    "saas_restriction": False,
                    "use_when": [
                        "Nghiên cứu skill retrieval/orchestration",
                        "DeepResearch, Code Genesis, video workflows",
                        "Agent Skills v2 library exploration",
                        "Reusable skills across multiple projects"
                    ],
                    "avoid_when": [
                        "Cần nền tảng mature, stable cho production ngay",
                        "Community size nhỏ là concern",
                        "Documentation tiếng Trung là barrier"
                    ],
                    "priority": "Ưu tiên cho R&D AI Skill/MCP"
                },
                {
                    "name": "AgentScope",
                    "role": "Multi-agent orchestration với governance",
                    "stars": 27100,
                    "license": "Apache-2.0 (clean)",
                    "saas_restriction": False,
                    "use_when": [
                        "Nghiên cứu multi-agent systems phức tạp",
                        "Cần permission control, sandbox, human-in-the-loop",
                        "Event system và multi-tenancy requirements",
                        "Cross-project agent coordination"
                    ],
                    "avoid_when": [
                        "Cần dựng app nghiệp vụ nhanh cho non-technical users",
                        "Single-agent use case (overkill)",
                        "Learning curve cao là blocker"
                    ],
                    "priority": "Ưu tiên cho multi-agent có kiểm soát"
                }
            ]
        }
    }


def generate_hybrid_architecture(context: Dict) -> str:
    """Propose hybrid architecture based on context."""
    
    timeline = context.get("timeline", "")
    team = context.get("team_skills", "")
    budget = context.get("budget", "")
    project_name = context.get("project_name", "Project")
    
    architecture = []
    
    # Production layer recommendation
    if "quick" in timeline.lower() or "demo" in timeline.lower():
        architecture.append(f"✅ **Layer 1 - Production PoC ({project_name}):** Dify + FastGPT")
        architecture.append("   - Dify: Workflow orchestration, enterprise features")
        architecture.append("   - FastGPT: Knowledge base/RAG specialist")
        architecture.append("   - Timeline: 1-2 weeks to first demo")
        architecture.append("   - Config: Use project-template.json for easy setup")
    
    # Research layer recommendation
    if team.lower() == "technical" or "rd" in timeline.lower():
        architecture.append("\n✅ **Layer 2 - Research & Customization:**")
        if "$0" in budget.upper():
            architecture.append("   - Qwen-Agent: Self-host Qwen models, zero API cost")
        architecture.append("   - MS-Agent: Skill-based agents, DeepResearch")
        architecture.append("   - AgentScope: Multi-agent orchestration")
        architecture.append("   - Timeline: 3-6 weeks for custom development")
        architecture.append("   - Benefit: Reusable across multiple projects")
    
    # Integration strategy
    architecture.append("\n🔗 **Integration Strategy:**")
    architecture.append("   - Use Dify/FastGPT APIs as entry points")
    architecture.append("   - Call Qwen-Agent/MS-Agent for complex tasks")
    architecture.append("   - AgentScope coordinates multi-agent workflows")
    architecture.append("   - Share skills/configs across projects")
    
    return "\n".join(architecture)


def generate_named_use_cases(context: Dict) -> List[Dict]:
    """Create specific named use cases instead of generic descriptions."""
    
    project_name = context.get("project_name", "Project").lower().replace(' ', '_').replace('-', '_')
    business_need = context.get("business_need", "general AI tasks")
    doc_types = context.get("document_types", "")
    
    use_cases = []
    
    # Generate context-specific use cases
    if "vendor" in business_need.lower() or "review" in business_need.lower():
        use_cases.append({
            "name": f"review_{project_name}_vendor_matrix",
            "description": "Review vendor datasheets, compare specifications, flag risks",
            "tool": "FastGPT or Dify",
            "metrics": ["accuracy_rate > 90%", "response_time < 5s", "false_positive_rate < 5%"]
        })
    
    if "document" in business_need.lower() or "qa" in business_need.lower():
        use_cases.append({
            "name": f"{project_name}_document_qa_bot",
            "description": f"Q&A over project documents ({doc_types if doc_types else 'HSYC, HSMT, contracts, specs'})",
            "tool": "FastGPT",
            "metrics": ["answer_accuracy > 85%", "source_citation_rate = 100%", "latency < 3s"]
        })
    
    if "report" in business_need.lower() or "leader" in business_need.lower():
        use_cases.append({
            "name": f"generate_{project_name}_executive_report",
            "description": "Auto-generate executive summaries from raw data",
            "tool": "Dify workflow",
            "metrics": ["completion_rate > 95%", "human_edit_time < 10min", "stakeholder_satisfaction > 4/5"]
        })
    
    # Multi-project use case (v3.0 feature)
    use_cases.append({
        "name": f"multi_project_workflow_generator",
        "description": "Generate workflows for multiple projects using config files",
        "tool": "china-search v3.0 scripts",
        "metrics": ["setup_time < 5min per project", "code_reuse_rate = 100%", "config_maintenance_effort < 1hr/month"]
    })
    
    # Default use cases if none matched
    if len(use_cases) == 1:  # Only has multi-project
        use_cases.insert(0, {
            "name": f"{project_name}_ai_assistant",
            "description": f"General AI assistant for {business_need}",
            "tool": "Dify",
            "metrics": ["task_completion_rate > 80%", "user_satisfaction > 4/5"]
        })
    
    return use_cases


def generate_security_warnings(context: Dict) -> List[str]:
    """Generate specific security warnings based on context."""
    
    warnings = []
    data_sensitivity = context.get("data_sensitivity", "").lower()
    
    if "contract" in data_sensitivity or "bid" in data_sensitivity or "internal" in data_sensitivity:
        warnings.append("🚨 **CRITICAL:** Never upload contracts, bids, or internal reports to cloud demos without legal/security approval.")
        warnings.append("✅ **Mitigation:** Use self-hosted deployment only for sensitive data.")
    
    warnings.append("⚠️ **Prompt Injection Risk:** Validate all uploaded documents before indexing into RAG.")
    warnings.append("⚠️ **Tool Execution Risk:** If using Qwen-Agent/MS-Agent Code Interpreter, implement sandbox with:")
    warnings.append("   - Filesystem isolation (read-only mounts)")
    warnings.append("   - Network access control (whitelist APIs only)")
    warnings.append("   - Timeout limits (max 30s per execution)")
    
    # v3.0: Multi-project security
    warnings.append("\n⚠️ **Multi-Project Security (v3.0):**")
    warnings.append("   - Isolate knowledge bases per project (KB-{project}-*)")
    warnings.append("   - Review config files for sensitive data before sharing")
    warnings.append("   - Use separate deployments for different security levels")
    
    return warnings


def generate_recommendation_report(context: Optional[Dict] = None) -> str:
    """Generate complete recommendation report with all learnings."""
    
    if context is None:
        context = get_project_context()
    
    tools_by_purpose = categorize_tools_by_purpose()
    
    report = []
    report.append("# 🎯 Khuyến Nghị Sử Dụng Công Cụ AI Trung Quốc (v3.0)")
    report.append(f"\n**Project:** {context.get('project_name', 'Not specified')}")
    report.append(f"**Industry:** {context.get('industry', 'Not specified')}")
    report.append(f"**Business Need:** {context.get('business_need', 'Not specified')}")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("\n---\n")
    
    # Section 1: Grouped Recommendations
    report.append("## 1. Phân Nhóm Theo Mục Đích Sử Dụng\n")
    
    for category, data in tools_by_purpose.items():
        report.append(f"### {data['name']}")
        report.append(f"*{data['description']}*\n")
        
        report.append("| Công cụ | Vai trò | Stars | License | Ưu tiên |")
        report.append("|---------|---------|-------|---------|---------|")
        
        for tool in data['tools']:
            saas_warning = " ⚠️ NO SaaS" if tool.get('saas_restriction') else ""
            report.append(f"| **{tool['name']}** | {tool['role']} | {tool['stars']:,} | {tool['license']}{saas_warning} | {tool['priority']} |")
        
        report.append("")
        
        # Detailed "When to use / When NOT to use"
        for tool in data['tools']:
            report.append(f"#### {tool['name']}\n")
            
            report.append("**✅ Nên dùng khi:**")
            for use_case in tool['use_when']:
                report.append(f"- {use_case}")
            
            report.append("\n**❌ Không nên dùng khi:**")
            for avoid_case in tool['avoid_when']:
                report.append(f"- {avoid_case}")
            
            report.append("")
        
        report.append("---\n")
    
    # Section 2: Hybrid Architecture
    report.append("## 2. Kiến Trúc Hybrid Đề Xuất\n")
    report.append(generate_hybrid_architecture(context))
    report.append("\n---\n")
    
    # Section 3: Named Use Cases
    report.append("## 3. Use Cases Cụ Thể Với Metrics\n")
    
    use_cases = generate_named_use_cases(context)
    for i, uc in enumerate(use_cases, 1):
        report.append(f"### {i}. `{uc['name']}`")
        report.append(f"- **Description:** {uc['description']}")
        report.append(f"- **Recommended Tool:** {uc['tool']}")
        report.append(f"- **Success Metrics:**")
        for metric in uc['metrics']:
            report.append(f"  - {metric}")
        report.append("")
    
    report.append("---\n")
    
    # Section 4: Security Warnings
    report.append("## 4. Cảnh Báo An Toàn Quan Trọng\n")
    
    warnings = generate_security_warnings(context)
    for warning in warnings:
        report.append(warning)
        report.append("")
    
    # Section 5: License Risk Summary
    report.append("## 5. Tóm Tắt Rủi Ro License\n")
    report.append("| Công cụ | Commercial Use | SaaS Provisioning | Action Required |")
    report.append("|---------|----------------|-------------------|-----------------|")
    
    for category, data in tools_by_purpose.items():
        for tool in data['tools']:
            commercial = "Allowed" if "Apache-2.0 (clean)" in tool['license'] else "Check Terms"
            saas = "✅ Allowed" if not tool.get('saas_restriction') else "❌ Forbidden without permission"
            action = "None" if "clean" in tool['license'] else "Review LICENSE + COMMERCIAL files"
            report.append(f"| {tool['name']} | {commercial} | {saas} | {action} |")
    
    report.append("\n---\n")
    
    # Section 6: Next Steps
    report.append("## 6. Các Bước Tiếp Theo\n")
    report.append("1. ✅ Review license terms cho tools được chọn")
    report.append("2. ✅ Setup self-hosted environment (tránh cloud demos cho sensitive data)")
    report.append("3. ✅ Chạy PoC với named use cases ở trên")
    report.append("4. ✅ Measure against defined metrics")
    report.append("5. ✅ Security review trước khi production deployment")
    report.append("6. ✅ Legal approval nếu có commercial/SaaS plans")
    report.append("7. ✅ **NEW v3.0:** Create project config file for easy reuse across projects")
    
    return "\n".join(report)


if __name__ == "__main__":
    print("🚀 Context-Aware AI Tool Recommendation Generator (v3.0)")
    print("=" * 60)
    print("\nThis tool generates recommendations based on:")
    print("  • Clear grouping (PoC vs R&D)")
    print("  • 'When to use / When NOT to use' guidance")
    print("  • Specific license risk warnings")
    print("  • Security mitigation strategies")
    print("  • Hybrid architecture proposals")
    print("  • Named use cases with metrics")
    print("  • **NEW v3.0:** Multi-project support with config files\n")
    
    report = generate_recommendation_report()
    
    # Save to file
    output_file = "recommendation_report.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"✅ Report generated: {output_file}")
    print("\n" + report)
