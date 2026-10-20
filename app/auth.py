from datetime import datetime, timedelta, timezone

import jwt


SECRET_KEY = "chave-secreta-apenas-para-aula"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


usuarios = {
    "ariel": {
        "username": "ariel",
        "perfil": "admin"
    },
    "maria": {
        "username": "maria",
        "perfil": "usuario"
    }
}

def criar_token(username: str, perfil: str) -> str:
    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    dados_token = {
        "sub": username,
        "perfil": perfil,
        "exp": expiracao
    }

    return jwt.encode(
        dados_token,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def validar_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )