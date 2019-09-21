import bimpy


def help_marker(help_text, highlight=False):
    if highlight:
        bimpy.text('(?)')
    else:
        bimpy.text_disabled('(?)')
    
    if bimpy.is_item_hovered():
        bimpy.begin_tooltip()
        bimpy.text(help_text)
        bimpy.end_tooltip()
