import logging
import os

import ofjustpy_react as ojr
#import webapp_framework as wf

if os:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

import versa_engine as ve

# ojr.UpdateAppStateAndUI


def START_DBSESSION(appstate, arg=None):
    logger.info(f"calling start dbsession =  {appstate.session_id}")
    dbsession_id = appstate.session_id
    run_dir = "~/DrivingRange/" + dbsession_id
    run_dir = "/tmp/tmp5gbgkb_2/"
    appstate.run_dir = run_dir
    appstate.connCtx_proxy = ve.launchdbjob(
        dbdesc=dbsession_id, run_dir=run_dir)
    appstate.op = "Start dbsession"
    if appstate.connCtx_proxy is not None:
        appstate.noticeboard_message = "successfully launched new database session"
        appstate.op_status = ojr.OpStatus.SUCCESS
    else:
        appstate.op_status = ojr.OpStatus.FAILED
        appstate.noticeboard_message = " Unable to launch dbsession: this event is logged"

    # be a nice boy..cleanup before you leave

    try:
        appstate.connCtx_proxy.conn.root.shutdown_proxyService()
    except EOFError:
        # when client closes the server; the client get EOFerror. This is expected. ignore it.
        pass
    return False, None


ojr.make_react(START_DBSESSION, ojr.ReactTag_BackendAction)


def CONNECT_DBSESSION(model, arg=None):
    """
    connect to existing running dbsession
    """
    #run_dir = "/tmp/tmp5gbgkb_2/"
    #
    # model.dbsession_id = "t"  # TODO

    model.dbconn, model.dbsession = ve.connect_dbsession(
        model.session_id, run_dir=model.run_dir)
    # model.run_dir = run_dir  # TODO

    #logger.info(f"connect dbsession = model.dbsession")
    return False, None


ojr.make_react(CONNECT_DBSESSION, ojr.ReactTag_BackendAction)
# def BUILD_ORM(model, arg=None):
#     # this should be run under dl context
#     cfgxml = dl.get_page_text(arg.name_csvpack)
#     cfgroot = xu.read_string(cfgxml)
#     all_rmos = vi.build_orms(cfgroot, model.run_dir)

#     model.op_status = OpStatus.SUCCESS
#     for rmo in all_rmos:
#         if not vu.check_model_exists(rmo, work_dir=model.run_dir):
#             model.op_status = OpStatus.FAILED
#             model.noticeboard_message = "unable to load all datasets from csvpack"
#             break

#     if model.op_status == OpStatus.SUCCESS:
#         model.noticeboard_message = "all datasets from csvpack loaded successfully"
#         for _ in all_rmos:
#             model.active_rmos[_]  = vu.import_model(_, model.run_dir)

#     pass
