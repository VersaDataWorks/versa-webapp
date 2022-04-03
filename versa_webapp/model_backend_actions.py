"""All backend and model functions/actions for the webapp
"""
import logging
import os
if os:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
from addict import Dict
import versa_engine as ve

import webapp_framework as wf
#import dataapis.export as ex


def CSV_URL_INPUT(model: Dict, event_args: Dict):
    fn = ve.download_url(event_args.url)

    if fn is None:
        model.op = "Download CSV file"
        model.op_status = wf.OpStatus.FAILED
        model.op_error_report = " Unable to access url: " + event_args.url
        logger.debug(f"unable to download url {event_args.url}")
        return

    return GEN_CSV_METADATAREPORT(model,
                                  Dict({
                                      'file_name': event_args.url,
                                      'file_content': fn
                                  }
                                  )
                                  )


def GEN_CSV_METADATAREPORT(model, event_args):
    '''
    file_value: is portion of the form data recieved from the front end.
    Contains fields file_content, name, size, type, etc.

    '''
    ################################
    # ui_action_value.file_name    #
    # ui_action_value.file_content #
    ################################
    logger.info(f"GEN_CSV_METADATAREPORT = {event_args.file_name}")
    cmr = None
    #cmr = cis.get_csv_report(ui_action_value.file_content)
    try:
        cmr = ve.get_csv_report(event_args.file_content)
    except Exception as e:
        model.op_status = wf.OpStatus.FAILED
        model.op = "GEN_CSV_METADATAREPORT"
        model.error_report = "Unable to parse as CSV file"
        logger.debug(f"GEN_CSV_METADATAREPORT: {model.error_report}  {e}")
        return
        #import sys
        #sys.exit("Encountered Errors ")
    model.metadata_report.delimiter = cmr.delimiter
    model.metadata_report.delimiter_name = cmr.delimiter_name
    model.metadata_report.cols_type = cmr.cols_type
    model.metadata_report.num_data_lines = cmr.num_data_lines
    model.metadata_report.num_header_lines = cmr.num_header_lines
    model.metadata_report.header_lines = cmr.header_lines
    if cmr.header_candidates:
        model.metadata_report.header_candidates = [_ for _ in zip(
            *cmr.header_candidates)]
        model.metadata_edits.cols_name = cmr.header_candidates[0]
    else:
        model.metadata_report.header_candidates = None
        model.metadata_edits.cols_name = None

    model.metadata_report.csv_samples = cmr.samples
    model.metadata_edits.cols_type = cmr.cols_type
    model.metadata_edits.delimiter = cmr.delimiter
    model.metadata_edits.annotation = [None for _ in cmr.cols_type]
    model.metadata_edits.is_pkey = [False for _ in cmr.cols_type]
    model.metadata_edits.csv_file_name = event_args.file_name
    model.op_status = wf.OpStatus.SUCCESS
    model.op = "GEN_CSV_METADATAREPORT"
    logger.debug(f"analyzed csv : {model.metadata_report}")
    logger.debug(f"analyzed csv : {model.metadata_edits}")
    pass


def CSV_METADATA_AS_XML(model, uav):
    '''
    uav: ui_action_value

    outcome:
    self.model.edcfg.schema_xdef: the metadata definition of csv file
    '''
    model.edcfg.schema_xdef = ve.csv_utils.build_csv_metadata_v2(
        uav.csv_datamodel_label,
        model.metadata_report.delimiter,
        model.metadata_report.delimiter_name,
        uav.pks,
        uav.hasnulls,
        uav.cols_name,
        uav.cols_type
    )
    logger.debug(f"metadata as xdef {model.edcfg.schema_xdef}")
    metadata_fn = uav.csv_datamodel_label + ".md"

    model.edcfg.schema_xelem = ve.dataapis.build_file_element(
        model.csv_file_name,
        model.metadata_fn,
        uav.csv_datamodel_label,
        model.metadata_report.delimiter_name,
        model.metadata_report.num_header_lines)
    logger.debug(f"edcfg defination: {model.edcfg.schema_xdef}")
    model.edcfg.schema_xfn = metadata_fn
    model.op_status = wf.OpStatus.SUCCESS
    model.op = "GEN_METADATA_FILE"
    pass


# def write_metadata_file():
#     """
#     using report and user input build the metadata file
#     """
#     col_types  : list
#     pk : list
#     has_nulls: list

#     col_names: list
#     model_name: str
