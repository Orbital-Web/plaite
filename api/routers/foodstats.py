from fastapi import APIRouter, Request

router = APIRouter()


# ---------------------------- API Endpoints ---------------------------- #


@router.get("/url_for_endpoint")
async def foo(request: Request) -> int:
    """Does something cool.

    Args:
        request (Request): The request object.

    Returns:
        int: Something cool.
    """
    # you can pull variables defined in the app itself like this
    var: int = request.app.var

    return var
