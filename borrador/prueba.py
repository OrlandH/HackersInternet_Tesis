from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from datetime import datetime

# Datos de ejemplo (JSON)
data = {
    "id": "LAP78490C",
    "marca": "Lenovo",
    "modelo": "ThinkPad",
    "estado": "Nuevo",
    "nombre Cliente": "Juan",
    "observaciones": "Sin observaciones"
}


# Función para crear el encabezado con los logos
def agregar_encabezado(canvas, doc, logo_path, logo_name_path):
    canvas.saveState()
    canvas.drawImage(logo_path, 40, 720, width=1.8 * inch, height=1.5 * inch,
                     mask='auto')  # Ajustar tamaño y posición del logo principal
    canvas.drawImage(logo_name_path, 200, 750, width=4 * inch, height=0.5 * inch,
                     mask='auto')  # Ajustar tamaño y posición del segundo logo
    canvas.line(40, 712, 550, 712)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawString(150, 695, "Ficha Técnica de Ingreso para Mantenimiento")
    canvas.restoreState()


# Función para crear la tabla de datos
def crear_tabla_de_datos(data):
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]

    # Obtener la fecha actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    # Datos para la tabla
    tabla_data = [
        ["Fecha Ingreso:", fecha_actual],
        ["ID", data["id"]],
        ["Marca", data["marca"]],
        ["Modelo", data["modelo"]],
        ["Estado", data["estado"]],
        ["Nombre Cliente", data["nombre Cliente"]],
        ["Observaciones", data["observaciones"]]
    ]

    # Crear tabla
    tabla = Table(tabla_data, colWidths=[150, 300])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    return tabla


# Función para crear el pie de página
def agregar_pie_de_pagina(canvas, doc, telefono):
    canvas.saveState()
    canvas.setFont("Helvetica", 10)
    canvas.drawString(40, 50, "Hackers Internet")
    canvas.setFillColor(colors.blue)
    canvas.drawString(400, 50, f"Tel: {telefono}")
    canvas.restoreState()


# Crear el documento PDF
def crear_ficha_tecnica(nombre_archivo, data, logo_path, logo_name_path, telefono):
    doc = SimpleDocTemplate(nombre_archivo, pagesize=A4)
    story = []

    # Agregar encabezado
    story.append(Spacer(1, 1.5 * inch))

    # Agregar tabla de datos
    tabla = crear_tabla_de_datos(data)
    story.append(tabla)

    # Crear PDF
    doc.build(story,
              onFirstPage=lambda canvas, doc: agregar_encabezado(canvas, doc, logo_path, logo_name_path),
              onLaterPages=lambda canvas, doc: agregar_pie_de_pagina(canvas, doc, telefono))


# Rutas de los logos
logo_path = "../assets/logo.png"
logo_name_path = "../assets/logoName.png"
telefono = "0987547665"

# Crear el PDF
crear_ficha_tecnica("ficha_tecnica_ingreso.pdf", data, logo_path, logo_name_path, telefono)

