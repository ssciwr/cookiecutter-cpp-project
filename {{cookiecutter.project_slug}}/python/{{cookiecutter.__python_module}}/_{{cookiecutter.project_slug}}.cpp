{% if cookiecutter.python_bindings == "pybind11" -%}
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
{%- elif cookiecutter.python_bindings == "nanobind" %}
#include <nanobind/nanobind.h>
{%- endif %}

#include "{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}.hpp"

{% if cookiecutter.python_bindings == "pybind11" -%}
namespace py = pybind11;
{%- elif cookiecutter.python_bindings == "nanobind" %}
namespace nb = nanobind;
{%- endif %}

namespace {{ cookiecutter|modname }} {

{% if cookiecutter.python_bindings == "pybind11" -%}
PYBIND11_MODULE{%- elif cookiecutter.python_bindings == "nanobind" %}
NB_MODULE
{%- endif -%}
(_{{ cookiecutter|modname }}, m)
{
  m.doc() = "Python Bindings for {{ cookiecutter.project_name }}";
  m.def("add_one", &add_one, "Increments an integer value");
}

} // namespace {{ cookiecutter|modname }}
