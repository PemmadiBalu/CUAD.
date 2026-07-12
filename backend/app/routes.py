
from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
import os

from .models import db, Contract
from .pdf_proc import extract_text_from_pdf
from .llm_proc import LLMProcessor
from .search import SearchService
api = Blueprint("api", __name__)

UPLOAD_FOLDER = "data"
ALLOWED_EXTENSIONS = {"pdf"}

llm_service = LLMProcessor()
search_service = SearchService()


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# -----------------------------
# Home API
# -----------------------------
@api.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "CUAD Legal Contract Analyzer API Running"
    })


# -----------------------------
# Upload PDF
# -----------------------------
@api.route("/upload", methods=["POST"])
def upload_pdf():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    file.save(filepath)

    return jsonify({
        "message": "PDF uploaded successfully",
        "filename": filename
    }), 201


# -----------------------------
# Process Contracts
# -----------------------------
@api.route("/process-cuad-subset", methods=["POST"])
def process_subset():

    upload_folder = current_app.config.get(
        "DATA_FOLDER",
        os.path.join(os.getcwd(), "data")
    )

    upload_folder = os.path.abspath(upload_folder)

    if not os.path.exists(upload_folder):
        return jsonify({
            "success": False,
            "error": f"Data folder not found: {upload_folder}"
        }), 400

    pdf_files = [
        f for f in os.listdir(upload_folder)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_files:
        return jsonify({
            "success": False,
            "error": "No PDF files found in the data folder."
        }), 400

    processed = 0
    skipped = 0
    failed = 0

    for filename in pdf_files:

        try:

            # Skip if already processed
            if Contract.query.filter_by(filename=filename).first():
                skipped += 1
                continue

            filepath = os.path.join(upload_folder, filename)

            # Extract text
            raw_text = extract_text_from_pdf(filepath)

            if not raw_text:
                failed += 1
                continue

            # Analyze with LLM
            analysis = llm_service.extract_contract_info(raw_text)

            if not isinstance(analysis, dict):
                failed += 1
                continue

            # Create database record
            contract = Contract(
                filename=filename,
                raw_text=raw_text,
                summary=analysis.get("summary", ""),
                termination_clause=analysis.get("termination", ""),
                confidentiality_clause=analysis.get("confidentiality", ""),
                liability_clause=analysis.get("liability", "")
            )

            searchable_text = " ".join([
                contract.summary or "",
                contract.termination_clause or "",
                contract.confidentiality_clause or "",
                contract.liability_clause or ""
            ])

            contract.embedding = search_service.generate_embedding(
                searchable_text
            )

            db.session.add(contract)

            processed += 1

        except Exception as e:

            db.session.rollback()

            failed += 1

            print(f"Error processing {filename}: {e}")

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    return jsonify({
        "success": True,
        "processed_contracts": processed,
        "skipped_contracts": skipped,
        "failed_contracts": failed,
        "total_files": len(pdf_files)
    }), 200
# -----------------------------
# List Processed Contracts
# -----------------------------
@api.route("/contracts", methods=["GET"])
def get_contracts():

    contracts = Contract.query.all()

    return jsonify([
        {
            "id": c.id,
            "filename": c.filename,
            "summary": c.summary
        }
        for c in contracts
    ])