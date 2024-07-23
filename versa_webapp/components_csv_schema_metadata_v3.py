import ofjustpy as oj

from py_tailwind_utils import *

from addict_tracking_changes import Dict
import macropy.activate
from .helpers import build_btn, build_kv_record
from . import background_sty
from hyperui_plugin.tables import Simple as SimpleTable
import ofjustpy_react as ojr

def on_alt_colname_inp(dbref, msg, to_ms):
    pass

def on_coltype_select(dbref, msg, to_ms):
    pass


def build_ui_stats(metadata_report):

    delimiter = build_kv_record("delimiter",
                                "delimiter",
                                metadata_report.delimiter_name
                            )
    numcols = build_kv_record("numcols",
                              "#cols", len(
                                  metadata_report.cols_type)
                              )
    numheaderlines = build_kv_record("numheaderlines", "#headers",
                                     metadata_report.num_header_lines,
                                     # readonly=False #TODO
                                     )
    numrecords = build_kv_record("numrecords", "#records",
                                 metadata_report.num_data_lines)

    return oj.PD.StackV(childs=[delimiter,
                                 numcols,
                                 numheaderlines,
                                 numrecords
            ])


def build_ui_samples(metadata_report):
    sample_table = SimpleTable()
    for row_data in metadata_report.csv_samples:
        _row = sample_table.add_row()
        for cell_data in row_data:
            _row.add_cell(cell_data)

    return sample_table

