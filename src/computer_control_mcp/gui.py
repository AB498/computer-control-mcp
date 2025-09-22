"""
GUI Test Harness for Computer Control MCP.

This module provides a graphical user interface for testing the Computer Control MCP functionality.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import pyautogui
import json
import io

from computer_control_mcp.core import mcp

class TestHarnessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Computer Control Test Harness")
        self.root.geometry("800x600")
        
        # Create main frame with scrollbar
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create test sections
        self.create_click_test_section()
        self.create_type_text_section()
        self.create_screenshot_section()
        self.create_output_section()
        
        # Initialize test results
        self.test_results = {}
    
    def create_click_test_section(self):
        frame = ttk.LabelFrame(self.main_frame, text="Mouse Click Test")
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Coordinates input
        coord_frame = ttk.Frame(frame)
        coord_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(coord_frame, text="X:").pack(side=tk.LEFT)
        self.x_entry = ttk.Entry(coord_frame, width=10)
        self.x_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(coord_frame, text="Y:").pack(side=tk.LEFT)
        self.y_entry = ttk.Entry(coord_frame, width=10)
        self.y_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame, text="Test Click", command=self.test_click).pack(pady=5)
    
    def create_type_text_section(self):
        frame = ttk.LabelFrame(self.main_frame, text="Type Text Test")
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(frame, text="Text to type:").pack(pady=2)
        self.text_entry = ttk.Entry(frame)
        self.text_entry.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(frame, text="Test Type Text", command=self.test_type_text).pack(pady=5)
    
    def create_screenshot_section(self):
        frame = ttk.LabelFrame(self.main_frame, text="Screenshot Test")
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(frame, text="Take Screenshot", command=self.test_screenshot).pack(pady=5)
        
        # Canvas for screenshot preview
        self.screenshot_canvas = tk.Canvas(frame, width=200, height=150)
        self.screenshot_canvas.pack(pady=5)
    
    def create_output_section(self):
        frame = ttk.LabelFrame(self.main_frame, text="Test Output")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(frame, height=10)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def log_output(self, test_name, request_data, response_data):
        self.output_text.insert(tk.END, f"\n===== TEST: {test_name} =====\n")
        self.output_text.insert(tk.END, f"REQUEST: {json.dumps(request_data, indent=2)}\n")
        self.output_text.insert(tk.END, f"RESPONSE: {response_data}\n")
        self.output_text.insert(tk.END, "======================\n")
        self.output_text.see(tk.END)
    
    def test_click(self):
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            request_data = {"x": x, "y": y}
            result = mcp.click_screen(**request_data)
            self.log_output("click_screen", request_data, result)
        except Exception as e:
            self.log_output("click_screen", request_data, f"Error: {str(e)}")
    
    def test_type_text(self):
        try:
            text = self.text_entry.get()
            request_data = {"text": text}
            result = mcp.type_text(**request_data)
            self.log_output("type_text", request_data, result)
        except Exception as e:
            self.log_output("type_text", request_data, f"Error: {str(e)}")
    
    def test_screenshot(self):
        try:
            result = mcp.take_screenshot()
            # Convert bytes to image for preview
            image = Image.open(io.BytesIO(result.data))
            # Resize for preview
            image.thumbnail((200, 150))
            photo = ImageTk.PhotoImage(image)
            self.screenshot_canvas.create_image(100, 75, image=photo)
            self.screenshot_canvas.image = photo  # Keep reference
            self.log_output("take_screenshot", {}, "Screenshot taken successfully")
        except Exception as e:
            self.log_output("take_screenshot", {}, f"Error: {str(e)}")

def main():
    root = tk.Tk()
    app = TestHarnessGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
