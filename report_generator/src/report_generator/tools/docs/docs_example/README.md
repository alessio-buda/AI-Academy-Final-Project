# Game Builder Crew - Sphinx Documentation

This directory contains the Sphinx documentation system for the Game Builder Crew project.

## Quick Start

### 1. Install Dependencies

```bash
# Option 1: Using the automated script
python build_docs.py install

# Option 2: Using pip directly
pip install -r requirements-docs.txt

# Option 3: Using poetry (if in project root)
poetry install --with docs
```

### 2. Build Documentation

```bash
# Build HTML documentation
python build_docs.py build

# Or using make (Linux/macOS)
make html

# Or using make.bat (Windows)
make.bat html
```

### 3. View Documentation

```bash
# Serve locally
python build_docs.py serve

# Or manually
cd _build/html
python -m http.server 8000
```

Open your browser to `http://localhost:8000`

## Development Workflow

### Live Reload Development

For active documentation development:

```bash
# Start live-reload server
python build_docs.py live

# Or using sphinx-autobuild directly
sphinx-autobuild source _build/html
```

This will:
- Watch for file changes in `source/`
- Automatically rebuild documentation
- Refresh your browser automatically

### Complete Workflow

```bash
# Run everything: install dependencies, clean build, build docs
python build_docs.py all
```

## Documentation Structure

```
docs/sphinx/
├── source/                 # Source files
│   ├── conf.py            # Sphinx configuration
│   ├── index.rst          # Main page
│   ├── installation.rst   # Installation guide
│   ├── quickstart.rst     # Quick start guide
│   ├── usage.rst          # Usage documentation
│   ├── examples.rst       # Game examples
│   ├── api/               # API reference
│   │   ├── modules.rst    # API overview
│   │   ├── crew.rst       # Crew module docs
│   │   ├── main.rst       # Main module docs
│   │   └── configuration.rst # Config docs
│   ├── development/       # Developer guides
│   │   ├── architecture.rst
│   │   ├── extending.rst
│   │   ├── testing.rst
│   │   └── troubleshooting.rst
│   ├── _static/           # Static files (CSS, images)
│   │   └── custom.css     # Custom styling
│   └── _templates/        # Custom templates
├── _build/                # Generated documentation
│   ├── html/              # HTML output
│   ├── latex/             # LaTeX output
│   └── epub/              # EPUB output
├── Makefile               # Unix build commands
├── make.bat               # Windows build commands
├── build_docs.py          # Python build script
├── requirements-docs.txt  # Documentation dependencies
└── README.md              # This file
```

## Available Commands

### Using build_docs.py

```bash
# Install Sphinx dependencies
python build_docs.py install

# Build documentation (HTML by default)
python build_docs.py build
python build_docs.py build --format html
python build_docs.py build --format pdf
python build_docs.py build --format epub

# Serve documentation locally
python build_docs.py serve
python build_docs.py serve --port 8080

# Live-reload development server
python build_docs.py live

# Clean build directory
python build_docs.py clean

# Check for broken links
python build_docs.py linkcheck

# Complete workflow
python build_docs.py all
```

### Using Make (Linux/macOS)

```bash
# Build HTML
make html

# Build PDF (requires LaTeX)
make latexpdf

# Build EPUB
make epub

# Clean build directory
make clean

# Check links
make linkcheck

# Live-reload server
make livehtml

# Serve documentation
make serve
```

### Using make.bat (Windows)

```cmd
REM Build HTML
make.bat html

REM Build PDF
make.bat latexpdf

REM Build EPUB
make.bat epub

REM Clean build
make.bat clean

REM Check links
make.bat linkcheck
```

## Writing Documentation

### File Formats

The documentation supports both reStructuredText (`.rst`) and Markdown (`.md`) files:

- **reStructuredText**: Primary format with full Sphinx features
- **Markdown**: Supported via MyST parser for simpler syntax

### Adding New Pages

1. Create new `.rst` or `.md` file in `source/`
2. Add it to the appropriate `toctree` directive
3. Rebuild documentation

Example:

```rst
.. toctree::
   :maxdepth: 2
   
   existing_page
   new_page
```

### API Documentation

API documentation is generated automatically from Python docstrings using Sphinx autodoc:

```rst
.. automodule:: game_builder_crew.crew
   :members:
   :undoc-members:
   :show-inheritance:
```

### Code Examples

Use code blocks with syntax highlighting:

```rst
.. code-block:: python

   from game_builder_crew.crew import GameBuilderCrew
   crew = GameBuilderCrew()
```

### Cross-References

Link to other documentation sections:

```rst
See :doc:`installation` for setup instructions.
Link to :ref:`specific-section` within a page.
```

## Customization

### Themes

The documentation uses the Read the Docs theme by default. To change themes, edit `conf.py`:

```python
html_theme = 'sphinx_rtd_theme'  # Current theme
# html_theme = 'furo'            # Alternative theme
# html_theme = 'sphinx_book_theme'  # Another option
```

### Styling

Custom CSS is in `source/_static/custom.css`. Modify this file to customize appearance.

### Configuration

Main configuration is in `source/conf.py`:

- Project information
- Extensions
- Theme settings
- Build options

## Output Formats

### HTML

- **Location**: `_build/html/`
- **Entry Point**: `_build/html/index.html`
- **Features**: Interactive, searchable, responsive

### PDF

- **Requirements**: LaTeX installation
- **Location**: `_build/latex/`
- **Command**: `make latexpdf`

### EPUB

- **Location**: `_build/epub/`
- **Features**: E-reader compatible format

## Troubleshooting

### Common Issues

**Import Errors in autodoc:**
```bash
# Make sure project is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/../../src"
```

**Missing Dependencies:**
```bash
pip install -r requirements-docs.txt
```

**Build Errors:**
```bash
# Clean build and retry
python build_docs.py clean
python build_docs.py build
```

**LaTeX/PDF Issues:**
```bash
# Install LaTeX (Ubuntu/Debian)
sudo apt-get install texlive-latex-recommended texlive-latex-extra

# Install LaTeX (macOS)
brew install --cask mactex

# Install LaTeX (Windows)
# Download and install MiKTeX or TeX Live
```

### Debugging

Enable verbose output:

```bash
sphinx-build -v source _build/html
```

Check for warnings:

```bash
sphinx-build -W source _build/html
```

## Contributing

When contributing to documentation:

1. Follow existing structure and style
2. Use clear, concise language
3. Include code examples where helpful
4. Test documentation builds locally
5. Check for broken links

### Style Guide

- Use present tense ("Click the button" not "You will click")
- Use active voice when possible
- Include code examples for complex concepts
- Use consistent terminology throughout
- Add cross-references to related topics

## Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [MyST Parser](https://myst-parser.readthedocs.io/)
- [Read the Docs Theme](https://sphinx-rtd-theme.readthedocs.io/)

---

For questions about the documentation system, please open an issue in the main repository.
