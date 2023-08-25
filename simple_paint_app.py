import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import ImageGrab, Image, ImageTk


class PaintApp:
    def __init__(self, root):
        self.brush_size = 10  # A more noticeable size
        self.shape = "Oval"   # A more noticeable shape
        self.color = "black"
        self.root = root
        self.root.title("BrushMagic: Your Digital Canvas")

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=4, rowspan=3, sticky="nsew")


        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(root, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=4, rowspan=3, sticky="nsew")

        self.brush_size = 2
        self.draw_status = False
        self.last_x = 0
        self.last_y = 0
        self.color = "black"
        self.last_selected_color = self.color
        self.shape = "line"  # Default shape is line
        self.undo_stack = []
        self.redo_stack = []

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        # Brush size control and shape changer at the bottom
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.grid(row=3, column=0, columnspan=4, pady=10, sticky="nsew")

        self.brush_preview = tk.Canvas(self.bottom_frame, width=50, height=50, bg="white")
        self.brush_preview.pack(side=tk.LEFT, padx=5)
        self.update_brush_preview()

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

        self.clear_button = tk.Button(self.bottom_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.color_button = tk.Button(self.bottom_frame, text="Change Color", command=self.change_color)
        self.color_button.pack(side=tk.LEFT, padx=5)

        self.eraser_button = tk.Button(self.bottom_frame, text="Eraser", command=self.use_eraser)
        self.eraser_button.pack(side=tk.LEFT, padx=5)

        self.draw_button = tk.Button(self.bottom_frame, text="Draw", command=self.use_draw)
        self.draw_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.bottom_frame, text="Save", command=self.save_canvas)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.load_button = tk.Button(self.bottom_frame, text="Load", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.bg_color_button = tk.Button(self.bottom_frame, text="BG Color", command=self.change_bg_color)
        self.bg_color_button.pack(side=tk.LEFT, padx=5)

        self.update_brush_preview()


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
        self.update_brush_preview()

    def change_color(self):
        color = colorchooser.askcolor(title="Choose a color")
        if color[1]:
            self.color = color[1]
            self.last_selected_color = self.color
            self.update_brush_preview()

    def use_eraser(self):
        self.color = "white"

    def use_draw(self):
        self.color = self.last_selected_color

    def change_shape(self, selected_shape):
        self.shape = selected_shape
        self.update_brush_preview()

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            ImageGrab.grab().crop((x, y, x1, y1)).save(file_path, "PNG")
    
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            image = Image.open(file_path)
            # Resize the image to fit the canvas (optional)
            image = image.resize((800, 600), Image.ANTIALIAS)
            self.image_tk = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
    
    def change_bg_color(self):
        color = colorchooser.askcolor(title="Choose a background color")
        if color[1]:
            self.canvas.config(bg=color[1])

    def clear_canvas(self):
        current_bg = self.canvas.cget("bg")
        self.canvas.delete("all")
        self.canvas.config(bg=current_bg)

    def update_brush_preview(self):
        self.brush_preview.delete("all")
        x, y = 25, 25  # Center of the canvas

        if self.shape == "Line":
            self.brush_preview.create_oval(x - self.brush_size/2, y - self.brush_size/2, x + self.brush_size/2, y + self.brush_size/2, fill=self.color)
        elif self.shape == "Rectangle":
            size = self.brush_size * 2
            half_size = size / 2
            self.brush_preview.create_rectangle(x - half_size, y - half_size, x + half_size, y + half_size, outline=self.color, width=self.brush_size)
        elif self.shape == "Oval":
            size = self.brush_size * 2
            half_size = size / 2
            self.brush_preview.create_oval(x - half_size, y - half_size, x + half_size, y + half_size, outline=self.color, width=self.brush_size)
        else:
            self.brush_preview.create_oval(x - self.brush_size/2, y - self.brush_size/2, x + self.brush_size/2, y + self.brush_size/2, fill=self.color)

    def undo(self):
        if self.undo_stack:
            last_image = self.undo_stack.pop()
            self.redo_stack.append(self.canvas.copy())
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=last_image, anchor=tk.NW)

    def redo(self):
        if self.redo_stack:
            last_image = self.redo_stack.pop()
            self.undo_stack.append(self.canvas.copy())
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=last_image, anchor=tk.NW)


if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
# TY for watching my project :)
# Made by CyberCode2012
