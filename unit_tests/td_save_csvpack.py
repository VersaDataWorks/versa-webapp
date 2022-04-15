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

import justpy as jp
from addict import Dict
from tracker import _hcs as stubStore, refBoard, session_dict

from versa_webapp.model_backend_actions import CSV_URL_INPUT
from versa_webapp.wp_save_csvpack import wp_save_csvpack


# build all the components
wp = wp_csvdata_input(None)

# print(stubStore.inputctx.form)
msg = Dict()
msg.page = wp
wp.model = Dict(track_changes=True)
# stubStore.inputctx.csvurl.target.setValue(
#     'https://query.data.world/s/rgz7coxjf2iutihqhbc2xybqkuhcxf')

stubStore.inputctx.csvurl.target.setValue(
    'http://192.168.0.183:9000/airport_to_counties.csv')
stubStore.inputctx.form.target.on_submit(msg)

# to prepare for csv metadata page

# populate the model with metadata report from url input
# CSV_URL_INPUT(session_dict.model, Dict({'url': 'http://192.168.0.183:9000/airport_to_counties.csv'})
#              )
#logger.debug(f"model = {session_dict.model}")

# call CSV_METADATA_AS_XML the round about way
wp = wp_csv_schema_metadata(None)

# call the form submit button
idx = 2
stubStore.csm.colnames[f"is_pk_{idx}cbox"].target.checked = True
idx = 0
stubStore.csm.colnames[f"is_hn_{idx}cbox"].target.checked = True
msg = Dict()
msg.page = wp
# start the chain reaction
stubStore.csm.gencsvcfg.btn.target.dbref_btn.on_click(msg)

wp = wp_save_csvpack(None)

stubStore.save_csvpack.local.newcfg.target.setValue('airport.cfg')
stubStore.save_csvpack.local.submit.target.on_click(msg)

# app = jp.app
# jp.justpy(wp_save_csvpack, start_server=False)
# #wp = wp_save_csvpack(None)
