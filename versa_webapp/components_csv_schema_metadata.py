"""
ui components for wp_csv_schema_metadata.
"""

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


with wf.uictx("csm") as _ctx:
    wf.Section("CSV schema")
    # BRB
