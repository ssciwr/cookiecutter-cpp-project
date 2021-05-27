#pragma once

namespace {{ cookiecutter.project_slug.replace("-", "") }} {

{% if cookiecutter.doxygen == "Yes" -%}
/** @brief A very interesting function!
 *
 * This function is of course just a self-explanatory placeholder,
 * but surprisingly often, things aren't this easy. You should
 * therefore *really* document your C++ code with Doxygen!
 *
 * @param x The number to increase
 * @returns the successor of x
 */
{%- endif %}
{% if cookiecutter.header_only == "Yes" %}inline {% endif %}int add_one(int x){% if cookiecutter.header_only == "No" %};{%- else %}{
  return x + 1;
}
{%- endif %}

} // namespace {{ cookiecutter.project_slug.replace("-", "") }}
