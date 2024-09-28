from fastapi import APIRouter, Request

router = APIRouter()


# ---------------------------- API Endpoints ---------------------------- #


@router.get("/url_for_endpoint")
async def bar(request: Request) -> int:
    """Does something not so nice.

    Args:
        request (Request): The request object.

    Returns:
        int: Something not so nice.
    """
    # you can pull variables defined in the app itself like this
    var: int = request.app.var

    return var
