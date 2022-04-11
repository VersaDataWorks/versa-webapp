from typing import Any, NamedTuple

from .dpathutils import dget, dnew
from addict import Dict
from aenum import Enum, auto
from dpath.util import set as dset


class AttrMeta(NamedTuple):
    """
    metadata about ui component
    """
    default: Any
    active: Any
    context: Any  # describes all scenarios when attribute is active


_cfg = cfg_model = Dict()
_cfg.dbsession.id = AttrMeta(None, True, [
                             ("/dbsession/stop", False)])
_cfg.dbsession.start = AttrMeta(
    False, False, [("/dbsession/id", True), ("/dbsession/id", "False"), ("/dbsession/stop", False)])
_cfg.dbsession.stop = AttrMeta(False, False, [("/dbsession/start", True)

                                              ])

# there is a flip in depedency: when stop is true then teardown is active
_cfg.dbsession.teardown = AttrMeta(False, False, [("/dbsession/stop", True)

                                                  ])
