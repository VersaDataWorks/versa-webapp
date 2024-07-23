from html_writer.macro_module import macros, writer_ctx
import ofjustpy as oj
from py_tailwind_utils import *
from ofjustpy.HC_wrappers import Halign
def build_btn(key, text, **kwargs):
    with writer_ctx:
        with Button(key=key, classes="group relative h-12 inline-block text-sm font-medium text-gray-600 focus:outline-none focus:ring active:text-gray-500", **kwargs) as btn_box:
            with Span(classes="absolute inset-0  bg-gray-600 ", extra_classes="translate-x-0.5 translate-y-0.5 transition-transform group-hover:translate-x-0 group-hover:translate-y-0"):
                pass
            with Span(classes="relative block border border-current bg-white px-8 py-3", text=text):
                pass

    return btn_box


def build_kv_record(key,
                    label,
                    text,
                    component_type="passive",
                    twsty_tags = []
                    ):
    #print (f"Build ui for {key}<===> {label} : ", component.key, " ", component.id, " ", component_type)
    component = oj.PD.Span(text=text,
                           twsty_tags = [W/8]
                           )
    component.add_twsty_tags(fz.sm, fw.normal, fc/slate/800)
    eq = oj.PC.Span(text=":", twsty_tags=[jc.center, fz.sm, fw.normal, fc/slate/800])
    label = oj.PC.Span(text=label , twsty_tags=[ta.end, W/fit, fz.sm, fw.normal, fc/gray/600])
    rec = oj.PD.StackH(key = f"input_row_{key}",
                            childs=[ oj.PD.Valign(label, height_tag=noop/noop, twsty_tags=[W/fit, jc.end]),
                                     oj.PD.Valign(eq,height_tag=noop/noop),
                                     oj.PD.Valign(Halign(component, "start", twsty_tags=[]), height_tag=noop/noop),
                                     #component

                            ],
                    twsty_tags=[W/full, *twsty_tags, pd/st/4, mr/y/2, pd/y/1, space/x/1, mr/x/1, pd/x/1, jc.center, boxtopo.bd, bd/transparent, bd/2, cc/bd/st/slate/400, bd/sl/slate/100, bd/sl/1])


    return rec
