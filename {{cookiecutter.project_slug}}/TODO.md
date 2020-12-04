This TODO list is automatically generated from the cookiecutter-cpp-project template.
The following tasks need to be done to get a fully working project:

* Set up a remote repository. You can e.g. create a project in GitHub or GitLab and run
  the following commands in your locally generated project folder:
  `git remote add origin <Remote-URL>`
{%- if cookiecutter.gitlab_ci == "Yes" -%}
* Make sure that CI/CD pipelines are enabled in your Gitlab project settings and that
  there is a suitable Runner available. If you are using the cloud-hosted gitlab.com,
  this should already be taken care of.
{%- endif -%}
{%- if cookiecutter.travis_ci == "Yes" -%}
* Enable your Travis CI integration by logging into travis-ci.org and enabling the
  relevant repository from e.g. your public Github repositories.
{%- endif -%}