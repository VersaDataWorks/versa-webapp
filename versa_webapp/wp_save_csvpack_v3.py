import logging
import os
import sys
import versa_engine as ve


if sys:
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename="launcher.log",
                        level=logging.DEBUG, format=FORMAT)

    logger = logging.getLogger(__name__)

import ofjustpy as oj
app = oj.load_app()
import ofjustpy_react as ojr
from aenum import Enum, extend_enum
from . import actions

ui_app_trmap_iter = [ 

    ("/save_csvpack/dl/savecfgas", "/save_csvpack/model_name", None
                       ),
    ("/save_csv_metadatacfg/local", "/save_csv_metadatacfg/local", None
                       )
                      
                     ]


def post_init(wp, session_manager=None):
    pass

from .components_save_csvpack_v3 import title, savecfg_panel
tlc = oj.HCCMutable.Container(childs = [title,
                                        savecfg_panel
                                        ]
                              )


endpoint = ojr.create_endpoint("wp_savecsvcfg",
                               [tlc
                                ],
                               ui_app_trmap_iter = ui_app_trmap_iter,
                               action_module = actions,
                               rendering_type="CSR",
                               csr_bundle_dir="hyperui",
                               #path_guards = path_guards,
                               post_init = post_init,
                               head_html =  """<script src="https://cdn.tailwindcss.com"></script> """,
                               reactctx = [ojr.Ctx("/wp_redirect", ojr.isstr, ojr.UIOps.REDIRECT)],

                                  )
oj.add_jproute("/savecfg", endpoint)


