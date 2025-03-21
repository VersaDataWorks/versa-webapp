import logging
import os
if os:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
import versa_engine as ve
from addict import Dict
import ofjustpy_react as ojr
import pickle
from . import  wp_csv_schema_metadata_v3
from . import wp_save_csvpack_v3
def GEN_CSV_METADATAREPORT(appstate, event_args):
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
        cmr = ve.csv_utils.get_csv_report(event_args.file_content)
    except Exception as e:
        appstate.op_status = ojr.OpStatus.FAILED
        appstate.op = "GEN_CSV_METADATAREPORT"
        appstate.error_report = "Unable to parse as CSV file"
        logger.debug(f"GEN_CSV_METADATAREPORT: {appstate.error_report}  {e}")
        return
        #import sys
        #sys.exit("Encountered Errors ")
    appstate.metadata_report.delimiter = cmr.delimiter
    appstate.metadata_report.delimiter_name = cmr.delimiter_name
    appstate.metadata_report.cols_type = cmr.cols_type
    appstate.metadata_report.num_data_lines = cmr.num_data_lines
    appstate.metadata_report.num_header_lines = cmr.num_header_lines
    appstate.metadata_report.header_lines = cmr.header_lines
    if cmr.header_candidates:
        appstate.metadata_report.header_candidates = [_ for _ in zip(
            *cmr.header_candidates)]
        appstate.metadata_edits.cols_name = cmr.header_candidates[0]
    else:
        appstate.metadata_report.header_candidates = None
        appstate.metadata_edits.cols_name = None

    appstate.metadata_report.csv_samples = cmr.samples
    appstate.metadata_edits.cols_type = cmr.cols_type
    appstate.metadata_edits.delimiter = cmr.delimiter
    appstate.metadata_edits.annotation = [None for _ in cmr.cols_type]
    appstate.metadata_edits.is_pkey = [False for _ in cmr.cols_type]
    appstate.metadata_edits.csv_file_name = event_args.file_name
    appstate.op_status = ojr.OpStatus.SUCCESS
    appstate.op = "GEN_CSV_METADATAREPORT"

    logger.debug(f"analyzed csv : {appstate.metadata_report}")
    logger.debug(f"analyzed csv : {appstate.metadata_edits}")
    pass

def ANALYZE_CSV_CONTENT(appstate, arg, webpage):
    """
    appctx=/csvinput/url_and_content
    """
    print ("calling ANALYZE_CSV_CONTENT")
    print ("with appstate= ", appstate )
    print ("with arg = ", arg)

    (url, content) = appstate.csvinput.url_and_content
    #url with no content
    if "http://" in url and not content:
        try:
            filename, content  = ve.download_url(url)
            logger.debug(f"ANALYZE url filename {url} {filename}")
            arg = Dict({
                                      'file_name': filename,
                                      'file_content': content,
                                  })
            GEN_CSV_METADATAREPORT(appstate, arg)
        except Exception as e:
            appstate.op = "Download CSV file"
            appstate.op_status = ojr.OpStatus.FAILED
            appstate.op_error_report = f" Unable to download url: {url} {e}" 
            logger.debug(f"unable to download url {url} : {e}")
            return
        

            
    return 

def SET_REDIRECT(appstate, arg, webpage):
    """
    appctx=/op_status
    """
    if appstate.op_status == ojr.OpStatus.SUCCESS and appstate.op == "GEN_CSV_METADATAREPORT":
        # TODO: define a unique label for this dataset
        data_label = "alpha"
        wp_csv_schema_metadata_v3.create_endpoint(appstate, data_label)
        
        appstate.wp_redirect = f"/csv_metadata_{data_label}"

    if appstate.op_status == ojr.OpStatus.SUCCESS and appstate.op == "CSV_METADATA_AS_XML":
        appstate.wp_redirect = "/savecfg"        
    
    #Redirect to home on failure
    pass


def CSV_METADATA_AS_XML(appstate, arg, webpage):
    '''
    appctx=/csv_schema_metadata/gencsvcfg_panel
    '''
    print ("calling CSV_METADATA_AS_XML: with arg = ", arg)
    uav = arg
    #uav = appstate.gencsvcfg_panel.value
    # with open("gencsvcfg_panel_value.pickle", "wb") as fh:
    #     import json
    #     jstr = json.dumps(uav)
    #     ttmp = json.loads(jstr)
    #     logger.debug(f"uav dump = {ttmp}")
    #     pickle.dump(ttmp, fh)

    appstate.edcfg.schema_xdef = ve.csv_utils.build_csv_metadata_v2(
        uav.csv_datamodel_label,
        appstate.metadata_report.delimiter,
        appstate.metadata_report.delimiter_name,
        uav.pks,
        uav.hasnulls,
        uav.cols_name,
        uav.cols_type
    )
    logger.debug(f"metadata as xdef {appstate.edcfg.schema_xdef}")
    metadata_fn = uav.csv_datamodel_label + ".md"
    logger.debug(f"csv_datamodel_label = {uav.csv_datamodel_label}")
    appstate.edcfg.schema_xelem = ve.dataapis.build_file_element(
        appstate.metadata_edits.csv_file_name,
        metadata_fn,
        uav.csv_datamodel_label,
        appstate.metadata_report.delimiter_name,
        appstate.metadata_report.num_header_lines)
    logger.debug(f"edcfg.schema_xelem: {appstate.edcfg.schema_xelem}")
    appstate.edcfg.schema_xfn = metadata_fn
    appstate.op_status = ojr.OpStatus.SUCCESS
    appstate.op = "CSV_METADATA_AS_XML"
    pass



def GEN_EDCFG_FILE(appstate, arg, page):
    """
    appctx=/save_csv_metadatacfg/local
    """
    
    appstate.edcfg.dpcfg_xfn = arg.model_name  + ".csvpack" # appstate.save_csvpack.model_name + ".csvpack"
    print ("schema_xelem = ", ve.xu.tostring(appstate.edcfg.schema_xelem))
    
    [dpcfg_xelem, xistr] = ve.build_edcfg_elem(
        [appstate.edcfg.schema_xelem], appstate.edcfg.dpcfg_xfn)


    appstate.edcfg.dpcfg_xelem = dpcfg_xelem
    appstate.edcfg.xistr = xistr
    
    print ("dpcfg_xelem = ",  ve.xu.tostring(appstate.edcfg.dpcfg_xelem))
    print ("xistr = ", appstate.edcfg.xistr)
    
    with open(appstate.edcfg.schema_xfn, "w") as fh:
        fh.write(appstate.edcfg.schema_xdef)

    with open(appstate.edcfg.dpcfg_xfn, "w") as fh:
        fh.write(ve.xu.tostring(appstate.edcfg.dpcfg_xelem))

    with open(arg.model_name + ".xistr", "w") as fh:
        fh.write(appstate.edcfg.xistr)
    pass
