from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, Response
from kink import di

from src.building_blocks.errors import APIErrorMessage
from src.clients.application.client_service import ClientService
from src.clients.application.dto import (
    ArchiveClientDTO,
    ChangeClientPersonalDataDTO,
    ClientDTO,
    CreateClientDTO,
    ExportClientsDTO,
)

router = APIRouter()


@router.post(
    "/clients",
    response_model=ClientDTO,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["clients"],
)
async def create_client(
    request: CreateClientDTO, service: ClientService = Depends(lambda: di[ClientService])
) -> JSONResponse:
    result = service.create(request)
    return JSONResponse(content=result.dict(), status_code=status.HTTP_201_CREATED)


@router.put(
    "/clients/{client_id}",
    response_model=ClientDTO,
    responses={400: {"model": APIErrorMessage}, 404: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["clients"],
)
async def change_personal_data(
    client_id: str, request: ChangeClientPersonalDataDTO, service: ClientService = Depends(lambda: di[ClientService])
) -> JSONResponse:
    request.client_id = client_id
    result = service.change_personal_data(request)
    return JSONResponse(content=result.dict(), status_code=status.HTTP_200_OK)


@router.delete(
    "/clients/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={400: {"model": APIErrorMessage}, 404: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["clients"],
)
async def archive(client_id: str, service: ClientService = Depends(lambda: di[ClientService])) -> Response:
    service.archive(ArchiveClientDTO(client_id=client_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/clients/exports",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={400: {"model": APIErrorMessage}, 500: {"model": APIErrorMessage}},
    tags=["clients"],
)
async def export(request: ExportClientsDTO, service: ClientService = Depends(lambda: di[ClientService])) -> Response:
    service.export(request)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
