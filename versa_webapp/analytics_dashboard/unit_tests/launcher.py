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
import justpy as jp
from addict import Dict

app = jp.app
#jp.justpy(wp_analytics_dashboard, host="192.168.0.183", start_server=False)
wp = wp_analytics_dashboard(None)
stubStore = wp.session_manager.stubStore
sessionid_dbref = stubStore.dbsession.id.target
msg = Dict()
msg.value = "H"
msg.page = wp
wp.update_ui_component(dbref, msg)


startbtn = stubStore.dbsession.start.target
# startbtn.on_click(msg)

#startbtn = stubStore.dbsession.save.target
# startbtn.on_click(msg)
#startbtn.run_event_function('change', msg)
func = getattr(startbtn, 'on_input')
func(msg)
