from fastapi import FastAPI
from database import get_db
from schemas import (
    PregnancyCreate,
    SymptomCreate,
    AppointmentCreate,
    SymptomAnalysisRequest
)

app = FastAPI(title="MotherCare 360")


@app.get("/")
def home():
    return {
        "message": "MotherCare 360 Backend is running"
    }


def create_tables():
    db = get_db()
    cursor = db.cursor()

    # Pregnancy information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pregnancy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            pregnancy_week INTEGER,
            due_date TEXT
        )
    """)

    # Symptoms
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS symptoms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptom TEXT,
            pregnancy_week INTEGER,
            created_at TEXT
        )
    """)

    # Doctor appointments
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor TEXT,
            date TEXT,
            purpose TEXT
        )
    """)

    db.commit()
    db.close()


create_tables()
@app.post("/pregnancy")
def add_pregnancy(data: PregnancyCreate):

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO pregnancy (name, pregnancy_week, due_date)
        VALUES (?, ?, ?)
        """,
        (data.name, data.pregnancy_week, data.due_date)
    )

    db.commit()
    db.close()

    return {
        "message": "Pregnancy information saved successfully"
    }
@app.get("/pregnancy")
def get_pregnancy():

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT id, name, pregnancy_week, due_date
        FROM pregnancy
        """
    )

    pregnancies = cursor.fetchall()
    db.close()

    result = []

    for pregnancy in pregnancies:
        result.append({
            "id": pregnancy[0],
            "name": pregnancy[1],
            "pregnancy_week": pregnancy[2],
            "due_date": pregnancy[3]
        })

    return result
@app.get("/symptoms")
def get_symptoms():

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT id, symptom, pregnancy_week, created_at
        FROM symptoms
        ORDER BY id DESC
        """
    )

    symptoms = cursor.fetchall()
    db.close()

    result = []

    for symptom in symptoms:
        result.append({
            "id": symptom[0],
            "symptom": symptom[1],
            "pregnancy_week": symptom[2],
            "created_at": symptom[3]
        })

    return result
@app.post("/symptoms")
def add_symptom(data: SymptomCreate):

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO symptoms (symptom, pregnancy_week, created_at)
        VALUES (?, ?, datetime('now'))
        """,
        (data.symptom, data.pregnancy_week)
    )

    db.commit()
    db.close()

    return {
        "message": "Symptom saved successfully"
    }
@app.get("/symptoms")
def get_symptoms():

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT id, symptom, pregnancy_week, created_at
        FROM symptoms
        ORDER BY id DESC
        """
    )

    symptoms = cursor.fetchall()
    db.close()

    result = []

    for symptom in symptoms:
        result.append({
            "id": symptom[0],
            "symptom": symptom[1],
            "pregnancy_week": symptom[2],
            "created_at": symptom[3]
        })

    return result
@app.post("/appointments")
def add_appointment(data: AppointmentCreate):

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO appointments (doctor, date, purpose)
        VALUES (?, ?, ?)
        """,
        (data.doctor, data.date, data.purpose)
    )

    db.commit()
    db.close()

    return {
        "message": "Appointment saved successfully"
    }
@app.get("/appointments")
def get_appointments():

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT id, doctor, date, purpose
        FROM appointments
        ORDER BY id DESC
        """
    )

    appointments = cursor.fetchall()
    db.close()

    result = []

    for appointment in appointments:
        result.append({
            "id": appointment[0],
            "doctor": appointment[1],
            "date": appointment[2],
            "purpose": appointment[3]
        })

    return result
@app.get("/timeline")
def get_timeline():

    db = get_db()
    cursor = db.cursor()

    timeline = []

    # Get symptoms
    cursor.execute("""
        SELECT symptom, pregnancy_week, created_at
        FROM symptoms
        ORDER BY created_at DESC
    """)

    symptoms = cursor.fetchall()

    for symptom in symptoms:
        timeline.append({
            "type": "symptom",
            "description": symptom[0],
            "pregnancy_week": symptom[1],
            "date": symptom[2]
        })

    # Get appointments
    cursor.execute("""
        SELECT doctor, date, purpose
        FROM appointments
        ORDER BY date DESC
    """)

    appointments = cursor.fetchall()

    for appointment in appointments:
        timeline.append({
            "type": "appointment",
            "description": appointment[2],
            "doctor": appointment[0],
            "date": appointment[1]
        })

    db.close()

    return timeline
@app.post("/analyze-symptom")
def analyze_symptom(data: SymptomAnalysisRequest):

    return {
        "symptom": data.symptom,
        "pregnancy_week": data.pregnancy_week,
        "message": "Symptom received for AI analysis"
    }