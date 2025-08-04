#!/usr/bin/env python3
"""
Comprehensive protocol buffer documentation generator using mkdocs-gen-files.
This script handles the complete workflow:
1. Downloads proto files from buf registry
2. Creates consolidated proto files per schema version
3. Runs proto-gen-md-diagrams to generate markdown
4. Creates virtual documentation pages with unified Mermaid diagrams
"""

import os
import re
import subprocess
import tempfile
from pathlib import Path
import mkdocs_gen_files

def download_proto_modules(schema_dir: Path, modules: list[str]) -> bool:
    """Download proto files from buf registry."""
    success = True
    for module in modules:
        try:
            print(f"Downloading module: {module}")
            result = subprocess.run([
                "buf", "export", f"buf.build/agntcy/{module}", 
                "--output", str(schema_dir / module)
            ], capture_output=True, text=True, check=True)
            print(f"Successfully downloaded {module}")
        except subprocess.CalledProcessError as e:
            print(f"Module {module} not found, skipping...")
            success = False
    return success

def find_proto_directories(schema_dir: Path, modules: list[str]) -> list[Path]:
    """Find all directories containing proto files."""
    proto_dirs = []
    for module in modules:
        module_path = schema_dir / module
        if module_path.exists():
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
    classes = {}
    relationships = []
    
    for diagram in re.findall(r'```mermaid\n(.*?)\n```', content, re.DOTALL):
        lines = diagram.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Extract complete class definitions
            if line.startswith('class ') and '{' in line:
                class_name = re.match(r'class\s+([^{]+)', line).group(1).strip()
                class_def = [line]
                i += 1
                
                # Continue reading until we find the closing brace
                while i < len(lines):
                    class_line = lines[i].strip()
                    class_def.append(class_line)
                    if '}' in class_line:
                        break
                    i += 1
                
                classes[class_name] = '\n'.join(class_def)
            
            # Extract relationships
            elif '-->' in line:
                relationships.append(line)
            
            i += 1
    
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

# Main execution - runs when mkdocs-gen-files loads this script
root = Path(__file__).parent.parent
schema_dir = root / "schema"
deps_dir = root / ".dep"
modules = ["dir", "oasf"]

# Download proto files
print("Downloading protocol buffer schemas...")
download_proto_modules(schema_dir, modules)

# Find all proto directories
proto_dirs = find_proto_directories(schema_dir, modules)
print(f"Found {len(proto_dirs)} proto directories")

if proto_dirs:
    for proto_dir in proto_dirs:
        try:
            rel_path = proto_dir.relative_to(schema_dir)
            clean_name = str(rel_path).replace('/', '-')
            module = rel_path.parts[0]
            
            # Create virtual page path
            virtual_path = f"{module}/{clean_name}.md"
            
            # Use temporary directory for processing
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
                header = f"# {rel_path} Protocol Buffer Documentation\n\nComplete definitions for {rel_path}.\n\n"
                
                generated_content = ""
                for md_file in temp_output.glob("*.md"):
                    generated_content += md_file.read_text()
                
                # Create final content with unified diagram
                final_content = header + create_unified_diagram(generated_content)
                
                # Create virtual file
                with mkdocs_gen_files.open(virtual_path, "w") as f:
                    f.write(final_content)
                
                # Set edit path to point to this generation script
                mkdocs_gen_files.set_edit_path(virtual_path, "mkdocs/gen_proto_docs.py")
                
        except Exception as e:
            print(f"Error processing {proto_dir}: {e}")
            continue

print(f"✅ Generated virtual documentation pages for {len(proto_dirs)} proto directories") 