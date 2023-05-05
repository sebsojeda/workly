from sqlalchemy.orm import Session

from . import models, schema


def get_employer(db: Session, employer_id: int):
    return db.query(models.Employer).filter(models.Employer.id == employer_id).first()


def get_employer_by_email(db: Session, email: str):
    return db.query(models.Employer).filter(models.Employer.email == email).first()


def get_employers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employer).offset(skip).limit(limit).all()


def create_employer(db: Session, employer: schema.EmployerCreate):
    db_employer = models.Employer(
        name=employer.name, email=employer.email, phone=employer.phone
    )
    db.add(db_employer)
    db.commit()
    db.refresh(db_employer)
    return db_employer


def update_employer(db: Session, employer: schema.EmployerUpdate, employer_id: int):
    db_employer = (
        db.query(models.Employer).filter(models.Employer.id == employer_id).first()
    )
    db_employer.name = employer.name
    db_employer.email = employer.email
    db_employer.phone = employer.phone
    db.commit()
    db.refresh(db_employer)
    return db_employer


def delete_employer(db: Session, employer_id: int):
    db_employer = (
        db.query(models.Employer).filter(models.Employer.id == employer_id).first()
    )
    db.delete(db_employer)
    db.commit()
    return db_employer


def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()


def get_jobs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    title: str = "",
    location: str = "",
    employer: str = "",
):
    return (
        db.query(models.Job)
        .filter(models.Job.title.contains(title))
        .filter(models.Job.location.contains(location))
        .filter(models.Job.employer.has(models.Employer.name.contains(employer)))
        .order_by(models.Job.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_employer_job(db: Session, job: schema.JobCreate):
    db_job = models.Job(
        title=job.title,
        description=job.description,
        location=job.location,
        salary=job.salary,
        status=job.status,
        employer_id=job.employer_id,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def update_job(db: Session, job: schema.JobUpdate, job_id: int):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    db_job.title = job.title
    db_job.description = job.description
    db_job.location = job.location
    db_job.salary = job.salary
    db_job.status = job.status
    db.commit()
    db.refresh(db_job)
    return db_job


def delete_job(db: Session, job_id: int):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    db.delete(db_job)
    db.commit()
    return db_job


def get_applicant(db: Session, applicant_id: int):
    return (
        db.query(models.Applicant).filter(models.Applicant.id == applicant_id).first()
    )


def get_applicant_by_email(db: Session, email: str):
    return db.query(models.Applicant).filter(models.Applicant.email == email).first()


def get_applicants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Applicant).offset(skip).limit(limit).all()


def create_applicant(db: Session, applicant: schema.ApplicantCreate):
    db_applicant = models.Applicant(
        name=applicant.name, email=applicant.email, phone=applicant.phone
    )
    db.add(db_applicant)
    db.commit()
    db.refresh(db_applicant)
    return db_applicant


def update_applicant(db: Session, applicant: schema.ApplicantUpdate, applicant_id: int):
    db_applicant = (
        db.query(models.Applicant).filter(models.Applicant.id == applicant_id).first()
    )
    db_applicant.name = applicant.name
    db_applicant.email = applicant.email
    db_applicant.phone = applicant.phone
    db.commit()
    db.refresh(db_applicant)
    return db_applicant


def delete_applicant(db: Session, applicant_id: int):
    db_applicant = (
        db.query(models.Applicant).filter(models.Applicant.id == applicant_id).first()
    )
    db.delete(db_applicant)
    db.commit()
    return db_applicant


def get_resume(db: Session, resume_id: int):
    return db.query(models.Resume).filter(models.Resume.id == resume_id).first()


def get_resumes(db: Session, applicant_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Resume)
        .filter(models.Resume.applicant_id == applicant_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_applicant_resume(db: Session, resume: schema.ResumeCreate):
    db_resume = models.Resume(resume=resume.resume, applicant_id=resume.applicant_id)
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume


def update_resume(db: Session, resume: schema.ResumeUpdate, resume_id: int):
    db_resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    db_resume.resume = resume.resume
    db.commit()
    db.refresh(db_resume)
    return db_resume


def delete_resume(db: Session, resume_id: int):
    db_resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    db.delete(db_resume)
    db.commit()
    return db_resume


def get_application(db: Session, application_id: int):
    return (
        db.query(models.Application)
        .filter(models.Application.id == application_id)
        .first()
    )


def get_applications(db: Session, job_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Application)
        .filter(models.Application.job_id == job_id)
        .order_by(models.Application.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_application(db: Session, application: schema.ApplicationCreate):
    db_application = models.Application(
        status=application.status,
        job_id=application.job_id,
        resume_id=application.resume_id,
        cover_letter=application.cover_letter,
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


def update_application(
    db: Session, application: schema.ApplicationUpdate, application_id: int
):
    db_application = (
        db.query(models.Application)
        .filter(models.Application.id == application_id)
        .first()
    )
    db_application.status = application.status
    db.commit()
    db.refresh(db_application)
    return db_application


def delete_application(db: Session, application_id: int):
    db_application = (
        db.query(models.Application)
        .filter(models.Application.id == application_id)
        .first()
    )
    db.delete(db_application)
    db.commit()
    return db_application


def get_notifications(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Notification)
        .order_by(models.Notification.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
