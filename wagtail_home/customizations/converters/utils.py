import markdown

def render_markdown(markdown_text):
    html = markdown.markdown(markdown_text,
                             extensions=[
                                 "extra",
                                 "codehilite",
                                 "wagtail_home.customizations.converters.mathjax_converter.converter"
                             ],
                             extension_configs={
                                 'codehilite': [
                                     ('guess_lang', False),
                                 ]
                             },
                             output_format="html5")
    return html