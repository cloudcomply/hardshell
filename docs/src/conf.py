from pathlib import Path

CURRENT_DIR = Path(__file__).parent

# Global Variables
author_name = "Tom Burge"
project_name = "hardshell"
release_name = "0.1.4"
version_name = "0.1.4"

# -- Options for Project Configuration ------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = f"{project_name}"
author = f"{author_name} and contributors to {project_name}"
copyright = f"2023-Present, {author_name} and contributors to {project_name}"
release = release_name
version = version_name

# -- Options for General Configuration ------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
add_function_parentheses = True
add_module_names = True
default_role = None
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
extensions = [
    # 1st Party Extensions
    # "sphinx.ext.autodoc", # Include documentation from docstrings
    # "sphinx.ext.autosectionlabel", # Allow reference sections using its title
    # "sphinx.ext.autosummary", # Generate autodoc summaries
    # "sphinx.ext.coverage", # Collect doc coverage stats
    # "sphinx.ext.doctest", # Test snippets in the documentation
    # "sphinx.ext.duration", # Measure durations of Sphinx processing
    # "sphinx.ext.extlinks", # Markup to shorten external links
    # "sphinx.ext.githubpages", # Publish HTML docs in GitHub Pages
    # "sphinx.ext.graphviz", # Add Graphviz graphs
    # "sphinx.ext.ifconfig", # Include content based on configuration
    # "sphinx.ext.imgconverter", # A reference image converter using Imagemagick
    # "sphinx.ext.inheritance_diagram", # Include inheritance diagrams
    # "sphinx.ext.intersphinx", # Link to other projects’ documentation
    # "sphinx.ext.linkcode", # Add external links to source code
    # "sphinx.ext.napoleon", # Support for NumPy and Google style docstrings
    # "sphinx.ext.todo", # Support for todo items
    # "sphinx.ext.viewcode", # Add links to highlighted source code
    # 3rd Party Extensions
    "myst_parser",  # A rich and extensible flavor of Markdown meant for technical documentation and publishing.
    "sphinx_copybutton",  # A small sphinx extension to add a "copy" button to code blocks.
    "sphinxcontrib.programoutput",  # Include program output (e.g. console output) in Sphinx documentation.
]
highlight_language = "default"
highlight_options = {}  # https://pygments.org/docs/lexers/
# include_patterns = []
keep_warnings = False
# manpages_url = ""
maximum_signature_line_length = None
# modindex_common_prefix = []
# needs_extensions = {}
needs_sphinx = "7.3.7"
nitpicky = False
# nitpicky_ignore = ()
# nitpicky_ignore_regex = ()
numfig = False
numfig_format = {
    "figure": "Fig. %s",
    "listing": "Listing %s",
    "table": "Table %s",
}
numfig_secnum_depth = 1
# option_emphasise_placeholders = False
primary_domain = "py"
pygments_style = "sphinx"
# rst_epilog = ""
# rst_prolog = ""
root_doc = "index"
show_authors = True
show_warning_types = False
smartquotes = True
smartquotes_action = "qDe"
smartquotes_excludes = {"languages": ["ja"], "builders": ["man", "text"]}
source_encoding = "utf-8-sig"
# source_parsers = None
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
strip_signature_backslash = False
suppress_warnings = [
    # Sphinx core warnings
    # "app.add_node",
    # "app.add_directive",
    # "app.add_role",
    # "app.add_generic_role",
    # "app.add_source_parser",
    # "config.cache",
    # "download.not_readable",
    # "epub.unknown_project_files",
    # "epub.duplicated_toc_entry",
    # "i18n.inconsistent_references",
    # "image.not_readable",
    # "index",
    # "misc.highlighting_failure",
    # "ref.term",
    # "ref.ref",
    # "ref.numref",
    # "ref.keyword",
    # "ref.option",
    # "ref.citation",
    # "ref.footnote",
    # "ref.doc",
    # "ref.python",
    # "toc.circular",
    # "toc.excluded",
    # "toc.not_readable",
    # "toc.secnum",
    # Sphinx 1st party warnings
    # "autodoc",
    # "autodoc.import_object",
    # "autosectionlabel.<document name>",
    # "autosummary",
    # "intersphinx.external",
]
# templates_bridge = ""
templates_path = ["_templates"]
# tls_cacerts = "/path/to/cacert.pem"
tls_verify = True
toc_object_entries = True
toc_object_entries_show_parents = "domain"  # all | domain | hide
trim_doctest_flags = True
# trim_footnote_reference_space = True
# today = None
today_fmt = "%b %d, %Y"
# user_agent = "Sphinx/X.Y.Z requests/X.Y.Z python/X.Y.Z"

# -- Options for Internationalization Configuration -----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-internationalization
# figure_language_filename = "{root}.{language}{ext}"
# gettext_additional_targets = []
# gettext_allow_fuzzy_translations = False
# gettext_auto_build = True
# gettext_compact = False
# gettext_location = True
# gettext_uuid = False
language = "en"
# locale_dirs = []
# translation_progress_classes = False

# -- Options for Math Configuration ---------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-math
# math_eqref_format = ""
math_number_all = False
math_numfig = True

# -- Options for Apple Help output ----------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-apple-help-output
# applehelp_bundle_id = ""
# applehelp_bundle_name = "<project>"
# applehelp_bundle_version = "1"
# applehelp_codesign_identity = None
# applehelp_codesign_flags = []
# applehelp_codesign_path = "/usr/bin/codesign"
# applehelp_dev_region = "en-us"
# applehelp_disable_external_tools = False
# applehelp_icon = None
# applehelp_index_anchors = False
# applehelp_indexer_path = "/usr/bin/hiutil"
# applehelp_kb_product = "<project>-<release>"
# applehelp_kb_url = None
# applehelp_locale = "en"
# applehelp_min_term_length = None
# applehelp_remote_url = None
# applehelp_stopwords = "en"
# applehelp_title = "<project> Help"

