"""
attrmeta is a graball module for all metadata about chartjs attributes
"""
from aenum import Enum, extend_enum
import logging
import os
if logging:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

import webapp_framework as wf
import justpy as jp
import components
from addict import Dict
if 'appdir' in os.environ:
    from tracker import _hcs as stubStore, session_dict, refBoard

from dpath.util import set as dset
from dpathutils import dget
from appstate_component_dependency import cfg_CM
import actions
from appstate_component_dependency_helper import update_cfg_CM_for_appstate_changes
cfg_ui = Dict(track_changes=True)
cfg_CM.clear_changed_history()


extend_enum(wf.ReactTag_UI, "UpdateActiveModels", "UpdateActiveModels")


def make_wp_react(wp):
    # def update_ui():
    #     """
    #     user has changed the state of input component.
    #     this change is reflected in cfg_ui.
    #     in this function we update ui on update to appstate
    #     1. update cfg_CM based on new context in cfg_ui
    #     2. update ui 'hidden' attribute based newly active cfgattrmeta
    #     """

    #     pass

    def update_appstate_and_ui():
        update_cfg_CM_for_appstate_changes(wp, cfg_CM)
        print("appstate = ", wp.appstate)
    wp.update_appstate_and_ui = update_appstate_and_ui
    # def update_appstate(dbref, msg):
    #     """
    #     this is where the cfg_ui is updated with latest ui value.
    #     then cascading
    #     """

    #     old_val = dget(cfg_ui, dbref.stub.spath)
    #     # logger.debug(
    #     #     f"react: updated cjs_cfg: key={dbref.key} from {old_val} to new value {msg.value}")
    #     wf.dupdate(cfg_ui, dbref.stub.spath, msg.value)
    #     cfg_CM.clear_changed_history()  # we should loop until done
    #     update_ui()

    # def update_cfg_UI(dbref, msg):
    #     match ReactTag_ModelUpdate:
    #         case Local:
    #         pass

    def react_ui(tag, arg):
        match tag:
            case wf.ReactTag_UI.UpdateActiveModels:
                stubStore.active_datamodels.fakelist.target.text = ",".join(
                    wp.appstate.active_datamodels)

    wp.react_ui = react_ui

    pass


def init_appstate(appstate):
    appstate.active_datamodels = []
    appstate.loaded_datamodel = None


def launcher(request):
    wp = jp.WebPage()
    wp.appstate = session_dict.appstate
    init_appstate(wp.appstate)
    wf.Container_(cgens=[stubStore.load_datamodels.panel,
                  stubStore.active_datamodels.panel])
    stubStore.tlc(wp)
    make_wp_react(wp)

    return wp


app = jp.app
jp.justpy(launcher, start_server=False)
# wp = launcher(None)
# msg = Dict()
# msg.page = wp
# stubStore.load_datamodels.local.fakedataload.target.on_click(msg)
