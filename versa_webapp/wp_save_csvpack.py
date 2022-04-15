import logging
import os
import sys
from base64 import b64encode
import versa_engine as ve

if sys:
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename="launcher.log",
                        level=logging.DEBUG, format=FORMAT)

    logger = logging.getLogger(__name__)
from base64 import b64encode
import justpy as jp
import webapp_framework as wf
from tracker import _hcs as stubStore, refBoard, session_dict
from . import components_save_csvpack
from aenum import Enum, extend_enum

extend_enum(wf.ReactTag_UI, "EDCFG_LOCAL_NEW", "EDCFG_LOCAL_NEW")


def make_wp_react(wp):
    model = wp.model

    def EDCFG_LOCAL_NEW():
        model.freeze()
        mdcontent = b64encode(
            bytes(model.edcfg.schema_xdef, 'utf8')).decode('ascii')

        dpcfgcontent = b64encode(
            bytes(ve.xu.tostring(model.edcfg.dpcfg_xelem), 'utf8')).decode('ascii')

        js_string = f"""download("data:text/plain;base64,{mdcontent}", "{model.edcfg.schema_xfn}", "text/plain");
        download(
        "data:text/plain;base64,{dpcfgcontent}", "{model.edcfg.dpcfg_xfn}", "text/plain");
        """

        print(js_string)
        jp.run_task(wp.run_javascript(js_string))
        model.unfreeze()

    def react_ui(tag, arg):
        logger.debug(f"in react_ui: {tag} {arg}")
        match tag:
            case wf.ReactTag_UI.PageRedirect:
                #wp.redirect = "/csv_metadata"
                print("savecfg wants redirection ...nowhere to go")
                pass
            # case FrontendReactActionTag.NoticeboardPost:
            #     dbref_banner_noticeboard.showText(model.noticeboard_message)
            #     pass
            case wf.ReactTag_UI.EDCFG_LOCAL_NEW:
                EDCFG_LOCAL_NEW()

    wp.react_ui = react_ui

    return


@jp.SetRoute('/savecfg')
def wp_save_csvpack(request):
    wf.Container_(cgens=[stubStore.save_csvpack.titleBanner,
                  stubStore.save_csvpack.deckSection])

    wp = wf.WebPage_("wp", page_type="quasar", head_html_stmts=[
                     """<script src = "http://danml.com/js/download.js" > </script >"""],  cgens=[stubStore.tlc])()
    wp.model = session_dict.model
    make_wp_react(wp)
    return wp
