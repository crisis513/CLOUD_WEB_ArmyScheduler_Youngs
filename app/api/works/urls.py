from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database.works_crud import *
from models.work import *

router = APIRouter()

@router.get("/", response_description="works retrieved")
async def get_works():
    works = await retrieve_works()
    return ResponseModel(works, "works data retrieved successfully") \
        if len(works) > 0 \
        else ResponseModel(
        works, "Empty list returned")


@router.get("/{id}", response_description="work data retrieved")
async def get_work_data(id):
    work = await retrieve_work(id)
    return ResponseModel(work, "work data retrieved successfully") \
        if work \
        else ErrorResponseModel("An error occured.", 404, "work doesn't exist.")


@router.post("/", response_description="work data added into the database")
async def add_work_data(work: WorkModel = Body(...)):
    work = jsonable_encoder(work)
    new_work = await add_work(work)
    return ResponseModel(new_work, "work added successfully.")


@router.delete("/{id}", response_description="work data deleted from the database")
async def delete_work_data(id: int):
    deleted_work = await delete_work(id)
    return ResponseModel("work with ID: {} removed".format(id), "work deleted successfully") \
        if deleted_work \
        else ErrorResponseModel("An error occured", 404, "work with id {0} doesn't exist".format(id))


@router.put("/{id}")
async def update_work(id: str, req: UpdateWorkModel = Body(...)):
    updated_work = await update_work_data(id, req.dict())
    return ResponseModel("work with ID: {} name update is successful".format(id),
                         "work name updated successfully") \
        if updated_work \
        else ErrorResponseModel("An error occurred", 404, "There was an error updating the work.".format(id))
