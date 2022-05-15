from . import actions
from addict import Dict
import logging
import ofjustpy_react as ojr
import os
if logging:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    
cfg_actions = Dict()


def exec_actions(action_list, appstate):
    """
    execute sequence of actions until failed. 
    This is a simple model for execution of actions. 
    

    """
    op_status = ojr.OpStatus.SUCCESS
    for action in action_list:
        if op_status == ojr.OpStatus.SUCCESS:
            logger.debug(f"invoking action {action}")
            action(appstate)
            op_status = appstate.op_status


def error_handle(appstate):
    print("TODO: should handle error")
    pass


cfg_actions[("/dbsession/start", True)
            ] = [actions.START_DBSESSION, actions.CONNECT_DBSESSION]

cfg_actions[("/dbsession/stop", True)
            ] = [actions.STOP_DBSESSION]


# cfg_actions[("/dbsession/start", True)
#             ] = [(actions.DUMMY_ACTION, error_handle)]
