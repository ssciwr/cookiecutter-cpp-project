{{ cookiecutter.project_name}}
{% for c in "{{ cookiecutter.project_name}}" %}={% endfor %}

.. toctree::
   :maxdepth: 2
   :caption: Contents:

This is an example function:

.. doxygenfunction:: {{ cookiecutter.project_slug.replace("-", "") }}::add_one
