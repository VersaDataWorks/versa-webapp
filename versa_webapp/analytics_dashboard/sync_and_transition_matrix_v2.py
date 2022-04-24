from typing import Any, NamedTuple

from dpathutils import dget, dnew
from addict import Dict
from aenum import Enum, auto
from dpath.util import set as dset


class AttrMeta(NamedTuple):
    """
    metadata about ui component
    """
    is_active: Any
    ui_context: Any
    appstate_context: Any


class UIOps(Enum):
    DISABLE = auto()
    ENABLE = auto()


_cfg = cfg_CM = Dict(track_changes=True)

_cfg.dbsession.id = AttrMeta(True, [],
                             [
                                 (("/dbsession/state", "running"), UIOps.DISABLE
                                  ),
                                 (("/dbsession/state", "stopped"), UIOps.ENABLE
                                  )
]
)

_cfg.dbsession.start = AttrMeta(True, [], [
    (("/dbsession/state", "running"), UIOps.DISABLE
     ),
    (("/dbsession/state", "stopped"), UIOps.ENABLE
     )
]
)

_cfg.dbsession.stop = AttrMeta(True, [], [(("/dbsession/state", "running"), UIOps.ENABLE),
                                          (("/dbsession/state", "stopped"),
                                           UIOps.DISABLE)
                                          ])

# there is a flip in depedency: when stop is true then teardown is active
_cfg.dbsession.teardown = AttrMeta(True, [], [(("/dbsession/state", "running"), UIOps.DISABLE),
                                              (("/dbsession/state",
                                               "stopped"), UIOps.ENABLE)
                                              ])
