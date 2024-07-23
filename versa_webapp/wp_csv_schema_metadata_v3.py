"""
creates a webpage to analyze CSV data
and display its schema and metadata
"""

import logging
import os
import sys
if sys:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
import ofjustpy as oj
import ofjustpy_react as ojr
from . import actions
from py_tailwind_utils import *

ui_app_kmap = [("/csv_schema_metadata/gencsvcfg_panel", "/csv_schema_metadata/gencsvcfg_panel", None)]
path_guards = set()
path_guards.add("/metadata_report")
path_guards.add("/metadata_edits")



from .components_csv_schema_metadata_v3 import build_components
def post_init(wp, session_manager=None):
    print("post_init called")
    assert "session_manager" is not None
    request = wp.session_manager.request
    request.state.form_data["/csv_metadata_schema/gencsvcfg_form"] = {}
    pass

app = oj.load_app()
def create_endpoint(appstate, label):
    # stats_box, samples_box, coltypes_box, colnames_box, gencsvcfg_box = build_components(appstate.metadata_report)

    with oj.uictx("csv_metadata_schema"):
        form_box = build_components(appstate.metadata_report)
    endpoint = ojr.create_endpoint(f"wp_csv_schema_metadata_{label}",
                                   [form_box

                                       ],
                                   ui_app_trmap_iter = ui_app_kmap,
                                   action_module = actions,
                                   rendering_type="CSR",
                                   csr_bundle_dir="hyperui",
                                   path_guards = path_guards,
                                   post_init = post_init,
                                   head_html =  """<script src="https://cdn.tailwindcss.com"></script> """,
                                   reactctx = [ojr.Ctx("/wp_redirect", ojr.isstr, ojr.UIOps.REDIRECT)]
                                   )



    oj.add_jproute(f"/csv_metadata_{label}", endpoint)
    # return endpoint for unit_test
    # see versa-webapp/unit_tests/td_create_csv_schema_metadata.py
    return endpoint
