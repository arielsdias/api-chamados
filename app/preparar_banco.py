from app.database import Base, SessionLocal, engine
from app.models import Chamado


Base.metadata.create_all(bind=engine)


db = SessionLocal()


if db.query(Chamado).count() == 0:
    chamados = [
        Chamado(
            titulo="Impressora não funciona",
            descricao="Impressora da recepção está offline.",
            prioridade="alta",
        ),
        Chamado(
            titulo="Mouse com defeito",
            descricao="Mouse não responde corretamente.",
            prioridade="baixa",
        ),
        Chamado(
            titulo="Sistema indisponível",
            descricao="Usuários não conseguem acessar o sistema.",
            prioridade="alta",
        ),
        Chamado(
            titulo="Teclado com problema",
            descricao="Algumas teclas não funcionam.",
            prioridade="media",
        ),
        Chamado(
            titulo="Monitor sem imagem",
            descricao="Monitor liga, mas não apresenta imagem.",
            prioridade="alta",
        ),
    ]

    db.add_all(chamados)
    db.commit()


db.close()


print("Banco preparado com sucesso!")