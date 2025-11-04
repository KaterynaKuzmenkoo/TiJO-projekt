from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .schemas import CalcRequest, CalcResponse
from . import calculations as logic

app = FastAPI(title="Kalkulator wynagrodzenia netto (UPROSZCZONY)",
              description="Model edukacyjny do testów – nie używać do rozliczeń!",
              version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/calculate", response_model=CalcResponse)
def calculate(req: CalcRequest):
    res = logic.calc(
        logic.Inputs(
            gross=float(req.gross),
            contract=logic.ContractType(req.contract.value),
            age=req.age,
            is_student=req.is_student,
            kup_fixed=req.kup_fixed,
            kup_percent=req.kup_percent,
            creative_50=req.creative_50,
            ulga_mlodzi=req.ulga_mlodzi,
            include_social_for_zlecenie=req.include_social_for_zlecenie,
        )
    )
    return CalcResponse(**res.__dict__)


app.mount("/static", StaticFiles(directory=str(Path(__file__).resolve().parent.parent / "static")), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
    index_path = Path(__file__).resolve().parent.parent / "static" / "index.html"
    return index_path.read_text(encoding="utf-8")