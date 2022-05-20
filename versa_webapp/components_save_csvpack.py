import logging
import os
if os:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)


from addict import Dict
import ofjustpy as oj
import ofjustpy_react as ojr
# from aenum import extend_enum, Enum
# from .model_backend_actions import GEN_EDCFG_FILE, EDCFG_DL_NEW, EDCFG_DL_APPEND
# extend_enum(wf.ReactTag_ModelUpdate, "GEN_EDCFG_FILE", GEN_EDCFG_FILE)
# extend_enum(wf.ReactTag_Backend,  "EDCFG_DL_NEW", EDCFG_DL_NEW)
# extend_enum(wf.ReactTag_Backend,  "EDCFG_DL_APPEND", EDCFG_DL_APPEND)

def build_components(session_manager):
    stubStore = session_manager.stubStore
    
    with session_manager.uictx("save_csvpack") as save_csvpack_ctx:
        def eh_toggle_localdl(self, msg):
            '''
            going from key to FQN
            self.value is the key
            '''
            print("eh_toggle_localdl called")
            # dbref_savecfgPanels.bring_to_front(
            #     self.value)  # TODO: not entirely correct
            # logger.debug("bring {_ctx[msg.value].panel.spath} to front")
            save_csvpack_ctx.deck.target.bring_to_front(save_csvpack_ctx[msg.value].panel.spath)
            pass
        with session_manager.uictx("dl") as dlctx:
            # build dlpanel
            _ictx = dlctx
            oj.Button_("btn", value="dl", text="on csvpack dl").event_handle(
                oj.click, eh_toggle_localdl
            )
            oj.InputChangeOnly_(
                "ti_newcfg", text="new cfg", placeholder="new_pck.cfg")
            or_sep = oj.Span_("or_sep", text="or")
            # dlsearchbar_ = dbr.dlsearchbar_db('progressivesearchbar')
            # will try MoinMoin
            dlsearchbar_ = oj.Span_("searchbar", text="make a mediawiki/search bar")

            @ojr.CfgLoopRunner
            def eh_submit_btn(self, msg):
                '''
                scd : savecfgdl
                '''
                print("eh_submit_btn called: dl")
                # existingcfg = None  # grab from progrssivesearchbar
                value_newcfg = dlctx.ti_newcfg.target.value.strip()
                return "/save_csvpack/dl/savecfgas", value_newcfg


            oj.Button_(
                "submit", text="submit", value="Submit").event_handle(oj.click, eh_submit_btn)

            oj.StackV_("panel", cgens=[_ictx.ti_newcfg,
                                 or_sep, _ictx.searchbar, _ictx.submit])

        with session_manager.uictx("local") as localctx:
            _ictx = localctx
            oj.Button_("btn", value="local", text="save to local csvpack").event_handle(oj.click, eh_toggle_localdl)
            oj.InputChangeOnly_(
                "newcfg", text="create new", placeholder="newpack.cfg")
            oj.Span_("or_sep", text="or")
            oj.Input_(
                "existingcfg", text="append to existing", type="file")

            #ojr.CfgLoopRunner
            def eh_submitbtn_click(self, msg):
                '''

                '''
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

            oj.Button_("submit", value="submit", text="Submit").event_handle(oj.click, eh_submitbtn_click
                       )

            oj.StackV_("panel", cgens=[_ictx.newcfg,
                                 _ictx.or_sep, _ictx.existingcfg, _ictx.submit])  # move to dc.Stackv.stackv_

        oj.StackD_("deck", cgens=[dlctx.panel, localctx.panel])
        panelToggler_ =oj.Halign_(oj.StackH_(
            "panelToggler", cgens=[dlctx.btn, localctx.btn]))

        oj.Subsection_("deckSection", heading_text="Save CSV metadata and config",
                       content_= oj.StackH_("panel", cgens=[panelToggler_, save_csvpack_ctx.deck]))
        oj.Halign_(oj.Title_("title", title_text="Build and save CSV datapack config"))
        
