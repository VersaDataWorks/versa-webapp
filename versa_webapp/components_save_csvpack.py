import logging
import os
if os:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

import webapp_framework as wf
from addict import Dict
from aenum import extend_enum, Enum
from .model_backend_actions import GEN_EDCFG_FILE, EDCFG_DL_NEW, EDCFG_DL_APPEND
extend_enum(wf.ReactTag_ModelUpdate, "GEN_EDCFG_FILE", GEN_EDCFG_FILE)
extend_enum(wf.ReactTag_Backend,  "EDCFG_DL_NEW", EDCFG_DL_NEW)
extend_enum(wf.ReactTag_Backend,  "EDCFG_DL_APPEND", EDCFG_DL_APPEND)

with wf.uictx("save_csvpack") as _ctx:
    def eh_toggle_localdl(self, msg):
        '''
        going from key to FQN
        self.value is the key
        '''
        # dbref_savecfgPanels.bring_to_front(
        #     self.value)  # TODO: not entirely correct
        logger.debug("bring {_ctx[msg.value].panel.spath} to front")
        _ctx.deck.target.bring_to_front(_ctx[msg.value].panel.spath)
        pass
    with wf.uictx("dl") as dlctx:
        # build dlpanel
        _ictx = dlctx
        wf.Button_("btn", "dl", "on csvpack dl", eh_toggle_localdl,
                   )
        wf.TextInput_(
            "ti_newcfg", "new cfg", "new_pck.cfg")
        or_sep = wf.Span_("or_sep", "or")
        # dlsearchbar_ = dbr.dlsearchbar_db('progressivesearchbar')
        # will try MoinMoin
        dlsearchbar_ = wf.Span_("searchbar", "make a mediawiki/search bar")

        @wf.MRVWLR
        def eh_submit_btn(self, msg):
            '''
            scd : savecfgdl
            '''

            existingcfg = None  # grab from progrssivesearchbar

            value_newcfg = _ictx.ti_newcfg.target.getInputValue().strip()
            # if value_append != '':
            #     uav = Dict()
            #     uav.target_dpcfg = value_append

            #     rts = TaskStack()
            #     rts.addTask(ModelUpdaterTag.EDCFG_APPEND, uav)
            #     rts.addTask(BackendReactActionTag.EDCFG_DL_APPEND, None)
            #     return msg.page, rts

            if value_newcfg != '':
                uav = Dict()
                uav.savecfgas = value_newcfg
                rts = wf.TaskStack()
                rts.addTask(wf.ReactTag_ModelUpdate.GEN_EDCFG_FILE, uav)
                rts.addTask(wf.ReactTag_Backend.EDCFG_DL_NEW,
                            None)
                return msg.page, rts

        wf.Button_(
            "submit", "submit", "Submit", eh_submit_btn)

        wf.StackV_("panel", [_ictx.ti_newcfg,
                             or_sep, _ictx.searchbar, _ictx.submit])

    with wf.uictx("local") as localctx:
        _ictx = localctx
        wf.Button_("btn", "local", "save to local csvpack", eh_toggle_localdl,
                   )
        wf.TextInput_(
            "newcfg", "create new", "newpack.cfg")
        wf.Span_("or_sep", "or")
        wf.FileInput_(
            "existingcfg", "append to existing")

        @wf.MRVWLR
        def eh_submitbtn_click(self, msg):
            '''

            '''
            value_newcfg = _ictx.newcfg.target.getInputValue().strip()
            value_existingcfg = _ictx.existingcfg.target.getInputValue().strip()
            rts = wf.TaskStack()
            print("IN LOCAL SUBMIT")
            rts.addTask(wf.ReactTag_ModelUpdate.GEN_EDCFG_FILE, Dict({'savecfgas':
                                                                      value_newcfg}))
            # TODO: handle edcfg local append
            rts.addTask(wf.ReactTag_UI.EDCFG_LOCAL_NEW, None)

            return msg.page, rts

        wf.Button_("submit", "submit", "Submit", eh_submitbtn_click
                   )

        wf.StackV_("panel", [_ictx.newcfg,
                             _ictx.or_sep, _ictx.existingcfg, _ictx.submit])  # move to dc.Stackv.stackv_

    wf.Decked_("deck", [dlctx.panel, localctx.panel])
    panelToggler_ = wf.Halign_(wf.StackH_(
        "panelToggler", [dlctx.btn, localctx.btn]))

    wf.Subsection_("deckSection", "Save CSV metadata and config",
                   wf.StackH_("panel", [panelToggler_, _ctx.deck]))
    wf.Halign_(wf.TitleBanner_(title="Build and save CSV datapack config"))
