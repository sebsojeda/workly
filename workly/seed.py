from . import crud, models, schema
from .database import SessionLocal

seed_data = {
    "employers": [
        {
            "name": "Apple",
            "email": "steve.jobs@apple.com",
            "phone": "1234567890",
        },
        {
            "name": "Meta",
            "email": "mark.zuckerberg@meta.com",
            "phone": "1234567890",
        },
        {
            "name": "Google",
            "email": "sundar.pichai@google.com",
            "phone": "1234567890",
        },
    ],
    "jobs": [
        {
            "id": 1,
            "title": "Designer",
            "description": "A designer",
            "location": "San Francisco, CA",
            "salary": 100000,
            "status": models.JobStatus.OPEN,
            "employerId": 1,
        },
        {
            "id": 2,
            "title": "Software Engineer",
            "description": "A software engineer",
            "location": "Menlo Park, CA",
            "salary": 150000,
            "status": models.JobStatus.OPEN,
            "employerId": 2,
        },
        {
            "id": 3,
            "title": "Software Engineer",
            "description": "A software engineer",
            "location": "Mountain View, CA",
            "salary": 200000,
            "status": models.JobStatus.OPEN,
            "employerId": 3,
        },
    ],
    "applicants": [
        {
            "name": "Jony Ives",
            "email": "jony.ives@apple.com",
            "phone": "1234567890",
        },
        {
            "name": "Sheryl Sandberg",
            "email": "sheryl.sandberg@meta.com",
            "phone": "1234567890",
        },
        {
            "name": "Guido van Rossum",
            "email": "guido.vanrossum@python.org",
            "phone": "1234567890",
        },
    ],
    "resumes": [
        {
            "id": 1,
            "applicantId": 1,
            "resume": "I'm a designer and I love Apple",
        },
        {
            "id": 2,
            "applicantId": 2,
            "resume": "I'm a software engineer and I love Meta",
        },
        {
            "id": 3,
            "applicantId": 3,
            "resume": "I'm a software engineer and I love Python",
        },
    ],
    "applications": [
        {
            "id": 1,
            "jobId": 1,
            "resumeId": 1,
            "coverLetter": "I love Apple",
            "status": models.ApplicationStatus.PENDING,
        },
        {
            "id": 2,
            "jobId": 2,
            "resumeId": 2,
            "coverLetter": "I love Meta",
            "status": models.ApplicationStatus.PENDING,
        },
        {
            "id": 3,
            "jobId": 3,
            "resumeId": 3,
            "coverLetter": "I love Python",
            "status": models.ApplicationStatus.PENDING,
        },
    ],
}


def seed_database(db: SessionLocal) -> None:
    """
    Seed the database with data if the database is empty.
    """

    for employer in seed_data["employers"]:
        if not crud.get_employer_by_email(db, email=employer["email"]):
            new_employer = schema.EmployerCreate(
                name=employer["name"],
                email=employer["email"],
                phone=employer["phone"],
            )
            crud.create_employer(db, employer=new_employer)

    for job in seed_data["jobs"]:
        if not crud.get_job(db, job_id=job["id"]):
            new_job = schema.JobCreate(
                title=job["title"],
                description=job["description"],
                location=job["location"],
                salary=job["salary"],
                status=job["status"],
                employerId=job["employerId"],
            )
            crud.create_employer_job(db, job=new_job)

    for applicant in seed_data["applicants"]:
        if not crud.get_applicant_by_email(db, email=applicant["email"]):
            new_applicant = schema.ApplicantCreate(
                name=applicant["name"],
                email=applicant["email"],
                phone=applicant["phone"],
            )
            crud.create_applicant(db, applicant=new_applicant)

    for resume in seed_data["resumes"]:
        if not crud.get_resume(db, resume_id=resume["id"]):
            new_resume = schema.ResumeCreate(
                applicantId=resume["applicantId"],
                resume=resume["resume"],
            )
            crud.create_applicant_resume(db, resume=new_resume)

    for application in seed_data["applications"]:
        if not crud.get_application(db, application_id=application["id"]):
            new_application = schema.ApplicationCreate(
                jobId=application["jobId"],
                resumeId=application["resumeId"],
                coverLetter=application["coverLetter"],
                status=application["status"],
            )
            crud.create_application(db, application=new_application)
