#!/usr/bin/env python3
"""Generate detailed comparison matrix for top 5 China AI repos."""

import csv
from datetime import datetime

def generate_shortlist_matrix():
    """Create comprehensive comparison of Dify, FastGPT, Qwen-Agent, MS-Agent, AgentScope."""
    
    repos = {
        "Dify": {
            "url": "https://github.com/langgenius/dify",
            "stars": 146429,
            "forks": 23032,
            "language": "TypeScript/Python",
            "license": "MIT (check commercial terms)",
            "last_update": "2026-06-24 (1h ago)",
            "focus": "Agentic workflow platform",
            "key_features": [
                "Visual workflow builder",
                "RAG pipeline orchestration",
                "Multi-agent collaboration",
                "Production-ready deployment",
                "API-first design",
                "SSO/RBAC support",
                ".agents/skills directory"
            ],
            "use_cases": [
                "Enterprise app development",
                "Customer service bots",
                "Document Q&A systems",
                "Workflow automation"
            ],
            "pros": [
                "Largest community (146k⭐)",
                "Very active development",
                "Production-ready",
                "Comprehensive documentation",
                "Enterprise features built-in"
            ],
            "cons": [
                "May be overkill for simple use cases",
                "Resource-intensive deployment",
                "Commercial license restrictions possible"
            ],
            "deployment": "Docker/K8s, Cloud SaaS available",
            "learning_curve": "Medium",
            "best_for": "Enterprise production deployments"
        },
        
        "FastGPT": {
            "url": "https://github.com/labring/FastGPT",
            "stars": 28600,
            "forks": 3200,
            "language": "TypeScript/Node.js",
            "license": "Apache-2.0 (commercial check needed)",
            "last_update": "2026-06-22 (v4.14.25)",
            "focus": "Knowledge-based RAG platform",
            "key_features": [
                "Visual AI workflow orchestration",
                "Data processing pipelines",
                "RAG retrieval optimization",
                "Knowledge base management",
                "Multi-model support",
                "Plugin ecosystem"
            ],
            "use_cases": [
                "Document-based Q&A",
                "Enterprise knowledge management",
                "Customer support with context",
                "Research assistance"
            ],
            "pros": [
                "Strong RAG capabilities",
                "User-friendly interface",
                "Good for non-technical users",
                "Active community (28k⭐)"
            ],
            "cons": [
                "Less flexible than Dify for complex workflows",
                "License has commercial restrictions",
                "Smaller ecosystem than Dify"
            ],
            "deployment": "Docker, Self-hosted or SaaS",
            "learning_curve": "Low-Medium",
            "best_for": "Knowledge-based applications"
        },
        
        "Qwen-Agent": {
            "url": "https://github.com/QwenLM/Qwen-Agent",
            "stars": 16600,
            "forks": 1800,
            "language": "Python",
            "license": "Apache-2.0",
            "last_update": "2026-06 (active)",
            "focus": "Alibaba/Qwen ecosystem agent framework",
            "key_features": [
                "Browser Assistant",
                "Code Interpreter",
                "MCP support",
                "RAG integration",
                "Tool calling framework",
                "Chrome extension",
                "DashScope API integration"
            ],
            "use_cases": [
                "Qwen model applications",
                "Browser automation agents",
                "Code generation tasks",
                "Multi-tool orchestration"
            ],
            "pros": [
                "Official Alibaba support",
                "Deep Qwen integration",
                "MCP native support",
                "Well-documented in Chinese",
                "Free Apache-2.0 license"
            ],
            "cons": [
                "Tied to Qwen ecosystem",
                "Smaller community than Dify",
                "Less enterprise features"
            ],
            "deployment": "Python package, Easy local deployment",
            "learning_curve": "Medium",
            "best_for": "Qwen-based applications, MCP workflows"
        },
        
        "MS-Agent": {
            "url": "https://github.com/modelscope/ms-agent",
            "stars": 4300,
            "forks": 450,
            "language": "Python",
            "license": "Apache-2.0",
            "last_update": "2026 (Agent Skills v2)",
            "focus": "ModelScope Agent Skills framework",
            "key_features": [
                "Agent Skills v2 library",
                "ms-agent-skills directory",
                "DeepResearch capability",
                "Code Genesis workflow",
                "Video workflow support",
                "WebUI for skill management",
                "Multi-source skill loading"
            ],
            "use_cases": [
                "Skill-based agent development",
                "Research automation",
                "Code generation pipelines",
                "Video content creation"
            ],
            "pros": [
                "Closest to 'AI Skill 仓库' concept",
                "Innovative features (DeepResearch, video)",
                "ModelScope ecosystem integration",
                "Lightweight framework"
            ],
            "cons": [
                "Smaller community (4.3k⭐)",
                "Less mature than Dify/FastGPT",
                "Fewer enterprise features"
            ],
            "deployment": "Python package, ModelScope cloud",
            "learning_curve": "Medium-High",
            "best_for": "Research, skill-based agents, cutting-edge features"
        },
        
        "AgentScope": {
            "url": "https://github.com/modelscope/agentscope",
            "stars": 27100,
            "forks": 2100,
            "language": "Python",
            "license": "Apache-2.0",
            "last_update": "2026-06-16 (v2.0.2)",
            "focus": "Multi-agent framework from Alibaba",
            "key_features": [
                "Multi-agent orchestration",
                "MCP protocol support",
                "Multi-modal agent support",
                "Observability tools",
                "Agent communication protocols",
                "Testing frameworks"
            ],
            "use_cases": [
                "Complex multi-agent systems",
                "Research on agent interactions",
                "Enterprise agent coordination",
                "Multi-modal applications"
            ],
            "pros": [
                "Strong multi-agent capabilities",
                "Alibaba backing (27k⭐)",
                "MCP native support",
                "Good for research + production",
                "Active development"
            ],
            "cons": [
                "Steeper learning curve",
                "More complex than single-agent solutions",
                "Requires understanding of agent patterns"
            ],
            "deployment": "Python package, Scalable to K8s",
            "learning_curve": "High",
            "best_for": "Multi-agent systems, research, complex orchestration"
        }
    }
    
    return repos

