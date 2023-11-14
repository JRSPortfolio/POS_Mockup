import win32print
import win32ui

def print_receipt(sales_list: list, username: str):
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
    printer_names = [printer[2] for printer in printers]
    print(printer_names)
    
    x = 100
    y = 100
    cabecalho = 'POS Mockup'
    
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC (printer_names[3])
    hDC.StartDoc ('recibo')
    hDC.StartPage()
    hDC.TextOut(x, y)
    hDC.EndPage()
    hDC.EndDoc()
    
def set_receipt_elements():
    ...