from flask import Flask, render_template, request, send_file
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A6
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer, Paragraph, PageTemplate, Frame
from io import BytesIO
from urllib.parse import urlencode
import requests
import qrcode
import barcode
import datetime
import subprocess
import win32print
import win32api

app = Flask(__name__)

def insert_to_erpnext(species, size, volume, mc_id, mc_date, trolley):
    # Change the URL accordingly
    url = 'http://192.168.0.17/api/resource/FJ Kanban'  
    
    headers = {"Authorization": "Token 8df92fdb0c01d52:65dc2d0b06f32fa", "Content-Type": "application/json"}
        
    data = {
        'species': species,
        'size': size,
        'volume': volume,
        'mc_id': mc_id,
        'date': mc_date,
        'trolley': trolley,
    }

    # Debug: Print the data being sent
    print('Data being sent:', data)

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print('Data inserted into ERPNext successfully')
    else:
        print('Failed to insert data into ERPNext')
        print(f'Status code: {response.status_code}')
        print(f'Response text: {response.text}')
        
def get_from_erpnext():
    # Change the URL accordingly
    url = 'http://192.168.0.17/api/resource/FJ Kanban?order_by=name%20desc'
        
    headers = {"Authorization": "Token 8df92fdb0c01d52:65dc2d0b06f32fa", "Content-Type": "application/json"}

    # Make a GET request to fetch data from ERPNext
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print('Data retrieved from ERPNext successfully')
        data = response.json()  # Convert response to JSON format
        return data
    else:
        print('Failed to retrieve data from ERPNext')
        print(f'Status code: {response.status_code}')
        print(f'Response text: {response.text}')
        return None
    


data = get_from_erpnext()
if data:
    print(data)
    
global running_number
running_number = None 


def extract_first_value(data):
    global running_number
    
    if 'data' in data and isinstance(data['data'], list) and len(data['data']) > 0:
        running_number = data['data'][0]['name']
        print('Extracted value:', running_number)
        return running_number
    else:
        print('Error: No valid array found in the provided data')
        return None
      
def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    img_byte_array = BytesIO()
    img.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)
    return img_byte_array


def generate_barcode_image(barcode_data):
    barcode_url = "https://barcode.tec-it.com/barcode.ashx"
    params = {
        "data": barcode_data,
        "code": "Code128",
        "unit": "Fit",
        "dpi": 96,
        "imagetype": "png"
    }
    # Encode the parameters and make a GET request to generate the barcode image
    response = requests.get(barcode_url, params=params)
    
    return response.content


def generate_pdf_document(species, size, volume, mc_id, mc_date, trolley, qr_code_img, running_number):
    # Define the PDF document with A6 page size in landscape orientation and adjust top margin
    pdf = SimpleDocTemplate("kanban.pdf", pagesize=landscape(A6), topMargin=10, leftMargin=10, rightMargin=10, bottomMargin=0)
    elements = []

    # Generate barcode image
    barcode_data = running_number  # Use running number as barcode data
    barcode_image_bytes = generate_barcode_image(barcode_data)

    # Add QR code image to the PDF
    qr_code_img_data = qr_code_img.read()
    qr_code_img.close()
    qr_code_img_obj = Image(BytesIO(qr_code_img_data))
    qr_code_img_obj.drawHeight = 70
    qr_code_img_obj.drawWidth = 70

    # Add barcode image to the PDF
    barcode_img_obj = Image(BytesIO(barcode_image_bytes))
    barcode_img_obj.drawHeight = 50  # Adjust height as needed
    barcode_img_obj.drawWidth = 150  # Adjust width as needed

    data = [['FJ Kanban', qr_code_img_obj]]
    table = Table(data, colWidths=[4.4 * inch, 1.0 * inch], rowHeights=[0.8 * inch])
    table.setStyle(TableStyle([
        # ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),  # Align the text in the first cell (top left corner) to the left
        ('VALIGN', (0, 0), (0, 0), 'TOP'),  # Align the text in the first cell (top left corner) to the top
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 20),
    ]))

    elements.append(table)

    data = [[barcode_img_obj]]

    table = Table(data, colWidths=[5.5 * inch, 1.2 * inch], rowHeights=[1.2 * inch])
    table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.white),
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white), ]))
    elements.append(table)

    # Add the first table
    data = [['Species', 'Size', 'Volume'],
            [species, size, volume],
            ['MC ID', 'MC Date', 'Trolley'],
            [mc_id, mc_date, trolley]]

    table = Table(data, colWidths=[1.8 * inch, 1.8 * inch, 1.8 * inch],
                  rowHeights=[0.4 * inch, 0.4 * inch, 0.4 * inch, 0.4 * inch])
    table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 2), (-1, 2), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('LINEBELOW', (0, 0), (-1, -1), 1, colors.black),  # Draw a line below each cell in the first row
        ('LINEAFTER', (0, 0), (-1, -1), 1, colors.black),  # Draw a line after each column
        ('BACKGROUND', (0, 1), (-1, -1), colors.white), ]))
    elements.append(table)

    # Build the PDF document
    pdf.build(elements)
    
@app.route('/')
def index():
    return render_template('kanban.html')


@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Get form data
    size = request.form['size']
    species = request.form['species']
    volume = request.form['volume']
    mc_id = request.form['mc_id']
    mc_date = request.form['mc_date']
    trolley = request.form['trolley']

    insert_to_erpnext(species, size, volume, mc_id, mc_date, trolley)

    data = get_from_erpnext()
    running_number = extract_first_value(data)

    # Generate PDF
    qr_code_data = f"Running Number: {running_number}"
    qr_code_img = generate_qr_code(qr_code_data)
    generate_pdf_document(species, size, volume, mc_id, mc_date, trolley, qr_code_img, running_number)

    # Print PDF
    pdf_file = r"C:\Users\PM-Intern\Downloads\pdf\Kanban.pdf"
    num_copies = 2
    print_pdf(pdf_file, num_copies)

    # Return PDF file as attachment
    return send_file(pdf_file, as_attachment=True)


def print_pdf(pdf_file, num_copies):
    
    printer_name = win32print.GetDefaultPrinter()

    # Print the PDF file using the default printer
    for _ in range(num_copies):
        win32api.ShellExecute(0, "print", pdf_file, f'/d:"{printer_name}"', ".", 0)

if __name__ == "__main__":
    app.run(debug=True)