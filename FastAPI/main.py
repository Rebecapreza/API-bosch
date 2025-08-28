from fastapi import FastAPI, HTTPException, status, Response, Depends
from models import personagemToyStory
from typing import Optional, Any
from routes import curso_router, usuario_router
import requests



app = FastAPI(title="API dos personagens de Toy Story - DS18", version='0.0.1', description="API realizada com o Wilson para aprender FastAPI")

app.include_router(curso_router.router, tags=["Cursos"])
app.include_router(usuario_router.router, tags=["Usuários"])

@app.get("/pokemon/{name}")
def get_pokemon(name: str):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    if response.status_code == 200:
        return response.json()
    return {"Message": "Pokemon not found"}

def fake_db():
    try:
        print("Conectadando com po banco")
    finally:
        print("Fechando banco")
        
        

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
async def get_personagens(db: any = Depends(fake_db)):
    return personagens

@app.get("/personagens/(personagem_id)", description="Retorna um personagem com um id específico", summary="Retorna um personagem")
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

@app.put("/personagens/{personagem_id}")
async def put_personagem(personagem_id:int, personagem: personagemToyStory):
    if personagem_id in personagens:
        personagens[personagem_id] = personagem
        personagem.id = personagem.id
        del personagem.id
        return personagem
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Personagem não encontrado")
 
@app.delete("/personagens/{personagem_id}")
async def delete_personagem(personagem_id):
    if personagem_id in personagens:
        del personagens[personagem_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, deital="Personagem não encontrado")
    
@app.get ("/calcular")
async def calcular (a: int, b: int):
    soma = a + b
    return "Resultado", soma

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, log_level="info", reload=True)