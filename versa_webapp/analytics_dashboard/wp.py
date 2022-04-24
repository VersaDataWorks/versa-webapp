"""
attrmeta is a graball module for all metadata about chartjs attributes
"""
import logging
import os
if logging:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

#import webapp_framework as wf
import justpy as jp
#import components
from addict import Dict
import ofjustpy as oj
import ofjustpy_react as ojr
import components
from sync_and_transition_matrix import cfg_CM
from sync_and_transition_matrix_helper import update_cfg_ui, update_cfg_model


from dpath.util import set as dset
from dpathutils import dget
cfg_ui = Dict(track_changes=True)


# build cfg_ui based on cfg_appstate
# i.e. all paths of cfg_appstate have corresponding
# vaule in cfg_ui
update_cfg_ui(cfg_CM, cfg_ui)
cfg_CM.clear_changed_history()
# make any other changes to ui as necessary


def make_wp_react(wp):
    stubStore = wp.session_manager.stubStore

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
            update_cfg_model(cfg_ui, cfg_CM, inactive_kpaths)
            cfg_ui.clear_changed_history()
            inactive_kpaths = update_cfg_ui(cfg_CM, cfg_ui)
            for kpath in cfg_CM.get_changed_history():
                logger.debug(f"iter {i}: make ui change for  {kpath}")
                #kpath = kpath.lstrip()
                attrmeta = dget(cfg_CM, kpath)
                # dbref = dget(refBoard, kpath)._go.target
                # TODO: we need to be consistent with dget or []
                dbref = dget(stubStore, kpath).target
                logger.debug(
                    f"debug_hide_unhide:  {cfg_CM.keys()} {cfg_CM.dbsession.keys()}")

                logger.debug(
                    f"debug_hide_unhide:  {kpath} {dbref.classes} {attrmeta}")

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
            cfg_CM.clear_changed_history()
            logger.debug("post update debugging")
            cfg_CM.clear_changed_history()
            cfg_ui.clear_changed_history()
            # ===================== end update_ui ====================

    def update_ui_component(dbref, msg):
        """
        this is where the cfg_ui is updated with latest ui value.
        then cascading
        """

        old_val = dget(cfg_ui, dbref.stub.spath)
        # logger.debug(
        #     f"react: updated cjs_cfg: key={dbref.key} from {old_val} to new value {msg.value}")
        ojr.dupdate(cfg_ui, dbref.stub.spath, msg.value)
        cfg_CM.clear_changed_history()  # we should loop until done
        update_ui()
    wp.update_ui_component = update_ui_component


# do a test drive
# stubStore.dbsession.id.target.value = "newuserfedname"
# dset(cfg_ui, "/dbsession/id", "newuserfedname")
# make_wp_react(None)
# update_cfg_model(cfg_ui, cfg_model)
# update_cfg_ui(cfg_model, cfg_ui)
# cfg_model.clear_changed_history()
# cfg_ui.clear_changed_history()


@ jp.SetRoute('/analytics_dashboard')
def wp_analytics_dashboard(request):

    session_manager = oj.get_session_manager(request.session_id)
    stubStore = session_manager.stubStore
    with oj.sessionctx(session_manager):
        oj.Container_(cgens=[stubStore.dbsession.section])
        wp = oj.WebPage_("wp_index", page_type='quasar', head_html_stmts=[
        ], cgens=[stubStore.tlc])()
    make_wp_react(wp)
    #wp.appstate = session_ctx.appstate
    wp.session_manager = session_manager
    return wp


#wp = wp_analytics_dashboard(None)
#stubStore.session['/dbsession/id'].target.on_input({'value': 'newval'})
