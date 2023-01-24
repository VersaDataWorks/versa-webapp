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
import ofjustpy as oj
import ofjustpy_react as ojr
from .wp_template import page_builder
from .components_csv_schema_metadata_v2 import build_components
from . import actions
from tailwind_tags import * 

ui_app_kmap = []
path_guards = set()
path_guards.add("/metadata_report")
path_guards.add("/metadata_edits")

def wp_csv_schema_metadata(request):
    def panel_builder(session_manager):
        with session_manager.uictx("body") as bodyCtx:
            _ictx = bodyCtx
            

            # setup for development and testing
            stubStore = session_manager.stubStore
            appstate = session_manager.appstate
            appstate.gencsvcfg_panel = None
            appstate.clear_changed_history()
            # ========================== init appst ==========================
            #appstate.csvinput.url_and_content = None
            appstate.csvinput.url_and_content = ("http://192.168.0.102:8000/static/Rdatasets/csv/Ecdat/efcedfffa54bd", None)
            actions.ANALYZE_CSV_CONTENT(appstate, None)
            # ========================= end init appstate =========================
            build_components(session_manager)

            oj.Container_("panel",
                      cgens=[
                          stubStore.tlctx.body.dockbar,
                          stubStore.tlctx.body.csm.stats.section,
                          stubStore.tlctx.body.csm.headers,
                          stubStore.tlctx.body.csm.samples.section,
                          stubStore.tlctx.body.csm.coltypes.section,
                          stubStore.tlctx.body.csm.colnames.section,
                          stubStore.tlctx.body.csm.gencsvcfg.section
                         ])

    wp =  page_builder("wp_csv_schema_metadata",
                       "Title here",
                       panel_builder,
                       WPtype=ojr.WebPage,
                       ui_app_trmap_iter = ui_app_kmap,
                       action_module = actions,
                       path_guards = path_guards,
                       reactctx = [ojr.Ctx("/wp_redirect", ojr.isstr, ojr.UIOps.REDIRECT)],
                       )(request)

    return wp
