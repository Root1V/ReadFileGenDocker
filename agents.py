# Agents

# Import Libraries
import os
import csv
import anthropic
from openai import OpenAI
from prompts import *

# Funcion para leer CSV file.
def read_csv(file_path):
    data = []
    with open(file_path, "r", newline="") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)
    return data

# Funcion para guardar datos en fotmato .csv
def save_csv(data, output_file, headers=None):
    mode = "w" if headers else "a"
    with open(output_file, mode, newline="") as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        for row in csv.reader(data.splitlines()):
            writer.writerow(row)

# Creamos un Analyzer Agent
def analyzer_agent_anthropic(client, model, sample_data):
    message = client.messages.create(
        model=model,
        max_tokens=400,
        temperature=0.1,
        system=ANALYZER_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": ANALYZER_USER_PROMPT.format(sample_data=sample_data)
            }
        ]
    )
    return message.content[0].text

# Creamos un Analyzer Agent
def analyzer_agent_openAI(client, model, sample_data):
    message = client.chat.completions.create(
        model=model,
        max_tokens=400,
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": ANALYZER_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": ANALYZER_USER_PROMPT.format(sample_data=sample_data)
            }
        ]
    )
    return message.choices[0].message.content

# Creamos un Generate Agent
def generate_agent_antropic(client, model, analysis_result, sample_data, num_rows=30):
    message= client.messages.create(
        model=model,
        max_tokens=1500,
        temperature=1,
        system=GENERATOR_SYSTEM_PROMPT,
        messages=[
            {
                "role":"user",
                "content": GENERATOR_USER_PROMPT.format(
                    num_rows=num_rows,
                    analysis_result=analysis_result,
                    sample_data=sample_data
                )
            }
        ]
    )
    return message.content[0].text

# Creamos un Generate Agent
def generate_agent_openai(client, model, analysis_result, sample_data, num_rows=30):
    message = client.chat.completions.create(
        model=model,
        max_tokens=1500,
        temperature=1,
        messages=[
            {
                "role": "system",
                "content": GENERATOR_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": GENERATOR_USER_PROMPT.format(
                    num_rows=num_rows,
                    analysis_result=analysis_result,
                    sample_data=sample_data
                )
            }
        ]
    )
    return message.choices[0].message.content


if __name__ == "__main__":
    # Cargamos la API al contexto
    llmType = input("Seleccione el modelo ('o' para OpenAI, 'a' para Anthropic):")

    if llmType == 'a' and not os.getenv("ANTHROPIC_API_KEY"):
        os.environ["ANTHROPIC_API_KEY"] = input("Ingresa tu API key Anthtropic:")
    elif llmType == 'o' and not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = input("Ingresa tu API key OpenAI:")
    else:
        llmType == 'x'
        print("Entrada no válida. Por favor ingrese 'o' para OpenAI o 'a' para Anthropic.")

    if llmType != 'x':
        # Get input from user
        file_path = input("\nIngresa el nombre de tu archivo CSV:")
        file_path = os.path.join("/app/data", file_path)
        desired_rows = int(input("Ingresa el numero de filas del nuevo dataset:"))

        # Read the sample data from the input csv file
        sample_data = read_csv(file_path)
        sample_data_str = "\n".join([",".join(row) for row in sample_data])

        client = {}
        model = 'noModel'
        analysis_result = 'NoModel'
        # Analizando los datos de ejemplos usando Analyzer Agent
        print("\nLanzando los Agentes de Analisis ...")

        if llmType == 'a':
            client = anthropic.Anthropic()
            model = "claude-3-5-sonnet-20240620"
            print("\ncon el modelo de Anthropic...")
            analysis_result = analyzer_agent_anthropic(client, model, sample_data_str)
        elif llmType == 'o':
             client = OpenAI()
             model = "gpt-4o-mini"
             print("\ncon el modelo de OpenAI...")
             analysis_result = analyzer_agent_openAI(client, model, sample_data_str)
        
        print("\n#### Salida del Agente Analizador: ####\n")
        print(analysis_result)
        print("\n-------------------------------------------------------------\n\nGenerando nuevos datos...")

        # SetUp del archivo de salida
        output_file = "/app/data/new_dataset.csv"
        headers = sample_data[0]

        # Creamos la salida del archivo con headers
        save_csv("", output_file, headers)

        batch_size = 20     # Numero de filas a generar en cada batch
        generated_rows = 0  # Cantidad para mantener el tracking de cuantas filas se han generado

        print("\nLanzando los Agentes de Generación ...")
        # Generamos datos en batches hasta que generemos el numero de filas deseados
        while generated_rows < desired_rows:
            
            rows_to_generate = min(batch_size, desired_rows - generated_rows)
            generate_data = {}
            if llmType == 'a':
                generate_data = generate_agent_antropic(client, model, analysis_result, sample_data_str, rows_to_generate)
            elif llmType == 'o':
                generate_data = generate_agent_openai(client, model, analysis_result, sample_data_str, rows_to_generate)

            print("\n#### Salida del Agente Generador: ####\n")
            print(generate_data)
            save_csv(generate_data, output_file)

            generated_rows += rows_to_generate

            print(f"Se generaron {generated_rows} filas de las {desired_rows} solicitadas")

        # Informamos la completitud de la tarea
        print(f"\nLos datos generados han sido guardados en {output_file}")



