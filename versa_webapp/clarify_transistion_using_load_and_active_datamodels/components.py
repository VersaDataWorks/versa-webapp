#import webapp_framework as wf
import traceback
import sys
import ofjustpy as oj
import ofjustpy_react as ojr
# uis for session control

#import actions


def build_components(session_manager):
    uictx = session_manager.uictx
    with uictx("load_datamodels") as load_datamodels_ctx:

        _ictx = load_datamodels_ctx

        with uictx("local") as localctx:
            _ictx = localctx

            @ojr.LoopRunner
            def on_button_click(dbref, msg):
                print("load data model called")
                rts = ojr.TaskStack()
                rts.addTask(ojr.ReactTag_AppstateUpdate.LOAD_DATAMODEL, {})
                return msg.page, rts

            oj.Button_("fakedataload", value="fakeload",
                       text="load data model").event_handle(oj.click, on_button_click)
        oj.Subsection_("panel", "Load data model from local store",
                       _ictx.fakedataload)

    with uictx("active_datamodels") as active_datamodels_ctx:
        _ictx = active_datamodels_ctx
        oj.Span_("fakelist", text="put list of models here")
        oj.Subsection_("panel", "Active datamodels", _ictx.fakelist)
