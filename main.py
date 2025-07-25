from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, delete
from typing import List
import json
from collections import defaultdict

from database import SessionLocal, engine
from models import SSSSurvey, SSSSurveyAnswer, SurveySummary, Base
from schemas import SurveySummaryResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Thống kê khảo sát", version="1.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/survey-summary", response_model=List[SurveySummaryResponse])
def survey_summary(db: Session = Depends(get_db)):
    try:
        all_surveys = db.query(SSSSurvey).all()
        if not all_surveys:
            raise HTTPException(status_code=404, detail="Không có khảo sát nào.")

        all_results = []
        valid_ratings = {'1', '2', '3', '4', '5'}

        for survey in all_surveys:
            records = db.query(SSSSurveyAnswer).filter(
                SSSSurveyAnswer.survey_id == survey.id
            ).limit(10000).all()

            survey_stats = defaultdict(lambda: defaultdict(int))

            for record in records:
                year = record.created_at.year if record.created_at else None
                if year is None:
                    continue

                survey_stats[year]['so_phieu_phat_ra'] += 1

                if not record.answers:
                    continue

                try:
                    # Sửa lỗi .replace cho answers là dict
                    if isinstance(record.answers, dict):
                        answers = record.answers
                    elif isinstance(record.answers, str):
                        answers = json.loads(record.answers.replace("'", '"'))
                    else:
                        continue

                    is_valid = False
                    for _, value in answers.items():
                        if isinstance(value, dict):
                            continue
                        value_str = str(value).strip()
                        if value_str in valid_ratings:
                            survey_stats[year][value_str] += 1
                            survey_stats[year]['total'] += 1
                            is_valid = True
                    if is_valid:
                        survey_stats[year]['so_phieu_thu_vao'] += 1
                except Exception as e:
                    print(f"[Lỗi JSON]: {e}")
                    continue

            for year, counts in survey_stats.items():
                total = counts.get("total", 0)
                if total == 0:
                    continue

                # Xóa thống kê cũ nếu có
                db.execute(
                    delete(SurveySummary).where(
                        and_(
                            SurveySummary.survey_id == survey.id,
                            SurveySummary.nam_khao_sat == year
                        )
                    )
                )

                summary = SurveySummary(
                    survey_id=survey.id,
                    nam_khao_sat=year,
                    co_so_dao_tao_id=survey.co_so_dao_tao_id,
                    so_phieu_phat_ra=counts.get("so_phieu_phat_ra", 0),
                    so_phieu_thu_vao=counts.get("so_phieu_thu_vao", 0),
                    ty_le_rat_khong_hai_long=round(counts.get('1', 0) / total * 100, 2),
                    ty_le_khong_hai_long=round(counts.get('2', 0) / total * 100, 2),
                    ty_le_binh_thuong=round(counts.get('3', 0) / total * 100, 2),
                    ty_le_hai_long=round(counts.get('4', 0) / total * 100, 2),
                    ty_le_rat_hai_long=round(counts.get('5', 0) / total * 100, 2),
                    tong_so_cau_tra_loi_hop_le=total
                )

                db.add(summary)
                all_results.append(summary)

        db.commit()
        return all_results

    except Exception as e:
        db.rollback()
        print(f"[Lỗi API]: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {e}")
