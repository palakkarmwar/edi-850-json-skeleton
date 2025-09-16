# 📦 EDI 850 → JSON Parser (Repo 1)

## 🔹 Overview
This project parses a Purchase Order (EDI 850 file) into structured JSON format for easier processing and automation in Supply Chain/EDI workflows.  

EDI data is usually received in raw text with delimiters (`*` and `~`).  
This script extracts key information like **PO Number, Buyer, Seller, Line Items, and Total Amount** into machine-readable JSON.

---

## 🔹 Why this project?
- **EDI 850 (Purchase Order)** is one of the most common supply chain transactions.  
- **JSON** makes it easier to analyze, automate, and connect with AI or RPA pipelines.  
- Forms the foundation for **AI-driven supply chain automation** (summaries, anomaly detection, dashboards).  

---

## 🔹 Features
✅ Reads raw EDI 850 text file (`sample_850.txt`)  
✅ Extracts PO Number, Buyer, Seller, Items  
✅ Calculates Total Amount from quantities × prices  
✅ Saves structured JSON (`po.json`)  
✅ Simple, extensible Python script (`edi850_to_json.py`)  

---

## 🔹 Example

**Input (EDI 850 segment):**
```BEG*00*SA*XX-1234**20170301**NA~
N1*BY*ABC AEROSPACE*9*1234567890101~
PO1*1*25*EA*36*PE*MG*XYZ-1234~```


**Output (po.json):**
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

🔹 Next Steps (Planned)

AI-based PO summarization (using GenAI).
Supplier performance analytics.
Integration with AWS S3 for storage + RPA automation triggers.
