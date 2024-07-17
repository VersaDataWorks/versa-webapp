"""
describes all components (nav-bar, footer,  etc) that form the pieces of a webpage on the wiki 
"""



import logging
import os
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
  
import justpy as jp
import ofjustpy as oj
from tailwind_tags import fw, fc, fz, gray, pd, y, ji, jc, text, mr, sb, ppos, bottom, container, H, screen, db, flx

top_level_nav = oj.PC.StackH(childs = [oj.PC.Span(text="Navigation",
                                                     twsty_tags=[fw.bold]
                                                     ), 
                                          oj.PC.A(href="#",
                                                  text="History"),
                                          oj.PC.A(href="#",
                                                  text="My account"),
                                          oj.PC.A(href="#",
                                                  text="Catalog"
                                                  ),
                                          oj.PC.A(href="#",
                                                  text="Public CSV"
                                                  )
                                       ]
                             )

top_panel = oj.PC.StackH(childs = [oj.PC.A(href="#",
                                      text="CSV Schema Builder"
                                      ),
                              top_level_nav

                              ],
                    twsty_tags=[pd/y/4, ji.center, jc.between]
                    )

# ============================== footer ==============================


# linkout = oj.PC.Subsection("",
#                            oj.PC.StackG(childs = [oj.PC.A(text="")

#                                ]

#                                )
#     )

# footer = oj.PC.Footer(childs = [oj.PC.Divider(twsty_tags=[mr/sb/4]
#                                               ),
                                
#                                 oj.PC.StackH(childs = [about,
#                                                        linkout

#                                     ]
#                                     )

#                                 ]
#                       )

# ================================ end ===============================
def page_builder(page_key, childs=[], rendering_type="CSR", **kwargs):
    tlc = oj.PC.Container(cgens= [,
                                  oj.PC.StackV(childs=childs),
                                  tlctx.footer.panel], pcp=[H/screen, db.f, flx.col])
    pass

    
# def page_builder(page_key, title, builder_pagebody, **kwargs):
#     def view_function(request):
#         session_manager = oj.get_session_manager(request.session_id)
#         stubStore = session_manager.stubStore
#         with oj.sessionctx(session_manager):
#             with session_manager.uictx("tlctx") as tlctx:
#                 _ictx = tlctx
#                 render_nav_bar(session_manager)
#                 builder_pagebody(session_manager)
#                 render_footer(session_manager)
#                 oj.Container_("tlc", cgens= [tlctx.topper.panel, _ictx.body.panel, tlctx.footer.panel], pcp=[H/screen, db.f, flx.col])
#                 wp_ = oj.WebPage_(page_key, cgens = [_ictx.tlc], title=title, session_manager = session_manager,  **kwargs)

#                 wp = wp_()
#         wp.session_manager = session_manager
#         return wp
#     return view_function


# def render_nav_bar(session_manager):
#     with session_manager.uictx("topper") as navbarCtx:
#         _ctx = navbarCtx
#         # a box placed at the  right end
#         top_level_nav_ = oj.StackH_("anchors",
#                                               cgens = [
#                                                   oj.Span_("navtitle", text="Navigation", pcp=[fw.bold]), 
#                                                   oj.A_("history", href="#", text="History"),
#                                                   oj.A_("index", href="#", text="My account"),
#                                                   oj.A_("tags", href="#", text="Catalog"),
#                                                   oj.A_("user", href="#", text="Public CSV"),
#                                               ]
#                                                )
        
        
#         # page_trail_  = oj.StackH_("pagetrail",
#         #                                       cgens = [
#         #                                           oj.Span_("title", text="Page Trail", pcp =[fw.bold])
#         #                                       ]
#         #                                        )

#         # item_nav_  = oj.StackH_("itemviews",
#         #                                       cgens = [
#         #                                           oj.Span_("itemview", text="Item views", pcp=[fw.bold]),
#         #                                           oj.A_("show", href="#", text="modify"),
#         #                                           oj.A_("history", href="#", text="history"),
#         #                                           oj.A_("Download", href="#", text="download"),
#         #                                           oj.A_("delete", href="#", text="delete"),
#         #                                           oj.A_("subitems", href="#", text="subitems"),
#         #                                           oj.A_("discussion", href="#", text="discussion"),
#         #                                           oj.A_("rename", href="#", text="rename"),
#         #                                           oj.A_("highlight", href="#", text="highlight"),
#         #                                           oj.A_("meta", href="#", text="Meta"),
#         #                                           oj.A_("sitemap", href="#", text="Site Map"),
#         #                                           oj.A_("similar", href="#", text="Similar")
#         #                                       ]
#         #                                        )        
        
#         navpanel_ = oj.Halign_(oj.StackV_("navpanel",
#                                           cgens = [top_level_nav_]),
#                                "end")
        

#         #oj.Halign_(oj.Span_("dummySpan", text="i am a dummy span", pcp=[bg/pink/2])),
#         cgens = [
#             oj.A_("HomeAnchor", pcp=[fc/gray/9, fz.xl, fw.extrabold],
#                   href="#", text="CSV Schema Builder"),

#              navpanel_
#         ]
#         abox_ = oj.StackH_("abox", cgens = cgens, pcp=[pd/y/4,  ji.center, jc.between])
#         oj.Nav_("panel", cgens=[abox_])

        
# def render_footer(session_manager):
#     with session_manager.uictx("footer") as footerbodyCtx:
#         _ictx = footerbodyCtx
#         oj.Prose_("aboutcontent",
#                   text= "CSV schema builder", pcp=[fz.sm, text/gray/600, pd/y/2])

#         oj.Subsection_("about", "About", _ictx.aboutcontent)

#         oj.StackG_("linkouthref", num_cols=3, cgens = [
#             oj.A_("pypower", text="Developed by Monal Webworks", href="#"), 
#             oj.A_("Licensed", text="GPL Licensed", href="#"),
#             oj.A_("ShreeLabs", text="Shree Labs Inc.", href="#")
            
#         ])
#         oj.Subsection_("linkout", "", _ictx.linkouthref)
        
#         oj.Footer_("panel", cgens=[oj.Divider_("bodyFooterDivider", pcp=[mr/sb/4]),
#                                     oj.StackH_("boxcontainer", cgens= [_ictx.about, _ictx.linkout]
#                                         )
#                                     ]
                   
#                    )


        
