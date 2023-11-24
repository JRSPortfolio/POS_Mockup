import win32print
import win32ui
from datetime import datetime

def print_receipt(sales_list: list, total: str, company_data: dict, username: str):
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
    printer_names = [printer[2] for printer in printers]
        
    x = 50
    
    header_font = win32ui.CreateFont({"name": "Courier New", "height": 24, "weight": 1200,})
    item_font = win32ui.CreateFont({"name": "Courier New", "height": 22, "weight": 500,})
    separator = f'{'_' * 40:^49}'
    
    print_doc = win32ui.CreateDC()
    print_doc.CreatePrinterDC (printer_names[3])
    print_doc.StartDoc ('recibo')
    print_doc.StartPage()
    
    company_name = f'{company_data['nome']}'
    company_address = f'{company_data['morada']}'
    user_date = f'Empregado: {username:<18}{datetime.now().strftime('%d-%m-%Y %H:%M'):>20}'
    sales_header = f'{'Produto':<25}{'IVA':^8}{'Qtd.':^6}{'Preço':>10}'
    
    print_doc.SelectObject(header_font)
    print_doc.TextOut(x, 50, company_name)
    print_doc.TextOut(x, 80, company_address)
    
    print_doc.SelectObject(item_font)
    print_doc.TextOut(x, 105, separator)
    print_doc.TextOut(x, 140, user_date)
    print_doc.TextOut(x, 180, sales_header)
    
    y = 205
    for sale in sales_list:
        produto = sale[0]
        iva = str(sale[1]) + '%'
        quantity = str(sale[2])
        price = str(sale[3]) + '€'
        line = f'{produto:<25}{iva:^8}{quantity:^6}{price:>10}'
        print_doc.TextOut(x, y, line)
        y += 25
    
    print_doc.TextOut(x, y, separator)
    y += 25
    str_total = 'Total: ' + str(total) + "€"
    line_total = f'{str_total:>49}'
    print_doc.TextOut(x, y, line_total)
        
    print_doc.EndPage()
    print_doc.EndDoc()
    

    