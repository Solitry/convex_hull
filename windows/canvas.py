import bimpy

from common.utils import im_col32
from common.value_type import Line, Point

from .convex_draw_component import ConvexDrawComponent
from .lines_draw_component import LinesDrawComponent
from .user_line_draw_component import UserLineDrawComponent
from .user_convex_draw_component import UserConvexDrawComponet


class CanvasWindow(object):
    def __init__(self):
        self.convex_draw_component = ConvexDrawComponent()
        self.lines_draw_component = LinesDrawComponent()
        self.user_line_draw_component = UserLineDrawComponent()
        self.user_convex_draw_component = UserConvexDrawComponet()

        # self.convex_draw_component.set_convex_points([
        #     Point(0.2, 0.1),
        #     Point(0.6, 0.6),
        #     Point(-0.1, 0.5),
        # ])

        # self.lines_draw_component.set_lines([
        #     Line(1, 1, -1),
        #     Line(1, 1, -1.05),
        # ])

        self._canvas_scale_ratio = 2
        self._canvas_scale_ratio_delta = 0.5
        self._canvas_scale_ratio_min = 1
        self._canvas_scale_ratio_max = 20

        self._drawing_start = False

    def render(self):
        bimpy.set_next_window_pos(bimpy.Vec2(40, 30), bimpy.Condition.FirstUseEver)
        bimpy.set_next_window_size(bimpy.Vec2(681, 700), bimpy.Condition.FirstUseEver)

        if not bimpy.begin('canvas window##canvas'):
            bimpy.end()
            return
        
        if not bimpy.begin_child('canvas##canvas', border=False):
            bimpy.end_child()
            return
        
        canvas_pos = bimpy.get_cursor_screen_pos()
        canvas_size = bimpy.get_content_region_avail()

        bimpy.invisible_button('canvas button##canvas', canvas_size)

        # mouse wheel scroll zoom
        if bimpy.is_item_hovered():
            mouse_wheel_delta = bimpy.get_mouse_wheel_delta()
            if mouse_wheel_delta < 0:
                self._canvas_scale_ratio = min(self._canvas_scale_ratio + self._canvas_scale_ratio_delta,
                                               self._canvas_scale_ratio_max)
            if mouse_wheel_delta > 0:
                self._canvas_scale_ratio = max(self._canvas_scale_ratio - self._canvas_scale_ratio_delta,
                                               self._canvas_scale_ratio_min)

        shift_ratio = 0.5 * (self._canvas_scale_ratio - 1) / self._canvas_scale_ratio
        origin = bimpy.Vec2(
            canvas_pos.x + canvas_size.x * shift_ratio,
            canvas_pos.y + canvas_size.y * (1 - shift_ratio)
        )
        scale = min(canvas_size.x, canvas_size.y) / self._canvas_scale_ratio

        mouse_pos = bimpy.get_mouse_pos()
        relative_pos = Point(
            (mouse_pos.x - origin.x) / scale,
            (mouse_pos.y - origin.y) / -scale,
        )

        # user line draw
        if self.user_line_draw_component.if_is_drawing():
            # print('is_drawing')
            if bimpy.is_item_hovered():
                if not self._drawing_start and bimpy.is_mouse_clicked(0, False):
                    self._drawing_start = True
                    self.user_line_draw_component.set_drawing_start_point(relative_pos)

            if self._drawing_start:
                mouse_down = bimpy.is_mouse_down(0)
                self._drawing_start = mouse_down
                self.user_line_draw_component.set_drawing_end_point(relative_pos, not mouse_down)
        
        # user convex draw
        if self.user_convex_draw_component.if_is_drawing():
            if bimpy.is_item_hovered():
                if bimpy.is_mouse_double_clicked(0):
                    self.user_convex_draw_component.set_user_done()
                elif bimpy.is_mouse_clicked(0, False):
                    self.user_convex_draw_component.set_user_add_point(relative_pos)                
                
                if bimpy.is_mouse_double_clicked(1):
                    self.user_convex_draw_component.set_user_cancel()
                elif bimpy.is_mouse_clicked(1, False):
                    self.user_convex_draw_component.set_user_pop_point()
        
        # draw background
        bimpy.add_rect_filled(
            canvas_pos,
            bimpy.Vec2(canvas_pos.x + canvas_size.x, canvas_size.y + canvas_size.y),
            im_col32(200, 200, 200),
        )

        bimpy.add_rect(
            bimpy.Vec2(origin.x, -scale + origin.y),
            bimpy.Vec2(scale + origin.x, origin.y),
            im_col32(0, 0, 0),
        )

        # draw others
        if self.user_convex_draw_component.if_is_drawing():
            self.user_convex_draw_component.render(origin, scale)
        else:
            self.convex_draw_component.render(origin, scale)

        self.lines_draw_component.render(origin, scale)

        self.user_line_draw_component.render(origin, scale)

        # show mouse pos
        if bimpy.is_mouse_pos_valid(None) and bimpy.is_item_hovered():
            bimpy.add_text_simple(
                bimpy.Vec2(canvas_pos.x + 15, canvas_pos.y + 10),
                im_col32(0, 0, 0),
                'x: {:.6f}  y: {:.6f}'.format(relative_pos.x, relative_pos.y),
            )
        
        # show drawing state
        if self.user_line_draw_component.if_is_drawing():
            bimpy.add_text_simple(
                bimpy.Vec2(canvas_pos.x + 15, canvas_pos.y + 30),
                im_col32(0, 0, 0),
                'drawing line {}'.format(self.user_line_draw_component.get_waitting_draw_line_index()),
            )

        bimpy.end_child()
        bimpy.end()

    def close(self):
        pass
