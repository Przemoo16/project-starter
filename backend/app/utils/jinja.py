import jinja2

from app.utils import translation

env = jinja2.Environment(  # nosec
    loader=jinja2.PackageLoader("app", "templates"),
    autoescape=jinja2.select_autoescape(["html", "htm", "xml", "html.jinja"]),
    extensions=["jinja2.ext.i18n"],
)
env.install_gettext_translations(translation.translations)
