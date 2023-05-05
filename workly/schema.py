from datetime import datetime

from pydantic import BaseModel, Field

from . import models


class EmployerBase(BaseModel):
    name: str = Field(example="John Doe", max_length=255, min_length=1)
    email: str = Field(example="john.doe@example.com", max_length=255, min_length=1)
    phone: str | None = Field(
        example="+1 123 456 7890", max_length=255, min_length=1, default=None
    )


class EmployerCreate(EmployerBase):
    pass


class EmployerUpdate(EmployerBase):
    pass


class Employer(EmployerCreate):
    id: int = Field(alias="employerId", title="Employer ID", gt=0, example=1)
    created_at: datetime = Field(alias="createdAt", title="Created At")
    updated_at: datetime = Field(alias="updatedAt", title="Updated At")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class JobBase(BaseModel):
    title: str = Field(example="Software Engineer", max_length=255, min_length=1)
    description: str = Field(
        example="We are looking for a software engineer...", min_length=1
    )
    location: str = Field(example="San Francisco, CA", max_length=255, min_length=1)
    salary: int = Field(example=100000, gt=0)
    status: models.JobStatus = Field(example=models.JobStatus.OPEN)


class JobCreate(JobBase):
    employer_id: int = Field(alias="employerId", title="Employer ID", gt=0, example=1)


class JobUpdate(JobBase):
    pass


class Job(JobBase):
    id: int = Field(alias="jobId", title="Job ID", gt=0, example=1)
    created_at: datetime = Field(alias="createdAt", title="Created At")
    updated_at: datetime = Field(alias="updatedAt", title="Updated At")
    employer: Employer = Field()

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ApplicantBase(BaseModel):
    name: str = Field(example="John Doe", max_length=255, min_length=1)
    email: str = Field(example="john.doe@example.com", max_length=255, min_length=1)
    phone: str | None = Field(
        example="+1 123 456 7890", max_length=255, min_length=1, default=None
    )


class ApplicantCreate(ApplicantBase):
    pass


class ApplicantUpdate(ApplicantBase):
    pass


class Applicant(ApplicantCreate):
    id: int = Field(alias="applicantId", title="Applicant ID", gt=0, example=1)
    created_at: datetime = Field(alias="createdAt", title="Created At")
    updated_at: datetime = Field(alias="updatedAt", title="Updated At")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ResumeBase(BaseModel):
    resume: str = Field(example="This is my resume...", min_length=1)


class ResumeCreate(ResumeBase):
    applicant_id: int = Field(
        alias="applicantId", title="Applicant ID", gt=0, example=1
    )


class ResumeUpdate(ResumeBase):
    pass


class Resume(ResumeBase):
    id: int = Field(alias="resumeId", title="Resume ID", gt=0, example=1)
    created_at: datetime = Field(alias="createdAt", title="Created At")
    updated_at: datetime = Field(alias="updatedAt", title="Updated At")
    applicant: Applicant = Field()

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ApplicationBase(BaseModel):
    cover_letter: str = Field(
        alias="coverLetter", example="This is my cover letter...", min_length=1
    )
    status: models.ApplicationStatus = Field(example=models.ApplicationStatus.PENDING)


class ApplicationCreate(ApplicationBase):
    job_id: int = Field(alias="jobId", title="Job ID", gt=0, example=1)
    resume_id: int = Field(alias="resumeId", title="Resume ID", gt=0, example=1)


class ApplicationUpdate(ApplicationBase):
    pass


class Application(ApplicationBase):
    id: int = Field(alias="applicationId", title="Application ID", gt=0, example=1)
    created_at: datetime = Field(alias="createdAt", title="Created At")
    updated_at: datetime = Field(alias="updatedAt", title="Updated At")
    job: Job = Field()
    resume: Resume = Field()

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Notification(BaseModel):
    message: str = Field(example="A new job was posted...", min_length=1)

    job: Job = Field()

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
