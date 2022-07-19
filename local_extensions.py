import datetime

from jinja2.ext import Extension

#
# Export the current date
#

class CurrentDateExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)

        environment.globals.update({
            "current_year": datetime.datetime.utcnow().year
        })

#
# Check whether we have pre-commit or not and make the result available
# as a template variable 'have_precommit'
#

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

#
# Define several convenience functions and register them as Jinja2 filters.
# Otherwise, this logic would be duplicated all over the cookiecutter. The
# usage of these is e.g. {{ cookiecutter|modname }}. I don't see a way around
# passing the cookiecutter dictionary as data input currently
#

def _modname(data):
    return data["project_slug"].replace("-", "")


def _is_github(data):
    return "github.com" in data["remote_url"]


def _is_gitlab(data):
    return "gitlab" in data["remote_url"]


def _provider_acronym(data):
    if _is_github(data):
        return "gh"
    if _is_gitlab(data):
        return "gl"
    return "none"


def _username(data):
    if data["remote_url"] == "None":
        return "None"
    
    return data["remote_url"].split("/")[-2].split(":")[-1]


def _remote_slug(data):
    if data["remote_url"] == "None":
        return "None"

    return data["remote_url"].replace(".git", "").split("/")[-1]


def _gitlab_instance(data):
    if data["remote_url"] == "None":
        return "None"

    return "https%3A%2F%2F" + data["remote_url"].replace("https://", "").replace("ssh://git@", "").split("/")[0].split(":")[0]


class ShortcutExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)

        environment.filters.update({
            "gitlab_instance": _gitlab_instance,
            "is_github": _is_github,
            "is_gitlab": _is_gitlab,
            "modname": _modname,
            "provider_acronym": _provider_acronym,
            "remote_slug": _remote_slug,
            "username": _username,
        })
