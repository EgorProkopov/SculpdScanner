from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from src.image_processor import ImageProcessor
from src.health_scanner import HealthScanner
from src.report_processing_expert import ReportProcessingExpert
from src.scanner_pipeline import ScannerPipeline


router = APIRouter()


class ScannerRequest(BaseModel):
    user_info: dict = Field(description="User data JSON.")
    image_url: str = Field(description="URL of the image to be processed.")


class ScannerResponse(BaseModel):
    scanner_result: dict = Field(description="Generated users photo descriptions and training recommendations.")


@router.post(path="/generate_scanner_description", response_model=ScannerResponse)
def generate_scanner_description(request_data: ScannerRequest, request: Request):
    user_info = request_data.user_info
    image_url = request_data.image_url

    try:
        state = request.app.state

        image_processor = ImageProcessor(
            state.scanner_config["image_processing"]
        )
        health_scanner = HealthScanner(
            state.api_key,
            state.scanner_config["health_scanner"],
            image_processor
        )

        report_processing_expert = ReportProcessingExpert(
            API_KEY=state.api_key,
            report_processing_config=state.report_processing_config
        )

        max_attempts = state.report_processing_config["max_attempts"]

        scanner_pipeline = ScannerPipeline(
            scanner=health_scanner,
            report_processing_expert=report_processing_expert,
            max_attempts=max_attempts
        )
        report = scanner_pipeline.run(image_path=image_url, user_info=user_info, is_url=True)
        report_json = report_processing_expert.convert_processed_report_to_json(report)
        return ScannerResponse(scanner_result=report_json)


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

