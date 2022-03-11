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
from .model_backend_actions import GEN_CSV_METADATAREPORT, CSV_URL_INPUT


extend_enum(wf.ReactTag_ModelUpdate, 'CSV_URL_INPUT', CSV_URL_INPUT)
extend_enum(wf.ReactTag_ModelUpdate, 'GEN_CSV_METADATAREPORT',
            GEN_CSV_METADATAREPORT)
if sys:
    # import components_csvdata_input only after extend_enum
    from . import components_csvdata_input


def page_ready(self, msg):
    stubStore.inputctx.csvurl.target.setValue(
        'http://192.168.0.183:9000/airport_to_counties.csv')


def make_wp_react(wp):

    def react_ui(tag, arg):
        logger.debug(f"in react_ui: {tag} {arg}")
        match tag:
            case wf.ReactTag_UI.PageRedirect:
                wp.redirect = "/csv_metadata"
                pass
    wp.react_ui = react_ui

    return


@jp.SetRoute('/csvdata_input')
def wp_csvdata_input(request):
    # stubStore.freeze()
    wf.Container_(cgens=[stubStore.inputctx.inputPanel])

    wp = wf.WebPage_("wp", page_type="quasar", cgens=[stubStore.tlc])()
    wp.model = session_dict.model
    make_wp_react(wp)
    wp.on('page_ready', page_ready)
    return wp
