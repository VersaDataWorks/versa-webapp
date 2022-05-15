import logging

import os
if os:
    try:
        os.remove("launcher.log")
    except:
        pass

import sys
if sys:
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename="launcher.log",
                        level=logging.DEBUG, format=FORMAT)
import justpy as jp
from addict import Dict

from versa_webapp.analytics_dashboard.wp_rmo_export import wp_rmo_export
import justpy as jp

# ======================== start versa engine and build rmo ========================
import versa_engine as ve
from versa_engine.common import xmlutils as xu
from versa_engine.dataapis import relational as vreapi
from versa_engine.dataapis import schema as vschapi
from versa_engine.dataapis import export as vexapi


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
s1 = vreapi.limit(dbsession, vschapi.proj(dbsession, xorm, ['variable']), 20)

# ====================== build an edcfg on orm =====================
csv_fn, file_fn = vexapi.export_rmo(dbsession, s1, "testmodel", export_dir=session_run_dir)
# =============================== done ===============================
#print(vexapi.scan(dbsession, s1))
#print(vexapi.build_tabulate(dbsession, s1, "fancy_grid"))
#print(s1)
# ================================ end ===============================
#request = Dict()
#request.session_id = "mysessionid"
#wp  = wp_rmo_export(request)

#app = jp.app
#jp.justpy(wp_rmo_export, start_server=False)
# session_manager = wp.session_manager
# #grab hold for the button
# stubStore = session_manager.stubStore
# appstate = session_manager.appstate
# appstate.dbsession.dbsession = dbsession
# appstate.analytics.active_rmo = s1
# appstate.clear_changed_history()
# exportrmo_btn=stubStore.exportrmo.btn.target
# msg = Dict()
# msg.value = "fancygrid"
# msg.page = wp
# exportrmo_btn.on_click(msg)
