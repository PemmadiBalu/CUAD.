
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text)
    termination_clause = db.Column(db.Text)
    confidentiality_clause = db.Column(db.Text)
    liability_clause = db.Column(db.Text)
    full_text = db.Column(db.Text)

    def to_dict(self):
        return {
            "contract_id": self.id,
            "filename": self.filename,
            "summary": self.summary,
            "termination_clause": self.termination_clause,
            "confidentiality_clause": self.confidentiality_clause,
            "liability_clause": self.liability_clause
        }