from src.domain.auth.service.authentication_domain_service import AuthenticationDomainService

class AuthenticationManagementService:
    def __init__(self, auth_domain_service: AuthenticationDomainService):
        self._authDomainService = auth_domain_service

    def register_user(self, register_request):

        self._authDomainService.save(register_request)