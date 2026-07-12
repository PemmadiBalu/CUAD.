
import os
import pandas as pd
from app import db, create_app
from app.pdf_proc import extract_text_from_pdf
from app.llm_proc import extract_contract_info
from app.models import Contract

def run_pipeline():
    app = create_app()
    with app.app_context():
        db.create_all()
        data_dir = app.config['UPLOAD_FOLDER']
        results = []

        for filename in os.listdir(data_dir):
            if filename.endswith(".pdf"):
                print(f"Processing {filename}...")
                file_path = os.path.join(data_dir, filename)
                
                # 1. Extract Text
                raw_text = extract_text_from_pdf(file_path)
                
                # 2. LLM Extraction
                analysis = extract_contract_info(raw_text)
                
                # 3. Save to DB
                new_contract = Contract(
                    filename=filename,
                    full_text=raw_text,
                    summary=analysis['summary'],
                    termination_clause=analysis['termination'],
                    confidentiality_clause=analysis['confidentiality'],
                    liability_clause=analysis['liability']
                )
                db.session.add(new_contract)
                db.session.commit()
                
                results.append(new_contract.to_dict())

        # 4. Save to CSV
        df = pd.DataFrame(results)
        df.to_csv("contract_analysis_results.csv", index=False)
        print("Pipeline Complete. Results saved to contract_analysis_results.csv")

if __name__ == "__main__":
    run_pipeline()