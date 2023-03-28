from datetime import datetime

from pydantic import BaseModel

from . import models


class EmployerBase(BaseModel):
    name: str
    email: str
    phone: str | None = None


class EmployerCreate(EmployerBase):
    pass


class EmployerUpdate(EmployerBase):
    pass


class Employer(EmployerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class JobBase(BaseModel):
    title: str
    description: str
    location: str
    salary: int
    status: models.JobStatus


class JobCreate(JobBase):
    employer_id: int


class JobUpdate(JobBase):
    pass


class Job(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ApplicantBase(BaseModel):
    name: str
    email: str
    phone: str | None = None


class ApplicantCreate(ApplicantBase):
    pass


class ApplicantUpdate(ApplicantBase):
    pass


class Applicant(ApplicantBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ResumeBase(BaseModel):
    resume: str


class ResumeCreate(ResumeBase):
    applicant_id: int


class ResumeUpdate(ResumeBase):
    pass


class Resume(ResumeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ApplicationBase(BaseModel):
    cover_letter: str
    status: models.ApplicationStatus


class ApplicationCreate(ApplicationBase):
    applicant_id: int
    job_id: int
    resume_id: int


class ApplicationUpdate(ApplicationBase):
    pass


class Application(ApplicationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
