
def user_context(request):
    full_name = "invité"
    name =""
    if request.user.is_authenticated:
        full_name = f"{request.user.first_name} {request.user.last_name}".strip()
        name = request.session.get('name')

    return {
        "user_full_name": full_name,
        "user_agency_name": name,
    }


def enterprise_context(request):
    enterprise_name= request.session.get('Name')

    return {
        "enterprise_name": enterprise_name
    }




