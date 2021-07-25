import traceback
import logging

from starlette.responses import JSONResponse
from fastapi import Request
from mlservefast.exception import MLServeFastException

logger = logging.getLogger(__name__)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except MLServeFastException as error:
        # you probably want some kind of logging here
        return JSONResponse({"error": error.to_dict()}, status_code=error.status_code)

    except Exception as err:  # pylint: disable=broad-except
        logger.error(err)
        logger.error(traceback.format_exc())
        error = MLServeFastException("Internal server error", {})
        return JSONResponse({"error": error.to_dict()}, status_code=error.status_code)
