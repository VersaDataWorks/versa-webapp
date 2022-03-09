"""
creates a webpage to input CSV file/url 
and analyze the content
"""

import logging
import os
import sys
if sys:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
import justpy as jp
import webapp_framework as wf
from tracker import _hcs as stubStore, session_dict, refBoard
from aenum import extend_enum, auto
import webapp_framework as wf
from . import components_csvdata_input
extend_enum(wf.ReactTag_ModelUpdate, 'CSV_URL_INPUT', 'CSV_URL_INPUT')
extend_enum(wf.ReactTag_ModelUpdate, 'CSV_GEN_METADATAREPORT',
            'CSV_GEN_METADATAREPORT')


@jp.SetRoute('/csvdata_input')
def wp_csvdata_input(request):
    # stubStore.freeze()
    wf.Container_(cgens=[stubStore.inputctx.inputPanel])

    wp = wf.WebPage_("wp", page_type="quasar", cgens=[stubStore.tlc])()

    return wp
