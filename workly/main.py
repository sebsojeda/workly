from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import crud, models, schema
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Workly", version="0.1.0", description="Workly API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def docs_redirect():
    return RedirectResponse(url="/docs")


@app.post("/employers", response_model=schema.Employer)
def create_employer(employer: schema.EmployerCreate, db: Session = Depends(get_db)):
    db_employer = crud.get_employer_by_email(db, email=employer.email)
    if db_employer:
        raise HTTPException(400, detail="Email already registered")
    return crud.create_employer(db=db, employer=employer)


@app.put("/employers/{employer_id}", response_model=schema.Employer)
def update_employer(
    employer: schema.EmployerUpdate, employer_id: int, db: Session = Depends(get_db)
):
    db_employer = crud.get_employer(db, employer_id=employer_id)
    if db_employer is None:
        raise HTTPException(404, detail="Employer not found")
    return crud.update_employer(db=db, employer=employer, employer_id=employer_id)


@app.get("/employers", response_model=list[schema.Employer])
def read_employers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employers = crud.get_employers(db, skip=skip, limit=limit)
    return employers


@app.get("/employers/{employer_id}", response_model=schema.Employer)
def read_employer(employer_id: int, db: Session = Depends(get_db)):
    db_employer = crud.get_employer(db, employer_id=employer_id)
    if db_employer is None:
        raise HTTPException(404, detail="Employer not found")
    return db_employer


@app.delete("/employers/{employer_id}", response_model=schema.Employer)
def delete_employer(employer_id: int, db: Session = Depends(get_db)):
    db_employer = crud.get_employer(db, employer_id=employer_id)
    if db_employer is None:
        raise HTTPException(404, detail="Employer not found")
    return crud.delete_employer(db=db, employer_id=employer_id)


@app.post("/jobs", response_model=schema.Job)
def create_job_for_employer(job: schema.JobCreate, db: Session = Depends(get_db)):
    return crud.create_employer_job(db=db, job=job)


@app.put("/jobs/{job_id}", response_model=schema.Job)
def update_job(job: schema.JobUpdate, job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(404, detail="Job not found")
    return crud.update_job(db=db, job=job, job_id=job_id)


@app.get("/jobs", response_model=list[schema.Job])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return jobs


@app.get("/jobs/{job_id}", response_model=schema.Job)
def read_job(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(404, detail="Job not found")
    return db_job


@app.delete("/jobs/{job_id}", response_model=schema.Job)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(404, detail="Job not found")
    return crud.delete_job(db=db, job_id=job_id)


@app.post("/applicants", response_model=schema.Applicant)
def create_applicant(applicant: schema.ApplicantCreate, db: Session = Depends(get_db)):
    db_applicant = crud.get_applicant_by_email(db, email=applicant.email)
    if db_applicant:
        raise HTTPException(400, detail="Email already registered")
    return crud.create_applicant(db=db, applicant=applicant)


@app.put("/applicants/{applicant_id}", response_model=schema.Applicant)
def update_applicant(
    applicant: schema.ApplicantUpdate, applicant_id: int, db: Session = Depends(get_db)
):
    db_applicant = crud.get_applicant(db, applicant_id=applicant_id)
    if db_applicant is None:
        raise HTTPException(404, detail="Applicant not found")
    return crud.update_applicant(db=db, applicant=applicant, applicant_id=applicant_id)


@app.get("/applicants", response_model=list[schema.Applicant])
def read_applicants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    applicants = crud.get_applicants(db, skip=skip, limit=limit)
    return applicants


@app.get("/applicants/{applicant_id}", response_model=schema.Applicant)
def read_applicant(applicant_id: int, db: Session = Depends(get_db)):
    db_applicant = crud.get_applicant(db, applicant_id=applicant_id)
    if db_applicant is None:
        raise HTTPException(404, detail="Applicant not found")
    return db_applicant


@app.delete("/applicants/{applicant_id}", response_model=schema.Applicant)
def delete_applicant(applicant_id: int, db: Session = Depends(get_db)):
    db_applicant = crud.get_applicant(db, applicant_id=applicant_id)
    if db_applicant is None:
        raise HTTPException(404, detail="Applicant not found")
    return crud.delete_applicant(db=db, applicant_id=applicant_id)


@app.post("/resumes", response_model=schema.Resume)
def create_resume_for_applicant(
    resume: schema.ResumeCreate, db: Session = Depends(get_db)
):
    return crud.create_applicant_resume(db=db, resume=resume)


@app.put("/resumes/{resume_id}", response_model=schema.Resume)
def update_resume(
    resume: schema.ResumeUpdate, resume_id: int, db: Session = Depends(get_db)
):
    db_resume = crud.get_resume(db, resume_id=resume_id)
    if db_resume is None:
        raise HTTPException(404, detail="Resume not found")
    return crud.update_resume(db=db, resume=resume, resume_id=resume_id)


@app.get("/resumes", response_model=list[schema.Resume])
def read_resumes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    resumes = crud.get_resumes(db, skip=skip, limit=limit)
    return resumes


@app.get("/resumes/{resume_id}", response_model=schema.Resume)
def read_resume(resume_id: int, db: Session = Depends(get_db)):
    db_resume = crud.get_resume(db, resume_id=resume_id)
    if db_resume is None:
        raise HTTPException(404, detail="Resume not found")
    return db_resume


@app.delete("/resumes/{resume_id}", response_model=schema.Resume)
def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    db_resume = crud.get_resume(db, resume_id=resume_id)
    if db_resume is None:
        raise HTTPException(404, detail="Resume not found")
    return crud.delete_resume(db=db, resume_id=resume_id)


@app.post("/applications", response_model=schema.Application)
def create_application_for_job(
    application: schema.ApplicationCreate, db: Session = Depends(get_db)
):
    return crud.create_application(db=db, application=application)


@app.put("/applications/{application_id}", response_model=schema.Application)
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


@app.get("/applications", response_model=list[schema.Application])
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    applications = crud.get_applications(db, skip=skip, limit=limit)
    return applications


@app.get("/applications/{application_id}", response_model=schema.Application)
def read_application(application_id: int, db: Session = Depends(get_db)):
    db_application = crud.get_application(db, application_id=application_id)
    if db_application is None:
        raise HTTPException(404, detail="Application not found")
    return db_application


@app.delete("/applications/{application_id}", response_model=schema.Application)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    db_application = crud.get_application(db, application_id=application_id)
    if db_application is None:
        raise HTTPException(404, detail="Application not found")
    return crud.delete_application(db=db, application_id=application_id)
