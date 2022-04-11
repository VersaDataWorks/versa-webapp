"""
attrmeta is a graball module for all metadata about chartjs attributes
"""
import logging
if logging:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)


import webapp_framework as wf

from dpath.util import set as dset
from .dpathutils import dget, dnew


def attrupdate(cfg, kpath, active):

    val_attr = dget(cfg, kpath)
    val_attr = val_attr._replace(active=bool(active))
    wf.dupdate(cfg, kpath, val_attr)


def update_cfgmodel_kpath(kpath, val, cfg_model, cfg_ui):
    ctx = (kpath, val)
    logger.info(
        f"=============update_cfgattrmeta_kpath: {kpath} {ctx}================")

    kpaths_in_context = [_ for _ in attrmeta_in_context(ctx, cfgattrmeta)]
    for dpath in kpaths_in_context:
        attrupdate(cfgattrmeta, dpath, bool(val))
        # as an example we have made x1/grid/display inactive with value None
        # when we next activate it .. its value would be False.
        # but in UI it would be true
        # either make it true in cjs_cfg/cfgattrmeta or make it false in ui
        # going with latter option as it is simpler
        logger.debug(f"update:cfgattrmeta: {dpath} active={bool(val)} ")
        logger.info(
            f"==========end update_cfgattrmeta_kpath: {kpath} {ctx}================")


def update_cfg_model(cfg_ui, cfg_model, new_inactive_kpaths=[]):
   for kpath in cfg_ui.get_changed_history():
        new_val = dget(cfg, kpath)
        logger.debug(f"{kpath} has changed in cfg_ui to  new_value={new_val}")
        update_cfgmodel_kpath(kpath, new_val, cfg_model, cfg_ui)

    for kpath in new_inactive_kpaths:
        # if the path is delete then set active to False
        attrmeta.attrupdate(cfgmodel, kpath, False)
        # update all dependent attributes
        update_cfgmodel_kpath(kpath, False, cfgAttrMeta, chartcfg)

    logger.debug("done update_cfgattrmeta...")
        

def update_cfg_ui(cfg_model, cfg_ui):
    logger.debug("=========== start update_cfg_ui  ===============")
    # remove everything thats changed and put it
    # back in only the active ones: this enables deletion
    inactive_kpaths = set()
    for kpath in cfg_model.get_changed_history():
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

    for kpath in filter(lambda kpath: dget(cfg_model, kpath).active,
                        cfg_model.get_changed_history()):

        evalue = attrmeta.get_defaultVal(dget(cfgattrmeta, kpath))
        dnew(cfg_ui, kpath, evalue)
        if kpath in inactive_kpaths:
            inactive_kpaths.remove(kpath)
        logger.debug(f"path {kpath} updated with {evalue} in cjscfg")

    # cfgattrmeta.clear_changed_history()
    if inactive_kpaths:
        logger.debug(f"paths that became inactive: {inactive_kpaths}")
    logger.debug("=========== done update_chartCfg  ===============")
    return inactive_kpaths

    