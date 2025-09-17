
project = "k4GeneratorsConfig"
copyright = "2025, k4GeneratorsConfig"
author = "k4GeneratorsConfig"
# html_theme = "furo"
html_theme = "sphinx_rtd_theme"
master_doc = "index"  # without extension

html_context = {
    "display_github": False,
    "github_user": "key4hep",
    "github_repo": "key4hep-doc",
    "github_version": "main",
    "conf_py_path": "/",
}

extensions = [
    "sphinx_copybutton",
    "sphinx_markdown_tables",
    "sphinx_design",
    "myst_parser",
    "sphinx.ext.mathjax"
]

source_suffix = {
    ".md": "markdown",
}


myst_heading_anchors = 4

myst_enable_extensions = ["colon_fence", "html_image", "dollarmath"]