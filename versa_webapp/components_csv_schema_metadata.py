"""
ui components for wp_csv_schema_metadata.
"""

import logging
import os
import sys
if sys:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
from addict import Dict
import justpy as jp
import webapp_framework as wf
import webapp_framework_extn as wfx

from tracker import _hcs as stubStore, session_dict, refBoard
from tailwind_tags import W

from aenum import extend_enum, auto
from .model_backend_actions import CSV_METADATA_AS_XML
extend_enum(wf.ReactTag_ModelUpdate,
            'CSV_METADATA_AS_XML', CSV_METADATA_AS_XML)


def build_components(model):
    with wf.uictx("csm") as _ctx:
        with wf.uictx("stats") as _statsctx:
            wf.KeyValue_("delimiter", "delimiter",
                         model.metadata_report.delimiter_name)
            wf.KeyValue_("numcols", "#cols",
                         len(
                             model.metadata_report.cols_type))

            wf.KeyValue_("numheaderlines", "#headers",
                         model.metadata_report.num_header_lines, readonly=False)
            wf.KeyValue_("numrecords", "#records",
                         model.metadata_report.num_data_lines)

            wf.StackV_("records", [_statsctx.delimiter, _statsctx.numcols,
                       _statsctx.numheaderlines, _statsctx.numrecords])
            wf.ExpansionContainer_(
                'stataccord', "Stats", _statsctx.records)
            wf.Subsection_("section", "Stats", _statsctx.stataccord)

        if model.metadata_report.header_lines:
            wfx.Table_(
                "headertbl", model.metadata_report.header_lines, add_cbox=True)
            wf.ExpansionContainer_(
                'headeraccord', "Header Lines", _ctx.headertbl)
            wf.Subsection_("headers", "Header Lines", _ctx.headeraccord)
        else:
            wf.Subsection_("headers", "Header Lines", wf.Span_(
                "noheadertext", "No header lines found"))
        with wf.uictx("samples") as _samplesCtx:
            wfx.Table_("samplestbl", model.metadata_report.csv_samples)
            wf.ExpansionContainer_(
                'samplesaccord', "Row Samples", _samplesCtx.samplestbl)
            wf.Subsection_("section", "Row Samples", _samplesCtx.samplesaccord)

        with wf.uictx("coltypes") as _ictx:
            def on_select(dbref, msg):
                pass

            # def cgens():
            #     for col_pos, col_type in enumerate(model.metadata_report.cols_type):
            #         yield wf.SelectorWBanner_(f"selector_{col_pos}", f"col {col_pos}", [col_type, 'string'], [col_type, 'string'], 0, on_select)
            coltype_selectors = [wf.SelectorWBanner_(f"selector_{col_pos}", f"col {col_pos}", [col_type, 'string'], [
                                                     col_type, 'string'], 0, on_select) for col_pos, col_type in enumerate(model.metadata_report.cols_type)]
            wf.StackW_("selectors", coltype_selectors)
            wf.Subsection_("section", "Column Types (Inferred)",
                           _ictx.selectors)

        with wf.uictx("colnames") as _ictx:
            def cgens():
                for col_pos, col_names in enumerate(model.metadata_report.header_candidates):
                    def items():
                        yield wf.SelectorWBanner_(f"selector_{col_pos}", f"col {col_pos}", col_names, col_names, 0, on_select)
                        yield wf.Checkboxinput_(f"oname_{col_pos}", f"col{col_pos}")
                        yield wf.Checkbox_(f"is_pk_{col_pos}", "is primary key", col_pos)
                        yield wf.Checkbox_(f"is_hn_{col_pos}", "has nulls", col_pos)

                    yield wf.StackV_(f"col_{col_pos}", [_ for _ in items()], pcp=[W/"1/3"])

            # we generate the stubs here itself, so that they get registered with context
            wf.StackW_("selectors", [_ for _ in cgens()])
            wf.Subsection_("section", "Column Names (Inferred)",
                           _ictx.selectors)
        with wf.uictx("gencsvcfg") as _ictx:
            @wf.MRVWLR
            def on_form_submit(dbref, msg):
                print("calling on form submit")
                res = Dict()  # collect all the results
                res.col_types = [_ctx.coltypes[f"selector_{idx}"].target.getValue(
                ) for idx, _ in enumerate(model.metadata_report.cols_type)]

                # TODO: cbox toplevel component is a Label but it doesn't have a getValue function
                # we need to design this better
                res.pks = [_ctx.colnames[f"is_pk_{idx}cbox"].target.checked for idx, _ in enumerate(
                    model.metadata_report.cols_type)]

                res.hasnulls = [_ctx.colnames[f"is_hn_{idx}cbox"].target.checked for idx, _ in enumerate(
                    model.metadata_report.cols_type)]

                res.cols_name = [_ctx.colnames[f"selector_{idx}"].target.getValue() for idx, _ in enumerate(
                    model.metadata_report.cols_type)]

                for idx, _ in enumerate(model.metadata_report.cols_type):
                    if _ctx.colnames[f"oname_{idx}cbox"].target.checked and _ctx.colnames[f"oname_{idx}inp"].target.getValue().strip() != "":
                        res.cols_name[idx] = _ctx.colnames[f"oname_{idx}inp"]
                # if _cb.checked and _in.value.strip() != '':
                #     uav.metadata_edits.cols_name[cpos] = _in.value.strip()
                # TODO: getInputValue vs. getInput
                res.csv_datamodel_label = _ictx.btn.target.getInputValue()
                print("pks = ", res.pks)
                print("hasnul = ", res.hasnulls)
                print("cols_name = ", res.cols_name)
                print("model name ", res.csv_datamodel_label)
                rts = wf.TaskStack()
                rts.addTask(wf.ReactTag_ModelUpdate.CSV_METADATA_AS_XML, res)
                rts.addTask(wf.ReactTag_Backend.CHECK_OP_STATUS, None)
                return msg.page, rts

                pass
            wf.InputJBtn_("btn", "Assing a  name", "nameme.cfg", "Generate metadata config",
                          on_form_submit, on_form_submit)

            wf.Subsection_("section", "Build CSV config file", _ictx.btn)

        wf.Halign_(wf.TitleBanner_(title="CSV schema and metadata"))
    # BRB
