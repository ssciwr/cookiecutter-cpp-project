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
{% endif %}
{{ "inline " if cookiecutter.header_only == "Yes" }}int
add_one(int x){{ ";" if cookiecutter.header_only == "No" }}
{% if cookiecutter.header_only == "Yes" %}
{
  return x + 1;
}
{% endif %}

} // namespace {{ cookiecutter.project_slug.replace("-", "") }}
