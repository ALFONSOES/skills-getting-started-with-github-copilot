"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Equipo de Baloncesto": {
        "description": "Únete a nuestro equipo competitivo de baloncesto y participa en torneos entre escuelas",
        "schedule": "Lunes y Miércoles, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Club de Tenis": {
        "description": "Desarrolla habilidades de tenis y compite en partidos amistosos",
        "schedule": "Martes y Jueves, 4:00 PM - 5:00 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu"]
    },
    "Club de Drama": {
        "description": "Actúa en obras de teatro y producciones teatrales escolares",
        "schedule": "Miércoles, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Estudio de Arte": {
        "description": "Explora pintura, escultura y otras artes visuales",
        "schedule": "Sábados, 10:00 AM - 12:00 PM",
        "max_participants": 18,
        "participants": ["mia@mergington.edu"]
    },
    "Equipo de Debate": {
        "description": "Desarrolla habilidades de argumentación y expresión oral a través de debates",
        "schedule": "Viernes, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    },
    "Club de Ciencias": {
        "description": "Realiza experimentos y explora descubrimientos científicos",
        "schedule": "Jueves, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["sophia@mergington.edu"]
    },
    "Club de Ajedrez": {
        "description": "Aprende estrategias y compite en torneos de ajedrez",
        "schedule": "Viernes, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Clase de Programación": {
        "description": "Aprende fundamentos de programación y construye proyectos de software",
        "schedule": "Martes y Jueves, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Clase de Educación Física": {
        "description": "Educación física y actividades deportivas",
        "schedule": "Lunes, Miércoles, Viernes, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
# Validar que el estudiante no esté ya registrado
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if student is already signed up
    activity = activities[activity_name]
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}

@app.post("/activities/{activity_name}/remove")
def remove_participant_from_activity(activity_name: str, email: str):
    """Remove a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]
    
    # Check if student is signed up
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Removed {email} from {activity_name}"}
