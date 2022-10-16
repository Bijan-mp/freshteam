import json


class JSONResponse:

    PERMISSION_DENIED = json.dumps(
        {
            "message":"You dont have permission."
        }
    )

    ASSIGNE_IS_NOT_PROJ_MEMBER = json.dumps(
        {
            "message":"You dont have permission."
        }
    )