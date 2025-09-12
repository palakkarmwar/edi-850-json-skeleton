# edi850_to_json.py
# Work in Progress: Skeleton for converting EDI 850 PO into JSON

edi_850_sample = """
ST*850*0001~
BEG*00*SA*PO12345**20250913~
N1*BY*Buyer Name~
N1*ST*Ship To Name~
PO1*1*100*EA*10.00*PE*BP*12345~
CTT*1~
SE*...~
"""

edi_850_json = {
    "Po_Number" : "PO12345",
    "Po_Date" : "20250913",
    "Buyer" : {"Name" :"Buyer Name"},
    "Seller" : {"Name" : "Ship To Name"},
    "Lines" : [
            {"Lines" : 1 , "Item" : "12345" , "Qty" : 100 , "UOM" : "EA" , "Price" : 10.00 }
    ]
}

print(edi_850_json)