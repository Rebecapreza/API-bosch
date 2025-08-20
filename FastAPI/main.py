from fastapi import FastAPI, HTTPException, status
from models import personagemToyStory
from typing import Optional



app = FastAPI()

personagens = {
    1:{
        "nome": "Woody",
        "dono": "Andy",
        "tamanho": "pequeno",
        "foto": "https://i.pinimg.com/736x/a6/58/d2/a658d2a07fe2ac19f0aba035aeb56924.jpg"
    },
    2:{
        "nome": "Buzz Lighter",
        "dono": "Bonnie",
        "tamanho": "Pequeno",
        "foto": "https://i.pinimg.com/736x/d8/64/5f/d8645f9fc842724ac2ba60a58cf35553.jpg"
    }
}



@app.get("/")
async def raiz():
    return {"Mensagem": "Funcionou"}

@app.get("/personagens")
async def get_personagens():
    return personagens

@app.get("/personagens/(personagem_id)")
async def get_personagens(personagem_id: int):
    try:
        personagem = personagens[personagem_id]
        return personagem
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")
    
@app.post("/personagens", status_code=status.HTTP_201_CREATED)
async def post_personagem(personagem: Optional[personagemToyStory] = None):
    next_id = len(personagens) + 1
    personagens[next_id] = personagem
    del personagem.id
    return personagem

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, log_level="info", reload=True)