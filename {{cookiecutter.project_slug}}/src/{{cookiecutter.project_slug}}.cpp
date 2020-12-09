#include "{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}.hpp"

namespace {{ cookiecutter.project_slug.replace("-", "") }} {

int add_one(int x){
  return x + 1;
}

} // namespace {{ cookiecutter.project_slug.replace("-", "") }}