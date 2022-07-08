import {{ cookiecutter|modname }}


def test_{{ cookiecutter|modname }}():
    assert {{ cookiecutter|modname }}.add_one(1) == 2
    assert {{ cookiecutter|modname }}.one_plus_one() == 2
