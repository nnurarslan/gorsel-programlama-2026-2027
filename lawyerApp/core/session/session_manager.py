class SessionManager:
    _access_token = None
    _refresh_token = None
    _user = None

    @classmethod
    def set_session(cls, access_token, refresh_token, user):
        cls._access_token = access_token
        cls._refresh_token = refresh_token
        cls._user = user

    @classmethod
    def clear(cls):
        cls._access_token = None
        cls._refresh_token = None
        cls._user = None

    @classmethod
    def is_authenticated(cls):
        return cls._access_token is not None

    @classmethod
    def access_token(cls):
        return cls._access_token

    @classmethod
    def user(cls):
        return cls._user
