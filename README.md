# API para análisis de recursos contra reglas YARA

Este es un ejemplo de una API Flask para analizar reglas YARA. Utiliza una base de datos SQLite para almacenar las reglas y permite agregar, actualizar y buscar reglas.

## Requerimientos

- Python 3.x
- Flask
- Flask-HTTPAuth
- YARA
- SQLite

## Uso

1. Clonar el repositorio:

2. Instalar las dependencias:
TOBEDONE ----------------- pip install -r requirements.txt

3. Ejecutar la aplicación:
TOBEDONE Docker --------------------------------

La aplicación se ejecutará en `http://localhost:5000`.

## Endpoints

### Agregar una regla YARA
POST /api/rule

Agrega una nueva regla YARA a la base de datos.

#### Parámetros

| Parámetro | Tipo   | Descripción                |
|-----------|--------|----------------------------|
| name      | string | Nombre de la regla YARA.   |
| rule      | string | Cuerpo de la regla YARA.    |

#### Respuestas

| Código | Descripción                                          |
|--------|------------------------------------------------------|
| 201    | La regla YARA se agregó correctamente.               |
| 400    | Los datos del cuerpo son incorrectos.                 |
| 401    | No se proporcionaron credenciales de autenticación.   |

### Obtener una regla YARA
GET /api/rule/:rule_id

Obtiene una regla YARA de la base de datos por su ID.

#### Parámetros

| Parámetro | Tipo   | Descripción                          |
|-----------|--------|--------------------------------------|
| rule_id  | integer | ID de la regla YARA a buscar.        |

#### Respuestas

| Código | Descripción                                 |
|--------|---------------------------------------------|
| 200    | La regla YARA se obtuvo correctamente.      |
| 404    | No se encontró la regla YARA.               |

### Actualizar una regla YARA
PUT /api/rule/:rule_id

Actualiza una regla YARA de la base de datos por su ID.

#### Parámetros

| Parámetro | Tipo   | Descripción                                |
|-----------|--------|--------------------------------------------|
| rule_id  | integer | ID de la regla YARA a actualizar.         |
| name      | string | Nuevo nombre de la regla YARA.             |
| rule      | string | Nuevo cuerpo de la regla YARA.             |

#### Respuestas

| Código | Descripción                                           |
|--------|-------------------------------------------------------|
| 200    | La regla YARA se actualizó correctamente.             |
| 400    | Los datos del cuerpo son incorrectos.                  |
| 404    | No se encontró la regla YARA.                          |

### Analizar texto con reglas YARA
POST /api/analyze/text

Compara un texto determinado contra un grupo de reglas YARA.

#### Parámetros

| Parámetro | Tipo   | Descripción                                |
|-----------|--------|--------------------------------------------|
| text  | string | texto a analizar         |
| rules      | json | JSON de duplas rule_id : id , indicando los ids de las reglas a validar             |

#### Respuestas

| Código | Descripción                                           |
|--------|-------------------------------------------------------|
| 200    | JSON con resultados BOOLEANOS de comparacion             |
| 401    | Autenticacion incorrecta.                  |

### Analizar archivo con reglas YARA
POST /api/analyze/file

Compara un archivo determinado contra un grupo de reglas YARA.

#### Parámetros

| Parámetro | Tipo   | Descripción                                |
|-----------|--------|--------------------------------------------|
| file  | file | ruta del archivo a analizar         |
| rules      | json | JSON de duplas rule_id : id , indicando los ids de las reglas a validar             |

#### Respuestas

| Código | Descripción                                           |
|--------|-------------------------------------------------------|
| 200    | JSON con resultados BOOLEANOS de comparacion             |
| 401    | Autenticacion incorrecta.                  |