def create_comparison_csv(repos, output_file="shortlist_comparison.csv"):
    """Create CSV comparison matrix."""
    
    fields = [
        "Repo", "Stars", "Focus", "License", "Best For", 
        "Learning Curve", "Deployment", "URL"
    ]
    
    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        
        for name, data in repos.items():
            writer.writerow({
                "Repo": name,
                "Stars": data["stars"],
                "Focus": data["focus"],
                "License": data["license"],
                "Best For": data["best_for"],
                "Learning Curve": data["learning_curve"],
                "Deployment": data["deployment"],
                "URL": data["url"]
            })
    
    print(f"✅ Created comparison CSV: {output_file}")

def create_usage_recommendations(repos):
    """Generate usage recommendations based on use cases."""
    
    recommendations = {
        "Enterprise Production (Quick Start)": {
            "primary": "Dify",
            "reason": "Largest community, production-ready, enterprise features",
            "alternatives": ["FastGPT"],
            "timeline": "1-2 weeks to PoC"
        },
        
        "Knowledge-Based Applications": {
            "primary": "FastGPT",
            "reason": "Best RAG capabilities, user-friendly for non-tech users",
            "alternatives": ["Dify"],
            "timeline": "1 week to PoC"
        },
        
        "Qwen Ecosystem Projects": {
            "primary": "Qwen-Agent",
            "reason": "Official Alibaba support, deep Qwen integration, MCP native",
            "alternatives": ["MS-Agent", "AgentScope"],
            "timeline": "2-3 weeks to PoC"
        },
        
        "Cutting-Edge Research": {
            "primary": "MS-Agent",
            "reason": "Agent Skills v2, DeepResearch, video workflows",
            "alternatives": ["AgentScope"],
            "timeline": "3-4 weeks to PoC"
        },
        
        "Multi-Agent Systems": {
            "primary": "AgentScope",
            "reason": "Best multi-agent orchestration, MCP support",
            "alternatives": ["Dify"],
            "timeline": "4-6 weeks to PoC"
        },
        
        "Budget-Constrained ($0 API)": {
            "primary": "Qwen-Agent",
            "reason": "Apache-2.0, can self-host Qwen models, no vendor lock-in",
            "alternatives": ["MS-Agent", "AgentScope"],
            "timeline": "2-3 weeks setup"
        }
    }
    
    return recommendations

if __name__ == "__main__":
    repos = generate_shortlist_matrix()
    create_comparison_csv(repos)
    recommendations = create_usage_recommendations(repos)
    
    print("\n📊 Usage Recommendations:")
    print("=" * 60)
    for use_case, rec in recommendations.items():
        print(f"\n{use_case}:")
        print(f"  ✅ Primary: {rec['primary']}")
        print(f"  💡 Reason: {rec['reason']}")
        print(f"  🔄 Alternatives: {', '.join(rec['alternatives'])}")
        print(f"  ⏱️ Timeline: {rec['timeline']}")
