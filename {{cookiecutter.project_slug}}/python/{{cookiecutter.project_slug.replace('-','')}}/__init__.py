{%- set modname = cookiecutter.project_slug.replace("-", "") -%}
from {{ modname }}._{{ modname }} import add_one


def one_plus_one():
    return add_one(1)
