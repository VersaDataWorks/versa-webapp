import webapp_framework as wf

# uis for session control
with wf.uictx("session") as sessionctx:
    _ictx = sessionctx

    def no_input(dbref, msg):
        pass
    wf.TextInput_("/dbsession/id", "enter session id", "mydbsession", on_input)

    def on_startbtn_click(dbref, msg):
        page = msg.page
        model = page.model
        rts = wf.TaskStack()
        rts.addTask(wf.ReactTag_Backend.START_DBSESSION, model)
        return page, rts

    def no_action(dbref, msg):
        pass
    wf.ToggleBtn_("/dbsession/start", "start", on_startbtn_click)
    wf.ToggleBtn_("/dbsession/stop", "stop", "stop", on_action)
    wf.Button_("/dbsession/save", "save", "save", on_action)
    wf.Button_("/dbsession/resume", "resume", "resume", on_action)
    wf.Halign_(wf.StackG_("panel", cgens=[
               _ictx.start, _ictx.stop, _ictx.save, _ictx.resume]))

    wf.Subsection("section", "Analytics Engine Control Panel", _ictx.panelWrap)
