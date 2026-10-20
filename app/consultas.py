from sqlalchemy import select

from app.database import SessionLocal
from app.models import Chamado


db = SessionLocal()


consulta = (
    select(Chamado)
    .where(Chamado.prioridade == "alta")
    .order_by(Chamado.id)
    .limit(2)
)

resultado = db.execute(consulta)


chamados = resultado.scalars().all()


for chamado in chamados:
    print(
        chamado.id,
        chamado.titulo,
        chamado.prioridade
    )


db.close()