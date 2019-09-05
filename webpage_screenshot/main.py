
from selenium import webdriver
from fpdf import FPDF
from PIL import Image
import sys

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, flowables

image_file = 'image.png'
pdf_file = 'output.pdf'
# print A4
# A4 = (1024, 768)
driver = webdriver.PhantomJS()
driver.set_window_size(*A4) # set the window size that you need
driver.get('http://facebook.com/')

driver.save_screenshot(image_file)


def drawPageFrame(canvas, doc):
    width, height = A4
    canvas.saveState()
    canvas.drawImage(
    image_file, 0, 0, height, width,
    preserveAspectRatio=True, anchor='c')
    canvas.restoreState()


def jpg2pdf(pdfname):
    width, height = A4
    # To make it landscape, pagesize is reversed
    # You can modify the code to add PDF metadata if you want
    doc = SimpleDocTemplate(pdfname, pagesize=(height, width))
    elem = []

    elem.append(flowables.Macro('canvas.saveState()'))
    elem.append(flowables.Macro('canvas.restoreState()'))

    doc.build(elem, onFirstPage=drawPageFrame)


jpg2pdf(pdf_file)

