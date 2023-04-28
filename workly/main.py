from sqlite3 import Connection as SQLite3Connection

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from . import crud, models, schema
from .database import SessionLocal, engine
from .seed import seedDatabase

app = FastAPI(title="Workly", version="0.1.0", description="Workly API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event(event_type="startup")
def startup_event():
    models.Base.metadata.create_all(bind=engine)
    seedDatabase(next(get_db()))


@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url="/docs", status_code=301)


@app.get("/healthcheck", include_in_schema=False, status_code=200)
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1")).fetchone()
    return {"status": "ok"}


@app.post(
    "/employers",
    response_model=schema.Employer,
    tags=["employers"],
    status_code=201,
    description="Create an employer",
)
def create_employer(employer: schema.EmployerCreate, db: Session = Depends(get_db)):
    db_employer = crud.get_employer_by_email(db, email=employer.email)
    if db_employer:
        raise HTTPException(400, detail="Email already registered")
    return crud.create_employer(db=db, employer=employer)


@app.put(
    "/employers/{employer_id}",
    response_model=schema.Employer,
    tags=["employers"],
    status_code=200,
    description="Update an employer",
)
def update_employer(
    employer: schema.EmployerUpdate, employer_id: int, db: Session = Depends(get_db)
):
    db_employer = crud.get_employer(db, employer_id=employer_id)
    if db_employer is None:
        raise HTTPException(404, detail="Employer not found")
    return crud.update_employer(db=db, employer=employer, employer_id=employer_id)


@app.get(
    "/employers",
    response_model=list[schema.Employer],
    tags=["employers"],
    status_code=200,
    description="Get all employers",
)
def read_employers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employers = crud.get_employers(db, skip=skip, limit=limit)
    return employers


@app.get(
    "/employers/{employer_id}",
    response_model=schema.Employer,
    tags=["employers"],
    status_code=200,
    description="Get an employer",
)
def read_employer(employer_id: int, db: Session = Depends(get_db)):
    db_employer = crud.get_employer(db, employer_id=employer_id)
    if db_employer is None:
        raise HTTPException(404, detail="Employer not found")
    return db_employer


@app.delete(
    "/employers/{employer_id}",
    tags=["employers"],
    status_code=204,
    description="Delete an employer",
)
def delete_employer(employer_id: int, db: Session = Depends(get_db)):
    db_employer = crud.get_employer(db, employer_id=employer_id)
    if db_employer is None:
        raise HTTPException(404, detail="Employer not found")
    crud.delete_employer(db=db, employer_id=employer_id)


@app.post(
    "/jobs",
    response_model=schema.Job,
    tags=["jobs"],
    status_code=201,
    description="Create a job",
)
def create_job_for_employer(job: schema.JobCreate, db: Session = Depends(get_db)):
    return crud.create_employer_job(db=db, job=job)


