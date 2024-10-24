"""
WTSS QGIS Plugin.

Python Client Library for Web Time Series Service.
Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/.
                              -------------------
begin                : 2019-05-04
git sha              : $Format:%H$
copyright            : (C) 2020 by INPE
email                : brazildatacube@dpi.inpe.br

This program is free software.

You can redistribute it and/or modify it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
WTSS QGIS Plugin documentation build configuration file, created by
sphinx-quickstart on Sun Feb 12 17:11:03 2012.
"""

import sphinx_rtd_theme

from wtss_plugin.version import __version__

# -- Project information -----------------------------------------------------

project = 'WTSS-QGIS'
copyright = '2020, INPE.'
author = 'Brazil Data Cube Team'

# The full version, including alpha/beta/rc tags.
release = __version__

# -- General configuration ---------------------------------------------------

# Enabled Sphinx extensions.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx_copybutton',
    'sphinx_rtd_theme',
]

# Paths that contain templates, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx.
language = 'en_US'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'analytics_id': 'XXXXXXXXXX',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'both',
    'style_external_links': True,
    'style_nav_header_background': '#2980B9',
    'collapse_navigation': True,
    'sticky_navigation': False,
    'navigation_depth': 3,
    'includehidden': True,
    'titles_only': False
}

html_title = 'WTSS-QGIS'

html_baseurl = 'https://brazil-data-cube.github.io/'

html_context = {
    'display_github': False,
    'github_user': 'brazil-data-cube',
    'github_repo': 'wtss-qgis',
    'last_updated': False,
}

html_show_sourcelink = False

html_logo = './assets/img/logo-bdc.png'

html_favicon = './assets/img/favicon.ico'

html_static_path = [
    '_static',
]

html_css_files = [ ]

html_last_updated_fmt = '%b %d, %Y'

html_show_sphinx = False

html_search_language = 'en'

numfig = True

numfig_format = {
    'figure': 'Figure %s -',
    'table': 'Table %s -',
    'code-block': 'Code snippet %s -',
    'section': 'Section %s.'
}

copybutton_prompt_text = r'>>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: '
copybutton_prompt_is_regexp = True

master_doc = 'index'