# -- Options for Epub output ----------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-epub-output
# epub_author = author
# epub_basename = project
# epub_contributor = "unknown"
# epub_copyright = copyright
# epub_cover = ()
# epub_css_files = {}
# epub_description = "unknown"
# epub_exclude_files = []
# epub_fix_images = False
# epub_guide = ()
# epub_identifier = "unknown"
# epub_language = "en"
# epub_max_image_width = 0
# epub_post_files = []
# epub_pre_files = []
# epub_publisher = author
# epub_scheme = "unknown"
# epub_show_urls = "inline"
# epub_theme = "epub"
# epub_theme_options = {}
# epub_title = project
# epub_tocdepth = 3
# epub_tocscope = "default"
# epub_tocdup = True
# epub_uid = "unknown"
# epub_use_index = True
# epub_writing_mode = "horizontal"

# -- Options for HTML output ----------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# html_additional_pages = {}
# html_baseurl = ""
html_codeblock_linenos_style = "inline"
html_compact_lists = True
# html_context = {}
html_copy_source = True
# html_css_files = []
# html_domain_indices = True
html_experimental_html5_writer = False
# html_extra_path = []
# html_favicon = None
html_file_suffix = None
# html_js_files = []
html_last_updated_fmt = "%b %d, %Y"
html_link_suffix = html_file_suffix
# html_logo = None
html_math_renderer = "mathjax"
html_output_encoding = "utf-8"
html_permalinks = True
html_permalinks_icon = "¶"
html_scaled_image_link = True
html_search_language = "en"
# html_search_options = {}
# html_search_scorer = ""
html_secnumber_suffix = ". "
# html_short_title = html_title
html_show_copyright = True
html_show_search_summary = True
html_show_sourcelink = True
html_show_sphinx = False
# html_sidebars = {}
html_sourcelink_suffix = ".txt"
html_split_index = False
html_static_path = ["_static"]
# html_style = ""
html_theme = "furo"
html_theme_options = {}
# html_theme_path = []
# html_title = "<project> v<revision> documentation"
html_use_index = True
# html_use_opensearch = ""
html_use_smartypants = True
html4_writer = False

### HTML Help Output
# htmlhelp_basename = "hardshelldoc"
# htmlhelp_file_suffix = ".html"
# htmlhelp_link_suffix = ".html"

### Single HTML
# singlehtml_sidebars = {}

# -- Options for LaTeX output ---------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-latex-output
# latex_additional_files = []
# latex_appendices = []
# latex_docclass = "jsbook"
# latex_documents = ()
# latex_domain_indices = True
# latex_elements = ""
# latex_engine = "pdflatex"
# latex_logo = None
# latex_toplevel_sectioning = None
# latex_show_pagerefs = False
# latex_show_urls = "no"
# latex_table_style = ["booktabs", "colorrows"]
# latex_theme = "manual"
# latex_theme_options = {}
# latex_theme_path = []
# latex_use_latex_multicolumn = False
# latex_use_xindy = False

# -- Options for Manul Page output ----------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-manual-page-output
# man_make_section_directory = True
# man_pages = []
# man_show_urls = False

# -- Options for Text output ----------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-text-output
# text_add_secnumbers = True
# text_newlines = "unix"
# text_sectionchars = '*=-~"+`'
# text_secnumber_suffix = ". "

# -- Options for Texinfo output -------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-texinfo-output
# texinfo_appendices = []
# texinfo_cross_references = True
# texinfo_documents = []
# texinfo_domain_indices = True
# texinfo_elements = {}
# texinfo_no_detailmenu = False
# texinfo_show_urls = "footnote"

# -- Options for QtHelp output --------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-qthelp-output
# qthelp_basename = project
# qthelp_namespace = "org.sphinx.<project_name>.<project_version>"
# qthelp_theme = "nonav"
# qthelp_theme_options = {}

# -- Options for Linkcheck Builder ----------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-linkcheck-builder
# linkcheck_allow_unauthorized = False
# linkcheck_allowed_redirects = {}
# linkcheck_anchors = True
# linkcheck_anchors_ignore = ["^!"]
# linkcheck_anchors_ignore_for_url = ()
# linkcheck_auth = []
# linkcheck_exclude_documents = []
# linkcheck_ignore = []
# linkcheck_rate_limit_timeout = 300
# linkcheck_report_timeouts_as_broken = False
# linkcheck_request_headers = {}
# linkcheck_retries = 1
# linkcheck_timeout = 30
# linkcheck_workers = 5

# -- Options for XML Builder ----------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-xml-builder
# xml_pretty = True

# -- Options for C Domain -------------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-c-domain
# c_extra_keywords = []
# c_id_attributes = []
# c_maximum_signature_line_length = maximum_signature_line_length
# c_paren_attributes = []

# -- Options for C++ Domain -----------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#cpp-config
# cpp_id_attributes = []
# cpp_index_common_prefix = []
# cpp_maximum_signature_line_length = maximum_signature_line_length
# cpp_paren_attributes = []

# -- Options for Python Domain --------------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-python-domain
# python_display_short_literal_types = False
# python_maximum_signature_line_length = maximum_signature_line_length
# python_use_unqualified_type_names = False

# -- Options for JavaScript Domain ----------------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-javascript-domain
# javascript_maximum_signature_line_length = maximum_signature_line_length
