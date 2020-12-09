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
int add_one(int x);

} // namespace {{ cookiecutter.project_slug.replace("-", "") }}
