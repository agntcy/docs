#!/usr/bin/env python3
"""
Protocol buffer documentation generator for MkDocs.
Downloads protos, consolidates them, and generates docs with Mermaid diagrams.
"""

import os
import re
import subprocess
import tempfile
from pathlib import Path
import mkdocs_gen_files  # type: ignore

def run_cmd(cmd, check=True):
    """Run subprocess command with simplified error handling."""
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=check)
    except subprocess.CalledProcessError:
        print(f"Command failed: {' '.join(cmd)}")
        return None

def download_protos(schema_dir, modules):
    """Download proto files from buf registry."""
    for module in modules:
        print(f"Downloading module: {module}")
        result = run_cmd(["buf", "export", f"buf.build/agntcy/{module}", "--output", str(schema_dir / module)], check=False)
        if result and result.returncode == 0:
            print(f"Successfully downloaded {module}")

def find_proto_dirs(schema_dir, modules):
    """Find directories containing proto files."""
    return [
        Path(root) for module in modules
        for root, _, files in os.walk(schema_dir / module)
        if any(f.endswith('.proto') for f in files)
    ]

def create_consolidated_proto(proto_dir, output_path):
    """Create single proto file from directory."""
    proto_files = list(proto_dir.glob("*.proto"))
    if not proto_files:
        return False
    
    # Extract package and imports
    package_line, imports = "", set()
    for proto_file in proto_files:
        for line in proto_file.read_text().splitlines():
            if line.startswith('package ') and not package_line:
                package_line = line
            elif line.startswith('import '):
                imports.add(line)
    
    # Build consolidated content
    content = ['syntax = "proto3";', '']
    if package_line:
        content.extend([package_line, ''])
    if imports:
        content.extend(sorted(imports) + [''])
    
    # Add all proto contents with improved comment and copyright handling
    for proto_file in sorted(proto_files):
        lines = proto_file.read_text().splitlines()
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Skip copyright headers and file headers
            if (line.strip().startswith('//') and 
                any(keyword in line.lower() for keyword in ['copyright', 'spdx-license', 'from:'])):
                i += 1
                continue
                
            if line.strip() and not any(line.startswith(p) for p in ['syntax ', 'package ', 'import ']):
                # Check if we're at the start of a comment block that precedes a message/enum/service
                if line.strip().startswith('//'):
                    # Look ahead to find if there's a message/enum/service declaration after this comment block
                    j = i
                    # Skip all consecutive comment lines and empty lines
                    while j < len(lines) and (lines[j].strip().startswith('//') or lines[j].strip() == ''):
                        j += 1
                    
                    # Check if the next non-comment line is a message/enum/service declaration
                    if (j < len(lines) and 
                        any(lines[j].strip().startswith(keyword) for keyword in ['message ', 'enum ', 'service '])):
                        
                        # Collect all comment lines from i to j-1
                        comment_parts = []
                        for k in range(i, j):
                            current_line = lines[k].strip()
                            if current_line.startswith('//'):
                                comment_text = current_line[2:].strip()
                                if comment_text:  # Skip empty comment lines
                                    comment_parts.append(comment_text)
                        
                        if comment_parts:
                            # Combine all comments into single line
                            combined_comment = ' '.join(comment_parts)
                            content.append(f'// {combined_comment}')
                            i = j - 1  # Skip to just before the message/enum/service declaration
                        else:
                            content.append(line)
                    else:
                        # Regular comment line, not before a declaration
                        content.append(line)
                else:
                    content.append(line)
            i += 1
        
        content.append('')
    
    output_path.write_text('\n'.join(content))
    return True

