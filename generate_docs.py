#!/usr/bin/env python3
"""
Comprehensive documentation generator for AGNTCY protocol buffer schemas.
Generates consolidated markdown files with unified Mermaid diagrams.
"""

import os
import re
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List

def find_proto_directories(schema_dir: Path, modules: List[str]) -> List[Path]:
    """Find all directories containing proto files."""
    proto_dirs = []
    for module in modules:
        module_path = schema_dir / module
        if module_path.exists():
            print(f"Processing module: {module}")
            proto_dirs.extend([
                Path(root) for root, _, files in os.walk(module_path)
                if any(f.endswith('.proto') for f in files)
            ])
    return proto_dirs

def create_consolidated_proto(proto_dir: Path, output_path: Path) -> None:
    """Create consolidated proto file from directory."""
    proto_files = list(proto_dir.glob("*.proto"))
    if not proto_files:
        raise ValueError(f"No proto files in {proto_dir}")
    
    # Extract package and imports
    package_line = ""
    imports = set()
    
    for proto_file in proto_files:
        content = proto_file.read_text()
        for line in content.splitlines():
            if line.startswith('package ') and not package_line:
                package_line = line
            elif line.startswith('import '):
                imports.add(line)
    
    # Build consolidated content
    consolidated = ['syntax = "proto3";', '']
    if package_line:
        consolidated.extend([package_line, ''])
    if imports:
        consolidated.extend(['// Imports'] + sorted(imports) + [''])
    
    # Add all proto contents (excluding syntax/package/import lines)
    consolidated.append('// Protocol buffer definitions')
    for proto_file in sorted(proto_files):
        consolidated.append(f'// From: {proto_file.name}')
        content = proto_file.read_text()
        body_lines = [
            line for line in content.splitlines()
            if line.strip() and not any(line.startswith(prefix) for prefix in ['syntax ', 'package ', 'import '])
        ]
        consolidated.extend(body_lines + [''])
    
    output_path.write_text('\n'.join(consolidated))

def run_proto_gen_md_diagrams(proto_dir: Path, output_dir: Path, deps_dir: Path) -> bool:
    """Run proto-gen-md-diagrams tool."""
    try:
        subprocess.run([
            str(deps_dir / "proto-gen-md-diagrams"), 
            "-d", str(proto_dir), 
            "-o", str(output_dir)
        ], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error generating diagrams: {e}")
        return False

def create_unified_diagram(content: str) -> str:
    """Extract and combine all Mermaid diagrams into one unified diagram."""
    # Extract all class definitions and relationships
    classes = {}
    relationships = []
    
    for diagram in re.findall(r'```mermaid\n(.*?)\n```', content, re.DOTALL):
        for line in diagram.splitlines():
            line = line.strip()
            if line.startswith('class ') and '{' in line:
                # Extract multi-line class definition
                class_name = re.match(r'class\s+([^{]+)', line).group(1).strip()
                classes[class_name] = line
            elif '-->' in line:
                relationships.append(line)
    
    if not classes:
        return content
    
    # Create unified diagram
    unified = [
        '```mermaid',
        'classDiagram',
        'direction TB',
        '',
        *classes.values(),
        '',
        *relationships,
        '```'
    ]
    
    # Replace individual diagrams with unified one
    content = re.sub(r'### \w+[\w\s]* Diagram\n\n```mermaid.*?```', '', content, flags=re.DOTALL)
    
    # Insert unified diagram
    insert_pos = content.find('## Enum:') or content.find('## Message:') or len(content)
    unified_section = f'\n## Complete Schema Diagram\n\n{chr(10).join(unified)}\n\n'
    
    return content[:insert_pos] + unified_section + content[insert_pos:]

def generate_documentation(schema_dir: Path, docs_dir: Path, deps_dir: Path) -> bool:
    """Generate all documentation."""
    modules = ["dir", "oasf"]
    generated_dir = docs_dir.parent / "generated"
    proto_dirs = find_proto_directories(schema_dir, modules)
    
    if not proto_dirs:
        print("No proto directories found!")
        return False
    
    success_count = 0
    
    for proto_dir in proto_dirs:
        try:
            rel_path = proto_dir.relative_to(schema_dir)
            clean_name = str(rel_path).replace('/', '-')
            module = rel_path.parts[0]
            output_file = generated_dir / module / f"{clean_name}.md"
            
            print(f"Processing: {rel_path}")
            
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                consolidated_proto = temp_path / "consolidated.proto"
                temp_output = temp_path / "output"
                temp_output.mkdir()
                
                # Generate consolidated proto and markdown
                create_consolidated_proto(proto_dir, consolidated_proto)
                
                if not run_proto_gen_md_diagrams(consolidated_proto.parent, temp_output, deps_dir):
                    continue
                
                # Combine generated content with unified diagrams
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                header = f"# {rel_path} Protocol Buffer Documentation\n\nComplete definitions for {rel_path}.\n\n"
                
                generated_content = ""
                for md_file in temp_output.glob("*.md"):
                    generated_content += md_file.read_text()
                
                # Create final file with unified diagram
                final_content = header + create_unified_diagram(generated_content)
                output_file.write_text(final_content)
                
                success_count += 1
                
        except Exception as e:
            print(f"Error processing {proto_dir}: {e}")
            continue
    
    print(f"\n✅ Generated {success_count}/{len(proto_dirs)} files in {generated_dir}")
    return success_count > 0

def main():
    if len(sys.argv) != 4:
        print("Usage: python generate_docs.py <schema_dir> <docs_dir> <deps_dir>")
        sys.exit(1)
    
    schema_dir, docs_dir, deps_dir = [Path(arg).resolve() for arg in sys.argv[1:4]]
    
    print(f"Generating documentation from {schema_dir}")
    
    if not schema_dir.exists():
        print(f"Schema directory not found: {schema_dir}")
        sys.exit(1)
    
    success = generate_documentation(schema_dir, docs_dir, deps_dir)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 