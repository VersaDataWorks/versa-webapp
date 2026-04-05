import logging
import os
if os:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)


from addict import Dict
import kavya as kv
import kavya_react as kvr
from kavya_components import StackD

# from aenum import extend_enum, Enum
# from .model_backend_actions import GEN_EDCFG_FILE, EDCFG_DL_NEW, EDCFG_DL_APPEND
# extend_enum(wf.ReactTag_ModelUpdate, "GEN_EDCFG_FILE", GEN_EDCFG_FILE)
# extend_enum(wf.ReactTag_Backend,  "EDCFG_DL_NEW", EDCFG_DL_NEW)
# extend_enum(wf.ReactTag_Backend,  "EDCFG_DL_APPEND", EDCFG_DL_APPEND)


with kv.uictx("save_csvpack") as save_csvpack_ctx:
    async def eh_toggle_localdl(dbref, msg, wp, request):
        '''
            going from key to FQN
            self.value is the key
        '''
        assert False
        print("eh_toggle_localdl called")

        print("deck via stubStore = ", msg.page.session_manager.stubStore.save_csvpack.savecfg_deck.target)

        deck_ms = to_ms(save_csvpack_ctx["savecfg_deck"])
        print("the deck ", deck_ms, " ", dbref.value)
        deck_ms.bring_to_front(dbref.value)
        
        # dbref_savecfgPanels.bring_to_front(
        #     self.value)  # TODO: not entirely correct
        # logger.debug("bring {_ctx[msg.value].panel.spath} to front")
        #save_csvpack_ctx.deck.target.bring_to_front(save_csvpack_ctx[msg.value].panel.spath)
        pass
    with kv.uictx("dl") as dlctx:
        dl_btn = kv.AD.Button(key="dlbtn",
                              value="/save_csvpack/dl/save_dl_panel",
                              text="on csvpack dl",
                              on_click = eh_toggle_localdl
                              )
        ti_newcfg = kv.AD.TextInput(key="ti_newcfg",
                                    value = "newcfg.cfg",
                                    placeholder = "newpack.cfg",
                                    
                                    )
        or_sep = kv.PC.Span(text="or")
        dlsearchbar = kv.PC.Span(text="make a mediawiki/search bar")
        @kvr.ReactDomino
        async def eh_submit_btn(dbref, msg, wp, request):
            '''
            scd : savecfgdl
            '''
            print("eh_submit_btn called: dl")
            # existingcfg = None  # grab from progrssivesearchbar
            #value_newcfg = dlctx.ti_newcfg.target.value.strip()
            #TODO: get value
            value_newcfg = False
            return [("/save_csvpack/dl/savecfgas", value_newcfg)]


        submit_btn = kv.AD.Button(key="submit",
                     text="submit",
                     value="Submit",
                     on_click = eh_submit_btn
                     )

        save_dl_panel = kv.MD.StackV(key="save_dl_panel", childs=[ti_newcfg,
                                    or_sep,
                                    dlsearchbar,
                                    submit_btn]
                             )
    with kv.uictx("local") as localctx:
        local_btn = kv.AD.Button(key="local_btn",
                                 value="/save_csvpack/local/save_local_panel",
                                 text="save to local csvpack", 
                                 on_click = eh_toggle_localdl
                     )
        newcfg_ti = kv.AD.TextInput(key="newcfg",
                                   text="create new",
                                   placeholder="newpack.cfg")
        or_sep = kv.PC.Span(text="or")
        
        existingcfg_ti = kv.AC.TextInput(key="existingcfg",
                                       text="append to existing",
                                         placeholder = "overwrite existing cfg",
                                         
                                       type="file"
                                       )

        @kvr.ReactDomino
        async def eh_submitbtn_click(self, msg, wp, request):
            '''

            '''
            # TODO:
            print("eh_submit_btn called: local")
            # value_newcfg = _ictx.newcfg.target.getInputValue().strip()
            # value_existingcfg = _ictx.existingcfg.target.getInputValue().strip()
            # rts = wf.TaskStack()
            # print("IN LOCAL SUBMIT")
            # rts.addTask(wf.ReactTag_ModelUpdate.GEN_EDCFG_FILE, Dict({'savecfgas':
            #                                                           value_newcfg}))
            # # TODO: handle edcfg local append
            # rts.addTask(wf.ReactTag_UI.EDCFG_LOCAL_NEW, None)

            # return msg.page, rts
            return  [("/save_csv_metadatacfg/local", "newcfg.cfg")]

        submit_btn = kv.AD.Button(key="submit",
                                  value="submit",
                                  text="Submit",
                                  on_click = eh_submitbtn_click
                                  )

        save_local_panel  = kv.MD.StackV(key="save_local_panel", 
                              childs=[newcfg_ti,
                                     or_sep,
                                     existingcfg_ti,
                                     submit_btn]
                              )  # move to dc.Stackv.stackv_

    savecfg_deck = StackD(key="savecfg_deck",
                      childs = [save_dl_panel,
                                save_local_panel
                                ],
                      )

    panelToggler =kv.PD.Halign(kv.PD.StackH(childs=[local_btn,
                                                 dl_btn]
                                         )
                            )

    savecfg_panel = kv.MD.TitledPara(heading_text="Save CSV metadata and config",
                                     childs= [kv.HM.StackV(childs=[panelToggler,
                                                                           savecfg_deck
                                                                           ]
                                                                   )
                                              ],
                                     key="savecfg_panel"
                                     )
    title = kv.PD.Title(title_text="Build and save CSV datapack config")
        
    
