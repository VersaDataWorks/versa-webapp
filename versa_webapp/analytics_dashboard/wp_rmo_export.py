from aenum import extend_enum
import logging
import os
if os:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

import ofjustpy as oj
import ofjustpy_react as ojr
from . import actions

# ========================= setup for testing ========================
import versa_engine as ve
from versa_engine.common import xmlutils as xu
datacfg_basedir = "/home/kabira/Databank/versa-dl"

edcfg_dir=f"{datacfg_basedir}/edcfgs"
content_dir=f"{datacfg_basedir}/content"
metadata_dir=f"{datacfg_basedir}/metadata"


edcfg_prefix=f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE edcfg [
<!ENTITY var_metadata_dir "{metadata_dir}">
<!ENTITY var_content_dir "{content_dir}">
]>


"""

edcfg_fn = f"{edcfg_dir}/x.csvpack"
#print(edcfg_prefix + open(edcfg_fn, "r").read())
edcfg_root = xu.read_string(edcfg_prefix + open(edcfg_fn, "r").read())
#print(edcfg_root)

session_run_dir = "/tmp/tmp5gbgkb_2"
session_name = "mydbsession"
[dbadapter, dbsession] = ve.connect_dbsession(session_name, session_run_dir)
#ve.build_orms(edcfg_root, session_run_dir)
xorm  = ve.import_model('x', session_run_dir)
s1 = ve.reapi.limit(dbsession, ve.schapi.proj(dbsession, xorm, ['variable']), 5)
# ================================ end ===============================

# ===================== react transition mapping =====================
ui_app_trmap = [ ("/exportrmo/tabulate/format", ("/exportrmo/tabulate/format", None))]
app_ui_trmap = [
    ("/exportrmo/tabulate/format", ojr.AttrMeta(None, [])),
    ("/dataviewport/tbltextview",
                 ojr.AttrMeta(None, [ojr.Ctx("/exportrmo/tabulate/text", ojr.isstr, ojr.UIOps.UPDATE_TEXT)])
                 )
                ]
app_actions_trmap_iter = [
    ("/exportrmo/tabulate/format", actions.EXPORT_RMO_TABULATE)
    
]
# ================================ end ===============================

def build_components(session_manager):
    stubStore = session_manager.stubStore
    with session_manager.uictx("exportrmo") as _exportrmotctx:
        _ictx = _exportrmotctx
        @ojr.CfgLoopRunner
        def on_exportbtn_click(dbref, msg):
            #stubStore.dataviewport.tbltextview.target.placeholder = "hello"
            return "/exportrmo/tabulate/format", "fancy_grid"

        oj.Button_("btn", text="export as tabulate-fancygrids", value="export").event_handle(oj.click, on_exportbtn_click)
    
    with session_manager.uictx("dataviewport") as _dataviewportctx:
        _ictx = _dataviewportctx
        oj.Textarea_("tbltextview", text="")
def wp_rmo_export(request):
    session_id = "asession"
    session_manager = oj.get_session_manager(session_id)
    stubStore = session_manager.stubStore
    appstate = session_manager.appstate
    # ========================= init appstate ========================
    appstate.exportrmo.tabulate.format = "plain"
    appstate.exportrmo.dataviewport.tbltextview = "nothing here"
    appstate.analytics.active_rmo = s1
    appstate.dbsession.dbsession = dbsession
    
    with oj.sessionctx(session_manager) as tlctx:
        build_components(session_manager)
        oj.Container_(
            "tlc", cgens=[stubStore.exportrmo.btn, stubStore.dataviewport.tbltextview])
        
        wp = oj.WebPage_("sty_wp", cgens=[stubStore.tlc], WPtype=ojr.WebPage, ui_app_trmap_iter=ui_app_trmap, app_ui_trmap_iter=app_ui_trmap, app_actions_trmap_iter=app_actions_trmap_iter, session_manager=session_manager )()
    print (session_manager.stubStore)
    return wp



