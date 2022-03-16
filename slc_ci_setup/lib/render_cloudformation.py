import jinja2


def render_cloudformation(template: str, **kwargs):
    env = jinja2.Environment(loader=jinja2.PackageLoader("slc_ci_setup"), autoescape=jinja2.select_autoescape())
    t = env.get_template(template)
    return t.render(**kwargs)
