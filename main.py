import json
import random
import string

# Cargar JSON original
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)


# Modificamos la categoría de acuerdo al tipo
def add_category_id(category):
    category = category.lower()
    # indicacion o instruccion
    if "instrucción" in category:
        return "INDICACION"
    # respuesta de usuario
    elif "díalogo" in category or "diálogo" in category:
        return "RESPUESTA_USUARIO"
    # Otros
    elif "salta" in category or "salto" in category:
        return "OTROS"
    else:
        return "CONSULTA_DATOS"


# Generamos un nuevo ID único combinando la categoría y caracteres aleatorios
def generate_new_id(id_category, length=50):
    new_id_category = id_category.replace(" ", "_")
    # Calculamos cuántos caracteres aleatorios necesitamos
    random_nums = length - len(new_id_category)
    # Definimos los caracteres
    characters = string.ascii_letters + string.digits
    # Generamos la cadena aleatoria
    random_nums = "".join(random.choice(characters) for _ in range(random_nums))
    return new_id_category + random_nums


# Transformamos recursivamente los IDs del objeto JSON y sus interacciones anidadas
def transform_ids(item):
    # Obtenemos la categoría basada en el tipo
    category = add_category_id(item.get("tipo", ""))
    # Generamos un nuevo ID único
    new_id = generate_new_id(category)
    # Agregamos los nuevos campos a cada campo correspondiente
    item["categoria_id"] = category
    item["id"] = new_id

    # Procesamos recursivamente las interacciones anidadas si existen
    if "interacciones" in item and isinstance(item["interacciones"], list):
        item["interacciones"] = [
            transform_ids(subitem) for subitem in item["interacciones"]
        ]

    return item


# Transformamos todos los elementos de la data
new_data = [transform_ids(item) for item in data]

# Guardamos el resultado en un nuevo archivo JSON
with open("new_data.json", "w", encoding="utf-8") as f:
    json.dump(new_data, f, indent=4, ensure_ascii=False)
