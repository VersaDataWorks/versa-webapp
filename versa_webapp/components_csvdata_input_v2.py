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

from py_tailwind_utils import noop, fz, bg, pink
from addict import Dict
import ofjustpy as oj
import ofjustpy_react as ojr
import versa_engine as ve


def no_action(dbref, msg):
    pass



    

@ojr.CfgLoopRunner
async def on_submit(dbref, msg, to_ms):
    form_data = msg.page.session_manager.request.state.form_data["/csvinput/form"]
    print (f"check form data : /csvinput/form", form_data)

    csvurl = form_data['/csvinput/csvurl']
    if csvurl:
        return [("/csvinput/panel", (csvurl, None))]
    else:
        print ("not valid input")
        
    # spath = None
    # csvurl = None
    # csvcontent = None
    # csvurl = msg.value
    # print("input url = ", _ss.csvinput.csvurl.target.value)
    # csvcontent = None
    # if csvurl != 'http://address.of.csv.file/':
    #     print("in form submit:url ", csvurl, csvcontent)
    #     return "/csvinput/panel", (csvurl, csvcontent)
    # selected_file_info = msg.form_data[1]
    # if selected_file_info.value.strip() != '':
    #     csvurl  = "file://" + selected_file_info.files[0].name
    #     csvcontent = base64.b64decode(
    #         selected_file_info.files[0].file_content)

    # print("in form submit:file ", csvurl, csvcontent)
    # return "/csvinput/panel", (csvurl, csvcontent)

def on_input_change(dbref, msg, to_ms):
    pass
with oj.uictx("csvinput") as csvinputctx:
    _ictx = csvinputctx
    _1 = oj.AC.TextInput(key="csvurl",
                         placeholder="Enter a url hosting raw csv data",
                         value = "http://address.of.csv.file/",
                         type="text",
                         on_change = on_input_change
                    )
    _2 = oj.AC.TextInput(key="csvfile",
                         placeholder="Choose an ondisk file",
                         value=None,
                         type="file")
    _3 = oj.Halign(oj.PC.Span(text="or", twsty_tags=[noop/fz.xl2]))
    _inp = oj.PC.StackV(childs=[_1, _3, _2]
                 )
    _btn = oj.AC.Button(key="submit",
                  text="Analyze CSV file",
                  on_click=on_submit)

    _form = oj.AD.Form(key="form",
               childs = [_inp, _btn

                         ],
               on_submit = on_submit
               )
    input_panel= oj.PC.Subsection("CSV data input form", oj.PC.StackV(childs = [_form]

                                                         )
                     )
    
    
