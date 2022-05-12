"""
attrmeta is a graball module for all metadata about chartjs attributes
"""
import logging
if logging:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)


import ofjustpy_react as ojr
from dpath.exceptions import PathNotFound
from dpath.util import set as dset
from .dpathutils import dget, dnew, dpop, walker as dictWalker


def get_defaultVal(attrmeta):  # TODO: ask SO if there is a better way to
    '''get default value of attrmeta
    '''
    cam = attrmeta
    match str(cam.vtype):
        case "<class 'int'>" | "<class 'bool'>" | "<class 'str'>" | "<class 'float'>":

            return cam.default

        # case "<aenum 'FalseDict'>":
        #     return cam.default

        # case "<aenum 'Position'>" | "<aenum 'PlotType'>" | "<aenum 'TextAlign'>" | "<aenum 'PointStyle'>" | "<aenum 'CubicInterpolationMode'>" | "<aenum 'BorderJoinStyle'>" | "<aenum 'BorderCapStyle'>" | "<aenum 'LineJoinStyle'>":
        #     return cam.default.value

        # case "<aenum 'Color'>":
        #     return hexify(cam.default)  # TODO: will deal with later

        case _:
            print("unkown vtype :", cam)
            raise ValueError


def attrmeta_in_context(ctx, cfgattrmeta):
    kpath = ctx[0]  # e.g./dbsession/id
    newval = ctx[1]  # mynewdbsession
    newvaltype = type(newval)

    # now look for all cfg element which have ctx has (kpath, newval)
    for _ in dictWalker(cfgattrmeta):
        # TODO: this check should become more sophisticated
        # moving to a sophisticated check
        if ctx in _[1].context:
            yield _[0]
        elif (kpath, newvaltype) in _[1].context:
            yield _[0]
    pass


def attrupdate(cfg, kpath, active):

    val_attr = dget(cfg, kpath)
    val_attr = val_attr._replace(active=bool(active))
    ojr.dupdate(cfg, kpath, val_attr)

# TODO: revisit if wp main loop does not fit the bill
# def update_cfgmodel_kpath(kpath, val, cfg_model, cfg_ui):
#     ctx = (kpath, val)
#     logger.info(
#         f"=============update_cfgattrmeta_kpath: {kpath} {ctx}================")

#     kpaths_in_context = [_ for _ in attrmeta_in_context(ctx, cfg_appstate)]
#     for dpath in kpaths_in_context:
#         attrupdate(cfg_model, dpath, bool(val))
#         # as an example we have made x1/grid/display inactive with value None
#         # when we next activate it .. its value would be False.
#         # but in UI it would be true
#         # either make it true in cjs_cfg/cfgattrmeta or make it false in ui
#         # going with latter option as it is simpler
#         logger.debug(f"update:cfgattrmeta: {dpath} active={bool(val)} ")
#         logger.info(
#             f"==========end update_cfgattrmeta_kpath: {kpath} {ctx}================")

# code already in make-react of wp; TODO: move it here
# def update_cfg_appstate(cfg_ui, cfg_appstate, new_inactive_kpaths=[]):
#     for kpath in cfg_ui.get_changed_history():
#         new_val = dget(cfg_ui, kpath)
#         logger.debug(f"{kpath} has changed in cfg_ui to  new_value={new_val}")
#         update_cfgmodel_kpath(kpath, new_val, cfg_appstate, cfg_ui)

#     for kpath in new_inactive_kpaths:
#         # if the path is delete then set active to False
#         attrupdate(cfg_model, kpath, False)
#         # update all dependent attributes
#         update_cfgmodel_kpath(kpath, False, cfg_model, cfg_ui)

#     logger.debug("done update_cfgattrmeta...")

# TODO: open up later. currently cfg_ui is not being updated from cfg_CM


def update_cfg_ui(cfg_CM, cfg_ui):
    logger.debug("=========== start update_cfg_ui  ===============")
    # remove everything thats changed and put it
    # back in only the active ones: this enables deletion
    inactive_kpaths = set()
    for kpath in cfg_CM.get_changed_history():
        logger.debug(f"path {kpath} changed in cfgattrmeta")
        try:
            # logger.debug("what bakwas")
            # opts = jsbeautifier.default_options()
            # logger.debug(jsbeautifier.beautify(json.dumps(cjscfg), opts))
            dpop(cfg_ui, kpath)
            inactive_kpaths.add(kpath)
        except PathNotFound as e:
            logger.info(f"skipping: {kpath} not found in cjscfg {e}")
            pass  # skip if path is not in chartcfg

    for kpath in filter(lambda kpath: dget(cfg_CM, kpath).is_active,
                        cfg_CM.get_changed_history()):

        #evalue = get_defaultVal(dget(cfg_CM, kpath))
        evalue = dget(cfg_CM, kpath).default
        dnew(cfg_ui, kpath, evalue)
        if kpath in inactive_kpaths:
            inactive_kpaths.remove(kpath)
        logger.debug(f"path {kpath} updated with {evalue} in cjscfg")

    # cfgattrmeta.clear_changed_history()
    if inactive_kpaths:
        logger.debug(f"paths that became inactive: {inactive_kpaths}")
    logger.debug("=========== done update_chartCfg  ===============")
    return inactive_kpaths


def components_in_appstate_changectx(kpath, val,  cfg_CM):
    """
    which components have registered for the change.
    returns components path in cfgCM
    """

    for path, am in dictWalker(cfg_CM):
        #am: attrmeta
        # TODO: this check should become more sophisticated
        # moving to a sophisticated check
        for ctx in am.appstate_context:
            if kpath == ctx.path:
                # candidate_ctx[1] is either a string value or a lambda
                if ctx.condition(val):
                    yield path, ctx.uiop


def update_cfg_CM_kpath_for_appstate_changes(kpath, val, cfg_CM, appstate):
    """
    update cfgCM in response to  changes in appstate at kpath
    """
    ctx = (kpath, val)

    logger.debug(f"evaluation ctx: {ctx}")
    paths_in_context = [
        _ for _ in components_in_appstate_changectx(kpath, val,  cfg_CM)]
    for path, uiop in paths_in_context:
        # TODO: we should change something for sure.
        # the bojective is to update the ui with newly added data model
        # dget(stubStore, path).target.update(val)
        # print(f"Que {path} {kpath} {val} {cm}")
        # match ctx.uiop:
        #     case UIOps.ENABLE:
        #         #dset(cfg_CM, path, "enabled")
        #         #am.is_enabled = True
        #     case UIOps.DISABLE:
        #         #dset(cfg_ui, path, "disabled")
        logger.info(
            f"changing ui for {path} with uiop {uiop}")

        yield path, uiop
        pass


def update_cfg_CM_for_appstate_changes(appstate,  cfg_CM, new_inactive_kpaths=[]):
    """
    a change on frontend/browser in recorded in cfg_ui and in appstate.
    update cfg_CM based on dependency
    """
    for kpath in appstate.get_changed_history():
        new_val = dget(appstate, kpath)
        logger.debug(
            f"{kpath} has changed in appstate to  new_value={new_val}")
        yield from update_cfg_CM_kpath_for_appstate_changes(
            kpath, new_val, cfg_CM, appstate)

    for kpath in new_inactive_kpaths:
        print("inactive paths are not implemented yet")
        pass

    logger.debug("done update_cfgattrmeta...")
