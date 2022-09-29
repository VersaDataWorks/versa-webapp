#import webapp_framework as wf
import logging
import os
if logging:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

import ofjustpy as oj
import ofjustpy_react as ojr
import traceback
import sys
# uis for session control

from . import actions


def build_components(session_manager):
    appstate = session_manager.appstate
    with session_manager.uictx("dbsession") as sessionctx:
        _ictx = sessionctx

        @ojr.CfgLoopRunner
        def on_input(dbref, msg):
            #page = msg.page
            #print("got id text input", msg.value)
            #page.update_ui_component(dbref, msg)
            pass
        oj.InputChangeOnly_("id", text="enter session id",
                            placeholder="mydbsession").event_handle(oj.change, on_input)

        @ojr.CfgLoopRunner
        def on_startbtn_click(dbref, msg):
            # traceback.print_stack(file=sys.stdout)
            print("i was called")
            page = msg.page
            appstate = page.appstate
            rts = ojr.TaskStack()
            rts.addTask(ojr.ReactTag_BackendAction.START_DBSESSION, None)
            rts.addTask(ojr.ReactTag_BackendAction.CONNECT_DBSESSION, None)
            return page, rts

        @ojr.CfgLoopRunner
        def on_stopbtn_click(dbref, msg):
            pass
        oj.ToggleBtn_("start", text="start",
                      value=False, pcp=['disabled']).event_handle(oj.input, on_startbtn_click)

        oj.ToggleBtn_("stop", text="stop",   pcp=['disabled']).event_handle(oj.input, on_stopbtn_click)

        def on_shutdown_click(dbref, msg):
            actions.shutdown_proxyService(appstate)
            pass
        
            
            
        oj.Button_("shutdown", text="shutdown", value="shutdown", pcp=['disabled']).event_handle(oj.click, on_shutdown_click)
        oj.Button_("save", text="save", value="save", pcp=['disabled'])
        oj.Button_("resume", text="resume",
                   value="resume",  pcp=['disabled'])
        oj.StackG_("btnpanel", cgens=[
                   _ictx.start, _ictx.stop, _ictx.save, _ictx.resume]
                   )
        oj.StackV_("panel", cgens=[_ictx.id,  _ictx.btnpanel])
        oj.Subsection_("section", "Analytics Engine Control Panel",
                       oj.Halign_(_ictx.panel))
