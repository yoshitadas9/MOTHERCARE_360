import time
from prism import send_trace
from fastapi import FastAPI
from database import get_db
from schemas import (
    PregnancyCreate,
    SymptomCreate,
    AppointmentCreate,
    SymptomAnalysisRequest,
    HealthEventCreate
)
from dotenv import load_dotenv

load_dotenv()

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
    db.execute("""
        CREATE TABLE IF NOT EXISTS health_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            description TEXT,
            pregnancy_week INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

    symptoms = db.execute("""
        SELECT symptom, pregnancy_week, created_at
        FROM symptoms
    """).fetchall()

    appointments = db.execute("""
        SELECT doctor, date, purpose
        FROM appointments
    """).fetchall()

    health_events = db.execute("""
        SELECT event_type, description, pregnancy_week, created_at
        FROM health_events
    """).fetchall()

    db.close()

    timeline = []

    # Symptoms
    for item in symptoms:
        timeline.append({
            "type": "symptom",
            "title": item[0],
            "pregnancy_week": item[1],
            "date": item[2]
        })

    # Appointments
    for item in appointments:
        timeline.append({
            "type": "appointment",
            "title": item[2],
            "doctor": item[0],
            "date": item[1]
        })

    # Health events
    for item in health_events:
        timeline.append({
            "type": "health_event",
            "title": item[0],
            "description": item[1],
            "pregnancy_week": item[2],
            "date": item[3]
        })

    # Newest first
    timeline.sort(
        key=lambda x: x.get("date", ""),
        reverse=True
    )

    return timeline
@app.post("/analyze-symptom")
def analyze_symptom(data: SymptomAnalysisRequest):

    start_time = time.time()

    ai_response = (
        f"Your symptom '{data.symptom}' has been received. "
        "Please consult a qualified healthcare professional for "
        "personalized medical advice."
    )

    latency_ms = int((time.time() - start_time) * 1000)

    send_trace(
        data.symptom,
        ai_response,
        data.pregnancy_week,
        latency_ms
    )

    return {
        "symptom": data.symptom,
        "pregnancy_week": data.pregnancy_week,
        "message": ai_response
    }
@app.post("/health-events")
def create_health_event(data: HealthEventCreate):

    db = get_db()

    db.execute(
        """
        INSERT INTO health_events
        (event_type, description, pregnancy_week)
        VALUES (?, ?, ?)
        """,
        (
            data.event_type,
            data.description,
            data.pregnancy_week
        )
    )

    db.commit()
    db.close()

    return {
        "message": "Health event added successfully",
        "event_type": data.event_type,
        "description": data.description,
        "pregnancy_week": data.pregnancy_week
    }
@app.get("/health-events")
def get_health_events():

    db = get_db()

    events = db.execute(
        """
        SELECT id, event_type, description,
               pregnancy_week, created_at
        FROM health_events
        ORDER BY created_at DESC
        """
    ).fetchall()

    db.close()

    return [
        {
            "id": event[0],
            "event_type": event[1],
            "description": event[2],
            "pregnancy_week": event[3],
            "created_at": event[4]
        }
        for event in events
    ]