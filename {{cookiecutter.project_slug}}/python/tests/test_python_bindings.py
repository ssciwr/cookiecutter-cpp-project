import {{ cookiecutter.project_slug.replace("-", "") }}


def test_{{ cookiecutter.project_slug.replace("-", "_") }}():
    assert {{ cookiecutter.project_slug.replace("-", "") }}.add_one(1) == 2
