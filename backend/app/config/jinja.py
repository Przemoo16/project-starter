import jinja2

env = jinja2.Environment(  # nosec
    loader=jinja2.PackageLoader("app", "templates"),
    autoescape=jinja2.select_autoescape(["html", "htm", "xml", "j2"]),
)
