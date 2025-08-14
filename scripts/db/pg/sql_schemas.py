import datetime
import uuid
from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, MappedColumn, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from scripts.db.pg.sessions import Base


class Roles(Base):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = MappedColumn(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    name: Mapped[str] = MappedColumn(nullable=False, unique=True, index=True)
    description: Mapped[str] = MappedColumn(nullable=True)
    is_active: Mapped[bool] = MappedColumn(default=True, nullable=False, index=True)
    permissions: Mapped[JSONB] = MappedColumn(
        JSONB, nullable=True, default=dict, index=True
    )
    created_at: Mapped[datetime.datetime] = MappedColumn(default=datetime.datetime.utcnow, nullable=False, index=True)
    updated_at: Mapped[datetime.datetime] = MappedColumn(
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
        index=True,
    )
    users = relationship("Users", back_populates="role_obj")
    idx_all = Index(
        "idx_role_all",
        id,
        name,
        postgresql_using="btree",
    )


class Users(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = MappedColumn(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    email: Mapped[str] = MappedColumn(nullable=False, unique=True, index=True)
    first_name: Mapped[str] = MappedColumn(nullable=False, index=True)
    last_name: Mapped[str] = MappedColumn(nullable=False, index=True)
    password: Mapped[str] = MappedColumn(nullable=False)  # Removed index
    is_active: Mapped[bool] = MappedColumn(default=True, nullable=False, index=True)
    role: Mapped[uuid.UUID] = MappedColumn(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime.datetime] = MappedColumn(default=datetime.datetime.utcnow, nullable=False, index=True
    )
    updated_at: Mapped[datetime.datetime] = MappedColumn(default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
        index=True,
    )
    role_obj = relationship("Roles", back_populates="users")
    user_metadata = relationship(
        "UserMetadata", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    user_audit = relationship(
        "UserAudit", back_populates="user", cascade="all, delete-orphan"
    )
    idx_all = Index(
        "idx_user_all",
        id,
        email,
        first_name,
        last_name,
        postgresql_using="btree",
    )

class UserAudit(Base):
    __tablename__ = "user_audit"

    id: Mapped[uuid.UUID] = MappedColumn(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    user_id: Mapped[uuid.UUID] = MappedColumn(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    action: Mapped[str] = MappedColumn(nullable=False, index=True)
    timestamp: Mapped[datetime.datetime] = MappedColumn(default=datetime.datetime.utcnow, nullable=False, index=True
    )
    user = relationship("Users", back_populates="user_audit")

    idx_all = Index(
        "idx_user_audit_all",
        id,
        user_id,
        action,
        postgresql_using="btree",
    )

class UserMetadata(Base):
    __tablename__ = "user_metadata"

    id: Mapped[uuid.UUID] = MappedColumn(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    user_id: Mapped[uuid.UUID] = MappedColumn(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    email_verified: Mapped[bool] = MappedColumn(
        default=False, nullable=False, index=True
    )
    phone_number: Mapped[str] = MappedColumn(nullable=True, index=True)
    address: Mapped[str] = MappedColumn(nullable=True, index=True)
    locked_until: Mapped[datetime.datetime] = MappedColumn(nullable=True, index=True
    )
    profile_picture: Mapped[str] = MappedColumn(
        nullable=True, index=True
    )  # URL or path to profile picture
    email_verification_token: Mapped[str] = MappedColumn(
        nullable=True, index=True
    )  # Token for email verification
    reset_password_token: Mapped[str] = MappedColumn(
        nullable=True, index=True
    )  # Token for password reset
    reset_password_expires_at: Mapped[datetime.datetime] = MappedColumn(nullable=True, index=True
    )  # Expiration time for password reset token
    created_at: Mapped[datetime.datetime] = MappedColumn(default=datetime.datetime.utcnow, nullable=False, index=True
    )
    updated_at: Mapped[datetime.datetime] = MappedColumn(
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
        index=True,
    )
    user = relationship("Users", back_populates="user_metadata")

    idx_all = Index(
        "idx_user_metadata_all",
        id,
        user_id,
        postgresql_using="btree",
    )
