from typing import Any, NamedTuple
import ofjustpy_react as ojr
from .dpathutils import dget, dnew
from addict import Dict
from aenum import Enum, auto
from dpath.util import set as dset


class AttrMeta(NamedTuple):
    """
    metadata about ui component
    """
    default: Any
    is_active: Any
    ui_context: Any
    appstate_context: Any

# class AttrMetaUIAppstate(NamedTuple):
#     ui_context:Any
# _cfg = cfg_UI_appstate_transition_matrix = Dict(track_changes=True)
# _cfg.dbsession.id  = AttrMetaUIAppstate("/dbsess


class Ctx(NamedTuple):
    path: Any
    condition: Any
    uiop: Any


class UIOps(Enum):
    DISABLE = auto()
    ENABLE = auto()
    UPDATE_NOTICEBOARD = auto()


def eq_op(val):
    return lambda x, val=val: x == val


def isstr(val):
    return isinstance(val, str)


_cfg = cfg_CM = Dict(track_changes=True)

_cfg.dbsession.id = AttrMeta(None, True, [],
                             [
                                 Ctx("/dbsession/state",
                                     eq_op("running"), UIOps.DISABLE),
                                 Ctx("/dbsession/state",
                                     eq_op("stopped"), UIOps.ENABLE)
]
)

_cfg.dbsession.start = AttrMeta(None, True, [], [

    Ctx("/dbsession/id", isstr, UIOps.ENABLE),
    Ctx("/dbsession/state", eq_op("running"), UIOps.DISABLE),
    Ctx("/dbsession/state", eq_op("stopped"), UIOps.ENABLE)
]
)

_cfg.dbsession.stop = AttrMeta(None, True, [],
                               [Ctx("/dbsession/state", eq_op("running"), UIOps.ENABLE),
                                Ctx("/dbsession/state",
                                    eq_op("stopped"), UIOps.DISABLE)
                                ]
                               )

# there is a flip in depedency: when stop is true then teardown is active
# _cfg.dbsession.teardown = AttrMeta(None, True, [],
#                                    [Ctx("/dbsession/state", eq_op("running"), UIOps.DISABLE),
#                                     Ctx("/dbsession/state",
#                                         eq_op("stopped"), UIOps.ENABLE)
#                                     ]
#                                    )

_cfg.misc.noticeboard = AttrMeta(None, True, [],
                                 [Ctx("/op_status", eq_op(ojr.OpStatus.FAILED), UIOps.UPDATE_NOTICEBOARD)])
