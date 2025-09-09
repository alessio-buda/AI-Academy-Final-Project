# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import sphinx_rtd_theme

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Game Builder Crew'
copyright = '2025, CrewAI Examples Team'
author = 'CrewAI Examples Team'
release = '1.0.0'
version = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',        # Include documentation from docstrings
    'sphinx.ext.autosummary',    # Generate autodoc summaries
    'sphinx.ext.viewcode',       # Include links to the source code of documented Python objects
    'sphinx.ext.napoleon',       # Support for NumPy and Google style docstrings
    'sphinx.ext.intersphinx',    # Link to other project's documentation
    'sphinx.ext.githubpages',    # Publish HTML docs in GitHub Pages
    'sphinx.ext.todo',           # Support for todo items
    'sphinx.ext.coverage',       # Collect doc coverage stats
    'sphinx.ext.ifconfig',       # Include content based on configuration
    'myst_parser',               # Support for Markdown files
    'sphinx_copybutton',         # Add copy button to code blocks
    'sphinx_design',             # Design elements like cards, tabs, etc.
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
source_suffix = {
    '.rst': None,
    '.md': 'myst_parser',
}

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
html_sidebars = {
    '**': [
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
    ]
}

# Output file base name for HTML help builder.
htmlhelp_basename = 'GameBuilderCrewdoc'

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    'preamble': '',

    # Latex figure (float) alignment
    'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'GameBuilderCrew.tex', 'Game Builder Crew Documentation',
     'CrewAI Examples Team', 'manual'),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'gamebuilder', 'Game Builder Crew Documentation',
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'GameBuilderCrew', 'Game Builder Crew Documentation',
     author, 'GameBuilderCrew', 'AI-powered game development crew using CrewAI.',
     'Miscellaneous'),
]

# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'crewai': ('https://docs.crewai.com/', None),
}

# -- Options for autodoc extension -------------------------------------------

# This value selects what content will be inserted into the main body of an autoclass directive
autoclass_content = 'both'

# This value is a list of autodoc directive flags that should be automatically applied to all autodoc directives
autodoc_default_flags = ['members', 'undoc-members', 'show-inheritance']

# This value controls the docstrings inheritance
autodoc_inherit_docstrings = True

# -- Options for napoleon extension ------------------------------------------

# True to parse NumPy style docstrings. False to disable NumPy style docstrings.
napoleon_numpy_docstring = True

# True to parse Google style docstrings. False to disable Google style docstrings.
napoleon_google_docstring = True

# True to include private members (like _membername) with docstrings in the documentation.
napoleon_include_private_with_doc = False

# True to include special members (like __membername__) with docstrings in the documentation.
napoleon_include_special_with_doc = True

# True to use the .. admonition:: directive for the Example and Examples sections.
napoleon_use_admonition_for_examples = False

# True to use the .. admonition:: directive for Notes sections.
napoleon_use_admonition_for_notes = False

# True to use the .. admonition:: directive for References sections.
napoleon_use_admonition_for_references = False

# True to use the :ivar: role for instance variables.
napoleon_use_ivar = False

# True to use the :param: role for parameters.
napoleon_use_param = True

# True to use the :rtype: role for the return type.
napoleon_use_rtype = True

# -- Options for MyST parser ------------------------------------------------

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]

# -- Custom CSS -------------------------------------------------------------

def setup(app):
    app.add_css_file('custom.css')
