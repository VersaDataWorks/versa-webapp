import webapp_framework as wf
import traceback
import sys
# uis for session control

#import actions

with wf.uictx("load_datamodels") as load_datamodels_ctx:
    _ictx = load_datamodels_ctx

    with wf.uictx("local") as localctx:
        _ictx = localctx

        @wf.MRVWLR
        def on_button_click(dbref, msg):
            print("load data model called")
            rts = wf.TaskStack()
            rts.addTask(wf.ReactTag_ModelUpdate.LOAD_DATAMODEL, {})
            return msg.page, rts

        wf.Button_("fakedataload", "fakeload",
                   "load data model", on_button_click)
    wf.Subsection_("panel", "Load data model from local store",
                   _ictx.fakedataload)


with wf.uictx("active_datamodels") as active_datamodels_ctx:
    _ictx = active_datamodels_ctx
    wf.Span_("fakelist", "putlist of models here")
    wf.Subsection_("panel", "Active datamodels", _ictx.fakelist)