def build_ui_colnames(metadata_report):
    def cgens():
        for col_pos, col_names in enumerate(metadata_report.header_candidates):
            def items():
                yield oj.WithBanner(f"Column {col_pos}:",
                                               oj.AD.Select(key=f"selector_{col_pos}",
                                                            value=col_names[0],
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
                yield oj.PD.StackH(childs = [ oj.AD.CheckboxInput(key=f"use_oname_{col_pos}cbox"),
                                              oj.WithBanner(f"Alt Name: ",
                                                            
                                                           oj.AD.TextInput(key=f"use_oname_{col_pos}inp",
                                                                           value=None,
                                                                           placeholder="alt name",
                                                                           on_change=on_alt_colname_inp,
                                                                           twsty_tags=[shadow.inner, boxshadow/gray/"400/50", pd/1]
                                                                           ),
                                                            twsty_tags=[ai.center, space/x/1]
                                                           
                                                 )
                                              ],
                                    twsty_tags=[ai.center, space/x/1, bg/gray/100, pd/1, mr/st/1]
                                    )
                yield oj.PD.StackH(childs =[oj.AD.CheckboxInput(key=f"is_pk_{col_pos}cbox", checked=False),
                                            oj.PC.Span(text="is primary key",
                                                       twsty_tags=[shadow.inner, boxshadow/gray/"400/50", pd/1])
                                            ],
                                    twsty_tags=[ai.center, space/x/1, bg/gray/100, pd/1, mr/st/1]
                                   )

                yield oj.PD.StackH(childs =[oj.AD.CheckboxInput(key=f"has_hn_{col_pos}cbox", checked=False),
                                            oj.PC.Span(text="has nulls",
                                                       twsty_tags=[shadow.inner, boxshadow/gray/"400/50", pd/1])
                                            ],
                                    twsty_tags=[ai.center, space/x/1, bg/gray/100, pd/1, mr/st/1]
                                   )                

            yield oj.PD.StackV(childs=[_ for _ in items()], twsty_tags=[space/y/2])

    return oj.PD.StackW(
                                childs=[_ for _ in cgens()],
        twsty_tags = [space/x/4, bg/pink/100, bd/pink/100, bd/st/transparent, bd/sb/green/500, pd/1, mr/1]
                                )
        
    pass



def build_ui_gencsvcfg(metadata_report):
    return oj.WithBanner("Provide a name/label for csv data:",
                         oj.AC.TextInput(key="model_name_inp",
                                         value="dummy_model", 
                                         placeholder="nameme"),
                         twsty_tags=[space/x/1, bg/gray/100, pd/1, mr/st/1, ai.center]
                         )

def build_ui_coltypes(metadata_report):
    return oj.PD.StackW(childs = [oj.WithBanner(f"Column {col_pos}",
                                         oj.AD.Select(key=f"selector_{col_pos}",
                                                      childs = [
                                                          oj.PC.Option(text=col_type, value=col_type, selected="selected"),
                                                                    oj.PC.Option(text='string',
                                                                                 value='string'
                                                                                 )
                                                                ],
                                                      twsty_tags=[W/28, pd/sl/2, shadow.inner, boxshadow/gray/"300/50"], 
                                                      on_click = on_coltype_select,
                                                      value = col_type
                                                      
                                                      ),
                                                twsty_tags=[space/x/1, bg/gray/100, pd/1, mr/st/1, ai.center]
                                         
                                                )


                                  for col_pos, col_type in enumerate(metadata_report.cols_type)
                                  ],
                        twsty_tags = [space/x/4, bg/pink/100, bd/pink/100, bd/st/transparent, bd/sb/green/500, pd/1, mr/1]
                        )
def on_select(dbref, msg, to_ms):
    pass



# #@ojr.CfgLoopRunner
# def on_form_submit(dbref, msg):
#     print("calling on form submit")
#     res = Dict()  # collect all the results
#     res.cols_type = [coltypesctx[f"selector_{idx}"].target.value
#      for idx, _ in enumerate(appstate.metadata_report.cols_type)]

#     # # TODO: cbox toplevel component is a Label 
#     # # we need to design this better to get checked value
#     res.pks = [colnamesctx[f"is_pk_{idx}cbox"].target.checked for idx, _ in enumerate(
#          appstate.metadata_report.cols_type)]

#     res.hasnulls = [colnamesctx[f"is_hn_{idx}cbox"].target.checked for idx, _ in enumerate(
#         appstate.metadata_report.cols_type)]
#     res.cols_name = [colnamesctx[f"selector_{idx}"].target.value for idx, _ in enumerate(
#         appstate.metadata_report.cols_type)]

#     for idx, _ in enumerate(appstate.metadata_report.cols_type):
#         if colnamesctx[f"oname_{idx}cbox"].target.checked and _ctx.colnames[f"oname_{idx}inp"].target.value.strip() != "":
#             res.cols_name[idx] = colnamesctx[f"oname_{idx}inp"].target.value

#     res.csv_datamodel_label = gencsvcfgctx.btninput.target.value
#     res.freeze()
#     return "/gencsvcfg_panel",  ojr.OpaqueDict(res)
            
def build_components(metadata_report):
    with oj.TwStyCtx(background_sty):

        with oj.uictx("stats"):
            stats_box = oj.PD.Details(classes="group", extra_classes="[&_summary::-webkit-details-marker]:hidden",
                          childs = [oj.PD.Summary(classes="flex cursor-pointer items-center justify-between gap-1.5 bg-slate-100 p-4 text-gray-900 rounded-t-lg",
                                                  childs=[oj.PD.Div(childs=[oj.PC.H2(text="Stats")],
                                                                    twsty_tags=[flx.one, db.f, jc.center]
                                                                    ),
                                                          oj.icons.FontAwesomeIcon(label="faPlus",
                                                                                   classes="w-5 h-5"
                                                                                   )

                                                          ]
                                                  ),
                                    build_ui_stats(metadata_report)
                                    

                              ]
                          )
            # stats_box = oj.PD.Subsection(heading_text="Stats",
            #                  content = build_ui_stats(metadata_report),
            #                  )

        with oj.uictx("samples"):

            samples_box = oj.PD.Details(classes="group", extra_classes="[&_summary::-webkit-details-marker]:hidden",
                          childs = [oj.PD.Summary(classes="flex cursor-pointer items-center justify-between gap-1.5 bg-slate-100 p-4 text-gray-900 rounded-t-lg",
                                                  childs=[oj.PD.Div(childs=[oj.PC.H2(text="Row Samples")],
                                                                    twsty_tags=[flx.one, db.f, jc.center]
                                                                    ),
                                                          oj.icons.FontAwesomeIcon(label="faPlus",
                                                                                   classes="w-5 h-5"
                                                                                   )

                                                          ]
                                                  ),
                                    build_ui_samples(metadata_report)
                                    

                              ]
                          )
       
            # samples_box = oj.PD.Subsection(heading_text="Row Samples",
            #                                content=build_ui_samples(metadata_report)

            #                                )
        with oj.uictx("coltypes") as coltypesctx:
            coltypes_box = oj.PD.Subsection(heading_text="Column Types (Inferred)",
                               content = build_ui_coltypes(metadata_report)
                             )

            pass
        with oj.uictx("colnames") as colnamesctx:
            colnames_box = oj.PD.Subsection(heading_text="Column Names (Inferred)",
                             content=build_ui_colnames(metadata_report)
                             )
            pass
        with oj.uictx("gencsvcfg") as gencsvcfgctx:
            gencsvcfg_box = oj.PD.Subsection(heading_text="Build CSV config file",
                             content= build_ui_gencsvcfg(metadata_report)
                             )
            
            pass

        # wrap everything within one giant form
        @ojr.CfgLoopRunner
        def on_form_submit(dbref, msg, to_ms):
            appstate = msg.page.session_manager.appstate
            res = Dict()  # collect all the results
            res.cols_type = [dbref.get_comp_value(msg.page, coltypesctx[f"selector_{idx}"].id)
                             for idx, _ in enumerate(appstate.metadata_report.cols_type)
                         ]
            res.pks = [dbref.get_comp_value(msg.page, colnamesctx[f"is_pk_{idx}cbox"].id)
                       for idx, _ in enumerate(appstate.metadata_report.cols_type)
                       ]

            res.hasnulls = [dbref.get_comp_value(msg.page, colnamesctx[f"has_hn_{idx}cbox"].id)
                       for idx, _ in enumerate(appstate.metadata_report.cols_type)
                       ]
            res.cols_name = [dbref.get_comp_value(msg.page, colnamesctx[f"selector_{idx}"].id)
                             for idx, _ in enumerate(appstate.metadata_report.cols_type)
                             ]
            for idx, _ in enumerate(appstate.metadata_report.cols_type):
                if dbref.get_comp_value(msg.page,
                                        colnamesctx[f"use_oname_{idx}cbox"].id) and dbref.get_comp_value(msg.page,
                                                                                                         colnamesctx[f"use_oname_{col_pos}inp"]).strip() != "":
                    res.cols_name[idx] = dbref.get_comp_value(msg.page,
                                                              colnamesctx[f"use_oname_{idx}inp"].id)


    

            res.csv_datamodel_label = dbref.get_comp_value(msg.page,
                                                           gencsvcfgctx.model_name_inp.id
                                                           )
            res.freeze()

            return "/csv_schema_metadata/gencsvcfg_panel",  res
        #return "/csv_schema_metadata/gencsvcfg_panel",  res


        
        form_box = oj.AD.Form(key="gencsvcfg_form",
                   childs =[stats_box,
                            samples_box,
                            coltypes_box,
                            colnames_box,
                            gencsvcfg_box,
                            build_btn("submit", "Submit")
                            ],
                              on_submit = on_form_submit, 
                   twsty_tags=[noop/container, mr/x/auto, space/y/2

                               ]
                   )
        
        

    return form_box #stats_box, samples_box, coltypes_box, colnames_box, gencsvcfg_box
