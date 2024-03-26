from flask import Flask, render_template, send_file
import subprocess
from PIL import Image

# from paint_board import execute_paint_board
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from collections import deque

app = Flask(__name__, static_url_path='/static')

def read_points_from_file():
    with open('points.txt', 'r') as f:
        # Read each line and convert it back to a list of points
        rpoints = deque(map(int, f.readline().strip().split()))
        gpoints = deque(map(int, f.readline().strip().split()))
        bpoints = deque(map(int, f.readline().strip().split()))
        ypoints = deque(map(int, f.readline().strip().split()))

    return rpoints, gpoints, bpoints, ypoints

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    subprocess.run(['python', 'mainfile.py'])
#     return 'Python file executed successfully!'
# # def execute_python_code():
    
    rpoints, gpoints, bpoints, ypoints = read_points_from_file()
    
    # Create a buffer to store PDF content
    pdf_buffer = io.BytesIO()

    # Generate PDF
    generate_pdf(pdf_buffer,rpoints,gpoints,bpoints,ypoints)

    # Move to the beginning of the buffer
    pdf_buffer.seek(0)

    # Send the PDF file as a downloadable attachment
    return send_file(pdf_buffer, as_attachment=True, download_name='drawing.png')

@app.route('/download', methods=['GET'])
def generate_pdf(buffer,rpoints,gpoints,bpoints,ypoints):
    
    import cv2
    import numpy as np

    # Read the paintWindow image
    paintWindow_image = cv2.imread('paintWindow.png')

    # Convert the image to a numpy array (if not already)
    paintWindow = np.array(paintWindow_image)

    
    c = canvas.Canvas(buffer, pagesize=letter)

    # Set up scaling and positioning for drawing
    scale_factor = 1  # Adjust this value as needed
    x_offset = 50     # Adjust this value as needed
    y_offset = 50     # Adjust this value as needed

    # Convert paintWindow to PIL image
    paint_image = Image.fromarray(paintWindow)

    # Convert PIL image to RGB mode (if not already)
    if paint_image.mode != "RGB":
        paint_image = paint_image.convert("RGB")

    # Resize paintWindow to fit the PDF canvas
    paint_image = paint_image.resize((c.width, c.height), Image.ANTIALIAS)

    # Draw paintWindow onto PDF canvas
    paint_image_bytes = io.BytesIO()
    paint_image.save(paint_image_bytes, format="PNG")
    c.drawImage(paint_image_bytes, 0, 0)

    # Draw lines based on the points stored in bpoints, gpoints, rpoints, and ypoints
    draw_lines(c, bpoints, (0, 0, 255), scale_factor, x_offset, y_offset)
    draw_lines(c, gpoints, (0, 255, 0), scale_factor, x_offset, y_offset)
    draw_lines(c, rpoints, (255, 0, 0), scale_factor, x_offset, y_offset)
    draw_lines(c, ypoints, (0, 255, 255), scale_factor, x_offset, y_offset)

    # Save the PDF document
    c.save()

def draw_lines(c, points_list, color, scale_factor, x_offset, y_offset):
    for points in points_list:
        if len(points) > 1:
            prev_point = points[0]
            for point in points[1:]:
                # Convert points from OpenCV coordinate system to PDF coordinate system
                x1, y1 = prev_point[0] * scale_factor + x_offset, prev_point[1] * scale_factor + y_offset
                x2, y2 = point[0] * scale_factor + x_offset, point[1] * scale_factor + y_offset

                # Draw line
                c.setStrokeColorRGB(color[0]/255, color[1]/255, color[2]/255)  # Convert color to RGB values between 0 and 1
                c.line(x1, y1, x2, y2)

                prev_point = point

if __name__ == '__main__':
    app.run(debug=True)
