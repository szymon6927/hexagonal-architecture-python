from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from kink import di

from src.building_blocks.errors import APIErrorMessage
from src.gym_passes.application.dto import CreateGymPassDTO, GymPassDTO, PauseGymPassDTO
from src.gym_passes.application.gym_pass_service import GymPassService

router = APIRouter()


@router.post(
    "/gym-passes",
    response_model=GymPassDTO,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["gym_passes"],
)
async def create_gym_pass(
    request: CreateGymPassDTO, service: GymPassService = Depends(lambda: di[GymPassService])
) -> JSONResponse:
    result = service.create(request)
    return JSONResponse(content=result.dict(), status_code=status.HTTP_201_CREATED)


@router.post(
    "/gym-passes/{gym_pass_id}/pauses",
    response_model=GymPassDTO,
    responses={400: {"model": APIErrorMessage}, 404: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["gym_passes"],
)
async def pause(
    gym_pass_id: str, request: PauseGymPassDTO, service: GymPassService = Depends(lambda: di[GymPassService])
) -> JSONResponse:
    request.gym_pass_id = gym_pass_id
    result = service.pause(request)
    return JSONResponse(content=result.dict(), status_code=status.HTTP_201_CREATED)


@router.put(
    "/gym-passes/{gym_pass_id}/renewal",
    response_model=GymPassDTO,
    responses={400: {"model": APIErrorMessage}, 404: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["gym_passes"],
)
async def renew(gym_pass_id: str, service: GymPassService = Depends(lambda: di[GymPassService])) -> JSONResponse:
    result = service.renew(gym_pass_id)
    return JSONResponse(content=result.dict(), status_code=status.HTTP_200_OK)


@router.get(
    "/gym-passes/{gym_pass_id}/verification",
    response_model=GymPassDTO,
    responses={400: {"model": APIErrorMessage}, 404: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["gym_passes"],
)
async def check(gym_pass_id: str, service: GymPassService = Depends(lambda: di[GymPassService])) -> JSONResponse:
    result = service.check(gym_pass_id)
    return JSONResponse(content=result.dict(), status_code=status.HTTP_200_OK)
