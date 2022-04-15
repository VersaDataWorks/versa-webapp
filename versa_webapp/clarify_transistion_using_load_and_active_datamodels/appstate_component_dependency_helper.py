import logging
if logging:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)


import webapp_framework as wf
from dpath.exceptions import PathNotFound
from dpath.util import set as dset

from dpathutils import dget, dnew, dpop, walker as dictWalker


def components_in_appstate_changectx(new_ctx, cfg_CM):
    """
    which components have registered for the change
    returns components path in cfgCM
    """
    kpath = new_ctx[0]  # e.g./dbsession/id
    for path, cm in dictWalker(cfg_CM):
        # TODO: this check should become more sophisticated
        # moving to a sophisticated check
        for candidate_ctx in cm.appstate_context:
            if kpath == candidate_ctx[0]:
                yield path, candidate_ctx


def cmeta_update_active(cfgCM, kpath, active):
    """
    """
    cmeta_curr = dget(cfgCM, kpath)
    cmeta_new = cmeta_curr._replace(active=bool(active))
    wf.dupdate(cfgCM, kpath, cmeta_new)


def update_cfg_CM_kpath_for_appstate_changes(kpath, val, cfg_CM, wp):
    """
    update cfgCM in response to  changes in appstate at kpath
    """
    ctx = (kpath, val)
    appstate = wp.appstate
    logger.info(
        f"=============update_cfgCM_kpath_for_appstate_changes: {ctx}================")

    paths_in_context = [
        _ for _ in components_in_appstate_changectx(ctx, cfg_CM)]
    for path, cm in paths_in_context:
        # TODO: we should change something for sure.
        # the bojective is to update the ui with newly added data model
        # dget(stubStore, path).target.update(val)
        print(f"Que {path} {kpath} {val} {cm}")
        # the actual corresponding
        # update_appstate()
        for op in cm[1]:
            op(wp,  val)
        # update_UI()

        pass


def update_cfg_CM_for_appstate_changes(wp, cfg_CM, new_inactive_kpaths=[]):
    """
    a change on frontend/browser in recorded in cfg_ui and in appstate.
    update cfg_CM based on dependency
    """
    print("herethere")
    for kpath in wp.appstate.get_changed_history():
        print("what man")
        new_val = dget(wp.appstate, kpath)
        logger.debug(
            f"{kpath} has changed in appstate to  new_value={new_val}")
        update_cfg_CM_kpath_for_appstate_changes(
            kpath, new_val, cfg_CM, wp)

    for kpath in new_inactive_kpaths:
        print("inactive paths are not implemented yet")
        pass

    logger.debug("done update_cfgattrmeta...")


def update_appstate_for_cfgui_changes(cfg_ui, appstate, new_inactive_kpaths=[]):
    """
    cfg_ui records the value of the state on the ui/browser.
    When a new change happens-- a downstream changes are invoke.
    first cfgCM is updated. and
    """
    for kpath in cfg_ui.get_changed_history():
        new_val = dget(cfg_ui, kpath)
        logger.debug(
            f"{kpath} has changed in appstate to  new_value={new_val}")
        # TODO:
        # update_appstate_kpath_for_cfgui_changes(
        #     kpath, new_val, appstate, cfg_ui)j

    for kpath in new_inactive_kpaths:
        print("inactive paths are not implemented yet")
        pass

    logger.debug("done update_cfgattrmeta...")
