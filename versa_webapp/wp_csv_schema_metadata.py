"""
creates a webpage to input CSV file/url 
and prints out it schema and metadata
"""

import logging
import os
import sys
if sys:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
import justpy as jp
import webapp_framework as wp


def wp_csv_schema_metadata(request):
    wp = wf.WebPage("wp", page_type="quasar")()

    return wp
