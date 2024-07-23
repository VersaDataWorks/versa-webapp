"""
invoke the event handler for submit on csv_input_url
"""


import ofjustpy as oj
from py_tailwind_utils import *

from versa_webapp.wp_csvdata_input_v2 import endpoint
request = Dict()
request.session_id = "abc"
wp = endpoint(request)

ss = wp.session_manager.stubStore

print(ss.csvinput.csvurl.target.event_handlers["on_change"])

csvurl_input_dbref = ss.csvinput.csvurl.target

def target_of(item, stubStore=ss):
    """
    item is a stub or staticCore
    supports item.id which is spath
    for the item
    """
    return dget(stubStore, item.id).target


msg = Dict()
msg.value = "http://192.168.0.114:9000/statesCensus.csv"
msg.page = wp


# invoke csvurl_input event handler: the form will intercept and keep a version of its
# value
csvurl_input_dbref.event_handlers["on_change"](csvurl_input_dbref, msg, target_of)

# invoke form submit  event handler : 
# this will GEN_CSV_METADATAREPORT 
inp_form_dbref = ss.csvinput.form.target
inp_form_submit_eh = inp_form_dbref.get_event_handler("submit")
import asyncio
asyncio.run(inp_form_submit_eh(inp_form_dbref, msg, target_of))

# automatic redirect to /csv_metadata_{data_label} will not happen
print(wp.session_manager.appstate)
data_label="alpha"

import versa_webapp
csv_metadata_endpoint = versa_webapp.wp_csv_schema_metadata_v3.create_endpoint(wp.session_manager.appstate, data_label)

wp_csvmetadata = csv_metadata_endpoint(request)
# now populate the inputs on wp_csvmetadata
# import jsbeautifier
# opts = jsbeautifier.default_options()
# res = jsbeautifier.beautify(json.dumps(ss, default=str), opts)
#print(res)

# grab hold of the final form component
# {
#     "csv_data_input": "<ofjustpy_engine.TF_impl.Stub_WebPage object at 0x8900f829810>",
#     "csvinput": {
#         "form": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88ffb3cd1d0>",
#         "csvurl": "<ofjustpy_engine.TF_impl.Stub_HCActive object at 0x88ffb3cc790>",
#         "csvfile": "<ofjustpy_engine.TF_impl.Stub_HCActive object at 0x88ffb453950>",
#         "submit": "<ofjustpy_engine.TF_impl.Stub_HCActive object at 0x88ffb3cd250>"
#     },
#     "wp_csv_schema_metadata_alpha": "<ofjustpy_engine.TF_impl.Stub_WebPage object at 0x88f4ab4f310>",
#     "csv_metadata_schema": {
#         "gencsvcfg_form": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f4ab4f510>",
#         "coltypes": {
#             "selector_0": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f4ab4fa10>",
#             "selector_1": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f4ab4f690>",
#             "selector_2": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f4ab4fa90>"
#         },
#         "colnames": {
#             "selector_0": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f4ab4f8d0>",
#             "use_oname_0": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f652ad890>",
#             "inp_oname_0": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f4ab4fd50>",
#             "is_pk_0": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f4ab4fe10>",
#             "is_hn_0": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f4ab4fe50>",
#             "selector_1": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f4ab4f7d0>",
#             "use_oname_1": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f4ab4fcd0>",
#             "inp_oname_1": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f4ab4fdd0>",
#             "is_pk_1": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f4ab4ff90>",
#             "is_hn_1": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f4ab4ffd0>",
#             "selector_2": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f4ab50150>",
#             "use_oname_2": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f576a6950>",
#             "inp_oname_2": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f4ab50310>",
#             "is_pk_2": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f4ab50190>",
#             "is_hn_2": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f4ab50110>"
#         },
#         "gencsvcfg": {
#             "model_name_inp": "<ofjustpy_engine.TF_impl.Stub_HCActive object at 0x88f576c6e50>"
#         },
#         "submit": "<ofjustpy_engine.TF_impl.Stub_DivActive object at 0x88f576b0c90>"
#     }
# }


gencsvcfg_form_dbref = ss.csv_metadata_schema.gencsvcfg_form.target
submit_eh = gencsvcfg_form_dbref.get_event_handler("submit")
msg = Dict()
msg.value = None # form itself has no data associated with it
msg.page = wp_csvmetadata

asyncio.run(submit_eh(gencsvcfg_form_dbref, msg, target_of))

arg = Dict()
arg.model_name = "dummy_model"
versa_webapp.actions.GEN_EDCFG_FILE(wp.session_manager.appstate, arg, None)

