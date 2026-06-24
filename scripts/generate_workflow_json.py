#!/usr/bin/env python3
"""Generate complete Dify workflow JSON from template with multi-project support.

Usage:
    # Simple: Just provide project name
    python generate_workflow_json.py --project "MyDataCenter" --output workflow.json
    
    # Advanced: With custom document types
    python generate_workflow_json.py \
        --project "MyFactory" \
        --doc-types "SPECIFICATION,CONTRACT,VENDOR_DATABOOK,MEETING_MINUTES" \
        --output workflow.json
    
    # Enterprise: Use config file
    python generate_workflow_json.py --config my-project.json --output workflow.json
"""

import json
import argparse
import os
from datetime import datetime
from typing import Dict, List, Optional


def load_config(config_path: str) -> Dict:
    """Load project configuration from JSON file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_default_document_types() -> Dict[str, List[str]]:
    """Return default document type mappings."""
    return {
        "technical": ["HSYC", "HSMT", "SPECIFICATION", "STANDARD", "tiêu chuẩn"],
        "legal": ["CONTRACT", "AGREEMENT", "MOU", "hợp đồng", "thỏa thuận"],
        "procurement": ["VENDOR_DATABOOK", "DATASHEET", "QUOTE", "vendor datasheet", "hồ sơ nhà cung cấp"],
        "meeting": ["MINUTES", "RFI", "ACTION_LOG", "biên bản họp", "biên bản"]
    }


def generate_workflow(
    project_name: str, 
    include_branches: List[str] = None,
    document_types: Dict[str, List[str]] = None,
    industry: str = "general",
    location: str = "Vietnam"
) -> dict:
    """Generate complete workflow JSON structure with dynamic project context."""
    
    if include_branches is None:
        include_branches = ["technical", "legal", "procurement", "meeting"]
    
    if document_types is None:
        document_types = get_default_document_types()
    
    # Generate unique ID from project name
    project_id = project_name.lower().replace(' ', '_').replace('-', '_')
    
    workflow = {
        "id": f"{project_id}_dossier_reviewer",
        "name": f"{project_name} Dossier Review Assistant",
        "description": f"Multi-branch workflow for reviewing {project_name} project documents",
        "version": "3.0",
        "project_context": {
            "name": project_name,
            "industry": industry,
            "location": location,
            "generated_at": datetime.now().isoformat()
        },
        "nodes": [],
        "edges": []
    }
    
    # Build dynamic document type options for user input
    all_doc_types = []
    for category, types in document_types.items():
        all_doc_types.extend(types)
    
    # Node 1: Start
    start_node = {
        "id": "start_node",
        "type": "start",
        "data": {
            "title": "User Input",
            "variables": [
                {"key": "question", "name": "Question", "type": "paragraph", "required": True},
                {
                    "key": "dossier_type", 
                    "name": "Document Type", 
                    "type": "select", 
                    "options": list(set(all_doc_types)), 
                    "required": True
                },
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
    
    # Node 3: Parameter Extractor (with dynamic project context)
    param_extractor = {
        "id": "param_extractor",
        "type": "llm",
        "data": {
            "title": "Classify & Normalize",
            "model": {"provider": "openai", "name": "gpt-4-turbo"},
            "prompt_template": f"""You are a document classifier for {project_name} project ({industry} industry, {location}).

Extract structured parameters from user input and uploaded files.

