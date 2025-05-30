# Importing Modules
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
import time
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



class BillWindow:
    def __init__(self, customer_name, customer_contact, items, master):
        """ Creates Bill/ Invoice and saves Screenshot and .Txt file as a record.
            Keyword agruments:
            customer_name -- String
            customer_contact -- Int upto 10 digits
            items -- List of items
            master -- master Level window
        """
        self.master = master
        self.items = items
        self.customer_name = customer_name
        self.customer_contact = customer_contact

        # Creating Top-level window & Setting Window Width and height
        self.bill_win = tk.Toplevel(master)
        win_width, win_height = 727, 492
        screen_width = master.winfo_screenwidth()   
        screen_height = master.winfo_screenheight()
        x = int((screen_width/2) - (win_width/2))  - 7
        y = int((screen_height/2) - (win_height/2)) - 35
        self.bill_win.geometry(f'{win_width}x{win_height}+{x}+{y}')
        self.bill_win.resizable(0,0) # Disabling resize of window
        # Forcing Top-level window to stay on Top
        self.bill_win.attributes('-topmost', 'true')
        # Setting Top Level Window Title
        self.bill_win.title("BILL")
        # Adding icon to title menu
        self.bill_win.iconbitmap("images/bill_title.ico")
        
        #============= BILL FRAME Background Body Frame ==============#

        bill_frame = ttk.Frame(self.bill_win, width=win_width, height=win_height)
        bill_frame.place(x=0, y=0)
        
        # Bill Title
        bill_title = ttk.Label(bill_frame, text="KMS FERTILIZER SHOP", font="Consolas 30 bold",
                              border=7, relief="groove", anchor='c',
                              background='#282c34', foreground='#fff')
        bill_title.grid(row=0, ipadx=317)
        # Bill Contents/Text Area
        self.bill_text = ScrolledText(bill_frame, font="Consolas 10",
                                      width=101, height=29)
        self.bill_text.grid(row=1, sticky='W')
        
        # Define attributes for Bill entry
        heading = "Retail Invoice"
        cust_name = f"Customer Name    : {customer_name}"
        cust_phno = f"Customer Number  : {customer_contact}"
        # Defining date and time variables
        self.date_string = "Date : "+time.strftime("%d/%b/%Y")
        self.time_string = "Time : "+time.strftime("%I:%M:%S %p")
        # print(date_string,time_string)    

        # First Deleting Entire bill Contents/Texts
        self.bill_text.delete('1.0','end')
        # Inserting to Clean bill/Texts
        self.bill_text.insert('end', "\n"+heading+"\n")
        self.bill_text.insert('end', "\n"+cust_name)
        self.bill_text.insert('end', "\t\t\t\t\t\t\t\t\t"+self.date_string+"\n")
        self.bill_text.insert('end', "\n"+cust_phno)
        self.bill_text.insert('end', "\t\t\t\t\t\t\t\t\t"+self.time_string+"\n\n")
        
        self.bill_text.insert('end', "-"*100+"\n")
        self.bill_text.insert('end', "No   Product Name\t\t\t\t\t\t   Quantity\t\t     Rate(\u20B9)\t\t     Total(\u20B9)\n")
        self.bill_text.insert('end', "-"*100+"\n")

        # Total Price set to 0 before calculating
        sum = 0.0
        # Inserting items to Bill and Calculating sum of all contents
        for i in range(len(items)):
            item = items[i]
            self.bill_text.insert('end',f"\n  {i+1}  {item[0]}\t\t\t\t\t\t\t{item[1]}\t\t{item[2]}\t\t{item[3]}")
            total_col = item[3]
            total_col = float(total_col.split("\u20B9")[1])
            sum = sum + total_col
            # print(items[i])
        # Inserting sum amount at the end
        self.bill_text.insert('end', "\n\n\n\n"+"-"*100+"\n")
        # print(sum)
        self.total_amt = f"\u20B9 {sum}"
        self.bill_text.insert('end', f"TOTAL =  {self.total_amt}")
        self.bill_text.insert('end', "\n"+"-"*100+"\n")
        
        # Tags and styling
        self.bill_text.tag_add('heading', '2.0', '2.end')
        self.bill_text.tag_config('heading', font='Arial 20 bold', justify='center')
        self.bill_text.tag_add('customer', '4.0', '6.end')
        self.bill_text.tag_config('customer', font='Consolas 11', lmargin1=20)
        self.bill_text.tag_add('sub-head', '9.0', '9.end')
        self.bill_text.tag_config('sub-head', font='Consolas 12 bold', lmargin1=10)
        
        total_line = str(i+17) # Calculating total lines to style Total Amount
        # print(total_line)
        self.bill_text.tag_add('total', f'{total_line}.0', f'{total_line}.end')
        self.bill_text.tag_config('total', font='Aerial 15 bold', justify='center')
        
        # Disabling modification of bill
        self.bill_text.config(state='disabled')

        # Creating Backup/Record in local disk
        self.write_to_disk(self.bill_win)
    
    #=======================  Other METHODS  ========================================#
    def write_to_disk(self, widget):
        """ Creates PDF backups/records of bills in Date-Time folders,
            sorted by Customer Name and Customer Contact strings.
            Keyword arguments:
            widget -- Tkinter window (unused in PDF version)
        """
        date_string = time.strftime("%d-%b-%Y")
        time_string = time.strftime("%I-%M-%S %p")
        folder = f"{date_string}\\{time_string}"
        
        if not os.path.exists(f"Bill Records\\{folder}"):
            os.makedirs(f"Bill Records\\{folder}")

        # Create PDF document
        pdf_path = f"Bill Records\\{folder}\\{self.customer_name}, {self.customer_contact}.pdf"
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        
        # Get sample styles
        styles = getSampleStyleSheet()
        elements = []
        
        # Add title
        title = Paragraph("KMS FERTILIZER SHOP", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Add invoice header
        header = Paragraph("Retail Invoice", styles['Heading2'])
        elements.append(header)
        elements.append(Spacer(1, 12))
        
        # Add customer info and date/time
        customer_info = [
            f"Customer Name: {self.customer_name}",
            f"Customer Number: {self.customer_contact}",
            f"Date: {time.strftime('%d/%b/%Y')}",
            f"Time: {time.strftime('%I:%M:%S %p')}"
        ]
        
        for info in customer_info:
            elements.append(Paragraph(info, styles['Normal']))
            elements.append(Spacer(1, 6))
        
        elements.append(Spacer(1, 12))
        
        # Create table data
        table_data = [
            ["No", "Product Name", "Quantity", "Rate(₹)", "Total(₹)"]
        ]
        
        # Add items to table
        for i, item in enumerate(self.items, 1):
            table_data.append([
                str(i),
                item[0],
                str(item[1]),
                item[2].replace('₹', '₹ '),
                item[3].replace('₹', '₹ ')
            ])
        
        # Add total row
        table_data.append(["", "", "", "TOTAL", self.total_amt])
        
        # Create table
        table = Table(table_data, colWidths=[0.5*inch, 3*inch, 0.8*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
        ]))
        
        elements.append(table)
        doc.build(elements)
        


if __name__ == "__main__":
    master = tk.Tk()
    master.attributes('-topmost', 'true')
    
    items = [['Set Wet Hair Gel Cool, 50ml', 10, '₹ 50.5', '₹ 505.0'], ['Set Wet Hair Gel Cool, 50ml', 20, '₹ 50.5', '₹ 1010.0'], ['Fair & Lovely Women, 50g', 50, '₹ 97.0', '₹ 4850.0'], ['Nivea Lip Balm, 4.8g', 140, '₹ 105.0', 
        '₹ 14700.0'], ['testing', 1, '₹ 1.0', '₹ 10.0'], ['testing', 1, '₹ 10.0', '₹ 10.0']]
    customer_name = "Testing"
    customer_contact = "999"
    win_obj = BillWindow(customer_name, customer_contact, items, master)
    master.mainloop()
