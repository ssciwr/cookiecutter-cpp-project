{%- set modname = cookiecutter.project_slug.replace('-', '') -%}
from skbuild import setup
{%- if cookiecutter.use_submodules == "No" %}
import os
import pybind11
{%- endif %}


setup(
    name='{{ modname }}',
    version='0.0.1',
    author='{{ cookiecutter.full_name }}',
    author_email='your@email.com',
    description='Add description here',
    long_description='',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
{%- if cookiecutter.license == "MIT" %}
        "License :: OSI Approved :: MIT License",
{%- elif cookiecutter.license == "BSD-2" %}
        "License :: OSI Approved :: BSD License",
{%- elif cookiecutter.license == "GPL-3.0" %}
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
{%- elif cookiecutter.license == "LGPL-3.0" %}
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
{%- endif %}
    ],
    zip_safe=False,
    packages=["{{ modname }}"],
    cmake_args=[
        "-DBUILD_TESTING=OFF",
        "-DBUILD_DOCS=OFF",
{%- if cookiecutter.use_submodules == "No" %}
        f"-DCMAKE_PREFIX_PATH={os.path.dirname(pybind11.__file__)}",
{%- endif %}
    ],
    package_dir={"": "python"},
    cmake_install_dir="python/{{ modname }}",
)
