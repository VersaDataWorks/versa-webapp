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
from versa_webapp.wp_csvdata_input import wp_csvdata_input
from versa_webapp.wp_csv_schema_metadata import wp_csv_schema_metadata
from versa_webapp.wp_save_csvpack import wp_save_csvpack
import justpy as jp
from addict import Dict


# =================== launch csvdata_input webpage ===================

# app = jp.app
# jp.justpy(wp_csvdata_input, start_server=False)
# ================================ end ===============================

# ================== td csvdata input button submit ==================
request = Dict()
request.session_id = "abc123"
# wp = wp_csvdata_input(request)
# stubStore = wp.session_manager.stubStore
# msg = Dict()
# msg.page = wp

# stubStore.csvinput.csvurl.target.value = 'http://192.168.0.183:9000/airport_to_counties.csv'
# stubStore.csvinput.form.target.on_submit(msg)
# print(wp.session_manager.appstate)
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
wp = wp_save_csvpack(request)

stubStore = wp.session_manager.stubStore
msg = Dict()
msg.page = wp
stubStore.save_csvpack.dl.ti_newcfg.target.value = "testmodel"
stubStore.save_csvpack.dl.submit.target.on_click(msg)
