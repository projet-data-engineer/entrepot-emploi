from pydantic import BaseModel


class Rome(BaseModel):
    code_3: str
    libelle_3: str
    code_2: str
    libelle_2: str
    code_1: str
    libelle_1: str