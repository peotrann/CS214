# Traffic Law Ontology

This project builds a traffic law ontology using Python and OWLReady2. It loads traffic law data from Excel files, constructs ontology individuals, extracts IF-THEN rules, and performs inference on traffic violations to determine applicable penalties.

## Libraries

The project uses the following Python libraries:
- pandas: for reading and processing Excel data
- owlready2: for building and manipulating ontology
- openpyxl: Excel engine required by pandas to read .xlsx files

Install them using:
`pip install pandas owlready2 openpyxl`

## Project Structure

CS214\Engine
- 01_ontology.py: defines ontology classes and properties for vehicles, actions, conditions, legal documents, and penalties.
- 02_load_data.py: loads Excel files into pandas DataFrames.
- 03_build_ontology.py: builds ontology individuals from loaded data and saves the ontology to traffic_ontology.owl.
- 04_knowledge_ifthen.py: extracts IF-THEN rules from the ontology.
- 05_inference_engine.py: provides functions to infer penalties based on vehicle type, action, and optional conditions.
- 06_query_example.py: demo queries showing inference results.
CS214\Data: folder containing Excel files (phuong_tien.xlsx, hanh_vi.xlsx, dieu_kien.xlsx, van_ban_phap_luat.xlsx, luat_xu_phat.xlsx).

## Setup

1. Create a virtual environment:
`python -m venv venv`
2. Activate the environment:
- Windows: `venv\Scripts\activate`
- Linux/macOS: `source venv/bin/activate`
3. Install dependencies:
`pip install pandas owlready2 openpyxl`

## How to Run

1. Build the ontology classes:
`python 01_ontology.py`
2. Load data from Excel files:
`python 02_load_data.py`
3. Populate ontology individuals and save:
`python 03_build_ontology.py`
4. Inspect IF-THEN rules extracted from the ontology:
`python 04_knowledge_ifthen.py`
5. Run inference examples:
`python 06_query_example.py`

The inference engine (`05_inference_engine.py`) can also be imported and used in other scripts to check penalties for specific vehicle types, actions, and conditions.

## Data Files

Place the following Excel files in the `Data/` folder:
- phuong_tien.xlsx
- hanh_vi.xlsx
- dieu_kien.xlsx
- van_ban_phap_luat.xlsx
- luat_xu_phat.xlsx

After building, the ontology is saved as `traffic_ontology.owl`.

## Output

- `traffic_ontology.owl`: OWL file representing the ontology with individuals populated from Excel.
- IF-THEN rules printed from `04_knowledge_ifthen.py`.
- Inference results printed from `06_query_example.py`.

## GitHub Push

1. Initialize repository:
`git init`
2. Add files:
`git add .`
3. Commit:
`git commit -m "Initial commit"`
4. Set main branch:
`git branch -M main`
5. Add remote repository:
`git remote add origin https://github.com/<your-username>/traffic-law-ontology.git`
6. Push:
`git push -u origin main`
