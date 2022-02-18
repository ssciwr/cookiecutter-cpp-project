{%- set modname = cookiecutter.project_slug.replace("-", "") -%}
import {{ modname }}


def test_{{ modname }}():
    assert {{ modname }}.add_one(1) == 2
    assert {{ modname }}.one_plus_one() == 2
