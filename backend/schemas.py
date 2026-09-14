from pydantic import BaseModel


class PregnancyCreate(BaseModel):
    name: str
    pregnancy_week: int
    due_date: str
class SymptomCreate(BaseModel):
    symptom: str
    pregnancy_week: int
class AppointmentCreate(BaseModel):
    doctor: str
    date: str
    purpose: str
class SymptomAnalysisRequest(BaseModel):
    symptom: str
    pregnancy_week: int