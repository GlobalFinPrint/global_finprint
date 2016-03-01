from global_finprint.core.mixins import UserAllowedMixin


def user_allowed_processor(request):
    return {'user_allowed': UserAllowedMixin.user_allowed(request.user)}
