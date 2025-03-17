"""
the v2 version uses ofjustpy-react, i.e, ui_app_keymap, actions (with context), and app_to_ui using react context. 

"""

import ofjustpy as oj
from py_tailwind_utils import H, full, bg, green, rose
import ofjustpy_react as ojr

from .components_csvdata_input_v2 import input_panel 
from . import actions
app = oj.load_app()
ui_app_trmap = [
    ("/csvinput/panel", "/csvinput/url_and_content", None)
    ]

# manually initialize the form-request-data
def post_init(wp, session_manager=None):
    print("post_init called")
    assert "session_manager" != None
    request = wp.session_manager.request
    request.state.form_data = {}
    request.state.form_data["/csvinput/form"] = {'test': 1}
    pass

# TODO: the_app middleware is not being invoked. 
endpoint = ojr.create_endpoint("csv_data_input",
                                  [input_panel
                                   ],
                               ui_app_trmap_iter = ui_app_trmap,
                               action_module = actions,
                               rendering_type="CSR",
                               csr_bundle_dir="hyperui",
                               #path_guards = path_guards,
                               post_init = post_init,
                               head_html =  """<script src="https://cdn.tailwindcss.com"></script> """,
                               reactctx = [ojr.Ctx("/wp_redirect", ojr.isstr, ojr.UIOps.REDIRECT)],

                                  )
oj.add_jproute("/", endpoint)
    
# def wp_csvdata_input(request):
#     def panel_builder(session_manager):
#         with session_manager.uictx("body") as bodyCtx:
#             _ictx = bodyCtx
#             build_components(session_manager)
#             #print (_ictx.panel)
#             #aspan_ = oj.Span_("aspan", text=f"Requested item  does not exists in wiki")
#             #oj.Container_("panel", cgens=[_ictx.csvinput.input_panel], pcp=[bg/rose/2, flx.one])

#     path_guards = set()
#     path_guards.add("/metadata_report")
#     path_guards.add("/metadata_edits")            

#     wp =  page_builder("wp_csvdata_input",
#                         "Title here",
#                         panel_builder,
#                        WPtype=ojr.WebPage,
#                        ui_app_trmap_iter = ui_app_kmap,
#                        action_module = actions,
#                        path_guards = path_guards,
#                        reactctx = [ojr.Ctx("/wp_redirect", ojr.isstr, ojr.UIOps.REDIRECT)],
#                         )(request)
#     return wp

