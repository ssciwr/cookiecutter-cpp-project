{{ cookiecutter.project_name }}
{{ "=" * cookiecutter.project_name|length }}

.. toctree::
   :maxdepth: 2
   :caption: Contents:

This is an example function:

.. doxygenfunction:: {{ cookiecutter.project_slug.replace("-", "") }}::add_one
