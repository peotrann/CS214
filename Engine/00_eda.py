import pandas as pd
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ENGINE_DIR.parent
DATA_DIR = PROJECT_ROOT / "Data"


def is_id_column(col_name):
    return col_name.lower().startswith("id_")


def print_values(values):
    for v in values:
        print("   -", v)


def eda_excel_file(path):
    print("=" * 100)
    print(f"FILE: {path.name}")
    print("=" * 100)

    xls = pd.ExcelFile(path)

    for sheet in xls.sheet_names:
        print(f"\n--- Sheet: {sheet} ---")
        df = pd.read_excel(xls, sheet_name=sheet)

        print(f"Số dòng: {len(df)}")
        print(f"Số cột: {len(df.columns)}")

        for col in df.columns:
            series = df[col]
            dtype = series.dtype
            uniques = series.dropna().unique()

            print(f"\nCột: {col}")
            print(f"  Kiểu dữ liệu: {dtype}")
            print(f"  Số giá trị khác nhau: {len(uniques)}")

            if is_id_column(col):
                print("  Danh sách ID:")
                print_values(uniques)

            else:
                if len(uniques) <= 30:
                    print("  Giá trị:")
                    print_values(uniques)
                else:
                    print("  Giá trị (30 mẫu đầu):")
                    print_values(uniques[:30])
                    print(f"  ... ({len(uniques) - 30} giá trị khác)")


def main():
    if not DATA_DIR.exists():
        print(f"[00_eda.py] ERROR: Data directory not found: {DATA_DIR}")
        return

    excel_files = sorted(DATA_DIR.glob("*.xlsx"))
    if not excel_files:
        print("[00_eda.py] ERROR: No Excel files found in Data directory")
        return

    print(f"[00_eda.py] Found {len(excel_files)} Excel files\n")

    for path in excel_files:
        eda_excel_file(path)


if __name__ == "__main__":
    main()
