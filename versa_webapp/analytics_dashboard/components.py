#import webapp_framework as wf
import ofjustpy as oj
import ofjustpy_react as ojr
import traceback
import sys
# uis for session control

import actions


def build_components(session_manager):
    with session_manager.uictx("dbsession") as sessionctx:
        _ictx = sessionctx

        def on_input(dbref, msg):
            page = msg.page
            print("got id text input", msg.value)
            page.update_ui_component(dbref, msg)
            pass
        oj.InputChangeOnly_("id", text="enter session id",
                            placeholder="mydbsession").event_handle(oj.iinput, on_input)

        @ojr.LoopRunner
        def on_startbtn_click(dbref, msg):
            # traceback.print_stack(file=sys.stdout)
            print("i was called")
            page = msg.page
            appstate = page.appstate
            rts = ojr.TaskStack()
            rts.addTask(ojr.ReactTag_BackendAction.START_DBSESSION, None)
            rts.addTask(ojr.ReactTag_BackendAction.CONNECT_DBSESSION, None)
            return page, rts

        oj.ToggleBtn_("start", text="start",
                      value=False, pcp=['hidden'])
        oj.ToggleBtn_("stop", text="stop",  pcp=['hidden'])
        oj.Button_("save", text="save", value="save", pcp=['hidden'])
        oj.Button_("resume", text="resume",
                   value="resume",  pcp=['hidden'])
        oj.StackG_("btnpanel", cgens=[
                   _ictx.start, _ictx.stop, _ictx.save, _ictx.resume]
                   )
        oj.Halign_(oj.StackV_("panel", cgens=[
                   _ictx.id,  _ictx.btnpanel]))
        oj.Subsection_("section", "Analytics Engine Control Panel",
                       _ictx.panelHalign)
