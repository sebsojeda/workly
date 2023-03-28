import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )


class Employer(Base):
    __tablename__ = "employers"

    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20))

    jobs: Mapped[List["Job"]] = relationship(back_populates="employer")

    def __repr__(self):
        return f"Employer(id={self.id!r}, name={self.name!r}, email={self.email!r}, phone={self.phone!r})"


class JobStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"


class Job(Base):
    __tablename__ = "jobs"

    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(500))
    location: Mapped[str] = mapped_column(String(100))
    salary: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(Enum(JobStatus))
    employer_id: Mapped[int] = mapped_column(ForeignKey("employers.id"))

    employer: Mapped[Employer] = relationship(back_populates="jobs")
    applications: Mapped[List["Application"]] = relationship(back_populates="job")

    def __repr__(self):
        return f"Job(id={self.id!r}, title={self.title!r}, description={self.description!r}, salary={self.salary!r}, status={self.status!r}, employer_id={self.employer_id!r})"


class Applicant(Base):
    __tablename__ = "applicants"

    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20))

    resumes: Mapped[List["Resume"]] = relationship(back_populates="applicant")
    applications: Mapped[List["Application"]] = relationship(back_populates="applicant")

    def __repr__(self):
        return f"Applicant(id={self.id!r}, name={self.name!r}, email={self.email!r}, phone={self.phone!r})"


class Resume(Base):
    __tablename__ = "resumes"

    resume: Mapped[str] = mapped_column(String(1000))
    applicant_id: Mapped[int] = mapped_column(ForeignKey("applicants.id"))

    applicant: Mapped[Applicant] = relationship(back_populates="resumes")
    applications: Mapped[List["Application"]] = relationship(back_populates="resume")

    def __repr__(self):
        return f"Resume(id={self.id!r}, resume={self.resume!r}, applicant_id={self.applicant_id!r})"


class ApplicationStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Application(Base):
    __tablename__ = "applications"

    cover_letter: Mapped[str] = mapped_column(String(1000))
    status: Mapped[str] = mapped_column(Enum(ApplicationStatus))
    applicant_id: Mapped[int] = mapped_column(ForeignKey("applicants.id"))
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"))

    applicant: Mapped[Applicant] = relationship(back_populates="applications")
    job: Mapped[Job] = relationship(back_populates="applications")
    resume: Mapped[Resume] = relationship(back_populates="applications")

    def __repr__(self):
        return f"Application(id={self.id!r}, cover_letter={self.cover_letter!r}, status={self.status!r}, applicant_id={self.applicant_id!r}, job_id={self.job_id!r}, resume_id={self.resume_id!r})"
