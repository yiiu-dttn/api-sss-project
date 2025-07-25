from sqlalchemy import Column, Integer, String, DateTime, Float, UniqueConstraint
from database import Base

class SSSSurvey(Base):
    __tablename__ = "SSS_SURVEY"
    id = Column("ID", Integer, primary_key=True, index=True)
    title = Column("TITLE", String)
    co_so_dao_tao_id = Column("CO_SO_DAO_TAO_ID", Integer)

class SSSSurveyAnswer(Base):
    __tablename__ = "SSS_SURVEY_ANSWER"
    id = Column("ID", Integer, primary_key=True, index=True)
    survey_id = Column("SURVEY_ID", Integer, index=True)
    answers = Column("ANSWERS", String)
    created_at = Column("CREATED_AT", DateTime)

class SurveySummary(Base):
    __tablename__ = "SURVEY_SUMMARY"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    survey_id = Column(Integer, index=True)
    nam_khao_sat = Column(Integer, index=True)
    co_so_dao_tao_id = Column(Integer)
    so_phieu_phat_ra = Column(Integer)
    so_phieu_thu_vao = Column(Integer)
    ty_le_rat_khong_hai_long = Column(Float)
    ty_le_khong_hai_long = Column(Float)
    ty_le_binh_thuong = Column(Float)
    ty_le_hai_long = Column(Float)
    ty_le_rat_hai_long = Column(Float)
    tong_so_cau_tra_loi_hop_le = Column(Integer)

    __table_args__ = (
        UniqueConstraint('survey_id', 'nam_khao_sat', name='unique_survey_year'),
    )
