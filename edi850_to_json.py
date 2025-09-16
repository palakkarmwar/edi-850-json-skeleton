#EDI 850 file --> json file

import json

def parsededi_850(file_path):
    with open(file_path,'r') as file:
        edi850_data = file.read()


        segments = edi850_data.strip().split("~")
        output = {"PO_Number":None,"Buyer" : None, "Seller" : None , "Items": []}

        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue

            parts = seg.split("*")
            
            if parts[0]=="BEG":
                output["PO_Number"] = parts[3]
            elif parts[0] == "N1":
                if parts[1] == "BY":
                    output["Buyer"] = parts[2]
                elif parts[1] == "ST":
                    output["Seller"] = parts[2]
            elif parts[0] == "PO1":
                item = {"Line" : parts[1],
                        "Qty" : parts[2],
                        "Quantity_UOM" : parts[3],
                        "Price" : parts[4],
                        "Item_ID" : parts[-1]
                        }
                output["Items"].append(item)

    return output


if __name__ == "__main__":
    result = parsededi_850("sample_edi/sample_850.txt")

    try:
        total = sum(int(item["Qty"]) * float(item["Price"]) for item in result["Items"])
        result["TotalAmount"] = total
    except Exception:
        result["TotalAmount"] = None  # fallback if Qty/Price missing    

    
    with open('po.json','w') as file:
        json.dump(result,file,indent=4)

    print("Po Parsed to json and saved as po.json")    
