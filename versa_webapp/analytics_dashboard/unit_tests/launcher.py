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

from versa_webapp.analytics_dashboard.wp import wp_analytics_dashboard
from versa_webapp.analytics_dashboard import actions
import justpy as jp
from addict import Dict

#app = jp.app
#jp.justpy(wp_analytics_dashboard, host="192.168.0.183", start_server=False)

request = Dict()
request.session_id = "mysessionid"
wp = wp_analytics_dashboard(request)



stubStore = wp.session_manager.stubStore
sessionid_dbref = stubStore.dbsession.id.target

msg = Dict()
msg.value = "mydbsession"
msg.page = wp
sessionid_dbref.on_change(msg)
#dbstart is enabled; turn it on
start_dbref = stubStore.dbsession.start.target
msg.value = True
start_dbref.on_input(msg)

#load a datamodel
arg = Dict()
arg.name_csvpack = "/home/kabira/Databank/versa-dl/countyhiv.cfg.csvpack"
actions.BUILD_ORM(wp.session_manager.appstate, arg)

                  
#stop btn is enabled; turn the database off
stop_dbref = stubStore.dbsession.stop.target
msg.value = True
stop_dbref.on_input(msg)

#clean up before leaving
actions.shutdown_proxyService(wp.session_manager.appstate)

                  
#startbtn = stubStore.dbsession.start.target
# startbtn.on_click(msg)

#startbtn = stubStore.dbsession.save.target
# startbtn.on_click(msg)
#startbtn.run_event_function('change', msg)
#func = getattr(startbtn, 'on_input')
# func(msg)
