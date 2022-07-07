{%- set modname = cookiecutter.project_slug.replace('-', '') -%}
from skbuild import setup
{%- if cookiecutter.use_submodules == "No" %}
import os
import pybind11
{%- endif %}


setup(
    packages=["{{ modname }}"],
    package_dir={"": "python"},
    zip_safe=False,
    cmake_args=[
        "-DBUILD_TESTING=OFF",
        "-DBUILD_DOCS=OFF",
{%- if cookiecutter.use_submodules == "No" %}
        f"-DCMAKE_PREFIX_PATH={os.path.dirname(pybind11.__file__)}",
{%- endif %}
    ],
    cmake_install_dir="python/{{ modname }}",
)
