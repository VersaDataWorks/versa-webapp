import logging
import os
if logging:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

import os
import traceback

import ofjustpy_react as ojr
#import webapp_framework as wf

if os:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

import versa_engine as ve

# ojr.UpdateAppStateAndUI

def DUMMY_ACTION(appstate, arg=None):
    logger.info(f"calling start dbsession =  {appstate.dbsession.id}")
    appstate.dummy_action.res = 1
    appstate.noticeboard_message = "successfully launched new database session"
    appstate.op_status = ojr.OpStatus.SUCCESS
    return appstate.op_status

def DUMMY_ACTION_FOLLOWUP(appstate, arg=None):
    logger.info(f"calling start dbsession =  {appstate.dbsession.id}")
    appstate.noticeboard_message = "successfully launched new database session"
    appstate.op_status = ojr.OpStatus.SUCCESS
    return appstate.op_status


ojr.make_react(DUMMY_ACTION, ojr.ReactTag_BackendAction)

def START_DBSESSION(appstate, arg=None):
    logger.info(f"calling start dbsession =  {appstate.dbsession.id}")
    dbsession_id = appstate.dbsession.id
    run_dir = "~/DrivingRange/" + dbsession_id
    run_dir = "/tmp/tmp5gbgkb_2/"
    appstate.dbsession.run_dir = run_dir
    try: 
        appstate.dbsession.connCtx_proxy = ve.launchdbjob(
            dbdesc=dbsession_id, run_dir=run_dir)
    except Exception as e:
        logger.debug(f"Unable to launch dbjob {e}")
        logger.debug(traceback.format_exc())
        appstate.dbsession.connCtx_proxy = None
        
    appstate.op = "Start dbsession"
    if appstate.dbsession.connCtx_proxy is not None:
        appstate.noticeboard_message = "successfully launched new database session"
        appstate.op_status = ojr.OpStatus.SUCCESS
    else:
        appstate.op_status = ojr.OpStatus.FAILED
        appstate.noticeboard_message = " Unable to launch dbsession: this event is logged"

    return appstate.op_status


ojr.make_react(START_DBSESSION, ojr.ReactTag_BackendAction)


def CONNECT_DBSESSION(appstate, arg=None):
    """
    connect to existing running dbsession
    """
    #run_dir = "/tmp/tmp5gbgkb_2/"
    #
    # model.dbsession_id = "t"  # TODO

    try:
        appstate.dbsession.dbconn, appstate.dbsession.dbsession = ve.connect_dbsession(
            appstate.dbsession.id, run_dir=appstate.dbsession.run_dir)
        appstate.dbsession.state = "running"
    except Exception as e:
        appstate.dbsession.state = "undefined"

        pass
    # model.run_dir = run_dir  # TODO

    #logger.info(f"connect dbsession = model.dbsession")
    return False, None


ojr.make_react(CONNECT_DBSESSION, ojr.ReactTag_BackendAction)

def STOP_DBSESSION(appstate, arg=None):
    try:
        appstate.dbsession.connCtx_proxy.conn.root.stopdb(appstate.dbsession.id)
        appstate.dbsession.state = "stopped"
    except Exception as e:
        appstate.dbsession.state = "undefined"
        logger.debug(f"Stop dbsession failed with error {e}")
        pass
    # model.run_dir = run_dir  # TODO

    #logger.info(f"connect dbsession = model.dbsession")
    return False, None
ojr.make_react(STOP_DBSESSION, ojr.ReactTag_BackendAction)

def shutdown_proxyService(appstate):
    # be a nice boy..cleanup before you leave
    try:
        appstate.dbsession.connCtx_proxy.conn.root.shutdown_proxyService()
    except EOFError:
        # when client closes the server; the client get EOFerror. This is expected. ignore it.
        pass


def BUILD_ORM(appstate, arg=None):
    with open(arg.name_csvpack, "r") as fh: # dl.get_page_text(arg.name_csvpack)
        cfgxml  = fh.read()
    print(cfgxml)
    cfgroot = ve.read_xmlstring(cfgxml)
    all_rmos = ve.build_orms(cfgroot, appstate.dbsession.run_dir)

    appstate.op_status = ojr.OpStatus.SUCCESS
    for rmo in all_rmos:
        if not ve.check_model_exists(rmo, work_dir=appstate.dbsession.run_dir):
            appstate.op_status = ojr.OpStatus.FAILED
            appstate.noticeboard_message = "unable to load all datasets from csvpack"
            break

    if appstate.op_status == ojr.OpStatus.SUCCESS:
        appstate.noticeboard_message = "all datasets from csvpack loaded successfully"
        for _ in all_rmos:
            appstate.dbsession.active_rmos[_] = ve.import_model(_, appstate.run_dir)

    pass


def EXPORT_RMO_TABULATE(appstate, arg=None):
    try:
        logger.debug("in actions.EXPORT_RMO_TABULATE")
        logger.debug(f"appstate = {appstate}")
        trmo = appstate.analytics.active_rmo
        dbsession = appstate.dbsession.dbsession
        exformat = appstate.exportrmo.tabulate.format
        res = ve.exapi.build_tabulate(dbsession, trmo, exformat)
        appstate.exportrmo.tabulate.text = f"{res}"
        appstate.noticeboard_message = "rmo tabulate export successful "
        appstate.op_status = ojr.OpStatus.SUCCESS
    except Exception as e:
        appstate.op_status = ojr.OpStatus.FAILED
        appstate.noticeboard_message = "Operation failed Unable to export"
        logger.debug(f"EXPORT_RMO_TABULATE failed with error {e}")
        logger.debug(traceback.format_exc())

        
        
