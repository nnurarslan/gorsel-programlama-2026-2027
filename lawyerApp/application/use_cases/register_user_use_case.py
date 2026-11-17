class RegisterUserUseCase:
    def __init__(self, auth_repository):
        self.auth_repository = auth_repository

    def execute(self, name, email, password):
        return self.auth_repository.register(
            name=name,
            email=email,
            password=password
        )
