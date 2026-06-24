#!/usr/bin/env python3
"""Generate complete Dify workflow JSON from template.

Usage:
    python generate_workflow_json.py --project "HN-DC03" --output workflow.json
"""

import json
import argparse
from datetime import datetime


def generate_workflow(project_name: str, include_branches: list = None) -> dict:
    """Generate complete workflow JSON structure."""
    
    if include_branches is None:
        include_branches = ["technical", "legal", "procurement", "meeting"]
    
    workflow = {
        "id": f"{project_name.lower().replace(' ', '_')}_dossier_reviewer",
        "name": f"{project_name} Dossier Review Assistant",
        "description": f"Multi-branch workflow for reviewing {project_name} project documents",
        "version": "2.0",
        "created_at": datetime.now().isoformat(),
        "workflow_type": "workflow",
        "nodes": [],
        "edges": []
    }
    
    # Node 1: Start
    start_node = {
        "id": "start_node",
        "type": "start",
        "data": {
            "title": "User Input",
            "variables": [
                {"key": "question", "name": "Question", "type": "paragraph", "required": True},
                {"key": "dossier_type", "name": "Document Type", "type": "select", 
                 "options": ["HSYC", "HSMT", "hợp đồng", "vendor datasheet", 
                           "biên bản họp", "RFI", "tiêu chuẩn", "báo cáo"], "required": True},
                {"key": "uploaded_files", "name": "Files", "type": "file_list", "required": False},
                {"key": "output_type", "name": "Output Type", "type": "select",
                 "options": ["Executive brief", "Issue log", "RFI list", "Checklist", "Full review"], "required": True},
                {"key": "risk_focus", "name": "Risk Focus", "type": "multi_select",
                 "options": ["kỹ thuật", "pháp lý", "thương mại", "vendor lock-in", "vận hành"]}
            ]
        }
    }
    workflow["nodes"].append(start_node)
    
    # Node 2: Doc Extractor
    doc_extractor = {
        "id": "doc_extractor",
        "type": "document-extractor",
        "data": {
            "title": "Extract Documents",
            "input_variable": "{{#start_node.uploaded_files#}}",
            "output_format": "text"
        }
    }
    workflow["nodes"].append(doc_extractor)
    workflow["edges"].append({"source": "start_node", "target": "doc_extractor"})
    
    # Node 3: Parameter Extractor
    param_extractor = {
        "id": "param_extractor",
        "type": "llm",
        "data": {
            "title": "Classify & Normalize",
            "model": {"provider": "openai", "name": "gpt-4-turbo"},
            "prompt_template": f"""You are a document classifier for {project_name} project.

Extract structured parameters from user input and uploaded files.

Return JSON with schema:
{{
  "project": "string",
  "document_type": "string",
  "discipline": "string",
  "main_entities": ["string"],
  "decision_required": "string",
  "risk_categories": ["technical", "legal", "commercial", ...],
  "urgency": "low|medium|high",
  "missing_information": ["string"]
}}

Rules:
- If uncertain, add to missing_information
- Do NOT conclude PASS/FAIL at this stage
- Only classify and normalize

User question: {{#start_node.question#}}
Extracted text: {{#doc_extractor.text#}}

Return ONLY valid JSON."""
        }
    }
    workflow["nodes"].append(param_extractor)
    workflow["edges"].append({"source": "doc_extractor", "target": "param_extractor"})
    
    # Node 4: IF/ELSE Router
    router = {
        "id": "router",
        "type": "if-else",
        "data": {
            "title": "Route by Document Type",
            "cases": [
                {
                    "id": "technical_branch",
                    "condition": '{{#param_extractor.output#}} contains "HSYC" or "HSMT" or "tiêu chuẩn"',
                    "label": "Technical Review"
                },
                {
                    "id": "legal_branch",
                    "condition": '{{#param_extractor.output#}} contains "hợp đồng"',
                    "label": "Legal Review"
                },
                {
                    "id": "procurement_branch",
                    "condition": '{{#param_extractor.output#}} contains "vendor" or "datasheet"',
                    "label": "Procurement Review"
                },
                {
                    "id": "meeting_branch",
                    "condition": '{{#param_extractor.output#}} contains "biên bản" or "RFI"',
                    "label": "Meeting/RFI Review"
                }
            ],
            "default_case_id": "general_branch"
        }
    }
    workflow["nodes"].append(router)
    workflow["edges"].append({"source": "param_extractor", "target": "router"})
    
    # Add branch nodes based on selection
    branch_configs = {
        "technical": {
            "kb_id": "KB-Technical",
            "prompt": "Technical review prompt...",
            "node_id": "technical_analysis"
        },
        "legal": {
            "kb_id": "KB-Legal",
            "prompt": "Legal review prompt...",
            "node_id": "legal_analysis"
        },
        "procurement": {
            "kb_id": "KB-Procurement",
            "prompt": "Procurement review prompt...",
            "node_id": "procurement_analysis"
        },
        "meeting": {
            "kb_id": "KB-Meeting",
            "prompt": "Meeting review prompt...",
            "node_id": "meeting_analysis"
        }
    }
    
    for branch in include_branches:
        if branch in branch_configs:
            config = branch_configs[branch]
            
            # RAG node
            rag_node = {
                "id": f"{branch}_rag",
                "type": "knowledge-retrieval",
                "data": {
                    "title": f"{branch.title()} KB Retrieval",
                    "knowledge_id": config["kb_id"],
                    "query": "{{#param_extractor.output#}}",
                    "top_k": 5
                }
            }
            workflow["nodes"].append(rag_node)
            workflow["edges"].append({
                "source": "router", 
                "target": f"{branch}_rag",
                "source_handle": config["node_id"]
            })
            
            # Analysis node
            analysis_node = {
                "id": config["node_id"],
                "type": "llm",
                "data": {
                    "title": f"{branch.title()} Analysis",
                    "model": {"provider": "openai", "name": "gpt-4-turbo"},
                    "prompt_template": config["prompt"]
                }
            }
            workflow["nodes"].append(analysis_node)
            workflow["edges"].append({"source": f"{branch}_rag", "target": config["node_id"]})
    
    # Risk Scoring Node
    risk_node = {
        "id": "risk_scoring",
        "type": "llm",
        "data": {
            "title": "Risk Assessment",
            "model": {"provider": "openai", "name": "gpt-4-turbo"},
            "prompt_template": """Score the overall risk based on analysis results.

Return JSON:
{
  "overall_risk": "low|medium|high|critical",
  "risk_score": 0-100,
  "top_risks": [{"risk": "...", "reason": "...", "evidence": "..."}],
  "go_no_go": "go|conditional_go|no_go|need_more_info"
}

Scoring:
- 0-30: low
- 31-60: medium
- 61-80: high  
- 81-100: critical

Analysis input: {{#branch_outputs#}}"""
        }
    }
    workflow["nodes"].append(risk_node)
    
    # Connect all branches to risk scoring
    for branch in include_branches:
        if branch in branch_configs:
            workflow["edges"].append({
                "source": branch_configs[branch]["node_id"],
                "target": "risk_scoring"
            })
    
    # Template Node (fixed - single line string)
    template_str = "# Báo Cáo - {{#param_extractor.project#}}\\n\\n**Risk Score:** {{#risk_scoring.risk_score#}}/100 ({{#risk_scoring.overall_risk#}})\\n**Decision:** {{#risk_scoring.go_no_go#}}\\n\\n## Kết Luận\\n{{#analysis_summary#}}\\n\\n## Rủi Ro Chính\\n{% for risk in risks %}\\n- {{ risk.risk }}: {{ risk.reason }}\\n{% endfor %}\\n\\n## Kiến Nghị\\n{{#recommendations#}}\\n\\n---\\n*Generated: {{ current_time }}*"
    
    template_node = {
        "id": "template_output",
        "type": "template-transform",
        "data": {
            "title": "Format Report",
            "template": template_str
        }
    }
    workflow["nodes"].append(template_node)
    workflow["edges"].append({"source": "risk_scoring", "target": "template_output"})
    
    # End Node
    end_node = {
        "id": "end_node",
        "type": "end",
        "data": {
            "title": "End",
            "outputs": ["{{#template_output.result#}}"]
        }
    }
    workflow["nodes"].append(end_node)
    workflow["edges"].append({"source": "template_output", "target": "end_node"})
    
    return workflow


def main():
    parser = argparse.ArgumentParser(description="Generate Dify workflow JSON")
    parser.add_argument("--project", default="HN-DC03", help="Project name")
    parser.add_argument("--branches", nargs="+", 
                       choices=["technical", "legal", "procurement", "meeting"],
                       default=["technical", "legal", "procurement", "meeting"],
                       help="Branches to include")
    parser.add_argument("--output", default="workflow.json", help="Output file")
    
    args = parser.parse_args()
    
    workflow = generate_workflow(args.project, args.branches)
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Workflow generated: {args.output}")
    print(f"   Nodes: {len(workflow['nodes'])}")
    print(f"   Edges: {len(workflow['edges'])}")
    print(f"   Branches: {', '.join(args.branches)}")


if __name__ == "__main__":
    main()
