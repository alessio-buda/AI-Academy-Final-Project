#!/usr/bin/env python3
"""
Sphinx Documentation Builder for Game Builder Crew

This script automates the installation of Sphinx dependencies and builds
the documentation in various formats.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Required packages for Sphinx documentation
SPHINX_PACKAGES = [
    'sphinx>=7.0.0',
    'sphinx-rtd-theme>=1.3.0',
    'myst-parser>=2.0.0',
    'sphinx-copybutton>=0.5.0',
    'sphinx-design>=0.5.0',
    'sphinx-autobuild>=2021.3.14',
    'sphinxcontrib-mermaid>=0.9.0',
]

def run_command(command, cwd=None, check=True):
    """Run a shell command and return the result."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        raise

def install_dependencies():
    """Install Sphinx and related dependencies."""
    print("Installing Sphinx dependencies...")
    
    # Update pip first
    run_command(f"{sys.executable} -m pip install --upgrade pip")
    
    # Install packages
    for package in SPHINX_PACKAGES:
        run_command(f"{sys.executable} -m pip install {package}")
    
    print("✅ All dependencies installed successfully!")

def build_documentation(output_format='html', clean=False):
    """Build documentation in specified format."""
    docs_dir = Path(__file__).parent
    source_dir = docs_dir / 'source'
    build_dir = docs_dir / '_build'
    
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")
    
    # Clean build directory if requested
    if clean and build_dir.exists():
        print("Cleaning build directory...")
        run_command(f"rm -rf {build_dir}", cwd=docs_dir)
    
    # Build documentation
    print(f"Building {output_format} documentation...")
    
    if output_format == 'html':
        run_command(f"sphinx-build -b html {source_dir} {build_dir}/html", cwd=docs_dir)
        print(f"✅ HTML documentation built in: {build_dir}/html")
        print(f"📖 Open: {build_dir}/html/index.html")
        
    elif output_format == 'pdf':
        run_command(f"sphinx-build -b latex {source_dir} {build_dir}/latex", cwd=docs_dir)
        run_command("make", cwd=build_dir / 'latex')
        print(f"✅ PDF documentation built in: {build_dir}/latex")
        
    elif output_format == 'epub':
        run_command(f"sphinx-build -b epub {source_dir} {build_dir}/epub", cwd=docs_dir)
        print(f"✅ EPUB documentation built in: {build_dir}/epub")
        
    else:
        raise ValueError(f"Unsupported format: {output_format}")

def serve_documentation(port=8000):
    """Serve documentation locally."""
    docs_dir = Path(__file__).parent
    html_dir = docs_dir / '_build' / 'html'
    
    if not html_dir.exists():
        print("HTML documentation not found. Building it first...")
        build_documentation('html')
    
    print(f"Serving documentation at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        run_command(f"{sys.executable} -m http.server {port}", cwd=html_dir)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")

def live_build():
    """Start live-reload development server."""
    docs_dir = Path(__file__).parent
    source_dir = docs_dir / 'source'
    build_dir = docs_dir / '_build' / 'html'
    
    print("Starting live-reload server...")
    print("📝 Edit files in source/ directory")
    print("🔄 Browser will auto-refresh on changes")
    print("Press Ctrl+C to stop")
    
    try:
        run_command(f"sphinx-autobuild {source_dir} {build_dir}", cwd=docs_dir)
    except KeyboardInterrupt:
        print("\n🛑 Live server stopped")

def check_links():
    """Check for broken links in documentation."""
    docs_dir = Path(__file__).parent
    source_dir = docs_dir / 'source'
    build_dir = docs_dir / '_build' / 'linkcheck'
    
    print("Checking for broken links...")
    run_command(f"sphinx-build -b linkcheck {source_dir} {build_dir}", cwd=docs_dir)
    print("✅ Link check completed")

def setup_project_paths():
    """Add project paths to Python path for autodoc."""
    project_root = Path(__file__).parent.parent.parent
    src_path = project_root / 'src'
    
    if src_path.exists():
        sys.path.insert(0, str(src_path))
        print(f"Added to Python path: {src_path}")
    else:
        print(f"Warning: Source path not found: {src_path}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Build Game Builder Crew documentation with Sphinx'
    )
    
    parser.add_argument(
        'action',
        choices=['install', 'build', 'serve', 'live', 'clean', 'linkcheck', 'all'],
        help='Action to perform'
    )
    
    parser.add_argument(
        '--format',
        choices=['html', 'pdf', 'epub'],
        default='html',
        help='Documentation format (for build action)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port for local server (for serve action)'
    )
    
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Clean build directory before building'
    )
    
    args = parser.parse_args()
    
    # Setup project paths for autodoc
    setup_project_paths()
    
    try:
        if args.action == 'install':
            install_dependencies()
            
        elif args.action == 'build':
            build_documentation(args.format, args.clean)
            
        elif args.action == 'serve':
            serve_documentation(args.port)
            
        elif args.action == 'live':
            live_build()
            
        elif args.action == 'clean':
            docs_dir = Path(__file__).parent
            build_dir = docs_dir / '_build'
            if build_dir.exists():
                run_command(f"rm -rf {build_dir}", cwd=docs_dir)
                print("✅ Build directory cleaned")
            else:
                print("Build directory already clean")
                
        elif args.action == 'linkcheck':
            check_links()
            
        elif args.action == 'all':
            print("🚀 Running complete documentation workflow...")
            install_dependencies()
            build_documentation('html', clean=True)
            print("\n📚 Documentation workflow completed!")
            print("Run 'python build_docs.py serve' to view documentation")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
