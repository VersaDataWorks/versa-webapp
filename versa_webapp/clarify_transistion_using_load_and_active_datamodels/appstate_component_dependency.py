from typing import Any, NamedTuple
from addict import Dict

import ofjustpy as oj
import ofjustpy_react as ojr


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
                         ojr.ReactTag_UI.UpdateActiveModels, None)
                 ]
                 )]
)