@app.put(
    "/jobs/{job_id}",
    response_model=schema.Job,
    tags=["jobs"],
    status_code=200,
    description="Update a job",
)
def update_job(job: schema.JobUpdate, job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(404, detail="Job not found")
    return crud.update_job(db=db, job=job, job_id=job_id)


@app.get(
    "/jobs",
    response_model=list[schema.Job],
    tags=["jobs"],
    status_code=200,
    description="Get all jobs",
)
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return jobs


@app.get(
    "/jobs/{job_id}",
    response_model=schema.Job,
    tags=["jobs"],
    status_code=200,
    description="Get a job",
)
def read_job(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(404, detail="Job not found")
    return db_job


@app.delete(
    "/jobs/{job_id}", tags=["jobs"], status_code=204, description="Delete a job"
)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(404, detail="Job not found")
    crud.delete_job(db=db, job_id=job_id)


@app.post(
    "/applicants",
    response_model=schema.Applicant,
    tags=["applicants"],
    status_code=201,
    description="Create an applicant",
)
def create_applicant(applicant: schema.ApplicantCreate, db: Session = Depends(get_db)):
    db_applicant = crud.get_applicant_by_email(db, email=applicant.email)
    if db_applicant:
        raise HTTPException(400, detail="Email already registered")
    return crud.create_applicant(db=db, applicant=applicant)


@app.put(
    "/applicants/{applicant_id}",
    response_model=schema.Applicant,
    tags=["applicants"],
    status_code=200,
    description="Update an applicant",
)
def update_applicant(
    applicant: schema.ApplicantUpdate, applicant_id: int, db: Session = Depends(get_db)
):
    db_applicant = crud.get_applicant(db, applicant_id=applicant_id)
    if db_applicant is None:
        raise HTTPException(404, detail="Applicant not found")
    return crud.update_applicant(db=db, applicant=applicant, applicant_id=applicant_id)


@app.get(
    "/applicants",
    response_model=list[schema.Applicant],
    tags=["applicants"],
    status_code=200,
    description="Get all applicants",
)
def read_applicants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    applicants = crud.get_applicants(db, skip=skip, limit=limit)
    return applicants


@app.get(
    "/applicants/{applicant_id}",
    response_model=schema.Applicant,
    tags=["applicants"],
    status_code=200,
    description="Get an applicant",
)
def read_applicant(applicant_id: int, db: Session = Depends(get_db)):
    db_applicant = crud.get_applicant(db, applicant_id=applicant_id)
    if db_applicant is None:
        raise HTTPException(404, detail="Applicant not found")
    return db_applicant


@app.delete(
    "/applicants/{applicant_id}",
    tags=["applicants"],
    status_code=204,
    description="Delete an applicant",
)
def delete_applicant(applicant_id: int, db: Session = Depends(get_db)):
    db_applicant = crud.get_applicant(db, applicant_id=applicant_id)
    if db_applicant is None:
        raise HTTPException(404, detail="Applicant not found")
    crud.delete_applicant(db=db, applicant_id=applicant_id)


@app.post(
    "/resumes",
    response_model=schema.Resume,
    tags=["resumes"],
    status_code=201,
    description="Create a resume",
)
def create_resume_for_applicant(
    resume: schema.ResumeCreate, db: Session = Depends(get_db)
):
    return crud.create_applicant_resume(db=db, resume=resume)


@app.put(
    "/resumes/{resume_id}",
    response_model=schema.Resume,
    tags=["resumes"],
    status_code=200,
    description="Update a resume",
)
def update_resume(
    resume: schema.ResumeUpdate, resume_id: int, db: Session = Depends(get_db)
):
    db_resume = crud.get_resume(db, resume_id=resume_id)
    if db_resume is None:
        raise HTTPException(404, detail="Resume not found")
    return crud.update_resume(db=db, resume=resume, resume_id=resume_id)


@app.get(
    "/resumes",
    response_model=list[schema.Resume],
    tags=["resumes"],
    status_code=200,
    description="Get all resumes",
)
def read_resumes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    resumes = crud.get_resumes(db, skip=skip, limit=limit)
    return resumes


@app.get(
    "/resumes/{resume_id}",
    response_model=schema.Resume,
    tags=["resumes"],
    status_code=200,
    description="Get a resume",
)
def read_resume(resume_id: int, db: Session = Depends(get_db)):
    db_resume = crud.get_resume(db, resume_id=resume_id)
    if db_resume is None:
        raise HTTPException(404, detail="Resume not found")
    return db_resume


@app.delete(
    "/resumes/{resume_id}",
    tags=["resumes"],
    status_code=204,
    description="Delete a resume",
)
def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    db_resume = crud.get_resume(db, resume_id=resume_id)
    if db_resume is None:
        raise HTTPException(404, detail="Resume not found")
    crud.delete_resume(db=db, resume_id=resume_id)


@app.post(
    "/applications",
    response_model=schema.Application,
    tags=["applications"],
    status_code=201,
    description="Create an application",
)
def create_application_for_job(
    application: schema.ApplicationCreate, db: Session = Depends(get_db)
):
    return crud.create_application(db=db, application=application)


@app.put(
    "/applications/{application_id}",
    response_model=schema.Application,
    tags=["applications"],
    status_code=200,
    description="Update an application",
)
def update_application(
    application: schema.ApplicationUpdate,
    application_id: int,
    db: Session = Depends(get_db),
):
    db_application = crud.get_application(db, application_id=application_id)
    if db_application is None:
        raise HTTPException(404, detail="Application not found")
    return crud.update_application(
        db=db, application=application, application_id=application_id
    )


@app.get(
    "/applications",
    response_model=list[schema.Application],
    tags=["applications"],
    status_code=200,
    description="Get all applications",
)
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    applications = crud.get_applications(db, skip=skip, limit=limit)
    return applications


@app.get(
    "/applications/{application_id}",
    response_model=schema.Application,
    tags=["applications"],
    status_code=200,
    description="Get an application",
)
def read_application(application_id: int, db: Session = Depends(get_db)):
    db_application = crud.get_application(db, application_id=application_id)
    if db_application is None:
        raise HTTPException(404, detail="Application not found")
    return db_application


@app.delete(
    "/applications/{application_id}",
    tags=["applications"],
    status_code=204,
    description="Delete an application",
)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    db_application = crud.get_application(db, application_id=application_id)
    if db_application is None:
        raise HTTPException(404, detail="Application not found")
    crud.delete_application(db=db, application_id=application_id)
