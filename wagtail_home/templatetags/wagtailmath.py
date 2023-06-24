from tags.templatetags import register
from wagtail_home.customizations.widgets.math_jax import MATHJAX_VERSION


@register.simple_tag
def mathjax(config='TeX-MML-AM_CHTML'):
    return f'https://cdnjs.cloudflare.com/ajax/libs/mathjax/{MATHJAX_VERSION}/MathJax.js?config={config}'
