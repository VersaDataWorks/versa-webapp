import logging
import os
import sys
from base64 import b64encode
import versa_engine as ve
import pickle

if sys:
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename="launcher.log",
                        level=logging.DEBUG, format=FORMAT)

    logger = logging.getLogger(__name__)
from base64 import b64encode
import justpy as jp
import ofjustpy as oj
import ofjustpy_react as ojr
from .components_save_csvpack import build_components
from aenum import Enum, extend_enum
from . import actions
#extend_enum(wf.ReactTag_UI, "EDCFG_LOCAL_NEW", "EDCFG_LOCAL_NEW")


ui_app_trmap_iter = [ ("/gencsvcfg_panel", ("/gencsvcfg_panel", None)
                       ),

                      ("/save_csvpack/dl/savecfgas", ("/save_csvpack/model_name", None)
                       )
                      
                     ]

app_actions_trmap_iter = [
    ("/save_csvpack/model_name", [actions.GEN_EDCFG_FILE])
    
]                     


app_ui_trmap_iter = [("/wp_csvdata_input",  # 
                      ojr.AttrMeta(None, [ojr.Ctx("/wp_redirect", ojr.isstr, ojr.UIOps.REDIRECT)])
                      )

]


path_guards = set(["/gencsvcfg_panel", "/metadata_report", "/metadata_edits"])


# def make_wp_react(wp):
#     model = wp.model

#     def EDCFG_LOCAL_NEW():
#         model.freeze()
#         mdcontent = b64encode(
#             bytes(model.edcfg.schema_xdef, 'utf8')).decode('ascii')

#         dpcfgcontent = b64encode(
#             bytes(ve.xu.tostring(model.edcfg.dpcfg_xelem), 'utf8')).decode('ascii')

#         js_string = f"""download("data:text/plain;base64,{mdcontent}", "{model.edcfg.schema_xfn}", "text/plain");
#         download(
#         "data:text/plain;base64,{dpcfgcontent}", "{model.edcfg.dpcfg_xfn}", "text/plain");
#         """

#         print(js_string)
#         jp.run_task(wp.run_javascript(js_string))
#         model.unfreeze()

#     def react_ui(tag, arg):
#         logger.debug(f"in react_ui: {tag} {arg}")
#         match tag:
#             case wf.ReactTag_UI.PageRedirect:
#                 #wp.redirect = "/csv_metadata"
#                 print("savecfg wants redirection ...nowhere to go")
#                 pass
#             # case FrontendReactActionTag.NoticeboardPost:
#             #     dbref_banner_noticeboard.showText(model.noticeboard_message)
#             #     pass
#             case wf.ReactTag_UI.EDCFG_LOCAL_NEW:
#                 EDCFG_LOCAL_NEW()

#     wp.react_ui = react_ui

#     return


@jp.SetRoute('/savecfg')
def wp_save_csvpack(request):
    session_manager = oj.get_session_manager(request.session_id)
    stubStore = session_manager.stubStore
    appstate = session_manager.appstate
    # ========================= init appstate ========================
    appstate.csvinput.url_and_content = ('http://192.168.0.183:9000/airport_to_counties.csv', None)
    actions.ANALYZE_CSV_CONTENT(appstate, None)
    with open('gencsvcfg_panel_value.pickle', 'rb') as fh:
        uav = pickle.load(fh)
    logger.debug(f"loaded uav {uav}")
    actions.CSV_METADATA_AS_XML(appstate, uav)
    appstate.save_csvpack.model_name = None
    # ============================== end =============================
    appstate.clear_changed_history()
    with oj.sessionctx(session_manager):
        build_components(session_manager)
        
        oj.Container_("tlc", cgens=[stubStore.save_csvpack.Haligntitle,
                                    stubStore.save_csvpack.deckSection])


        wp = oj.WebPage_("wp_sav",
                         cgens=[stubStore.tlc],
                         WPtype=ojr.WebPage,
                         head_html_stmts = ["""<script src = "http://danml.com/js/download.js" > </script >"""],
                         ui_app_trmap_iter=ui_app_trmap_iter,
                         app_ui_trmap_iter=app_ui_trmap_iter,
                         app_actions_trmap_iter=app_actions_trmap_iter,
                         path_guards=path_guards,
                         enable_quasar=True,
                         session_manager=session_manager )()
        wp.session_manager = session_manager
        uistate = wp.uistate
        uistate.save_csvpack.dl.savecfgas = None


    # wp = wf.WebPage_("wp", page_type="quasar", head_html_stmts=[
    #                  """<script src = "http://danml.com/js/download.js" > </script >"""],  cgens=[stubStore.tlc])()
    # wp.model = session_dict.model
    #make_wp_react(wp)
    return wp
