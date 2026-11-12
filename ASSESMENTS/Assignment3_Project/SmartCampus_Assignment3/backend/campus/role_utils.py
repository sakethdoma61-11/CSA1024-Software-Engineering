def campus_role(user):
    if not user or not user.is_authenticated:
        return "ANONYMOUS"
    if user.is_superuser:
        return "ADMIN"
    try:
        return user.campus_profile.role
    except Exception:
        return "STUDENT"
