from typing import Any, NamedTuple
from addict import Dict

import webapp_framework as wf


class ComponentMeta(NamedTuple):
    """
    metadata about ui component
    """
    # if is active then it is shown
    is_active: Any
    active_context: Any
    appstate_context: Any


_cfg = cfg_CM = Dict(track_changes=True)

_cfg.load_datamodels.local.fakedataload = ComponentMeta(
    True, [], [])
_cfg.active_datamodels.fakelist = ComponentMeta(
    True,  [], [("/loaded_datamodel",
                 [
                     lambda wp, val: wp.appstate.active_datamodels.append(val),
                     lambda wp, val: wp.react_ui(
                         wf.ReactTag_UI.UpdateActiveModels, None)
                 ]
                 )]
)
