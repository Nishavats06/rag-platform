from pydantic import BaseModel, ConfigDict


class LiveData(BaseModel):
    model_config = ConfigDict(json_schema_extra={"examples": [{"status": "ok"}]})

    status: str


class LiveResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"success": True, "message": "alive", "data": {"status": "ok"}}
            ]
        }
    )

    success: bool = True
    message: str
    data: LiveData


class ReadyData(BaseModel):
    model_config = ConfigDict(json_schema_extra={"examples": [{"database": "ok"}]})

    database: str


class ReadyResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"success": True, "message": "ready", "data": {"database": "ok"}}
            ]
        }
    )

    success: bool = True
    message: str
    data: ReadyData