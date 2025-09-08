# AI Academy Report Generator - Documentation

This directory contains the Sphinx documentation for the AI Academy Final Project Report Generator.

## Quick Start

### 1. Install Dependencies

```bash
# Using the build script (recommended)
python build_docs.py install

# Or manually
pip install -r requirements-docs.txt
```

### 2. Build Documentation

```bash
# Using the build script
python build_docs.py build

# Or using make (Windows)
make.bat html

# Or directly with Sphinx
sphinx-build -b html source _build/html
```

### 3. View Documentation

```bash
# Serve locally with the build script
python build_docs.py serve

# Or using make
make.bat serve

# Or manually
cd _build/html
python -m http.server 8000
```

Open your browser to `http://localhost:8000`

## Development Workflow

### Live Reload Development

For active documentation development with automatic rebuilding:

```bash
# Using the build script
python build_docs.py watch

# Or using make
make.bat watch

# Or directly
sphinx-autobuild source _build/html
```

This will:
- Watch source files for changes
- Automatically rebuild when files change
- Refresh your browser automatically
- Serve on `http://localhost:8000`

### Building Different Formats

```bash
# HTML (default)
python build_docs.py build

# PDF (requires LaTeX)
python build_docs.py build --builder latexpdf

# EPUB
python build_docs.py build --builder epub
```

## Documentation Structure

```
docs/
├── build_docs.py           # Build script with multiple commands
├── make.bat                # Windows batch file for building
├── requirements-docs.txt   # Documentation dependencies
├── README.md              # This file
├── source/                # Source files
│   ├── conf.py            # Sphinx configuration
│   ├── index.rst          # Main documentation index
│   ├── installation.rst   # Installation guide
│   ├── quickstart.rst     # Quick start guide
│   ├── usage.rst          # Usage documentation
│   ├── architecture/      # Architecture documentation
│   ├── api/              # API reference (auto-generated)
│   ├── examples/         # Example usage
│   ├── development/      # Development guides
│   └── _static/          # Static files (images, CSS, etc.)
└── _build/               # Generated documentation
    └── html/             # HTML output
```

## Writing Documentation

### RestructuredText (RST)

Most documentation is written in RST format:

```rst
Section Title
=============

Subsection
----------

This is a paragraph with **bold** and *italic* text.

.. code-block:: python

   def example_function():
       return "Hello, World!"

.. note::
   This is a note admonition.
```

### Markdown Support

Markdown files are also supported via MyST parser:

```markdown
# Section Title

## Subsection

This is a paragraph with **bold** and *italic* text.

```python
def example_function():
    return "Hello, World!"
```

:::{note}
This is a note admonition.
:::
```

### Auto-Generated API Documentation

API documentation is automatically generated from docstrings:

```python
def example_function(param1: str, param2: int = 0) -> str:
    """
    Example function with documented parameters.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2
        
    Returns:
        Description of return value
        
    Example:
        >>> example_function("hello", 42)
        "hello world"
    """
    return f"{param1} world"
```

## Advanced Features

### Mermaid Diagrams

Include diagrams using Mermaid syntax:

```rst
.. mermaid::

   graph TD
       A[Start] --> B[Process]
       B --> C[End]
```

### Cross-References

Link to other documentation sections:

```rst
See :doc:`installation` for setup instructions.
See :ref:`api-reference` for API details.
```

### Code Examples with Copy Button

Code blocks automatically include a copy button:

```rst
.. code-block:: python

   # This code block will have a copy button
   import report_generator
   result = report_generator.generate_report()
```

## Customization

### Themes

The documentation uses the Read the Docs theme by default. To change themes, edit `source/conf.py`:

```python
html_theme = 'sphinx_rtd_theme'  # Default
# html_theme = 'furo'            # Alternative modern theme
# html_theme = 'sphinx_book_theme'  # Book-style theme
```

### Extensions

Add new Sphinx extensions in `source/conf.py`:

```python
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'myst_parser',
    'sphinx_copybutton',
    # Add more extensions here
]
```

### Custom CSS

Add custom styling in `source/_static/custom.css` and reference it in `conf.py`:

```python
html_static_path = ['_static']
html_css_files = ['custom.css']
```

## Troubleshooting

### Common Issues

**Import errors when building API docs:**
- Ensure the project is installed: `pip install -e ../report_generator`
- Check Python path in `conf.py`

**Missing dependencies:**
- Run `python build_docs.py install`
- Check `requirements-docs.txt` for missing packages

**Build failures:**
- Check syntax in RST/Markdown files
- Verify all referenced files exist
- Look for missing cross-references

**Slow builds:**
- Use `sphinx-autobuild` for development
- Consider excluding large directories in `conf.py`

### Performance Tips

- Use `sphinx-autobuild` for development
- Enable parallel builds: `sphinx-build -j auto`
- Cache API documentation between builds

## Contributing

When adding new documentation:

1. Follow the existing structure
2. Use consistent formatting
3. Include code examples
4. Add cross-references where appropriate
5. Test your changes with `python build_docs.py build`
6. Check for broken links with `python build_docs.py linkcheck`

## Deployment

### GitHub Pages

The documentation can be deployed to GitHub Pages:

1. Build the documentation: `python build_docs.py build`
2. Copy `_build/html` contents to a `gh-pages` branch
3. Enable GitHub Pages in repository settings

### Read the Docs

For automatic building on Read the Docs:

1. Connect your repository to Read the Docs
2. Configure the build in `.readthedocs.yml` (if needed)
3. Documentation will build automatically on commits

## Getting Help

- Check the [Sphinx documentation](https://www.sphinx-doc.org/)
- Review [MyST Parser guide](https://myst-parser.readthedocs.io/)
- See [Read the Docs theme docs](https://sphinx-rtd-theme.readthedocs.io/)
- Ask questions in the project's GitHub issues
