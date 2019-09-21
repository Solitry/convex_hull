import bimpy

# from logging_tool import logging
from windows.dash import DashWindow
from windows.canvas import CanvasWindow


def main():
    ctx = bimpy.Context()
    ctx.init(1200, 800, 'tester')

    dash_window = DashWindow()
    canvas_window = CanvasWindow()

    while not ctx.should_close():
        with ctx:
            # bimpy.show_demo_window()

            dash_window.render()

            # lines data  [dash lines] -> [canvas lines draw]
            canvas_window.lines_draw_component.set_lines(
                dash_window.lines_componnet.get_line_data())

            # highlight line index  [dash lines] -> [canvas lines draw]
            canvas_window.lines_draw_component.set_highlight_line_index(
                dash_window.lines_componnet.get_highlight_line_index())

            # waitting draw line index  [dash lines] -> [canvas lines draw]
            canvas_window.lines_draw_component.set_waitting_draw_line_index(
                dash_window.lines_componnet.get_waitting_draw_line_index())

            # convex points  [dash convex] -> [canvas convex draw]
            canvas_window.convex_draw_component.set_convex_points(
                dash_window.convex_component.get_convex_data())

            # waitting draw line index  [dash lines] -> [canvas user lines draw]
            canvas_window.user_line_draw_component.set_waitting_draw_line_index(
                dash_window.lines_componnet.get_waitting_draw_line_index())
            
            # convex draw [dash convex] -> [canvas user convex draw]
            canvas_window.user_convex_draw_component.set_convex_draw_flag(
                dash_window.convex_component.get_convex_draw_flag())
            
            canvas_window.render()

            # waitting draw line value  [canvas lines draw] -> [dash lines]
            dash_window.lines_componnet.set_waitting_draw_line_value(
                canvas_window.user_line_draw_component.get_waitting_draw_line_value())

            # convex draw [canvas user convex draw] -> [dash convex]
            dash_window.convex_component.set_convex_draw_value(
                canvas_window.user_convex_draw_component.get_convex_draw_value())
            # logging.render()

    dash_window.close()
    canvas_window.close()

if __name__ == '__main__':
    main()