Return JSON with schema:
{{
  "project": "{project_name}",
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
- Consider {industry} industry standards and {location} regulations

User question: {{#start_node.question#}}
Extracted text: {{#doc_extractor.text#}}

Return ONLY valid JSON."""
        }
    }
    workflow["nodes"].append(param_extractor)
    workflow["edges"].append({"source": "doc_extractor", "target": "param_extractor"})
    
    # Node 4: IF/ELSE Router (with dynamic conditions)
    router_cases = []
    
    # Technical branch condition
    tech_types = document_types.get("technical", [])
    tech_condition = ' or '.join([f'contains "{t}"' for t in tech_types[:5]])  # Limit to avoid overly long conditions
    router_cases.append({
        "id": "technical_branch",
        "condition": f'{{#param_extractor.output#}} {tech_condition}',
        "label": "Technical Review"
    })
    
    # Legal branch condition
    legal_types = document_types.get("legal", [])
    legal_condition = ' or '.join([f'contains "{t}"' for t in legal_types[:5]])
    router_cases.append({
        "id": "legal_branch",
        "condition": f'{{#param_extractor.output#}} {legal_condition}',
        "label": "Legal Review"
    })
    
    # Procurement branch condition
    proc_types = document_types.get("procurement", [])
    proc_condition = ' or '.join([f'contains "{t}"' for t in proc_types[:5]])
    router_cases.append({
        "id": "procurement_branch",
        "condition": f'{{#param_extractor.output#}} {proc_condition}',
        "label": "Procurement Review"
    })
    
    # Meeting branch condition
    meeting_types = document_types.get("meeting", [])
    meeting_condition = ' or '.join([f'contains "{t}"' for t in meeting_types[:5]])
    router_cases.append({
        "id": "meeting_branch",
        "condition": f'{{#param_extractor.output#}} {meeting_condition}',
        "label": "Meeting/RFI Review"
    })
    
    router = {
        "id": "router",
        "type": "if-else",
        "data": {
            "title": f"Route by Document Type ({project_name})",
            "cases": router_cases,
            "default_case_id": "general_branch"
        }
    }
    workflow["nodes"].append(router)
    workflow["edges"].append({"source": "param_extractor", "target": "router"})
    
    # Add branch nodes based on selection
    branch_configs = {
        "technical": {
            "kb_id": f"KB-{project_id}-Technical",
            "prompt": f"Technical review prompt for {project_name}...",
            "node_id": "technical_analysis"
        },
        "legal": {
            "kb_id": f"KB-{project_id}-Legal",
            "prompt": f"Legal review prompt for {project_name}...",
            "node_id": "legal_analysis"
        },
        "procurement": {
            "kb_id": f"KB-{project_id}-Procurement",
            "prompt": f"Procurement review prompt for {project_name}...",
            "node_id": "procurement_analysis"
        },
        "meeting": {
            "kb_id": f"KB-{project_id}-Meeting",
            "prompt": f"Meeting review prompt for {project_name}...",
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
                    "title": f"{branch.title()} KB Retrieval ({project_name})",
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
            
            # Analysis node with dynamic prompt
            analysis_prompt = f"""You are a {branch} expert reviewer for {project_name} project.
Industry: {industry}
Location: {location}

Analyze the document based on {branch} considerations specific to {industry} projects in {location}.

Consider:
- Industry-specific standards and best practices
- Local regulations and compliance requirements
- Project-specific constraints mentioned in the document

Return structured analysis with:
1. Key findings
2. Risk assessment
3. Recommendations
4. Action items

Input: {{#param_extractor.output#}}
Retrieved knowledge: {{#{branch}_rag.context#}}"""
            
            analysis_node = {
                "id": config["node_id"],
                "type": "llm",
                "data": {
                    "title": f"{branch.title()} Analysis ({project_name})",
                    "model": {"provider": "openai", "name": "gpt-4-turbo"},
                    "prompt_template": analysis_prompt
                }
            }
            workflow["nodes"].append(analysis_node)
            workflow["edges"].append({"source": f"{branch}_rag", "target": config["node_id"]})
    
    # Risk Scoring Node
    risk_node = {
        "id": "risk_scoring",
        "type": "llm",
        "data": {
            "title": f"Risk Assessment ({project_name})",
            "model": {"provider": "openai", "name": "gpt-4-turbo"},
            "prompt_template": f"""Score the overall risk based on analysis results for {project_name} project.

Consider {industry} industry risks and {location} regulatory environment.

Return JSON:
{{
  "overall_risk": "low|medium|high|critical",
  "risk_score": 0-100,
  "top_risks": [{{"risk": "...", "reason": "...", "evidence": "..."}}],
  "go_no_go": "go|conditional_go|no_go|need_more_info"
}}

Scoring:
- 0-30: low (proceed with monitoring)
- 31-60: medium (additional review needed)
- 61-80: high (executive approval required)  
- 81-100: critical (stop, immediate action)

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
    
    # Template Node (fixed - single line string, avoid f-string issues)
    template_str = "# Báo Cáo - {{#param_extractor.project#}}\\n\\n**Project:** " + project_name + "\\n**Risk Score:** {{#risk_scoring.risk_score#}}/100 ({{#risk_scoring.overall_risk#}})\\n**Decision:** {{#risk_scoring.go_no_go#}}\\n\\n## Kết Luận\\n{{#analysis_summary#}}\\n\\n## Rủi Ro Chính\\n{% for risk in risks %}\\n- {{ risk.risk }}: {{ risk.reason }}\\n{% endfor %}\\n\\n## Kiến Nghị\\n{{#recommendations#}}\\n\\n---\\n*Generated: {{ current_time }}*"
    
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
    parser = argparse.ArgumentParser(
        description="Generate Dify workflow JSON with multi-project support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple: Just provide project name
  python generate_workflow_json.py --project "MyDataCenter" --output workflow.json
  
  # Advanced: With custom document types
  python generate_workflow_json.py --project "MyFactory" \\
    --doc-types "SPECIFICATION,CONTRACT,VENDOR_DATABOOK" --output workflow.json
  
  # Enterprise: Use config file
  python generate_workflow_json.py --config my-project.json --output workflow.json
        """
    )
    
    parser.add_argument("--project", "-p", help="Project name (required if --config not provided)")
    parser.add_argument("--config", "-c", help="Path to project configuration JSON file")
    parser.add_argument("--branches", "-b", nargs="+", 
                       choices=["technical", "legal", "procurement", "meeting"],
                       default=["technical", "legal", "procurement", "meeting"],
                       help="Branches to include (default: all)")
    parser.add_argument("--doc-types", "-d", help="Comma-separated custom document types")
    parser.add_argument("--industry", "-i", default="general", help="Industry type (default: general)")
    parser.add_argument("--location", "-l", default="Vietnam", help="Project location (default: Vietnam)")
    parser.add_argument("--output", "-o", default="workflow.json", help="Output file")
    
    args = parser.parse_args()
    
    # Load configuration
    if args.config:
        config = load_config(args.config)
        project_name = config.get("project", {}).get("name", "Untitled_Project")
        document_types = config.get("document_types", get_default_document_types())
        industry = config.get("project", {}).get("industry", args.industry)
        location = config.get("project", {}).get("location", args.location)
    else:
        if not args.project:
            parser.error("Either --project or --config must be provided")
        project_name = args.project
        document_types = get_default_document_types()
        
        # Parse custom document types if provided
        if args.doc_types:
            custom_types = [t.strip() for t in args.doc_types.split(",")]
            # Add to technical category by default
            document_types["technical"].extend(custom_types)
        
        industry = args.industry
        location = args.location
    
    # Generate workflow
    workflow = generate_workflow(
        project_name=project_name,
        include_branches=args.branches,
        document_types=document_types,
        industry=industry,
        location=location
    )
    
    # Write output
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"✅ Workflow generated: {args.output}")
    print(f"   Project: {project_name}")
    print(f"   Industry: {industry}")
    print(f"   Location: {location}")
    print(f"   Nodes: {len(workflow['nodes'])}")
    print(f"   Edges: {len(workflow['edges'])}")
    print(f"   Branches: {', '.join(args.branches)}")
    print(f"   Document types: {sum(len(types) for types in document_types.values())} total")


if __name__ == "__main__":
    main()
