ADMINS = (
    ("[admin_user]", "[admin_email]"),
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = "yourSecretKey"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    [auth_backends]
)

SOCIAL_AUTH_ENABLED_BACKENDS = ([auth_backends_enabled])

[auth_data]
