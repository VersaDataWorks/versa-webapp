import logging
import os
if os:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)


def START_DBSESSION(model, arg=None):
    logger.info(f"calling start dbsession =  {model.session_id}")
    dbsession_id = model.session_id
    run_dir = "~/DrivingRange/" + dbsession_id
    run_dir = "/tmp/tmp5gbgkb_2/"
    model.run_dir = run_dir
    model.connCtx_proxy = frontend_controller.launchdbjob(
        dbsession_id, run_dir="~/DrivingRange/" + dbsession_id)
    model.op = "Start dbsession"
    if model.connCtx_proxy is not None:
        model.noticeboard_message = "successfully launched new database session"
        model.op_status = OpStatus.SUCCESS
    else:
        model.op_status = OpStatus.FAILED
        model.noticeboard_message = " Unable to launch dbsession: this event is logged"

    pass


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
