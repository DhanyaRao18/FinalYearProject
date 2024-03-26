# FinalYearProject
open cmd prompt and run these commands

--------------   creating virtual environment   ------------------
python -m venv myenv
myenv\Scripts\activate

---------------    install required libraries  ------------------
pip install opencv-python
pip install mediapipe
pip install Flask
pip install reportlab

---------------   run python file    ------------------------
python app.py
open a web browser and navigate to http://localhost:5000

# Create a new PDF document
    # c = canvas.Canvas(buffer, pagesize=letter)

    # # Set up scaling and positioning for drawing
    # scale_factor = 10  # Adjust this value as needed
    # x_offset = 50      # Adjust this value as needed
    # y_offset = 50      # Adjust this value as needed

    # # Draw lines based on the points stored in bpoints, gpoints, rpoints, and ypoints
    # draw_lines(c, bpoints, (0, 0, 255), scale_factor, x_offset, y_offset)
    # draw_lines(c, gpoints, (0, 255, 0), scale_factor, x_offset, y_offset)
    # draw_lines(c, rpoints, (255, 0, 0), scale_factor, x_offset, y_offset)
    # draw_lines(c, ypoints, (0, 255, 255), scale_factor, x_offset, y_offset)

    # # Save the PDF document
    # c.save()

            
