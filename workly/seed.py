from . import crud, models, schema
from .database import SessionLocal


def seedDatabase(db: SessionLocal) -> None:
    employer = crud.get_employer_by_email(db, email="john.doe@example.com")
    if not employer:
        new_employer = schema.EmployerCreate(
            name="John Doe", email="john.doe@example.com", phone="1234567890"
        )
        employer = crud.create_employer(db, employer=new_employer)

    job = crud.get_job(db, job_id=1)
    if not job:
        new_job = schema.JobCreate(
            title="Software Engineer",
            description="A software engineer",
            location="San Francisco",
            salary=100000,
            status=models.JobStatus.OPEN,
            employerId=employer.id,
        )
        job = crud.create_employer_job(db, job=new_job)

    applicant = crud.get_applicant_by_email(db, email="steve.jobs@example.com")
    if not applicant:
        new_applicant = schema.ApplicantCreate(
            name="Steve Jobs", email="steve.jobs@example.com", phone="1234567890"
        )
        applicant = crud.create_applicant(db, applicant=new_applicant)

    resume = crud.get_resume(db, resume_id=1)
    if not resume:
        new_resume = schema.ResumeCreate(
            applicantId=applicant.id,
            resume="This is my resume",
        )
        resume = crud.create_applicant_resume(db, resume=new_resume)

    application = crud.get_application(db, application_id=1)
    if not application:
        new_application = schema.ApplicationCreate(
            jobId=job.id,
            applicantId=applicant.id,
            resumeId=resume.id,
            coverLetter="This is my cover letter",
            status=models.ApplicationStatus.PENDING,
        )
        application = crud.create_application(db, application=new_application)
