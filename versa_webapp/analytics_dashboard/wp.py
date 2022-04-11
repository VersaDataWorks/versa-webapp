"""
attrmeta is a graball module for all metadata about chartjs attributes
"""
import logging
if logging:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

import webapp_framework as wf
import justpy as jp
import components
from addict import Dict

from sync_and_transition_matrix import cfg_model
from sync_and_transition_matrix_helper import update_cfg_ui, update_cfg_model
if 'appdir' in os.environ:
    from tracker import _hcs as stubStore, session_dict, refBoard

from dpath.util import set as dset
from .dpathutils import dget
cfg_ui = Dict()


# build cfg_ui based on cfg_modelv
# i.e. all paths of cfg_model have corresponding
# vaule in cfg_ui
update_cfg_ui(cfg_model, cfg_ui)
cfg_model.clear_changed_history()
# make any other changes to ui as necessary


def make_wp_react(wp):

    def update_ui():
        """
        user has changed the state of input component. 
        this has led to change in cfg_ui. 
        in this function we update ui on update to cfg_ui
        1. update cfg_mode based on new context in cfg_ui
        2. update ui 'hidden' attribute based newly active cfgattrmeta
        """
        logger.debug("in update_ui")
        inactive_kpaths = set()
        for i in range(2):
            update_cfg_model(cfg_ui, cfg_model, inactive_kpaths)
            cfg_ui.clear_changed_history()
            inactive_kpaths = update_cfg_ui(cfg_model, cfg_ui)
            for kpath in cfg_ui.get_changed_history():
                logger.debug(f"iter {i}: make ui change for  {kpath}")
                kpath = kpath.lstrip()
                attrmeta = dget(cfg_model, kpath)
                dbref = dget(refBoard, kpath)._go.target

                if attrmeta.active and 'hidden' in dbref.classes:
                    logger.debug(f"unhide {kpath}")
                    dbref.remove_class("hidden")
                    # sync frontend ui and cjscfg value here
                    logger.debug(f"""ui for {kpath} has been made visible: setting value to {dget(cfg_ui, kpath)}
                    """)
                    dbref.value = dget(cfg_ui, kpath)

                    # print(kpath, " ", dbref.classes)
                elif not attrmeta.active and not 'hidden' in dbref.classes:
                    logger.debug(f"hide {kpath}")
                    dbref.set_class("hidden")
            # if new attrmeta elements have active;add them to cjs_cfg
            # we should loop over updates until fix point is reached

            cfg_model.clear_changed_history()

            logger.debug("post update debugging")

            cfg_model.clear_changed_history()
            cfg_ui.clear_changed_history()
            # ===================== end update_ui ====================

    update_ui()  # for test drive


# do a test drive
stubStore.dbsession.id.target.value = "newuserfedname"
dset(cfg_ui, "/dbsession/id", "newuserfedname")
make_wp_react(None)
#update_cfg_model(cfg_ui, cfg_model)
#update_cfg_ui(cfg_model, cfg_ui)
# cfg_model.clear_changed_history()
# cfg_ui.clear_changed_history()
