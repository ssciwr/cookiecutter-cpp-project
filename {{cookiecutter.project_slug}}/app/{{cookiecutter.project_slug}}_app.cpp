#include "{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}.hpp"
#include <iostream>

int main(){
  int result = {{ cookiecutter.project_slug.replace("-", "") }}::add_one(1);
  std::cout << "1 + 1 = " << result << std::endl;
}