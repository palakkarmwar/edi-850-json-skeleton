# 📦 EDI 850 → JSON Parser (Repo 1)

---

## 🔹 Overview
This project parses a Purchase Order (**EDI 850 file**) into structured JSON format for easier processing and automation in Supply Chain/EDI workflows.  

EDI data is usually received in raw text with delimiters (`*` and `~`).  
This script extracts key information like **PO Number, Buyer, Seller, Line Items, and Total Amount** into machine-readable JSON.

---

## 🔹 Why this project?
- **EDI 850 (Purchase Order)** is one of the most common supply chain transactions.  
- JSON makes it easier to analyze, automate, and connect with AI or RPA pipelines.  
- Forms the foundation for **AI-driven supply chain automation** (summaries, anomaly detection, dashboards).  

---

## 🔹 Features
✅ Reads raw EDI 850 text file (`sample_850.txt`)  
✅ Extracts PO Number, Buyer, Seller, Items  
✅ Calculates Total Amount from quantities × prices  
✅ Saves structured JSON (`po.json`)  
✅ Generates **AI-based PO summary** (`outputs/summary.txt`)  
✅ Simple, extensible Python script (`edi850_to_json.py`)  

---

## 🔹 Example

### Input (EDI 850 segment):
BEG00SAXX-123420170301NA~
N1BYABC AEROSPACE91234567890101~
PO1125EA36PEMGXYZ-1234~


### Output (`po.json`):
```json
{
  "PO_Number": "XX-1234",
  "Buyer": "ABC AEROSPACE",
  "Seller": null,
  "Items": [
    {
      "Line": "1",
      "Qty": "25",
      "Quantity_UOM": "EA",
      "Price": "36",
      "Item_ID": "XYZ-1234"
    }
  ],
  "TotalAmount": 900.0
}
```

---

🔹 AI Summary (outputs/summary.txt)

PO XX-1234 from ABC AEROSPACE / None contains 1 line items.  
Total quantity: 25, Total spend: 900.00  
Items details:  
- XYZ-1234: Qty=25, Price=36  

---

🔹 License  

🚫 **Private Repository – No License**  
This code is for personal/educational use only.  
Re-use, modification, or distribution is not permitted without permission.
