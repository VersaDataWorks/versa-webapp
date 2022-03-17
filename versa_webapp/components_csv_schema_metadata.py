"""
ui components for wp_csv_schema_metadata.
"""

import logging
import os
import sys
if sys:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
import justpy as jp
import webapp_framework as wf
import webapp_framework_extn as wfx

from tracker import _hcs as stubStore, session_dict, refBoard
from tailwind_tags import W


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

        with wf.uictx("samples") as _samplesCtx:
            wfx.Table_("samplestbl", model.metadata_report.csv_samples)
            wf.ExpansionContainer_(
                'samplesaccord', "Row Samples", _samplesCtx.samplestbl)
            wf.Subsection_("section", "Row Samples", _samplesCtx.samplesaccord)

        with wf.uictx("coltypes") as _ictx:
            def on_select(dbref, msg):
                pass

            def cgens():
                for col_pos, col_type in enumerate(model.metadata_report.cols_type):
                    yield wf.SelectorWBanner_(f"selector_{col_pos}", f"col {col_pos}", [col_type, 'string'], [col_type, 'string'], 0, on_select)
            wf.StackW_("selectors", cgens())
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

                    yield wf.StackV_(f"items{col_pos}", items(), pcp=[W/"1/3"])
            wf.StackW_("selectors", cgens())
            wf.Subsection_("section", "Column Names (Inferred)",
                           _ictx.selectors)
        with wf.uictx("gencsvcfg") as _ictx:
            def on_form_submit(dbref, msg):
                pass
            wf.InputJBtn_("btn", "Assing a  name", "nameme.cfg",
                          on_form_submit, "Generate metadata config", on_form_submit)

            wf.Subsection_("section", "Build CSV config file", _ictx.btn)

        wf.Halign_(wf.TitleBanner_(title="CSV schema and metadata"))
    # BRB
