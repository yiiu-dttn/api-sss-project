from pydantic import BaseModel, Field

class SurveySummaryResponse(BaseModel):
    survey_id: int = Field(..., alias="SURVEY_ID")
    nam_khao_sat: int = Field(..., alias="NAM_KHAO_SAT")
    ty_le_rat_khong_hai_long: float = Field(..., alias="Tỉ lệ Rất không hài lòng")
    ty_le_khong_hai_long: float = Field(..., alias="Tỉ lệ Không hài lòng")
    ty_le_binh_thuong: float = Field(..., alias="Tỉ lệ Bình thường")
    ty_le_hai_long: float = Field(..., alias="Tỉ lệ Hài lòng")
    ty_le_rat_hai_long: float = Field(..., alias="Tỉ lệ Rất hài lòng")
    tong_so_cau_tra_loi_hop_le: int = Field(..., alias="Tổng số câu trả lời hợp lệ")

    model_config = {
        "validate_by_name": True,
        "from_attributes": True
    }
