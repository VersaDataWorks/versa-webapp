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
from .components_csv_schema_metadata import build_components


def make_wp_react(wp):

    def react_ui(tag, arg):
        logger.debug(f"in react_ui: {tag} {arg}")
        match tag:
            case wf.ReactTag_UI.PageRedirect:
                wp.redirect = "/savecfg"
                pass
    wp.react_ui = react_ui

    return


@jp.SetRoute('/csv_metadata')
def wp_csv_schema_metadata(request):
    logger.debug("building webpage")
    build_components(session_dict.model)
    wf.Container_(cgens=[stubStore.csm.titleBannerHalign,
                         stubStore.csm.stats.section, stubStore.csm.headers, stubStore.csm.samples.section,
                         stubStore.csm.coltypes.section, stubStore.csm.colnames.section, stubStore.csm.gencsvcfg.section

                         ])
    wp = wf.WebPage_("wp", page_type="quasar", cgens=[stubStore.tlc])()
    wp.model = session_dict.model  # TODO: should happen automatically, i think
    make_wp_react(wp)
    return wp
