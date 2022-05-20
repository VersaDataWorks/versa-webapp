"""
creates a webpage to analyze CSV data
and display its schema and metadata
"""

import logging
import os
import sys
if sys:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
import justpy as jp
import ofjustpy as oj
import ofjustpy_react as ojr
from .components_csv_schema_metadata import build_components
from . import actions
ui_app_trmap_iter = [ ("/gencsvcfg_panel", ("/gencsvcfg_panel", None)
                       )
                     ]

#its called app_ui_trmap but ui-spath comes first followed by list of app-paths in the ojr.Ctx
app_ui_trmap_iter = [("/wp_csv_schema_metadata",  # 
                      ojr.AttrMeta(None, [ojr.Ctx("/wp_redirect", ojr.isstr, ojr.UIOps.REDIRECT)])
                      ),
                     ("/csm/colnames/selector_0", ojr.AttrMeta("col_0", [])),
                     ("/csm/colnames/selector_1", ojr.AttrMeta("col_1", [])),
                     ("/csm/colnames/selector_2", ojr.AttrMeta("col_1", [])),
                     ("/csm/colnames/is_pk_0cbox", ojr.AttrMeta("True", [])),
                     ("/csm/colnames/is_pk_1cbox", ojr.AttrMeta("False", [])),
                     ("/csm/colnames/is_pk_2cbox", ojr.AttrMeta("True", [])),
                     ("/csm/colnames/is_hn_0cbox", ojr.AttrMeta("True", [])),
                     ("/csm/colnames/is_hn_1cbox", ojr.AttrMeta("False", [])),
                     ("/csm/colnames/is_hn_2cbox", ojr.AttrMeta("True", [])),                     
                     ("/csm/coltypes/selector_0", ojr.AttrMeta("int", [])),
                     ("/csm/coltypes/selector_1", ojr.AttrMeta("string", [])),
                     ("/csm/coltypes/selector_2", ojr.AttrMeta("float", [])),
                     ("/csm/gencsvcfg/btninput", ojr.AttrMeta("testmodel", []))
]

app_actions_trmap_iter = [
    ("/gencsvcfg_panel", [actions.CSV_METADATA_AS_XML, actions.SET_REDIRECT])
    
]                     

path_guards = set(["/gencsvcfg_panel", "/metadata_report", "/metadata_edits"])

# def make_wp_react(wp):

#     def react_ui(tag, arg):
#         logger.debug(f"in react_ui: {tag} {arg}")
#         match tag:
#             case wf.ReactTag_UI.PageRedirect:
#                 wp.redirect = "/savecfg"
#                 pass
#     wp.react_ui = react_ui

#     return


@jp.SetRoute('/csv_schema_metadata')
def wp_csv_schema_metadata(request):
    logger.debug("building webpage")
    session_manager = oj.get_session_manager(request.session_id)
    stubStore = session_manager.stubStore
    appstate = session_manager.appstate
    appstate.gencsvcfg_panel = None
    appstate.clear_changed_history()
    # ========================== init appst ==========================
    #appstate.csvinput.url_and_content = None
    appstate.csvinput.url_and_content = ('http://192.168.0.183:9000/airport_to_counties.csv', None)
    actions.ANALYZE_CSV_CONTENT(appstate, None)
    # ========================= end init appstate =========================
    with oj.sessionctx(session_manager):
        build_components(session_manager)
        oj.Container_("tlc",
                      cgens=[stubStore.csm.Halignpagetitle,
                             stubStore.csm.stats.section,
                             stubStore.csm.headers,
                             stubStore.csm.samples.section,
                             stubStore.csm.coltypes.section,
                             stubStore.csm.colnames.section,
                             stubStore.csm.gencsvcfg.section

                         ])
        wp = oj.WebPage_("wp_csv_schema_metadata",
                         cgens=[stubStore.tlc],
                         WPtype=ojr.WebPage,
                         ui_app_trmap_iter=ui_app_trmap_iter,
                         app_ui_trmap_iter=app_ui_trmap_iter,
                         app_actions_trmap_iter=app_actions_trmap_iter,
                         path_guards=path_guards,
                         enable_quasar=True,
                         session_manager=session_manager )()
        wp.session_manager = session_manager
        uistate = wp.uistate
        #initialize uistate with paths not in app_ui_trmap
        uistate.gencsvcfg_panel = None
        #wp = wf.WebPage_("wp", page_type="quasar", cgens=[stubStore.tlc])()
        #wp.model = session_dict.model  # TODO: should happen automatically, i think
        #make_wp_react(wp)
    return wp