def generate_docs(proto_dir, deps_dir):
    """Generate markdown docs with unified diagrams."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        consolidated_proto = temp_path / "consolidated.proto"
        temp_output = temp_path / "output"
        temp_output.mkdir()
        
        if not create_consolidated_proto(proto_dir, consolidated_proto):
            return None
            
        if not run_cmd([str(deps_dir / "proto-gen-md-diagrams"), "-d", str(temp_path), "-o", str(temp_output)]):
            return None
        
        content = "".join(md_file.read_text() for md_file in temp_output.glob("*.md"))
        return create_unified_diagram(content)

def create_unified_diagram(content):
    """Combine all Mermaid diagrams into one."""
    classes, relationships = {}, []
    
    for diagram in re.findall(r'```mermaid\n(.*?)\n```', content, re.DOTALL):
        lines = diagram.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if line.startswith('class ') and '{' in line:
                class_name = re.match(r'class\s+([^{]+)', line).group(1).strip()
                class_def = [line]
                i += 1
                while i < len(lines):
                    class_line = lines[i].strip()
                    class_def.append(class_line)
                    if '}' in class_line:
                        break
                    i += 1
                classes[class_name] = '\n'.join(class_def)
            elif '-->' in line:
                relationships.append(line)
            i += 1
    
    if not classes:
        return content
    
    # Create unified diagram
    unified = [
        '```mermaid', 'classDiagram', 'direction TB', '',
        *classes.values(), '', *relationships, '```'
    ]
    
    # Replace individual diagrams with unified one
    content = re.sub(r'### \w+[\w\s]* Diagram\n\n```mermaid.*?```', '', content, flags=re.DOTALL)
    insert_pos = content.find('## Enum:') or content.find('## Message:') or len(content)
    unified_section = f'\n## Complete Schema Diagram\n\n{chr(10).join(unified)}\n\n'
    
    return content[:insert_pos] + unified_section + content[insert_pos:]

def create_reference_page(name, title, versions, output_path):
    """Create a reference page with version tabs."""
    content = [
        "---",
        "hide:",
        "  - toc",
        "---",
        "",
        f"# {title}",
        "",
        f"Complete API reference for {name} across all versions.",
        "",
        "Choose a version to view its protocol buffer definitions and schema diagrams:",
        ""
    ]
    
    # Sort versions with newer first
    sorted_versions = sorted(versions.items(), key=lambda x: x[0], reverse=True)
    
    for version_name, version_content in sorted_versions:
        display_name = version_name.replace("/", " ").title()
        clean_content = version_content.replace("# Package:", "## Package:")
        
        content.extend([
            f"=== \"{display_name}\"",
            "",
            f"    Complete schema for {version_name}.",
            "",
            *[f"    {line}" for line in clean_content.split("\n")],
            ""
        ])
    
    with mkdocs_gen_files.open(output_path, "w") as f:
        f.write("\n".join(content))
    mkdocs_gen_files.set_edit_path(output_path, "mkdocs/gen_proto_docs.py")

# Main execution
root = Path(__file__).parent.parent
schema_dir = root / "schema"
deps_dir = root / ".dep"
modules = ["dir", "oasf"]

print("Downloading protocol buffer schemas...")
download_protos(schema_dir, modules)

proto_dirs = find_proto_dirs(schema_dir, modules)
print(f"Found {len(proto_dirs)} proto directories")

# Process all proto directories and collect versions
oasf_versions = {}
dir_services = {}

for proto_dir in proto_dirs:
    try:
        rel_path = proto_dir.relative_to(schema_dir)
        clean_name = str(rel_path).replace('/', '-')
        module = rel_path.parts[0]
        
        # Generate docs
        content = generate_docs(proto_dir, deps_dir)
        if not content:
            continue
            
        # Create individual page
        header = f"---\nhide:\n  - toc\n---\n\n# {rel_path} Protocol Buffer Documentation\n\nComplete definitions for {rel_path}.\n\n"
        final_content = header + content
        
        virtual_path = f"{module}/{clean_name}.md"
        with mkdocs_gen_files.open(virtual_path, "w") as f:
            f.write(final_content)
        mkdocs_gen_files.set_edit_path(virtual_path, "mkdocs/gen_proto_docs.py")
        
        # Collect versions for reference pages
        if module == "oasf":
            version_name = "/".join(rel_path.parts[1:])
            oasf_versions[version_name] = content
        elif module == "dir" and len(rel_path.parts) >= 3:
            service_name = rel_path.parts[1]
            version_name = rel_path.parts[2]
            if service_name not in dir_services:
                dir_services[service_name] = {}
            dir_services[service_name][version_name] = content
            
    except Exception as e:
        print(f"Error processing {proto_dir}: {e}")

# Create reference pages
if oasf_versions:
    create_reference_page(
        "all OASF (Open Agentic Schema Framework) versions",
        "OASF API Reference", 
        oasf_versions, 
        "oasf/api-reference.md"
    )
    print(f"INFO    -  Generated OASF API Reference with {len(oasf_versions)} version tabs (newer first)")

if dir_services:
    for service_name, versions in dir_services.items():
        create_reference_page(
            f"DIR {service_name} service",
            f"DIR {service_name.title()} Service Reference",
            versions,
            f"dir/{service_name}-reference.md"
        )
    
    service_count = len(dir_services)
    total_versions = sum(len(versions) for versions in dir_services.values())
    print(f"INFO    -  Generated {service_count} DIR service reference pages with {total_versions} total versions")

print(f"INFO    -  Generated virtual documentation pages for {len(proto_dirs)} proto directories") 