
import io

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfMerger

from garmin_automatic_reports.config import PATH_PDF, PATH_SAVE_IMG
from garmin_automatic_reports.config import GarminIndicator, CstIndicator, CommunIndicator, Alert, ImageForPdf

# ------------------------ The main function ---------------------------------
# ----------------------------------------------------------------------------
def generate_pdf(cst_data_pdf, garmin_data_pdf, commun_data_pdf, alerts_dict):
    in_pdf_path = PATH_PDF + "/empty.pdf"
    out_pdf_file = PATH_PDF + "/result.pdf"

    generate_page(cst_data_pdf, garmin_data_pdf, commun_data_pdf, alerts_dict, in_pdf_path, out_pdf_file)

# ----------------------- Internal functions ---------------------------------
# ----------------------------------------------------------------------------

def generate_page(cst_data_pdf, garmin_data_pdf, commun_data_pdf, alerts_dict, in_pdf_path, out_pdf_file):

    # Costrunct pdf   
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize = A4)

    # GARMIN
    for garmin_indicator in GarminIndicator:
        dict_aux = garmin_data_pdf[garmin_indicator.value]
        for key in dict_aux:
            _add_text(
                can = can, 
                text_parameters = dict_aux[key],
            )
            
    # CST
    for cst_indicator in CstIndicator:
        dict_aux = cst_data_pdf[cst_indicator.value]
        for key in dict_aux:
            _add_text(
                can = can, 
                text_parameters = dict_aux[key],
            )
    # COMMUN
    for commun_indicator in CommunIndicator:
        dict_aux = commun_data_pdf[commun_indicator.value]
        for key in dict_aux:
            _add_text(
                can = can, 
                text_parameters = dict_aux[key],
            )
    
    # ALERTS
    for key in alerts_dict:
        _add_image(
            can = can, 
            image_parameters = alerts_dict[key],
        )
    
    # IMAGES
    for image_parameters in ImageForPdf:
        _add_image(can, image_parameters.value)
        
    can.showPage()
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)

    # Create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    
    # Read your existing PDF
    existing_pdf = PdfFileReader(open(in_pdf_path, "rb"))
    output = PdfFileWriter()

    # Add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    # Finally, write "output" to a real file
    output_stream = open(out_pdf_file, "wb")
    output.write(output_stream)
    output_stream.close()

def _add_text(can, text_parameters):
    text = text_parameters["text"]
    x = text_parameters["x"]
    y = text_parameters["y"]
    color = text_parameters["color"]
    font = text_parameters["font"]
    size = text_parameters["size"]

    y_top = 11.69
    x_start = x*inch
    y_start = (y_top - y)*inch
    
    can.setFillColor(color)
    can.setFont(font, size)
    can.drawString(x_start, y_start, text)

def _add_image(can, image_parameters):
    x = image_parameters["x"]
    y = image_parameters["y"]
    width = image_parameters["w"]
    height = image_parameters["h"]
    path_img = image_parameters["path"]

    width = width*inch 
    height = height*inch

    y_top = 11.69
    x_start = x*inch
    y_start = (y_top - y)*inch 

    can.drawImage(path_img, x_start, y_start, width, height,
                  preserveAspectRatio = True, mask = 'auto')