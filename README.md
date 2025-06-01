# Procesador de Datos JSON con Traducción

Este programa procesa archivos JSON, modifica sus IDs y traduce su contenido al inglés utilizando la API de DeepL.

## Dependencias

El proyecto requiere las siguientes dependencias:

```bash
python-dotenv==1.0.0
deepl==1.15.0
```

## Configuración

1. Crea un archivo `.env` en la raíz del proyecto
2. Agrega tu API key de DeepL:

```
DEEPL_AUTH_KEY=tu-api-key-aquí
```

## Estructura del Programa

### Funciones Principales

1. `category(actor_str)`

   - Recibe un string que representa el actor
   - Se eliminan caracteres que puedan interferir con replace
   - Retorna una categoría específica basada en el actor:
     - "des.usuario" → "RESPUESTA_USUARIO"
     - "instrucción" → "INDICACION"
     - "salto" → "OTROS"
     - otros → "CONSULTA_DATOS"

2. `create_id(category, length=50)`

   - Genera IDs únicos para cada objeto en el JSON
   - Formatea la categoría a 20 caracteres (rellena con "\_" si es necesario)
   - Combina la categoría con caracteres aleatorios para crear un ID único usando "string" y sus métodos `ascii_letters` `digits`

3. `modify_ids(data)`
   - Procesa el JSON y realiza tres operaciones principales:
     - Accede al valor de "actor" para modificar la id en base a su categoría
     - Genera nuevos IDs basados en la categoría del actor
     - Reemplaza el nuevo ID generado en la key "id"
   - Se genera una iteración con el método .items para acceder key como a su value
     - Excluye las claves "interacciones" e "isExpanded" de la traducción
     - Traduce el value de cada key con la API de Deepl
   - Maneja recursivamente las interacciones anidadas validando si key == "interacciones" y accede al valor de la misma

### Flujo del Programa

1. Carga las variables de entorno y configura el traductor DeepL
2. Lee el archivo JSON de entrada (`data.json`)
3. Procesa cada objeto en el JSON:
   - Genera nuevos IDs
   - Traduce el contenido al inglés
4. Guarda el resultado en `data_translated.json`

## Uso

1. Asegúrate de tener todas las dependencias instaladas
2. Configura tu API key de DeepL en el archivo `.env`
3. Coloca tu archivo JSON de entrada como `data.json`
4. Ejecuta el programa:

```bash
python main.py
```

## Salida

El programa genera un archivo `data_translated.json` que contiene:

- Los mismos datos del JSON original
- IDs modificados según la categoría del actor
- Contenido traducido al inglés
