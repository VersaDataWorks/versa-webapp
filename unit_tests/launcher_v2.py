import logging
import os
if os:
    try:
        os.remove("launcher.log")
    except:
        pass

import sys
if sys:
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename="launcher.log",
                        level=logging.DEBUG, format=FORMAT)

    logger = logging.getLogger(__name__)
from versa_webapp.wp_csvdata_input_v2 import wp_csvdata_input
from versa_webapp.wp_csv_schema_metadata_v2 import wp_csv_schema_metadata
import justpy as jp
from addict import Dict


app = jp.build_app()
app.add_jproute("/csv_metadata", wp_csv_schema_metadata, "csv_schema_metadata")

request = Dict()
request.session_id = "abc123"

#wp = wp_csv_schema_metadata(request)
# _sm = wp.session_manager
# _ss = _sm.stubStore

# # from starlette.testclient import TestClient
# # client = TestClient(app)
# # response = client.get('/csv_metadata')

# ======================= test wp_csvdata_input ======================
app.add_jproute("/", wp_csvdata_input, "csvdata_input")
#wp = wp_csvdata_input(request)
# stubStore = wp.session_manager.stubStore
# msg = Dict()
# msg.page = wp
# stubStore.freeze()

# print(stubStore.tlctx.body.csvinput.submit)
# stubStore.tlctx.body.csvinput.csvurl.target.value = "http://192.168.0.102:8000/static/Rdatasets/csv/Ecdat/efcedfffa54bd"
# stubStore.tlctx.body.csvinput.submit.target.on_click(msg)

# ================================ end ===============================

# import jsbeautifier
# import json
# opts = jsbeautifier.default_options()
# res = jsbeautifier.beautify(json.dumps(wp.session_manager.appstate), opts)
    
# print(res)
# ================================ end ===============================




# ================= launch csv metadata page ================
#app = jp.app
#jp.justpy(wp_csv_schema_metadata, start_server=False)
# ================================ end ===============================
# wp_csm = wp_csv_schema_metadata(request)

# # # call the form submit button
# idx = 2
# stubStore.csm.colnames[f"is_pk_{idx}cbox"].target.checked = True
# idx = 0
# stubStore.csm.colnames[f"is_hn_{idx}cbox"].target.checked = True
# msg = Dict()
# msg.page = wp_csm
# # # start the chain reaction
# stubStore.csm.gencsvcfg.btnbtn.target.on_click(msg)


#app = jp.app
#jp.justpy(wp_save_csvpack, start_server=False)


# wp = wp_save_csvpack(request)

# stubStore = wp.session_manager.stubStore
# msg = Dict()
# msg.page = wp
# stubStore.save_csvpack.dl.ti_newcfg.target.value = "testmodel"
# stubStore.save_csvpack.dl.submit.target.on_click(msg)

