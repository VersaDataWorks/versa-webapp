"""
attrmeta is a graball module for all metadata about chartjs attributes
"""
import logging
import os
if logging:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

# import webapp_framework as wf
import justpy as jp
# import components
from addict import Dict
import ofjustpy as oj
import ofjustpy_react as ojr
from .components import build_components
from .sync_and_transition_matrix_v2 import cfg_CM, UIOps
from .sync_and_transition_matrix_helper import update_cfg_ui, update_cfg_CM_for_appstate_changes


from dpath.util import set as dset, search as dsearch
from .dpathutils import dget
from .cfg_actions import cfg_actions, exec_actions
cfg_ui = Dict(track_changes=True)


# build cfg_ui based on cfg_CM
# i.e. all paths of cfg_appstate have corresponding
# vaule in cfg_ui
# TODO:
update_cfg_ui(cfg_CM, cfg_ui)
cfg_CM.clear_changed_history()
cfg_ui.clear_changed_history()
logger.debug("---------init cfg_ui----------")
logger.debug(cfg_ui)
# make any other changes to ui as necessary


def make_wp_react(wp):
    stubStore = wp.session_manager.stubStore
    appstate = wp.session_manager.appstate
    appstate.clear_changed_history()
    def cfg_update_loop():
        """
        user has changed the state of input component.
        this has led to change in cfg_ui.
        in this function we update ui on update to cfg_ui
        1. update cfg_mode based on new context in cfg_ui
        2. update ui 'hidden' attribute based newly active cfgattrmeta
        """

        # update appstate from cfg_ui
        for _ in cfg_ui.get_changed_history():
            try:
                res = dget(appstate, _)
                # as long as path exists update appstate
                if res == None or res:
                    logger.debug(f"react-cfguichange: update appstate for path {_}")
                    ojr.dupdate(appstate, _,  dget(cfg_ui, _))
            except KeyError as e:
                print(f"path {_} not in appstate")
            except Exception as e:
                print("here")

        cfg_ui.clear_changed_history()
        # perform actions for updated appstate
        
        appstate_changeset = [_ for _ in appstate.get_changed_history()]
        logger.debug(f"post cfgui update  appstate changes {appstate_changeset}")
        for kpath in appstate_changeset:
            kval = dget(appstate, kpath)
            if(kpath, kval) in cfg_actions:
                logger.debug(f"TODO: Exec actions for {kpath}, {kval}")
                exec_actions(cfg_actions[(kpath,kval)], appstate)
                print (appstate.op_status)
            pass

        # actions and cfg_ui have updated appstate  ==> try to update cfg_CM and the ui
        for kpath, uiop in update_cfg_CM_for_appstate_changes(appstate, cfg_CM):
            match uiop:
                case UIOps.ENABLE:
                    target_dbref = dget(stubStore, kpath).target
                    target_dbref.remove_class("disabled")
                    pass
                case UIOps.DISABLE:
                    pass
                case UIOps.UPDATE_NOTICEBOARD:
                    print("notice board not yet implemented")

        appstate.clear_changed_history()
        pass

    def cfg_ui_setval(spath, value):
        """
        set value of cfg_ui at spath value
        """

        old_val = dget(cfg_ui, spath)
        logger.debug(
             f"react: update cfg_ui: key={spath} from {old_val} to new value {value}")
        ojr.dupdate(cfg_ui, spath, value)

    wp.cfg_ui_setval = cfg_ui_setval
    wp.cfg_update_loop = cfg_update_loop


# do a test drive
# stubStore.dbsession.id.target.value = "newuserfedname"
# dset(cfg_ui, "/dbsession/id", "newuserfedname")
# make_wp_react(None)
# update_cfg_model(cfg_ui, cfg_model)
# update_cfg_ui(cfg_model, cfg_ui)
# cfg_model.clear_changed_history()
# cfg_ui.clear_changed_history()

def init_appstate(appstate):
    appstate.dbsession.id = None
    appstate.dbsession.start = None
    appstate.dbsession.stop = None
    appstate.clear_changed_history()


@jp.SetRoute('/analytics_dashboard')
def wp_analytics_dashboard(request):
    session_manager = oj.get_session_manager(request.session_id)
    stubStore = session_manager.stubStore
    with oj.sessionctx(session_manager):
        build_components(session_manager)
        init_appstate(session_manager.appstate)
        oj.Container_("tlc", cgens=[stubStore.dbsession.section])
        wp = oj.WebPage_("wp_index", page_type='quasar', head_html_stmts=[
        ], cgens=[stubStore.tlc])()
    wp.session_manager = session_manager
    make_wp_react(wp)
    # wp.appstate = session_ctx.appstate

    return wp

# wp = wp_analytics_dashboard(None)
# stubStore.session['/dbsession/id'].target.on_input({'value': 'newval'})
