from enum import Enum

class RoleDTO(str, Enum):
    """
    Available roles for user registration.
    Admin role cannot be selected during registration
    """
    OBSERVER = "observer"
    ESTIMATOR = "estimator"