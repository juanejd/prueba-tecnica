import json
import random
from string import ascii_letters, digits
import deepl
from dotenv import load_dotenv
import os

load_dotenv()

auth_key = os.getenv("DEEPL_AUTH_KEY")
translator = deepl.Translator(auth_key)

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)


def category(actor_str):
    """
    funcion que recibe el value de "actor" y retorna el valor solicitado
    """
    actor_str = actor_str.replace(" ", "").lower()  # formateamos el string
    if actor_str == "des.usuario":
        return "RESPUESTA_USUARIO"
    elif actor_str == "instrucción":
        return "INDICACION"
    elif actor_str == "salto":
        return "OTROS"
    else:
        return "CONSULTA_DATOS"


def create_id(category, length=50):
    """
    funcion que crea un id para cada objeto del JSON
    """
    # valida la cantidad de caracteres de la palabra, en caso de que sea menor a 20, lo rellena con "_"
    if len(category) > 20:
        category = category[:20]
    else:
        category = category.ljust(20, "_")
    characters = ascii_letters + digits
    new_id = category + "".join(
        random.choice(characters) for _ in range(length - len(category))
    )
    return new_id


def modify_ids(data):
    """
    Funcion que modifica el id de cada objeto, tomando el value de actor y creando un id nuevo
    en la funcion create_id
    """
    get_actor = category(data.get("actor"))
    new_id = create_id(get_actor)
    data["id"] = new_id  # modificamos el id

    for key, values in data.items():
        if key != "interacciones" and key != "isExpanded":
            data[key] = translator.translate_text(values, target_lang="EN-US").text
        if key == "interacciones":
            for item in values:  # recorre cada objeto de interacciones recursivamente
                modify_ids(item)
    return data


new_data = [modify_ids(json_data) for json_data in data]

with open("data_translated.json", "w", encoding="utf-8") as f:
    json.dump(new_data, f, indent=4, ensure_ascii=False)
