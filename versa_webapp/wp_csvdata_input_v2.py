"""
the v2 version uses ofjustpy-react, i.e, ui_app_keymap, actions (with context), and app_to_ui using react context. 
It also use templates. and versa webapp uistyles.
"""

from .wp_template import page_builder
import ofjustpy as oj
import justpy as jp
from tailwind_tags import H, full, bg, green, rose, flx
import ofjustpy_react as ojr

from .components_csvdata_input_v2 import build_components
from . import actions
app = jp.build_app()
ui_app_kmap = [
    ("/csvinput/panel", "/csvinput/url_and_content", None)
    ]
def wp_csvdata_input(request):
    def panel_builder(session_manager):
        with session_manager.uictx("body") as bodyCtx:
            _ictx = bodyCtx
            build_components(session_manager)
            print (_ictx.panel)
            #aspan_ = oj.Span_("aspan", text=f"Requested item  does not exists in wiki")
            #oj.Container_("panel", cgens=[_ictx.csvinput.input_panel], pcp=[bg/rose/2, flx.one])

    path_guards = set()
    path_guards.add("/metadata_report")
    path_guards.add("/metadata_edits")            

    wp =  page_builder("wp_csvdata_input",
                        "Title here",
                        panel_builder,
                       WPtype=ojr.WebPage,
                       ui_app_trmap_iter = ui_app_kmap,
                       action_module = actions,
                       path_guards = path_guards,
                       reactctx = [ojr.Ctx("/wp_redirect", ojr.isstr, ojr.UIOps.REDIRECT)],
                        )(request)
    return wp

