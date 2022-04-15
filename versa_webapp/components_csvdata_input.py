"""
ui components for wp_csvdata_input
"""

import base64
import logging
import os
import sys


if sys:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
import justpy as jp
import webapp_framework as wf
import webapp_framework_extn as wfx

from tracker import _hcs as stubStore, session_dict, refBoard
from tailwind_tags import noop, fz
from addict import Dict


def no_action(dbref, msg):
    pass


with wf.uictx("inputctx") as _ctx:
    @wf.MRVWLR
    def on_submit(dbref, msg):
        #print("csvfile target", _ctx.csvfile.target)
        print("msg == ", msg)
        csvurl = _ctx.csvurl.target.getValue()
        print("csvurl = ", csvurl)
        rts = wf.TaskStack()
        if csvurl.strip() != 'http://address.of.csv.file/':
            rts.addTask(wf.ReactTag_ModelUpdate.CSV_URL_INPUT,
                        Dict({'url': csvurl}))
            rts.addTask(wf.ReactTag_Backend.CHECK_OP_STATUS, None)
            return msg.page, rts

        selected_file_info = msg.form_data[1]
        if selected_file_info.value.strip() != '':
            csvfile = selected_file_info.files[0].name
            csvcontent = base64.b64decode(
                selected_file_info.files[0].file_content)

            # _ctx.form.target.files[0].name
            # _ctx.form.target.files[0].file_content

            rts.addTask(wf.ReactTag_ModelUpdate.GEN_CSV_METADATAREPORT, Dict(
                {'file_name': csvfile, 'file_content': csvcontent}))
            rts.addTask(wf.ReactTag_Backend.CHECK_OP_STATUS, None)
            print("pass batton to MVULR")
            return msg.page, rts

        pass
    wf.TextInput_("csvurl", "Enter a url hosting raw csv data",
                  "http://address.of.csv.file/")
    wf.FileInput_("csvfile", "Choose an ondisk file")
    wf.Wrapdiv_(wf.Span_("orsep", "or", pcp=[noop/fz.xl2]))
    wf.StackV_("input", cgens=[_ctx.csvurl, _ctx.orsepWrap, _ctx.csvfile])
    wf.Button_("submit", "Submit", "Analyze CSV file", no_action)
    #wf.StackH_("contentFrame", cgens=[_ctx.input, _ctx.submit])
    wf.Form_("form", _ctx.input, _ctx.submit, on_submit)
    wf.Subsection_("inputPanel", "CSV data input form", _ctx.form)

    # BRB
