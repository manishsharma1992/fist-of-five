import re

from pydantic import BaseModel, Field, EmailStr, field_validator

from app.application.auth.dtos.role_dto import RoleDTO


class RegisterRequest(BaseModel):
    uid: str = Field(
        ...,
        min_length=6,
        max_length=6,
        description="Employee ID (format: letter + 5 digits, eg., f93328)",
        examples=["f93328", "h99887"]
    )

    email: EmailStr = Field(
        ...,
        description="Corporate email address",
        examples=["john.wick@bnpparibas.com"]
    )

    password: str = Field(
        ...,
        min_length=8,
        description="Password (minimum 8 characters)",
        examples=["SecurePassword1234!"]
    )

    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="First Name",
        examples=["John"]
    )

    last_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Last Name",
        examples=["Wick"]
    )

    middle_name: str = Field(
        None,
        max_length=100,
        description="Middle Name (Optional)",
        examples=["Volodymyr"]
    )

    role: RoleDTO = Field(
        ...,
        description="User role for planning poker sessions",
        examples=["estimator"]
    )

    @field_validator('uid')
    @classmethod
    def validate_uid_format(cls, v: str) -> str:
        """
        Validate UID format: [a-zA-Z0-9]{1}[0-9]{5}

        First character: uppercase letter, lowercase letter, or digit
        Next 5 characters: digits only

        Valid examples:
        - f93328 (lowercase letter)
        - H99776 (uppercase letter)
        - 5123456 (digit)
        """
        pattern = r'^[a-zA-Z0-9][0-9]{5}$'
        if not re.match(pattern, v):
            raise ValueError(
                'UID must be 6 characters: first char (letter or digit), followed by 5 digits (e.g., f93328, H99776, 5123456)'
            )
        return v

    @field_validator('email')
    @classmethod
    def validate_email_domain(cls, v: str) -> str:
        """
        Validate email belongs to bnpparibas.com domain (including subdomains).

        Valid formats:
        - user@bnpparibas.com
        - user@asia.bnpparibas.com
        - user@external.bnpparibas.com
        """
        email_lower = v.lower()

        # Extract domain part (after @)
        if '@' not in email_lower:
            raise ValueError('Invalid email format')

        domain = email_lower.split('@')[1]

        # Check if domain is bnpparibas.com or ends with .bnpparibas.com
        if domain != 'bnpparibas.com' and not domain.endswith('.bnpparibas.com'):
            raise ValueError('Email must be from bnpparibas.com domain or its subdomains')

        return email_lower

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Validate password strength:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')

        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')

        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')

        return v

    class Config:
        json_schema_extra = {
            "example": {
                "uid": "f93328",
                "email": "john.doe@bnpparibas.com",
                "password": "SecurePass123",
                "first_name": "John",
                "last_name": "Doe",
                "middle_name": "Michael",
                "role": "estimator"
            }
        }


class RegisterResponse(BaseModel):
    """
    Registration success response.
    Simple message confirming account creation.
    """
    message: str = Field(
        ...,
        description="Success message",
        examples=["Registration successful. Please login to continue."]
    )
    uid: str = Field(
        ...,
        description="User's employee ID",
        examples=["f93328"]
    )
    email: str = Field(
        ...,
        description="Registered email address",
        examples=["john.doe@bnpparibas.com"]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Registration successful. Please login to continue.",
                "uid": "f93328",
                "email": "john.doe@bnpparibas.com"
            }
        }


class ErrorResponse(BaseModel):
    """
    Standard error response.
    FastAPI will use this for validation errors and exceptions.
    """
    detail: str = Field(
        ...,
        description="Error message",
        examples=["Email already registered"]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Email already registered"
            }
        }