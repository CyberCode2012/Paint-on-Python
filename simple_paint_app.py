import tkinter as tk
from tkinter import colorchooser

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BrushMagic: Your Digital Canvas")

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.grid(row=0, column=0, columnspan=4, rowspan=3, sticky="nsew")

        self.brush_size = 2
        self.draw_status = False
        self.last_x = 0
        self.last_y = 0
        self.color = "black"
        self.last_selected_color = self.color
        self.shape = "line"  # Default shape is line

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        # Brush size control and shape changer at the bottom
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.grid(row=3, column=0, columnspan=4, pady=10, sticky="nsew")

        self.brush_size_label = tk.Label(self.bottom_frame, text="Brush Size:")
        self.brush_size_label.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(self.bottom_frame, from_=1, to=30, orient=tk.HORIZONTAL, command=self.change_brush_size)
        self.brush_size_scale.set(self.brush_size)
        self.brush_size_scale.pack(side=tk.LEFT)

        self.shape_label = tk.Label(self.bottom_frame, text="Shape:")
        self.shape_label.pack(side=tk.LEFT, padx=(20, 0))

        self.shape_var = tk.StringVar(root)
        self.shape_var.set("Line")
        self.shape_menu = tk.OptionMenu(self.bottom_frame, self.shape_var, "Line", "Rectangle", "Oval", command=self.change_shape)
        self.shape_menu.pack(side=tk.LEFT)

        self.clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
        self.clear_button.grid(row=4, column=0, sticky="ew")

        self.color_button = tk.Button(root, text="Change Color", command=self.change_color)
        self.color_button.grid(row=4, column=1, sticky="ew")

        self.eraser_button = tk.Button(root, text="Eraser", command=self.use_eraser)
        self.eraser_button.grid(row=4, column=2, sticky="ew")

        self.draw_button = tk.Button(root, text="Draw", command=self.use_draw)
        self.draw_button.grid(row=4, column=3, sticky="ew")

    def start_draw(self, event):
        self.last_x = event.x
        self.last_y = event.y
        self.draw_status = True

    def draw(self, event):
        x, y = event.x, event.y
        if self.draw_status:
            if self.shape == "Line":
                self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.color, width=self.brush_size)
            elif self.shape == "Rectangle":
                self.canvas.create_rectangle(self.last_x, self.last_y, x, y, outline=self.color, width=self.brush_size)
            elif self.shape == "Oval":
                self.canvas.create_oval(self.last_x, self.last_y, x, y, outline=self.color, width=self.brush_size)
            else:
                self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.color, width=self.brush_size)
        self.last_x = x
        self.last_y = y

    def stop_draw(self, event):
        self.draw_status = False

    def clear_canvas(self):
        self.canvas.delete("all")

    def change_brush_size(self, new_size):
        self.brush_size = int(new_size)

    def change_color(self):
        color = colorchooser.askcolor(title="Choose a color")
        if color[1]:
            self.color = color[1]
            self.last_selected_color = self.color

    def use_eraser(self):
        self.color = "white"

    def use_draw(self):
        self.color = self.last_selected_color

    def change_shape(self, selected_shape):
        self.shape = selected_shape

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
# TY for watching my project :)
