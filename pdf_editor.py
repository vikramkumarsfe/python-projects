import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import Scrollbar
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import os

class PDFRedactorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Redactor with Selection Tool")
        self.input_pdf = None
        self.pdf_document = None
        self.page_number = 0
        self.rectangles = {}
        
        self.create_widgets()

    def create_widgets(self):
        # Input file selection
        tk.Button(self.root, text="Open PDF", command=self.browse_input_file).pack(pady=10)

        # Scrollbars
        self.h_scroll = Scrollbar(self.root, orient='horizontal')
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scroll = Scrollbar(self.root, orient='vertical')
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas for PDF display
        self.canvas = tk.Canvas(self.root, cursor="cross", xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)
        self.canvas.pack(expand=True, fill="both")
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.h_scroll.config(command=self.canvas.xview)
        self.v_scroll.config(command=self.canvas.yview)

        # Navigation buttons
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(pady=10)
        tk.Button(nav_frame, text="Previous Page", command=self.prev_page).pack(side="left", padx=5)
        tk.Button(nav_frame, text="Next Page", command=self.next_page).pack(side="left", padx=5)

        # Redact button
        tk.Button(self.root, text="Redact Selected Areas", command=self.redact_areas).pack(pady=10)

    def browse_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.input_pdf = file_path
            self.load_pdf()

    def load_pdf(self):
        self.pdf_document = fitz.open(self.input_pdf)
        self.page_number = 0
        self.rectangles = {}
        self.display_page()

    def display_page(self):
        if not self.pdf_document:
            return

        page = self.pdf_document[self.page_number]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        self.canvas.config(scrollregion=(0, 0, pix.width, pix.height))

        # Draw existing rectangles for the current page
        self.canvas.delete("rect")
        for rect in self.rectangles.get(self.page_number, []):
            self.canvas.create_rectangle(rect, outline='red', tags="rect")

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = None

    def on_move_press(self, event):
        cur_x, cur_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)
        else:
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, cur_x, cur_y, outline='red', tags="rect")

    def on_button_release(self, event):
        end_x, end_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        rect = (self.start_x, self.start_y, end_x, end_y)
        if self.page_number not in self.rectangles:
            self.rectangles[self.page_number] = []
        self.rectangles[self.page_number].append(rect)

    def prev_page(self):
        if self.pdf_document and self.page_number > 0:
            self.page_number -= 1
            self.display_page()

    def next_page(self):
        if self.pdf_document and self.page_number < len(self.pdf_document) - 1:
            self.page_number += 1
            self.display_page()

    def redact_areas(self):
        if not self.pdf_document:
            return

        for page_number in range(len(self.pdf_document)):
            page = self.pdf_document[page_number]
            for rect in self.rectangles.get(page_number, []):
                x0, y0, x1, y1 = rect
                redact_rect = fitz.Rect(x0, y0, x1, y1)
                page.add_redact_annot(redact_rect, fill=(1, 1, 1))  # Fill with white
            page.apply_redactions()

        # Create output file path
        input_dir = os.path.dirname(self.input_pdf)
        input_filename = os.path.basename(self.input_pdf)
        output_filename = f"redacted_{input_filename}"
        output_path = os.path.join(input_dir, output_filename)

        self.pdf_document.save(output_path)
        messagebox.showinfo("Success", f"Redaction applied and saved as '{output_path}'")

# Set up the main application window
root = tk.Tk()
app = PDFRedactorApp(root)
root.mainloop()
