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
import ofjustpy as oj
import ofjustpy_components as ojx
import ofjustpy_react as ojr
from py_tailwind_utils import (W,
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


def build_kv_record(key, label, component, component_type="passive", twsty_tags = []):
    #print (f"Build ui for {key}<===> {label} : ", component.key, " ", component.id, " ", component_type)
    component.add_twsty_tags(fz.sm, fw.normal, fc/slate/800)
    eq = oj.PC.Span(text=":", twsty_tags=[jc.center, fz.sm, fw.normal, fc/slate/800])
    label = oj.PC.Span(text=label , twsty_tags=[ta.end, W/fit, fz.sm, fw.normal, fc/gray/600])
    if component_type == "passive":
        rec = oj.Mutable.StackH(key = f"input_row_{key}",
                                childs=[ oj.PD.Valign(label, height_tag=noop/noop, twsty_tags=[W/fit, jc.end]),
                                         oj.PD.Valign(eq,height_tag=noop/noop),
                                         oj.PD.Valign(Halign(component, "start", twsty_tags=[]), height_tag=noop/noop),
                                         #component
                                         
                                ],
                        twsty_tags=[W/full, *twsty_tags, pd/st/4, mr/y/2, pd/y/1, space/x/1, mr/x/1, pd/x/1, jc.center, boxtopo.bd, bd/transparent, bd/2, bd/st/slate/400, bd/sl/slate/100, bd/sl/1])
    elif component_type == "mutable":
        rec = oj.Mutable.StackH(key = f"input_row_{key}",
                                childs=[ label,
                                         eq,
                                         oj.HCCMutable.Halign(component, "start", twsty_tags=[] )
                                         #component                          
                                        ],
                                twsty_tags=[W/full, *twsty_tags, pd/st/4, mr/y/2, pd/y/1, mr/x/1, pd/x/1, jc.center, boxtopo.bd, bd/transparent, bd/2, bd/st/slate/400, bd/sl/slate/100, bd/sl/1]
                                )
    return rec


def on_alt_colname_inp(dbref, msg, to_ms):
    pass

def build_ui_colnames():
    def cgens():
        for col_pos, col_names in enumerate(appstate.metadata_report.header_candidates):
            def items():
                yield oj.WithBanner(f"Column {col_pos}:",
                                               oj.AD.Select(key=f"selector_{col_pos}",
                                                            childs=[oj.PC.Option(
                                                                          text=col_names[0],
                                                                          value=col_names[0],
                                                                          selected="selected"),
                                                             *[oj.PC.Option(
                                                                            text=col_name,
                                                                            value=col_name)
                                                               for col_name  in col_names[1:]
                                                               ]
                                                             ],
                                                            on_click = on_select,
                                                            twsty_tags=[W/28, pd/sl/2, shadow.inner, boxshadow/gray/"300/50"]
                                                            ),
                                    twsty_tags=[space/x/1, bg/gray/100, pd/1, mr/st/1, ai.center]
                                         )
                yield oj.PD.StackH(childs = [ oj.AD.CheckboxInput(key=f"use_oname_{col_pos}"),
                                              oj.WithBanner(f"Alt Name: ",
                                                            
                                                           oj.AD.TextInput(key=f"inp_oname_{col_pos}",
                                                                           placeholder="alt name",
                                                                           on_change=on_alt_colname_inp,
                                                                           twsty_tags=[shadow.inner, boxshadow/gray/"400/50", pd/1]
                                                                           ),
                                                            twsty_tags=[ai.center, space/x/1]
                                                           
                                                 )
                                              ],
                                    twsty_tags=[ai.center, space/x/1, bg/gray/100, pd/1, mr/st/1]
                                    )

            yield oj.PD.StackV(childs=[_ for _ in items()], twsty_tags=[space/y/2])

    return oj.PD.StackW(
                                childs=[_ for _ in cgens()],
        twsty_tags = [space/x/4, bg/pink/100, bd/pink/100, bd/st/transparent, bd/sb/green/500, pd/1, mr/1]
                                )
        
    pass

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

            delimiter = build_kv_record("delimiter", "delimiter", appstate.metadata_report.delimiter_name
                            )
            numcols = build_kv_record("numcols", "#cols", len(
                             appstate.metadata_report.cols_type)
                            )
            numheaderlines = build_kv_record("numheaderlines", "#headers",
                            appstate.metadata_report.num_header_lines,
                            # readonly=False #TODO
                            )
            numrecords = build_kv_record("numrecords", "#records",
                            appstate.metadata_report.num_data_lines)
            
            
            box = oj.PD.StackV(childs=[delimiter,
                                 numcols,
                                 numheaderlines,
                                 numrecords
            ])

            panel = oj.PD.Subsection(heading_text="Stats",
                             content =box,
                             twsty_tags=[ppos.relative],
                             dock_label= "Stats"
                             )
            # TODO
            #dock_btn = dockbar_.dockify(_statsctx.section)
            # TODO
            #_statsctx.section.add_cgen(dock_btn)

        if appstate.metadata_report.header_lines and False:
            #TODO:
            # ojx.Table_("headertbl",
            #            appstate.metadata_report.header_lines,
            #            add_cbox=True)
            
            # # oj.ExpansionContainer_(
            # #     'headeraccord', "Header Lines", _ctx.headertbl)
            # oj.Subsection_("headers",
            #                heading_text="Header Lines",
            #                content_=_ctx.headertbl,
            #                pcp=[ppos.relative],
            #                dock_label= "Headers"
            #                )
            # dock_btn = dockbar_.dockify(_ctx.headers)
            # _ctx.headers.add_cgen(dock_btn)
            pass
        else:
            oj.PD.Subsection(
                           heading_text="Header Lines",
                           content_=oj.PC.Span(text="No header lines found")
                           )
        with session_manager.uictx("samples") as _samplesCtx:
            simple_table = SimpleTable()
            for row_data in appstate.metadata_report.csv_samples:
                _row = simple_table.add_row()
                for cell_data in row_data:
                    _row.add_cell(cell_data)
            #ojx.Table_("samplestbl", appstate.metadata_report.csv_samples)
            # oj.ExpansionContainer_(
            #     'samplesaccord', "Row Samples", _samplesCtx.samplestbl)
            oj.PD.Subsection_(
                           heading_text="Row Samples",
                           content_=_samplesCtx.samplestbl,
                           pcp=[ppos.relative],
                           dock_label= "Samples",
                           
                           )
            # dock_btn = dockbar_.dockify(_samplesCtx.section)
            # _samplesCtx.section.add_cgen(dock_btn)

        with oj.uictx("coltypes") as coltypesctx:
            def on_select(dbref, msg):
                pass

            # def cgens():
            #     for col_pos, col_type in enumerate(model.metadata_report.cols_type):
            #         yield wf.SelectorWBanner_(f"selector_{col_pos}", f"col {col_pos}", [col_type, 'string'], [col_type, 'string'], 0, on_select)
                
            coltype_selectors = [oj.PC.WithBanner(f"Column {col_pos}",
                                            oj.AD.Select(key=f"selector_{col_pos}",
                                                   childs = [
                                                                    oj.Option_(col_type, text=col_type, value=col_type, selected="selected"),
                                                                    oj.Option_('string', text='string', type='string')
                                                                ],
                                                   on_click = on_select
                                                   )
                                      )
                                 for col_pos, col_type in enumerate(appstate.metadata_report.cols_type)
                                 ]

            oj.PD.StackW(childs=coltype_selectors)
            oj.PD.Subsection("section", heading_text="Column Types (Inferred)",
                           content_ = coltypesctx.selectors)

        with oj.uictx("colnames") as colnamesctx:
            oj.PD.Subsection(heading_text="Column Names (Inferred)",
                             content=build_ui_colnames()
                             )
        with oj.uictx("gencsvcfg") as gencsvcfgctx:
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
