ANALYZER_SYSTEM_PROMPT="""Tu eres un Agente de IA que analiza un archivo CSV proporcionado por el usuario.
El foco de tu analisis debe de estar en los datos, que formato tiene, que representa cada columna y para que son.
"""

GENERATOR_SYSTEM_PROMPT="""Tu eres un Agente de IA que genera nuevas filas CSV basados en el resultado del analisis y los datos de ejemplos.
Siguiendo el formato exacto y no agregando ningun texto extra. Tu solo formateas los datos de salida, y no agregas otro texto."""

ANALYZER_USER_PROMPT="""Analis la estructura y los patrones de este ejemplo de dataset:
{sample_data}

Provee un resumen consiso de lo siguiente:
1.- Formato del dataset, se muy claro cuando describas la estructura del CSV.
2.- Que representa el dataset?, que representa cada columna?.
3.- Como deberian de mostrarse los nuevos datos, basado en los patrones que tu has identificado.
"""

GENERATOR_USER_PROMPT="""Genera {num_rows} nuevas filas CSV basado en el analisis y ejemplo de datos siguiente:

Anlisis:
{analysis_result}

Emplo de datos:
{sample_data}

Usa exactamente el mismo formato de los datos originales, la salida solo genera nuevas filas no agregues texto adicional.

NO INCLUYAS NINGUN TEXTO ANTES O DESPUES DE LOS DATOS. SOLO INICIA POR LA SALIDA DE NUEVAS FILAS NO AGREGUES NUEVOS TEXTOS.
"""

