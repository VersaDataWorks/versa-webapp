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

ui_app_kmap = []
path_guards = set()
path_guards.add("/metadata_report")
path_guards.add("/metadata_edits")

appstate = Dict()
appstate.metadata_report.header_candidates = [["cp0_nc1", "cp0_nc2"],
                                              ["cp1_nc1", "cp1_nc2"],
                                              ["cp2_nc1", "cp2_nc2"]
                                              ]
appstate.metadata_report.cols_type = ["int", "float", "string"
    ]

appstate.metadata_report.delimiter_name = "comma"

appstate.metadata_report.num_header_lines = 5

appstate.metadata_report.num_data_lines = 10
appstate.metadata_report.csv_samples = [ [1, "abc", 3, 5]


    ]

from .components_csv_schema_metadata_v3 import build_components

app = oj.load_app()
def create_endpoint(appstate, label):
    stats_box, samples_box, coltypes_box, colnames_box, gencsvcfg_box = build_components(appstate.metadata_report)
    tlc = oj.PD.Container(childs = [stats_box,
                              samples_box,
                              coltypes_box,
                              colnames_box,
                              gencsvcfg_box

                              ]


        )



    
    endpoint = ojr.create_endpoint(f"wp_csv_schema_metadata_{label}",
                                   [tlc

                                       ],
                                   ui_app_trmap_iter = ui_app_kmap,
                                   action_module = actions,
                                   rendering_type="CSR",
                                   csr_bundle_dir="hyperui",
                                   path_guards = path_guards,
                                   head_html =  """<script src="https://cdn.tailwindcss.com"></script> """,
                                   reactctx = [ojr.Ctx("/wp_redirect", ojr.isstr, ojr.UIOps.REDIRECT)]
                                   )



    oj.add_jproute(f"/csv_metadata_{label}", endpoint)    
