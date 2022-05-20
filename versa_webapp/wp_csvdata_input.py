"""
creates a webpage to input CSV file/url 
and analyze the content
"""

import logging
import os
import sys
if sys:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
import justpy as jp
from aenum import extend_enum, auto

import ofjustpy as oj
import ofjustpy_react as ojr

from .model_backend_actions import GEN_CSV_METADATAREPORT, CSV_URL_INPUT
from . import actions

#extend_enum(wf.ReactTag_ModelUpdate, 'CSV_URL_INPUT', CSV_URL_INPUT)
#extend_enum(wf.ReactTag_ModelUpdate, 'GEN_CSV_METADATAREPORT',
#            GEN_CSV_METADATAREPORT)

# import components_csvdata_input only after extend_enum

ui_app_trmap_iter = [ ("/csvinput/panel", ("/csvinput/url_and_content", None)
                       )
                     ]

app_app_trmap_iter = [
    ]
app_ui_trmap_iter = [("/wp_csvdata_input",  # 
                      ojr.AttrMeta(None, [ojr.Ctx("/wp_redirect", ojr.isstr, ojr.UIOps.REDIRECT)])
                      )

]

app_actions_trmap_iter = [
    ("/csvinput/url_and_content", [actions.ANALYZE_CSV_CONTENT, actions.SET_REDIRECT])
    
]                     


   
from .components_csvdata_input import build_components




# def make_wp_react(wp):

#     def react_ui(tag, arg):
#         logger.debug(f"in react_ui: {tag} {arg}")
#         match tag:
#             case wf.ReactTag_UI.PageRedirect:
#                 wp.redirect = "/csv_metadata"
#                 pass
#     wp.react_ui = react_ui

#     return


@jp.SetRoute('/csvdata_input')
def wp_csvdata_input(request):
    # stubStore.freeze()
    session_manager = oj.get_session_manager(request.session_id)
    
    stubStore = session_manager.stubStore
    appstate = session_manager.appstate

    # ========================== init appst ==========================
    appstate.csvinput.url_and_content = None
    
    # ========================= end init appstate =========================
    

    
    def page_ready(self, msg):
        stubStore.csvinput.csvurl.target.value =  'http://192.168.0.183:9000/airport_to_counties.csv'


    #directs all stubs created to be part of this session_manager
    with oj.sessionctx(session_manager):
        build_components(session_manager)
        oj.Container_("tlc", cgens=[stubStore.csvinput.panel])
        path_guards = set()
        path_guards.add("/metadata_report")
        path_guards.add("/metadata_edits")
        wp = oj.WebPage_("wp_csvdata_input", cgens=[stubStore.tlc], WPtype=ojr.WebPage,
                         
                        ui_app_trmap_iter=ui_app_trmap_iter, app_ui_trmap_iter=app_ui_trmap_iter,
                         app_actions_trmap_iter=app_actions_trmap_iter, path_guards=path_guards, session_manager=session_manager )()

        
    uistate = wp.uistate
    #initialize uistate with paths not in app_ui_trmap
    uistate.csvinput.panel = None
    #wp.model = session_dict.model
    #make_wp_react(wp)
    wp.session_manager = session_manager
    wp.on('page_ready', page_ready)
    return wp
