#!/usr/bin/env python3
"""
Documentation build script for AI Academy Report Generator.

This script provides an easy way to build, serve, and manage
the Sphinx documentation for the project.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
import http.server
import socketserver
import webbrowser
import time
import threading

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()
SOURCE_DIR = SCRIPT_DIR / "source"
BUILD_DIR = SCRIPT_DIR / "_build"
HTML_DIR = BUILD_DIR / "html"
REQUIREMENTS_FILE = SCRIPT_DIR / "requirements-docs.txt"


def run_command(cmd, cwd=None, check=True):
    """Run a command and handle errors."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd or SCRIPT_DIR,
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error output: {e.stderr}")
        if check:
            sys.exit(1)
        return e


def install_dependencies():
    """Install documentation dependencies."""
    print("Installing documentation dependencies...")
    
    if REQUIREMENTS_FILE.exists():
        cmd = f"{sys.executable} -m pip install -r {REQUIREMENTS_FILE}"
        run_command(cmd)
        print("✅ Documentation dependencies installed successfully!")
    else:
        print(f"❌ Requirements file not found: {REQUIREMENTS_FILE}")
        sys.exit(1)


def clean_build():
    """Clean the build directory."""
    print("Cleaning build directory...")
    
    if BUILD_DIR.exists():
        import shutil
        shutil.rmtree(BUILD_DIR)
        print("✅ Build directory cleaned!")
    else:
        print("Build directory already clean.")


def build_docs(builder="html", verbose=False):
    """Build the documentation."""
    print(f"Building documentation with {builder} builder...")
    
    # Ensure build directory exists
    BUILD_DIR.mkdir(exist_ok=True)
    
    # Build command
    verbosity = "-v" if verbose else ""
    cmd = f"sphinx-build {verbosity} -b {builder} {SOURCE_DIR} {BUILD_DIR}/{builder}"
    
    result = run_command(cmd, check=False)
    
    if result.returncode == 0:
        print(f"✅ Documentation built successfully!")
        print(f"📁 Output directory: {BUILD_DIR}/{builder}")
        return True
    else:
        print(f"❌ Documentation build failed!")
        return False


def serve_docs(port=8000, open_browser=True):
    """Serve the documentation locally."""
    if not HTML_DIR.exists():
        print("HTML documentation not found. Building first...")
        if not build_docs():
            return
    
    print(f"Serving documentation on http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    def start_server():
        """Start the HTTP server."""
        try:
            os.chdir(HTML_DIR)
            with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
                if open_browser:
                    # Open browser after a short delay
                    def open_browser_delayed():
                        time.sleep(1)
                        webbrowser.open(f"http://localhost:{port}")
                    
                    browser_thread = threading.Thread(target=open_browser_delayed)
                    browser_thread.daemon = True
                    browser_thread.start()
                
                httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
        except OSError as e:
            if e.errno == 48:  # Address already in use
                print(f"❌ Port {port} is already in use. Try a different port with --port")
            else:
                print(f"❌ Server error: {e}")
    
    start_server()


def watch_and_rebuild():
    """Watch for file changes and rebuild automatically."""
    try:
        print("Starting live reload server...")
        print("Watching for changes in source files...")
        print("Press Ctrl+C to stop")
        
        cmd = f"sphinx-autobuild {SOURCE_DIR} {HTML_DIR} --host 0.0.0.0 --port 8000"
        run_command(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Live reload stopped")


def check_links():
    """Check for broken links in the documentation."""
    print("Checking for broken links...")
    
    cmd = f"sphinx-build -b linkcheck {SOURCE_DIR} {BUILD_DIR}/linkcheck"
    result = run_command(cmd, check=False)
    
    if result.returncode == 0:
        print("✅ Link check completed successfully!")
    else:
        print("❌ Some links may be broken. Check the output above.")


def main():
    """Main command-line interface."""
    parser = argparse.ArgumentParser(
        description="Build and manage AI Academy Report Generator documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build_docs.py install          # Install dependencies
  python build_docs.py build            # Build HTML docs
  python build_docs.py serve            # Serve docs locally
  python build_docs.py watch            # Live reload development
  python build_docs.py clean build      # Clean and rebuild
        """
    )
    
    parser.add_argument("command", 
                       choices=["install", "build", "serve", "clean", "watch", "linkcheck"],
                       help="Command to execute")
    
    parser.add_argument("--builder", "-b", 
                       default="html",
                       choices=["html", "latexpdf", "epub", "man"],
                       help="Sphinx builder to use (default: html)")
    
    parser.add_argument("--port", "-p",
                       type=int,
                       default=8000,
                       help="Port for serving docs (default: 8000)")
    
    parser.add_argument("--no-browser",
                       action="store_true",
                       help="Don't open browser automatically when serving")
    
    parser.add_argument("--verbose", "-v",
                       action="store_true",
                       help="Verbose output")
    
    args = parser.parse_args()
    
    if args.command == "install":
        install_dependencies()
    
    elif args.command == "clean":
        clean_build()
    
    elif args.command == "build":
        build_docs(builder=args.builder, verbose=args.verbose)
    
    elif args.command == "serve":
        serve_docs(port=args.port, open_browser=not args.no_browser)
    
    elif args.command == "watch":
        watch_and_rebuild()
    
    elif args.command == "linkcheck":
        check_links()


if __name__ == "__main__":
    main()
