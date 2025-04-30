"""Taller evaluable"""

import glob
import os

import pandas as pd  # type: ignore


def load_input(input_directory):
    """Load text files in 'input_directory/'"""
    #
    # Lea los archivos de texto en la carpeta input/ y almacene el contenido en
    # un DataFrame de Pandas. Cada línea del archivo de texto debe ser una
    # entrada en el DataFrame.
    #
    
    # Obtiene una lista de todos los archivos en el directorio de entrada.
    files = glob.glob(f"{input_directory}/*")
    
    # Lee cada archivo de texto en la lista de archivos y los almacena en una lista de DataFrames.
    # Se asume que los archivos están delimitados por tabulaciones y no tienen encabezados.
    dataframes = [
        pd.read_csv(
            file,
            header=None,  # No hay encabezados en los archivos de entrada.
            delimiter="\t",  # Se utiliza tabulación como delimitador.
            names=["line"],  # Se asigna el nombre "line" a la columna.
            index_col=None,  # No se utiliza ninguna columna como índice.
        )
        for file in files
    ]

    # Combina todos los DataFrames en uno solo, ignorando los índices originales.
    dataframe = pd.concat(dataframes, ignore_index=True)

    # Devuelve el DataFrame combinado.
    return dataframe


def clean_text(dataframe):
    """Text cleaning"""
    #
    # Elimine la puntuación y convierta el texto a minúsculas.
    #
    
    # Crea una copia del DataFrame original para no modificarlo directamente.
    dataframe = dataframe.copy()
    
    # Convierte todo el texto en la columna "line" a minúsculas.
    dataframe["line"] = dataframe["line"].str.lower()
    
    # Elimina las comas del texto en la columna "line".
    dataframe["line"] = dataframe["line"].str.replace(",", "")
    
    # Elimina los puntos del texto en la columna "line".
    dataframe["line"] = dataframe["line"].str.replace(".", "")
    
    # Devuelve el DataFrame con el texto limpio.
    return dataframe


def count_words(dataframe):
    """Word count"""

    # Crea una copia del DataFrame original para no modificarlo directamente.
    dataframe = dataframe.copy()
    
    # Divide el texto en palabras separadas en la columna "line".
    # Esto convierte cada línea en una lista de palabras.
    dataframe["line"] = dataframe["line"].str.split()
    
    # Explota las listas de palabras en filas individuales.
    # Cada palabra ahora será una fila separada en el DataFrame.
    dataframe = dataframe.explode("line")
    
    # Agrupa las palabras por su valor y cuenta cuántas veces aparece cada una.
    # El resultado es un DataFrame con dos columnas: "line" (la palabra) y "count" (su frecuencia).
    dataframe = dataframe.groupby("line").size().reset_index(name="count")
    
    # Devuelve el DataFrame con las palabras y sus frecuencias.
    return dataframe


def save_output(dataframe, output_directory):
    """Save output to a file."""

    # Verifica si el directorio de salida ya existe.
    if os.path.exists(output_directory):
        # Obtiene una lista de todos los archivos en el directorio de salida.
        files = glob.glob(f"{output_directory}/*")
        # Elimina cada archivo en el directorio de salida.
        for file in files:
            os.remove(file)
        # Elimina el directorio de salida después de vaciarlo.
        os.rmdir(output_directory)

    # Crea un nuevo directorio de salida.
    os.makedirs(output_directory)

    # Guarda el DataFrame en un archivo CSV en el directorio de salida.
    # - El archivo se llama "part-00000".
    # - Se utiliza tabulación como delimitador.
    # - No se incluye el índice ni encabezados en el archivo.
    dataframe.to_csv(
        f"{output_directory}/part-00000",
        sep="\t",
        index=False,
        header=False,
    )


#
# La siguiente función crea un archivo llamado _SUCCESS en el directorio
# entregado como parámetro.
#
def create_marker(output_directory):
    """Create Marker"""

    # Abre (o crea) un archivo llamado "_SUCCESS" en el directorio de salida.
    # El archivo se abre en modo escritura ("w") y con codificación UTF-8.
    with open(f"{output_directory}/_SUCCESS", "w", encoding="utf-8") as f:
        # Escribe una cadena vacía en el archivo.
        # Este archivo se utiliza como marcador para indicar que el proceso se completó con éxito.
        f.write("")


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run_job(input_directory, output_directory):
    """Job"""

    # Carga los archivos de texto desde el directorio de entrada y los almacena en un DataFrame.
    dataframe = load_input(input_directory)

    # Limpia el texto eliminando puntuación y convirtiendo a minúsculas.
    dataframe = clean_text(dataframe)

    # Cuenta la frecuencia de cada palabra en el texto.
    dataframe = count_words(dataframe)

    # Guarda el resultado en un archivo en el directorio de salida.
    save_output(dataframe, output_directory)

    # Crea un archivo marcador (_SUCCESS) para indicar que el proceso se completó correctamente.
    create_marker(output_directory)


if __name__ == "__main__":
    #
    # Punto de entrada principal del programa.
    # 
    # Llama a la función `run_job` con los directorios de entrada y salida.
    # - "files/input": Directorio donde se encuentran los archivos de texto de entrada.
    # - "files/output": Directorio donde se guardará el resultado del procesamiento.
    #
    run_job(
        "files/input",
        "files/output",
    )