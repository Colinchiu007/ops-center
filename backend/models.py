"""SQLAlchemy models for OpsCenter config management."""
import datetime
from sqlalchemy import Column, String, Integer, Text, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Project(Base):
    __tablename__ = "projects"

    code = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    config_file_path = Column(String, default="")
    config_format = Column(String, default="yaml")
    enabled = Column(Integer, default=1)

    config_items = relationship("ConfigItem", back_populates="project")


class ConfigItem(Base):
    __tablename__ = "config_items"

    id = Column(String, primary_key=True)
    project_code = Column(String, ForeignKey("projects.code"), nullable=False)
    category = Column(String, nullable=False)
    key = Column(String, nullable=False)
    value = Column(Text, nullable=False, default="")
    value_type = Column(String, default="string")
    description = Column(Text, default="")
    is_secret = Column(Integer, default=0)
    is_required = Column(Integer, default=0)
    default_value = Column(Text, default="")
    created_at = Column(String, default=lambda: datetime.datetime.utcnow().isoformat())
    updated_at = Column(String, default=lambda: datetime.datetime.utcnow().isoformat())
    updated_by = Column(String, default="")

    project = relationship("Project", back_populates="config_items")


class ConfigAuditLog(Base):
    __tablename__ = "config_audit_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    config_id = Column(String, nullable=False)
    old_value = Column(Text, default="")
    new_value = Column(Text, default="")
    changed_by = Column(String, nullable=False)
    changed_at = Column(String, default=lambda: datetime.datetime.utcnow().isoformat())
    change_type = Column(String, nullable=False)
    source_ip = Column(String, default="")


class OfficialKey(Base):
    __tablename__ = "official_keys"

    id = Column(String, primary_key=True)  # "openai-gpt4o"
    provider = Column(String, nullable=False)  # openai / doubao / minimax / ...
    name = Column(String, nullable=False)  # "OpenAI GPT-4o"
    api_key = Column(Text, nullable=False)  # Fernet encrypted
    base_url = Column(String, default="")
    models = Column(Text, default="[]")  # JSON array
    priority = Column(Integer, default=1)
    is_active = Column(Integer, default=1)
    tier_access = Column(Integer, default=1)  # 1=all tiers, 2=standard+, 3=pro only
    cost_per_1k_tokens = Column(Float, default=0.0)
    expires_at = Column(String, default="")
    created_at = Column(String, default=lambda: datetime.datetime.utcnow().isoformat())
    updated_at = Column(String, default=lambda: datetime.datetime.utcnow().isoformat())
