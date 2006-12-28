#printer_list.py
#The purpose of this module is to provide a list of both printers and computers.
#To add a printer:
#Data should be in the following format
#printers = 'ID':{'IP':'ip','PORT':'portNumber','Driver':'drive','Description':'ADesc'}
#To add a computer:
#computers = {'IPADDRESS':{'Description':'DESC','ReportPrinter':'PRINTERID','ReceiptPrinter':'PRINTERID','LabelPrinter':'PRINTERID'},



printers = {'RCT1':{'IP':'127.0.0.1','PORT':'9600','Driver':'TDP646','Description':'Registration Receipt Printer'},
            'RCT2':{'IP':'192.168.11.2','PORT':'9600','Driver':'TDP646','Description':'Registration Receipt Printer'},
            'LBL1':{'IP':'192.168.11.3','PORT':'9600','Driver':'TDP646','Description':'Registration Label Printer'},
            'LBL2':{'IP':'192.168.11.4','PORT':'9600','Driver':'TDP646','Description':'Registration Label Printer'},
            'RPT1':{'IP':'192.168.11.5','PORT':'9600','Driver':'TDP646','Description':'Registration Report Printer'},
            'RPT2':{'IP':'192.168.11.10','PORT':'9600','Driver':'TDP646','Description':'Registration Report Printer'}
            }



computers = {'127.0.0.1':{'Description':'Server','ReportPrinter':'RPT1','ReceiptPrinter':'RCT1','LabelPrinter':'LBL1'},
             '192.168.11.1':{'Description':'Server','ReportPrinter':'RPT1','ReceiptPrinter':'RCT1','LabelPrinter':'LBL1'},
             '192.168.11.2':{'Description':'Reg','ReportPrinter':'RPT1','ReceiptPrinter':'RCT2','LabelPrinter':'LBL2'},
             '192.168.11.3':{'Description':'Reg','ReportPrinter':'RPT1','ReceiptPrinter':'RCT2','LabelPrinter':'LBL2'},
             '192.168.11.4':{'Description':'Reg','ReportPrinter':'RPT1','ReceiptPrinter':'RCT2','LabelPrinter':'LBL2'},
             '192.168.11.5':{'Description':'Reg','ReportPrinter':'RPT1','ReceiptPrinter':'RCT2','LabelPrinter':'LBL2'},
             '192.168.11.6':{'Description':'Reg','ReportPrinter':'RPT1','ReceiptPrinter':'RCT2','LabelPrinter':'LBL2'},
             '192.168.11.7':{'Description':'Reg','ReportPrinter':'RPT1','ReceiptPrinter':'RCT2','LabelPrinter':'LBL2'},
             '192.168.11.8':{'Description':'Reg','ReportPrinter':'RPT1','ReceiptPrinter':'RCT2','LabelPrinter':'LBL2'},
             '10.211.55.2':{'Description':'Reg','ReportPrinter':'RPT2','ReceiptPrinter':'RCT2','LabelPrinter':'LBL2'},
             '192.168.11.254':{'Description':'Reg','ReportPrinter':'RPT1','ReceiptPrinter':'RCT2','LabelPrinter':'LBL2'}}
