import webapp_framework as wf
import traceback
import sys
# uis for session control

import actions
with wf.uictx("dbsession") as sessionctx:
    _ictx = sessionctx

    def on_input(dbref, msg):
        page = msg.page
        print("got id text input", msg.value)
        page.update_ui_component(dbref, msg)
        pass
    wf.TextInput_("id",
                  "enter session id", "mydbsession", on_input)

    def on_startbtn_click(dbref, msg):
        # traceback.print_stack(file=sys.stdout)
        print("i was called")
        page = msg.page
        model = page.model
        rts = wf.TaskStack()
        rts.addTask(wf.ReactTag_Backend.START_DBSESSION, model)
        rts.addTask(wf.ReactTag_Backend.CONNECT_DBSESSION, model)
        return page, rts
        pass

    def no_action(dbref, msg):
        pass
    wf.ToggleBtn_("start", "start",
                  on_startbtn_click, value=False, pcp=['hidden'])
    wf.ToggleBtn_("stop", "stop",  no_action, pcp=['hidden'])
    wf.Button_("save", "save", "save", no_action, pcp=['hidden'])
    wf.Button_("resume", "resume",
               "resume", no_action, pcp=['hidden'])
    wf.StackG_("btnpanel", cgens=[
               _ictx.start, _ictx.stop, _ictx.save, _ictx.resume]
               )
    wf.Halign_(wf.StackV_("panel", cgens=[
               _ictx.id,  _ictx.btnpanel]))
    wf.Subsection_("section", "Analytics Engine Control Panel",
                   _ictx.panelHalign)
