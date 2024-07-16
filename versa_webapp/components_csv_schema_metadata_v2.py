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
import ofjustpy as oj
import ofjustpy_extn as ojx
import ofjustpy_react as ojr
from tailwind_tags import (W,
                           H,
                           bsw,
                           bg,
                           cyan,
                           sw,
                           gray,
                           fc,
                           slate,
                           bd,
                           bsw,
                           variant,
                           green,
                           ppos,
                           absolute,
                           top,
                           right
                           )
from aenum import extend_enum, auto

def build_components(session_manager):
    stubStore = session_manager.stubStore
    appstate = session_manager.appstate

    undock_btn_sty = [bsw.xl,
                      bg/gray/2,
                      bd/gray/5,
                      sw/cyan/"500/50",
                      *variant(bg/gray/4,
                               fc/slate/5,
                               bd/slate/2,
                               bsw.none,
                               rv="disabled")
                      
                      ]

    dock_btn_gen = lambda key: oj.Button_(f"dock_{key}",
                                          text="-",
                                          pcp=[bg/green/1,
                                               W/6,
                                               H/6,
                                               top/1,
                                               right/1,
                                               absolute,
                                               ])
    dockbar_ = ojx.Dockbar_('dockbar',
                            undock_btn_sty = undock_btn_sty,
                            dock_btn_gen=dock_btn_gen,
                            
                            )

    with session_manager.uictx("csm") as _ctx:
        with session_manager.uictx("stats") as _statsctx:
            oj.KeyValue_("delimiter", "delimiter",
                         appstate.metadata_report.delimiter_name)
            oj.KeyValue_("numcols", "#cols",
                         len(
                             appstate.metadata_report.cols_type))

            oj.KeyValue_("numheaderlines", "#headers",
                         appstate.metadata_report.num_header_lines, readonly=False)
            oj.KeyValue_("numrecords", "#records",
                         appstate.metadata_report.num_data_lines)

            oj.StackV_("records", cgens=[_statsctx.delimiter, _statsctx.numcols,
                       _statsctx.numheaderlines, _statsctx.numrecords])
            # oj.ExpansionContainer_(
            #     'stataccord', "Stats", _statsctx.records)
            oj.Subsection_("section",
                           heading_text="Stats",
                           content_=_statsctx.records,
                           pcp=[ppos.relative],
                           dock_label= "Stats"
                           )
            dock_btn = dockbar_.dockify(_statsctx.section)
            _statsctx.section.add_cgen(dock_btn)

        if appstate.metadata_report.header_lines:
            ojx.Table_(
                "headertbl", appstate.metadata_report.header_lines, add_cbox=True)
            # oj.ExpansionContainer_(
            #     'headeraccord', "Header Lines", _ctx.headertbl)
            oj.Subsection_("headers",
                           heading_text="Header Lines",
                           content_=_ctx.headertbl,
                           pcp=[ppos.relative],
                           dock_label= "Headers"
                           )
            dock_btn = dockbar_.dockify(_ctx.headers)
            _ctx.headers.add_cgen(dock_btn)
        else:
            oj.Subsection_("headers",
                           heading_text="Header Lines",
                           content_=oj.Span_(
                               "noheadertext", text="No header lines found")
                           )
        with session_manager.uictx("samples") as _samplesCtx:
            ojx.Table_("samplestbl", appstate.metadata_report.csv_samples)
            # oj.ExpansionContainer_(
            #     'samplesaccord', "Row Samples", _samplesCtx.samplestbl)
            oj.Subsection_("section",
                           heading_text="Row Samples",
                           content_=_samplesCtx.samplestbl,
                           pcp=[ppos.relative],
                           dock_label= "Samples",
                           
                           )
            dock_btn = dockbar_.dockify(_samplesCtx.section)
            _samplesCtx.section.add_cgen(dock_btn)

        with session_manager.uictx("coltypes") as coltypesctx:
            def on_select(dbref, msg):
                pass

            # def cgens():
            #     for col_pos, col_type in enumerate(model.metadata_report.cols_type):
            #         yield wf.SelectorWBanner_(f"selector_{col_pos}", f"col {col_pos}", [col_type, 'string'], [col_type, 'string'], 0, on_select)
            coltype_selectors = [oj.WithBanner_(f"coltype_banner_{col_pos}",
                                            f"Column {col_pos}", oj.Select_(f"selector_{col_pos}",
                                                                            [
                                                                                oj.Option_(col_type, text=col_type, value=col_type, selected="selected"),
                                                                                oj.Option_('string', text='string', type='string')
                                                                            ]
                                                                            ).event_handle(oj.click, on_select))
                                                                 for col_pos, col_type in enumerate(appstate.metadata_report.cols_type)
                                 ]

            oj.StackW_("selectors", cgens=coltype_selectors)
            oj.Subsection_("section", heading_text="Column Types (Inferred)",
                           content_ = coltypesctx.selectors)

        with session_manager.uictx("colnames") as colnamesctx:
            def cgens():
                for col_pos, col_names in enumerate(appstate.metadata_report.header_candidates):
                    def items():
                        yield oj.WithBanner_(f"banner_{col_pos}", f"Column {col_pos}",
                                             oj.Select_(f"selector_{col_pos}", [oj.Option_(f"colname_option_{col_pos}", text=col_names[0], value=col_names[0], selected="selected"),
                                                                            *[oj.Option_(f"colname_option_{col_pos}", text=col_name, value=col_name) for col_name  in col_names[1:]]
                                                                            ]
                                         ).event_handle(oj.click, on_select)
                                         )

                        yield oj.CheckboxInput_(f"oname_{col_pos}", f"col{col_pos}")
                        yield oj.Checkbox_(f"is_pk_{col_pos}", "is primary key", col_pos)
                        yield oj.Checkbox_(f"is_hn_{col_pos}", "has nulls", col_pos)

                    yield oj.StackV_(f"col_{col_pos}", cgens=[_ for _ in items()], pcp=[W/"1/3"])

            # we generate the stubs here itself, so that they get registered with context
            oj.StackW_("selectors", cgens=[_ for _ in cgens()])
            oj.Subsection_("section", heading_text="Column Names (Inferred)",
                           content_=colnamesctx.selectors)
        with session_manager.uictx("gencsvcfg") as gencsvcfgctx:
            #@ojr.CfgLoopRunner
            def on_form_submit(dbref, msg):
                print("calling on form submit")
                res = Dict()  # collect all the results
                res.cols_type = [coltypesctx[f"selector_{idx}"].target.value
                 for idx, _ in enumerate(appstate.metadata_report.cols_type)]

                # # TODO: cbox toplevel component is a Label 
                # # we need to design this better to get checked value
                res.pks = [colnamesctx[f"is_pk_{idx}cbox"].target.checked for idx, _ in enumerate(
                     appstate.metadata_report.cols_type)]

                res.hasnulls = [colnamesctx[f"is_hn_{idx}cbox"].target.checked for idx, _ in enumerate(
                    appstate.metadata_report.cols_type)]
                res.cols_name = [colnamesctx[f"selector_{idx}"].target.value for idx, _ in enumerate(
                    appstate.metadata_report.cols_type)]

                for idx, _ in enumerate(appstate.metadata_report.cols_type):
                    if colnamesctx[f"oname_{idx}cbox"].target.checked and _ctx.colnames[f"oname_{idx}inp"].target.value.strip() != "":
                        res.cols_name[idx] = colnamesctx[f"oname_{idx}inp"].target.value

                res.csv_datamodel_label = gencsvcfgctx.btninput.target.value
                res.freeze()
                return "/gencsvcfg_panel",  ojr.OpaqueDict(res)
            

            oj.InputJBtn_("btn", oj.InputChangeOnly_("btninput",  text="Given a name/label to csv data", placeholder="nameme"), oj.Button_("btnbtn", text="Generate metadata config",
                                                                                                                                 ).event_handle(oj.click, on_form_submit))

            oj.Subsection_("section", heading_text="Build CSV config file", content_=gencsvcfgctx.btn)

        # oj.Halign_(oj.Title_("pagetitle", title_text="CSV schema and metadata"))
    # BRB
