import bimpy


class LoggingWindow(object):
    def __init__(self):
        self._distance = 10.0

        self._logging_info = []
    
    def render(self):
        # display_size = bimpy.get_display_size()
        window_pos = bimpy.Vec2(self._distance, self._distance)
        window_pos_pivot = bimpy.Vec2(0.0, 0.0)
        bimpy.set_next_window_pos(window_pos, bimpy.Condition.FirstUseEver, window_pos_pivot)
        bimpy.set_next_window_bg_alpha(0.35)

        flags = bimpy.WindowFlags.NoDecoration \
              | bimpy.WindowFlags.AlwaysAutoResize \
              | bimpy.WindowFlags.NoSavedSettings \
              | bimpy.WindowFlags.NoFocusOnAppearing \
              | bimpy.WindowFlags.NoFocusOnAppearing \
              | bimpy.WindowFlags.NoNav
        
        if bimpy.begin("logging overlay##logging_tools", flags=flags):
            if bimpy.is_mouse_pos_valid(None):
                mouse_pos = bimpy.get_mouse_pos()
                bimpy.text("Mouse Pos: ({:.1f},{:.1f})".format(mouse_pos.x, mouse_pos.y))
            else:
                bimpy.text("Mouse Pos: <invalid>")

        bimpy.end()


logging = LoggingWindow()
