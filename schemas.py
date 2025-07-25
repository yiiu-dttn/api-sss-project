from pydantic import BaseModel, Field

class SurveySummaryResponse(BaseModel):
    survey_id: int = Field(..., alias="survey_id")
    nam_khao_sat: int = Field(..., alias="nam_khao_sat")
    co_so_dao_tao_id: int = Field(..., alias="co_so_dao_tao_id")
    so_phieu_phat_ra: int = Field(..., alias="so_phieu_phat_ra")
    so_phieu_thu_vao: int = Field(..., alias="so_phieu_thu_vao")
    ty_le_rat_khong_hai_long: float = Field(..., alias="ty_le_rat_khong_hai_long")
    ty_le_khong_hai_long: float = Field(..., alias="ty_le_khong_hai_long")
    ty_le_binh_thuong: float = Field(..., alias="ty_le_binh_thuong")
    ty_le_hai_long: float = Field(..., alias="ty_le_hai_long")
    ty_le_rat_hai_long: float = Field(..., alias="ty_le_rat_hai_long")
    tong_so_cau_tra_loi_hop_le: int = Field(..., alias="tong_so_cau_tra_loi_hop_le")

    model_config = {
        "validate_by_name": True,
        "from_attributes": True
    }
