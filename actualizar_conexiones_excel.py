# Importamos las librerías necesarias para la ejecución
import os
import win32com.client

# Especificamos el directorio que contiene los archivos Excel
ruta_directorio = "C:\Mis Programas\"

#
# Función que realiza la actualización automática de las conexiones de datos
#
def actualizar_conexiones(directorio):

    # Creamos una instancia de la aplicación Excel
    excel_app = win32com.client.Dispatch("Excel.Application")

    # Hacemos la aplicación invisible para el usuario
    excel_app.Visible = False

    # Recorremos todos los archivos en el directorio especificado
    for filename in os.listdir(directorio):
        # Solo seleccionamos las hojas de cálculo, evitando los archivos ocultos
        if (filename.endswith(".xlsx") or filename.endswith(".xlsm")) and not filename.startswith("~"):
            file_path = os.path.join(directorio, filename)
            print(f"Actualizando conexiones de datos en: {file_path}")

            # Creamos un libro excel en memoria con la ruta del archivo
            workbook = excel_app.Workbooks.Open(file_path)

            try:
                # Recorremos todas las conexiones de datos del libro
                for connection in workbook.Connections:
                    print(f"Habilitando contenido: {connection.Name}")
                    connection.Refresh()
                    # Para hacer esperar la ejecución hasta que termine la actualización de datos:
                    excel_app.CalculateUntilAsyncQueriesDone()
                    # Para evitar que se abran ventanas de diálogo que pararían el proceso:
                    excel_app.DisplayAlerts = False

            except Exception as e:
                print(f"Error al actualizar la conexión")

            finally:
                # Guardamos y cerramos el libro
                workbook.Save()
                workbook.Close()

    # Cerramos la aplicación Excel (ojo, no es lo mismo que cerrar el libro excel creado)
    excel_app.Quit()

    print("Actualización de conexiones de datos completada.")


# Llamada a la función para actualizar las conexiones de datos
actualizar_conexiones(ruta_directorio)
