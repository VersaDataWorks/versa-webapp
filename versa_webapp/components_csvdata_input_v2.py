"""
ui components for wp_csvdata_input
"""
import requests
import base64
import logging
import os
import sys

if sys:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
import justpy as jp
from tailwind_tags import noop, fz, bg, pink, flx
from addict import Dict
import ofjustpy as oj
import ofjustpy_react as ojr
import versa_engine as ve


def no_action(dbref, msg):
    pass


def build_components(session_manager):
    stubStore = session_manager.stubStore

    with session_manager.uictx("csvinput") as csvinputctx:
        _ictx = csvinputctx
        
        @ojr.CfgLoopRunner
        def on_submit(dbref, msg):
            #print("csvfile target", _ctx.csvfile.target)
            print("on submit called")
            spath = None
            csvurl = None
            csvcontent = None
            
            # print("msg == ", msg)
            csvurl = _ictx.csvurl.target.value
            csvcontent = None
            if csvurl != 'http://address.of.csv.file/':
                print("in form submit:url ", csvurl, csvcontent)
                return "/csvinput/panel", (csvurl, csvcontent)
            # # print("csvurl = ", csvurl)
            # # rts = wf.TaskStack()
            # # if csvurl.strip() != 'http://address.of.csv.file/':
            # #     rts.addTask(wf.ReactTag_ModelUpdate.CSV_URL_INPUT,
            # #                 Dict({'url': csvurl}))
            # #     rts.addTask(wf.ReactTag_Backend.CHECK_OP_STATUS, None)
            selected_file_info = msg.form_data[1]
            if selected_file_info.value.strip() != '':
                csvurl  = "file://" + selected_file_info.files[0].name
                csvcontent = base64.b64decode(
                    selected_file_info.files[0].file_content)

            # rts.addTask(wf.ReactTag_ModelUpdate.GEN_CSV_METADATAREPORT, Dict(
            #     {'file_name': csvfile, 'file_content': csvcontent}))
            # rts.addTask(wf.ReactTag_Backend.CHECK_OP_STATUS, None)
            # print("pass batton to MVULR")
            print("in form submit:file ", csvurl, csvcontent)
            return "/csvinput/panel", (csvurl, csvcontent)

        oj.InputChangeOnly_("csvurl", text="Enter a url hosting raw csv data",
                       value = "http://address.of.csv.file/", type="text")
        oj.Input_("csvfile", text="Choose an ondisk file", type="file")
        oj.Halign_(oj.Span_("orsep", text="or", pcp=[noop/fz.xl2]))
        oj.StackV_("input", cgens=[_ictx.csvurl, _ictx.Halignorsep, _ictx.csvfile])
        oj.Button_("submit", text="Analyze CSV file").event_handle(oj.click, on_submit)
        #wf.StackH_("contentFrame", cgens=[_ctx.input, _ctx.submit])
        oj.Form_("form", _ictx.input, _ictx.submit)
    oj.Align_(oj.Subsection_("input_panel_body", "CSV data input form", _ictx.form), key="panel", pcp=[flx.one])

    # BRB
