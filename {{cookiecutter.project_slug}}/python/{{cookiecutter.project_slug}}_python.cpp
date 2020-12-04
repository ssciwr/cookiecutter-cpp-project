#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}.hpp"

namespace py = pybind11;

namespace {{ cookiecutter.project_slug.replace("-", "") }} {

PYBIND11_MODULE({{ cookiecutter.project_slug }}_python, m)
{
  m.doc() = "Python Bindings for {{ cookiecutter.project_name }}";
  m.def("add_one", &add_one, "Increments an integer value");
}

} // namespace {{ cookiecutter.project_slug.replace("-", "") }}
