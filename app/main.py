from pathlib import Path

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import (
    ParkingError,
    calculate_exit_details,
    confirm_payment_and_exit,
    get_dashboard_data,
    record_vehicle_entry,
)


BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


app = FastAPI(
    title="Smart Parking Management System",
    description="Data Structures and Algorithms Task One",
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


@app.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    db: Session = Depends(get_db),
):
    dashboard = get_dashboard_data(db)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            **dashboard,
            "message": None,
            "error": None,
        },
    )


@app.post("/entry", response_class=HTMLResponse)
def vehicle_entry(
    request: Request,
    registration_number: str = Form(...),
    vehicle_type: str = Form("CAR"),
    db: Session = Depends(get_db),
):
    message = None
    error = None

    try:
        parking_session = record_vehicle_entry(
            db,
            registration_number,
            vehicle_type,
        )

        message = (
            "Vehicle entered successfully. "
            f"Parking session #{parking_session.session_id} "
            "has been created."
        )

    except ParkingError as exc:
        error = str(exc)

    dashboard = get_dashboard_data(db)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            **dashboard,
            "message": message,
            "error": error,
        },
    )


@app.post("/exit", response_class=HTMLResponse)
def vehicle_exit(
    request: Request,
    registration_number: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        parking_session = calculate_exit_details(
            db,
            registration_number,
        )

        return templates.TemplateResponse(
            request=request,
            name="payment.html",
            context={
                "session": parking_session,
                "vehicle": parking_session.vehicle,
                "slot": parking_session.parking_slot,
                "error": None,
            },
        )

    except ParkingError as exc:
        dashboard = get_dashboard_data(db)

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                **dashboard,
                "message": None,
                "error": str(exc),
            },
        )


@app.post(
    "/payment/{session_id}",
    response_class=HTMLResponse,
)
def process_payment(
    request: Request,
    session_id: int,
    payment_method: str = Form("SIMULATED"),
    db: Session = Depends(get_db),
):
    try:
        result = confirm_payment_and_exit(
            db,
            session_id,
            payment_method,
        )

        return templates.TemplateResponse(
            request=request,
            name="exit-success.html",
            context={
                "session": result["session"],
                "payment_status": result[
                    "payment_status"
                ],
                "barrier_status": result[
                    "barrier_status"
                ],
                "transaction_reference": result[
                    "transaction_reference"
                ],
            },
        )

    except ParkingError as exc:
        dashboard = get_dashboard_data(db)

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                **dashboard,
                "message": None,
                "error": str(exc),
            },
        )


@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "system": "Smart Parking Management System",
    }
