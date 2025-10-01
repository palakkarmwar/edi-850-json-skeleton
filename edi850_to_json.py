# -------------------------------
# Repo 1: EDI 850 → JSON Parser + Cleanup + SQL + AI-style Summary
# CLI-ready version (Free, No external tokens)
# -------------------------------

import json
import logging
import pandas as pd
import sqlite3
import argparse

# -------------------------------
# Logging Setup
# -------------------------------
logging.basicConfig(
    filename="parser.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------
# Parse EDI 850
# -------------------------------
def parse_edi_850(file_path):
    """Parse EDI 850 file into structured JSON."""
    logging.info(f"Reading EDI file: {file_path}")
    with open(file_path, 'r') as file:
        edi_data = file.read()

    segments = edi_data.strip().split("~")
    output = {"PO_Number": None, "Buyer": None, "Seller": None, "Items": []}

    for seg in segments:
        seg = seg.strip()
        if not seg:
            continue
        parts = seg.split("*")

        if parts[0] == "BEG":
            output["PO_Number"] = parts[3]
        elif parts[0] == "N1":
            if parts[1] == "BY":
                output["Buyer"] = parts[2]
            elif parts[1] == "ST":
                output["Seller"] = parts[2]
        elif parts[0] == "PO1":
            item = {
                "Line": parts[1],
                "Qty": parts[2],
                "Quantity_UOM": parts[3],
                "Price": parts[4],
                "Item_ID": parts[-1],
                "Seller": output["Seller"]
            }
            output["Items"].append(item)

    logging.info(f"Parsed PO_Number={output['PO_Number']}, Items={len(output['Items'])}")
    return output

# -------------------------------
# Clean Data with Pandas
# -------------------------------
def cleanup_data(parsed_json):
    df = pd.DataFrame(parsed_json["Items"])
    df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["LineTotal"] = df["Qty"] * df["Price"]
    df = df.dropna(subset=["Qty", "Price"])

    df.to_csv("outputs/po_clean.csv", index=False)
    df.to_json("outputs/po_clean.json", orient="records", indent=4)
    logging.info("Cleaned data saved to outputs/po_clean.csv and outputs/po_clean.json")
    return df

# -------------------------------
# Run SQL Queries
# -------------------------------
def run_sql_queries(df):
    try:
        conn = sqlite3.connect("outputs/po_data.db")
        df.to_sql("purchase_orders", conn, if_exists="replace", index=False)
        logging.info("SQLite DB created and table purchase_orders populated")

        total_spend = conn.execute("SELECT SUM(LineTotal) FROM purchase_orders").fetchone()[0]
        print("Total Spend:", total_spend)

        qty_per_item = conn.execute(
            "SELECT Item_ID, SUM(Qty) as TotalQty FROM purchase_orders GROUP BY Item_ID"
        ).fetchall()
        print("Qty per Item:", qty_per_item)

        supplier_spend = conn.execute("""
            SELECT Seller, SUM(LineTotal)*100.0/(SELECT SUM(LineTotal) FROM purchase_orders) as SpendPercent
            FROM purchase_orders
            GROUP BY Seller
        """).fetchall()
        print("Supplier Spend %:", supplier_spend)

        # Save results to README_results.txt
        with open("outputs/README_results.txt", "w") as f:
            f.write("### SQL Query Results\n\n")
            f.write(f"Total Spend: {total_spend}\n\n")
            f.write("Qty per Item:\n")
            for row in qty_per_item:
                f.write(f"  - {row}\n")
            f.write("\nSupplier Spend %:\n")
            for row in supplier_spend:
                f.write(f"  - {row}\n")

        return total_spend, qty_per_item, supplier_spend

    except Exception as e:
        logging.error(f"SQLite queries failed: {e}")
        return None, None, None
    finally:
        conn.close()

# -------------------------------
# AI-style Summary (Python-only)
# -------------------------------
def generate_ai_summary(parsed_json):
    po_number = parsed_json.get("PO_Number", "Unknown")
    buyer = parsed_json.get("Buyer", "Unknown")
    seller = parsed_json.get("Seller", "Unknown")
    items = parsed_json.get("Items", [])

    num_items = len(items)
    total_qty = sum(int(item["Qty"]) for item in items if item["Qty"])
    total_value = sum(int(item["Qty"]) * float(item["Price"]) for item in items if item["Qty"] and item["Price"])

    # Simple AI-style summary logic
    summary = (
        f"AI Summary:\nPO {po_number} from {buyer} / {seller} contains {num_items} line items.\n"
        f"Total quantity: {total_qty}, Total spend: {total_value:.2f}\n"
        f"Items details:\n"
    )
    for item in items:
        summary += f"- {item['Item_ID']}: Qty={item['Qty']}, Price={item['Price']}\n"

    # Save summary
    with open("outputs/summary.txt", "w") as f:
        f.write(summary)

    print(summary)
    logging.info("AI-style summary saved to outputs/summary.txt")

# -------------------------------
# CLI Arguments
# -------------------------------
parser = argparse.ArgumentParser(description="Parse EDI 850 file to JSON, clean, run SQL, and generate AI summary.")
parser.add_argument(
    "--input",
    type=str,
    default="sample_edi/sample_850.txt",
    help="Path to EDI 850 file (default: sample_edi/sample_850.txt)"
)
args = parser.parse_args()
edi_file_path = args.input

# -------------------------------
# Main Script
# -------------------------------
if __name__ == "__main__":
    # Step 1: Parse EDI 850
    result = parse_edi_850(edi_file_path)

    # Step 2: Calculate Total Amount
    try:
        total_amount = sum(int(item["Qty"]) * float(item["Price"]) for item in result["Items"])
        result["TotalAmount"] = total_amount
        logging.info(f"Total Amount Calculated: {total_amount}")
    except Exception as e:
        result["TotalAmount"] = None
        logging.error(f"Error calculating total amount: {e}")

    # Step 3: Save Raw JSON
    with open("outputs/po.json", "w") as f:
        json.dump(result, f, indent=4)
    logging.info("Saved outputs/po.json successfully")

    # Step 4: Cleanup Data
    df_clean = cleanup_data(result)

    # Step 5: Run SQL Queries
    total_spend, qty_per_item, supplier_spend = run_sql_queries(df_clean)

    # Step 6: Generate AI-style Summary
    generate_ai_summary(result)

    print("✅ All steps completed: outputs/po.json, outputs/po_clean.csv, outputs/po_clean.json, outputs/po_data.db, outputs/README_results.txt, outputs/summary.txt")