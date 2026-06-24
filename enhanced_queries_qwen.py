#!/usr/bin/env python3
"""Enhanced query generator for China AI research based on real-world examples.

This script generates targeted queries based on the learning from:
- Terminology normalization (AI Skill 仓库 → 智能体/Agent/MCP/插件/工作流)
- Specific repo names (Dify, FastGPT, Qwen-Agent, MS-Agent, AgentScope)
- Platform-specific searches (ModelScope, Coze, WeChat AI)
"""

import csv
from urllib.parse import quote_plus

def generate_enhanced_queries():
    """Generate enhanced queries based on real research patterns."""
    
    queries = []
    
    # Group 1: Terminology Normalization (from user's insight)
    terminology_queries = [
        ("terminology", "AI Skill 仓库 智能体 技能库", "baidu", "Find how China calls 'skill repository'"),
        ("terminology", "Agent Skills 技能库 MCP 插件", "baidu", "Find Agent Skills + MCP terminology"),
        ("terminology", "智能体 插件 工作流 开源", "gitee", "Find open-source agent/plugin/workflow"),
        ("terminology", "大模型 智能体 工具调用 MCP", "baidu", "Find LLM agent tool-calling + MCP"),
    ]
    
    # Group 2: Specific High-Star Repos (from evidence table)
    specific_repos = [
        ("repo_dify", "langgenius dify agentic workflow", "github", "Dify official repo - 146k stars"),
        ("repo_fastgpt", "labring FastGPT RAG workflow", "github", "FastGPT - 28.6k stars, knowledge-based"),
        ("repo_agentscope", "agentscope-ai agentscope multi-agent", "github", "AgentScope - 27.1k stars, Alibaba"),
        ("repo_qwen_agent", "QwenLM Qwen-Agent MCP tool-calling", "github", "Qwen-Agent - 16.6k stars, official"),
        ("repo_ms_agent", "modelscope ms-agent Agent Skills v2", "github", "MS-Agent - closest to 'AI Skill 仓库'"),
        ("repo_aiwaves", "aiwaves-cn agents self-evolving", "github", "aiwaves Agents - 5.9k stars, Apache-2.0"),
        ("repo_lightagent", "wxai-space LightAgent MCP skill Qwen", "github", "LightAgent - lightweight, supports Qwen/DeepSeek"),
    ]
    
    # Group 3: ModelScope Platform Specific
    modelscope_queries = [
        ("modelscope_platform", "ModelScope 智能体 MCP 官方文档", "baidu", "ModelScope official agent docs"),
        ("modelscope_skills", "ModelScope Agent Skills v2 DeepResearch", "bing", "Find Agent Skills v2 features"),
        ("modelscope_qwen", "通义千问 Agent 官方文档 DashScope", "baidu", "Qwen Agent + DashScope integration"),
        ("modelscope_workflow", "ModelScope 工作流 可视化编排", "baidu", "ModelScope visual workflow orchestration"),
    ]
    
    # Group 4: Latest Trends 2026 (from user's summary)
    trend_2026 = [
        ("trend_2026", "中国 AI 应用 智能体 最新进展 2026", "baidu", "Latest AI agent trends in China 2026"),
        ("trend_wechat", "微信 AI 智能体 Tencent agent WeChat", "bing", "WeChat AI agent integration (FT news)"),
        ("trend_mcp", "MCP 智能体 开源 GitHub 2026", "github", "MCP-based agents 2026"),
        ("trend_deepresearch", "AI Deep Research 代码生成 视频生成", "baidu", "Deep research + code/video generation"),
    ]
    
    # Group 5: Compliance & Risk (from CAC regulation)
    compliance_queries = [
        ("compliance_cac", "生成式人工智能服务管理暂行办法 CAC 2023", "baidu", "CAC generative AI regulation"),
        ("compliance_algorithm", "算法备案 大模型备案 中国", "baidu", "Algorithm filing requirements"),
        ("risk_security", "AI 智能体 数据泄露 提示注入 安全", "bing", "Agent security risks: data leak, prompt injection"),
    ]
    
    # Group 6: Secondary Sources (CSDN, OSChina, Zhihu)
    secondary_sources = [
        ("csdn_tutorial", "CSDN 智能体 MCP 教程 2026", "baidu", "CSDN tutorials (secondary source)"),
        ("oschina_discuss", "开源中国 AI Agent 讨论", "baidu", "OSChina discussions"),
        ("zhihu_analysis", "知乎 AI Agent 应用 中国", "baidu", "Zhihu analysis articles"),
    ]
    
    all_queries = (
        terminology_queries +
        specific_repos +
        modelscope_queries +
        trend_2026 +
        compliance_queries +
        secondary_sources
    )
    
    # Build full query matrix with URLs
    source_urls = {
        "baidu": "https://www.baidu.com/s?wd={q}",
        "github": "https://github.com/search?q={q}&type=repositories",
        "gitee": "https://search.gitee.com/?q={q}",
        "bing": "https://cn.bing.com/search?q={q}",
    }
    
    result = []
    for group, query_zh, source, purpose in all_queries:
        url_template = source_urls.get(source, "")
        url = url_template.format(q=quote_plus(query_zh)) if url_template else ""
        
        result.append({
            "group": group,
            "query_zh": query_zh,
            "source": source,
            "purpose": purpose,
            "manual_url": url,
            "priority": "high" if group.startswith(("repo_", "modelscope_")) else "medium"
        })
    
    return result

if __name__ == "__main__":
    queries = generate_enhanced_queries()
    
    # Write to CSV
    output_file = "enhanced_qwen_china_ai.csv"
    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["group", "query_zh", "source", "purpose", "manual_url", "priority"])
        writer.writeheader()
        writer.writerows(queries)
    
    print(f"✅ Generated {len(queries)} enhanced queries")
    print(f"📁 Output: {output_file}")
    print("\n🔥 Top Priority Queries:")
    for q in queries[:10]:
        if q["priority"] == "high":
            print(f"  • {q['query_zh']} [{q['source']}]")
            print(f"    → {q['manual_url'][:80]}...")
