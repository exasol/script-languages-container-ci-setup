import jinja2


def _get_env():
    return jinja2.Environment(
        loader=jinja2.PackageLoader("exasol.slc_ci_setup"),
        autoescape=jinja2.select_autoescape(),
        keep_trailing_newline=True,
    )


def list_templates(prefix: str):
    env = _get_env()
    return env.list_templates(filter_func=lambda t: t.startswith(prefix))


def render_template(template: str, **kwargs):
    env = _get_env()
    t = env.get_template(template)
    return t.render(**kwargs)
