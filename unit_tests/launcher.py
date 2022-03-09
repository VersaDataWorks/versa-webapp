import logging
import os
if os:
    try:
        os.remove("launcher.log")
    except:
        pass

import sys
if sys:
    logging.basicConfig(filename="launcher.log", level=logging.INFO)


from versa_webapp.wp_csvdata_input import wp_csvdata_input
import justpy as jp

from tracker import _hcs, refBoard

app = jp.app
jp.justpy(wp_csvdata_input, start_server=False)
#wp = wp_csvdata_input(None)
