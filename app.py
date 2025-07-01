from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

EXCEL_FILE = "Vendor-INGR.xlsx"  
SHEETS = ["Kalasin", "Sikhiu"]   

def load_farmers_from_excel():
    farmers_all = []
    for sheet in SHEETS:
        try:
            df = pd.read_excel(EXCEL_FILE, sheet_name=sheet)
            df = df[["ชื่อผู้ขาย"]].dropna()
            df = df.rename(columns={"ชื่อผู้ขาย": "name"})
            df["area"] = sheet  
            farmers_all.append(df)
        except Exception as e:
            print(f"❗โหลดชีต {sheet} ไม่ได้: {e}")
    combined_df = pd.concat(farmers_all, ignore_index=True)
    combined_df["id"] = range(1, len(combined_df) + 1)
    return combined_df[["id", "name", "area"]].to_dict(orient="records")


farmers = load_farmers_from_excel()

@app.route("/api/farmers")
def get_farmers():
    return jsonify(farmers)

if __name__ == "__main__":
    app.run(debug=True)
