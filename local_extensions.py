from jinja2.ext import Extension


# Check whether we have pre-commit or not
try:
    import pre_commit
    have_precommit = True
except ImportError:
    have_precommit = False


class PrecommitExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)

        environment.globals.update({
            "have_precommit": have_precommit
        })