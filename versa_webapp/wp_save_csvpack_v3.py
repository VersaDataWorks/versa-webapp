import logging
import os
import sys
import versa_engine as ve


if sys:
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename="launcher.log",
                        level=logging.DEBUG, format=FORMAT)

    logger = logging.getLogger(__name__)

import kavya as kv
app = kv.load_app()
import kavya_react as kvr
from aenum import Enum, extend_enum
from . import actions

ui_app_trmap_iter = [ 

    ("/save_csvpack/dl/savecfgas", "/save_csvpack/model_name", None
                       ),
    ("/save_csv_metadatacfg/local", "/save_csv_metadatacfg/local", None
                       )
                      
                     ]


def post_init(session_manager=None):
    pass

from .components_save_csvpack_v3 import title, savecfg_panel
tlc = kv.HM.Container(childs = [title,
                                        savecfg_panel
                                        ]
                              )


endpoint = kvr.create_endpoint("wp_savecsvcfg",
                               [tlc
                                ],
                               ui_app_trmap_iter = ui_app_trmap_iter,
                               action_module = actions,
                               rendering_type="MutableSSR",
                               svelte_bundle_dir="hyperui",
                               #path_guards = path_guards,
                               post_init = post_init,
                               head_html =  """<script src="https://cdn.tailwindcss.com"></script> """,
                               reactctx = [kvr.Ctx("/wp_redirect", kvr.isstr, kvr.UIOps.REDIRECT)],

                                  )
kv.add_route("/savecfg", endpoint)


