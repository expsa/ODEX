
import json
from lxml import html
from odoo.addons.base.ir.ir_qweb.qweb  import QWeb
from werkzeug import urls
from odoo.http import request
from odoo import models, tools
from odoo.tools import pycompat
from odoo.modules.module import get_resource_path

class IrQWeb(models.AbstractModel, QWeb):
    """ Base QWeb rendering engine
    * to customize ``t-field`` rendering, subclass ``ir.qweb.field`` and
      create new models called :samp:`ir.qweb.field.{widget}`
    Beware that if you need extensions or alterations which could be
    incompatible with other subsystems, you should create a local object
    inheriting from ``ir.qweb`` and customize that.
    """

    _inherit = 'ir.qweb'

    @tools.ormcache_context('xmlid', 'options.get("lang", "en_US")', keys=("website_id",))
    def _get_asset_content(self, xmlid, options):
        options = dict(options,
            inherit_branding=False, inherit_branding_auto=False,
            edit_translations=False, translatable=False,
            rendering_bundle=True)

        env = self.env(context=options)

        # TODO: This helper can be used by any template that wants to embedd the backend.
        #       It is currently necessary because the ir.ui.view bundle inheritance does not
        #       match the module dependency graph.
        def get_modules_order():
            if request:
                from odoo.addons.web.controllers.main import module_boot
                return json.dumps(module_boot())
            return '[]'
        template = env['ir.qweb'].render(xmlid, {"get_modules_order": get_modules_order})
        if options.get("lang", "en_US").startswith('ar'):
            template += b'''\n<link href="/web_rtl/static/src/css/bootstrap-rtl.min.css" rel="stylesheet"/>
                            \n<link href="/report_rtl/static/src/css/rtl.css" rel="stylesheet"/>\n'''
        files = []
        remains = []
        for el in html.fragments_fromstring(template):
            if isinstance(el, pycompat.string_types):
                remains.append(pycompat.to_text(el))
            elif isinstance(el, html.HtmlElement):
                href = el.get('href', '')
                src = el.get('src', '')
                atype = el.get('type')
                media = el.get('media')

                can_aggregate = not urls.url_parse(href).netloc and not href.startswith('/web/content')
                if el.tag == 'style' or (el.tag == 'link' and el.get('rel') == 'stylesheet' and can_aggregate):
                    if href.endswith('.sass'):
                        atype = 'text/sass'
                    elif href.endswith('.less'):
                        atype = 'text/less'
                    if atype not in ('text/less', 'text/sass'):
                        atype = 'text/css'
                    path = [segment for segment in href.split('/') if segment]
                    filename = get_resource_path(*path) if path else None
                    files.append({'atype': atype, 'url': href, 'filename': filename, 'content': el.text, 'media': media})
                elif el.tag == 'script':
                    atype = 'text/javascript'
                    path = [segment for segment in src.split('/') if segment]
                    filename = get_resource_path(*path) if path else None
                    files.append({'atype': atype, 'url': src, 'filename': filename, 'content': el.text, 'media': media})
                else:
                    remains.append(html.tostring(el, encoding='unicode'))
            else:
                try:
                    remains.append(html.tostring(el, encoding='unicode'))
                except Exception:
                    # notYETimplementederror
                    raise NotImplementedError

        return (files, remains)