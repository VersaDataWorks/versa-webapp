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
import justpy as jp
import webapp_framework as wf

from tracker import _hcs as stubStore, session_dict, refBoard


def make_wp_react(wp):

    def react_ui(tag, arg):
        logger.debug(f"in react_ui: {tag} {arg}")
        match tag:
            case wf.ReactTag_UI.PageRedirect:
                wp.redirect = "/csv_metadata"
                pass
    wp.react_ui = react_ui

    return


@jp.SetRoute('/csv_metadata')
def wp_csv_schema_metadata(request):
    logger.debug("building webpage")
    wf.Container_(cgens=[wf.Span_("TBD", "TBD")])
    wp = wf.WebPage_("wp", page_type="quasar", cgens=[stubStore.tlc])()
    wp.model = session_dict.model
    make_wp_react(wp)
    return wp
