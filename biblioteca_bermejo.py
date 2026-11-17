from datetime import date

ARCHIVO_LIBROS = "libros.txt"
ARCHIVO_PRESTAMOS = "prestamos.txt"

LIBROS_INICIALES = [
    {
        "codigo": 1,
        "titulo": "Python para todos",
        "autor": "Charles Severance",
        "estado": "Disponible"
    },
    {
        "codigo": 2,
        "titulo": "Aprende Java",
        "autor": "Ana Torres",
        "estado": "Disponible"
    },
    {
        "codigo": 3,
        "titulo": "Bases de datos",
        "autor": "Carlos Mora",
        "estado": "Disponible"
    }
]


def guardar_libros(libros):
    with open(ARCHIVO_LIBROS, "w", encoding="utf-8") as archivo:
        for libro in libros:
            archivo.write(
                f"{libro['codigo']},{libro['titulo']},"
                f"{libro['autor']},{libro['estado']}\n"
            )

    return len(libros)


def guardar_prestamos(prestamos):
    with open(ARCHIVO_PRESTAMOS, "w", encoding="utf-8") as archivo:
        for prestamo in prestamos:
            archivo.write(
                f"{prestamo['numero']},{prestamo['codigo_libro']},"
                f"{prestamo['estudiante']},{prestamo['fecha']},"
                f"{prestamo['estado']}\n"
            )

    return len(prestamos)


def cargar_libros():
    lista_libros = []

    try:
        with open(ARCHIVO_LIBROS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if linea.strip() != "":
                    datos = linea.strip().split(",")

                    try:
                        if len(datos) == 4:
                            lista_libros.append({
                                "codigo": int(datos[0]),
                                "titulo": datos[1],
                                "autor": datos[2],
                                "estado": datos[3]
                            })
                        else:
                            print("Hay una linea de libros incompleta.")

                    except ValueError:
                        print("Un codigo del archivo esta mal escrito.")

    except FileNotFoundError:
        for libro in LIBROS_INICIALES:
            lista_libros.append(dict(libro))

        guardar_libros(lista_libros)
        print("Se crearon los libros de inicio.")

    return lista_libros


def cargar_prestamos():
    lista_prestamos = []

    try:
        with open(ARCHIVO_PRESTAMOS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if linea.strip() != "":
                    datos = linea.strip().split(",")

                    try:
                        if len(datos) == 5:
                            lista_prestamos.append({
                                "numero": int(datos[0]),
                                "codigo_libro": int(datos[1]),
                                "estudiante": datos[2],
                                "fecha": datos[3],
                                "estado": datos[4]
                            })
                        else:
                            print("Hay una linea de prestamos incompleta.")

                    except ValueError:
                        print("Un numero del archivo de prestamos esta mal.")

    except FileNotFoundError:
        guardar_prestamos(lista_prestamos)

    return lista_prestamos


def leer_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            return valor

        except ValueError:
            print("Dato incorrecto, ingrese un numero entero.")


def leer_texto(mensaje):
    while True:
        respuesta = input(mensaje).strip()

        if respuesta == "":
            print("Este espacio no puede quedar vacio.")
        elif "," in respuesta:
            print("No coloque comas, vuelva a escribir.")
        else:
            return respuesta


def buscar_por_codigo(libros, codigo):
    for elemento in libros:
        if elemento["codigo"] == codigo:
            return elemento

    return None


def registrar_libro(libros):
    print("\nREGISTRAR NUEVO LIBRO")

    codigo = 1

    for libro in libros:
        if libro["codigo"] >= codigo:
            codigo = libro["codigo"] + 1

    nuevo = {
        "codigo": codigo,
        "titulo": leer_texto("Nombre del libro: "),
        "autor": leer_texto("Nombre del autor: "),
        "estado": "Disponible"
    }

    libros.append(nuevo)
    guardar_libros(libros)

    print(f"\nRegistro completado. Codigo asignado: {codigo}")

    return nuevo


def mostrar_libros(libros):
    print("\nLISTA DE LIBROS")
    print("-" * 90)
    print(
        f"{'Codigo':<8}"
        f"{'Titulo':<34}"
        f"{'Autor':<28}"
        f"{'Estado'}"
    )
    print("-" * 90)

    cantidad = 0

    for libro in libros:
        print(
            f"{libro['codigo']:<8}"
            f"{libro['titulo']:<34}"
            f"{libro['autor']:<28}"
            f"{libro['estado']}"
        )
        cantidad += 1

    if cantidad == 0:
        print("No hay libros para mostrar.")

    print("-" * 90)
    print(f"Se muestran {cantidad} libros.")

    return cantidad


def buscar_libro(libros):
    print("\nBUSCAR UN LIBRO")

    texto = leer_texto("Que palabra desea buscar: ").lower()
    resultados = []

    for libro in libros:
        if texto in libro["titulo"].lower():
            resultados.append(libro)

    if len(resultados) == 0:
        print("No se encontro un titulo con esa palabra.")
    else:
        mostrar_libros(resultados)

    return len(resultados)


def prestar_libro(libros, prestamos):
    print("\nPRESTAR UN LIBRO")

    codigo = leer_entero("Escriba el codigo: ")
    seleccionado = buscar_por_codigo(libros, codigo)

    if seleccionado is None:
        print("Ese codigo no esta registrado.")
        return False

    if seleccionado["estado"] != "Disponible":
        print("El libro esta ocupado, no se puede prestar.")
        return False

    numero = 1

    for registro in prestamos:
        if registro["numero"] >= numero:
            numero = registro["numero"] + 1

    nombre = leer_texto("Estudiante que recibe el libro: ")

    prestamos.append({
        "numero": numero,
        "codigo_libro": codigo,
        "estudiante": nombre,
        "fecha": str(date.today()),
        "estado": "Activo"
    })

    seleccionado["estado"] = "Prestado"

    guardar_libros(libros)
    guardar_prestamos(prestamos)

    print("\nPrestamo realizado.")
    print(f"Numero de prestamo: {numero}")
    print(f"Libro entregado: {seleccionado['titulo']}")
    print(f"Recibido por: {nombre}")

    return True


def devolver_libro(libros, prestamos):
    print("\nDEVOLVER UN LIBRO")

    codigo = leer_entero("Codigo del libro que devuelve: ")
    seleccionado = buscar_por_codigo(libros, codigo)

    if seleccionado is None:
        print("Revise el codigo, ese libro no existe.")
        return False

    if seleccionado["estado"] != "Prestado":
        print("El libro ya esta disponible.")
        return False

    pendiente = None

    for registro in prestamos:
        if registro["codigo_libro"] == codigo:
            if registro["estado"] == "Activo":
                pendiente = registro
                break

    if pendiente is None:
        print("No se encontro el prestamo pendiente.")
        return False

    pendiente["estado"] = "Devuelto"
    seleccionado["estado"] = "Disponible"

    guardar_libros(libros)
    guardar_prestamos(prestamos)

    print(f"Devolucion registrada: {seleccionado['titulo']}")
    print("El libro se puede prestar nuevamente.")

    return True


def mostrar_prestamos(prestamos, libros):
    print("\nPRESTAMOS REALIZADOS")
    print("-" * 105)
    print(
        f"{'Numero':<8}"
        f"{'Titulo del libro':<34}"
        f"{'Estudiante':<30}"
        f"{'Fecha':<14}"
        f"{'Estado'}"
    )
    print("-" * 105)

    cantidad = 0

    for registro in prestamos:
        encontrado = buscar_por_codigo(
            libros, registro["codigo_libro"]
        )

        titulo = "Sin informacion"

        if encontrado is not None:
            titulo = encontrado["titulo"]

        print(
            f"{registro['numero']:<8}"
            f"{titulo:<34}"
            f"{registro['estudiante']:<30}"
            f"{registro['fecha']:<14}"
            f"{registro['estado']}"
        )

        cantidad += 1

    if cantidad == 0:
        print("Aun no se realizan prestamos.")

    print("-" * 105)

    return cantidad


def reporte_general(libros, prestamos):
    resumen = {
        "total_libros": len(libros),
        "disponibles": 0,
        "prestados": 0,
        "total_prestamos": len(prestamos),
        "activos": 0
    }

    for libro in libros:
        if libro["estado"] == "Disponible":
            resumen["disponibles"] += 1
        elif libro["estado"] == "Prestado":
            resumen["prestados"] += 1

    for registro in prestamos:
        if registro["estado"] == "Activo":
            resumen["activos"] += 1

    try:
        porcentaje = (
            resumen["prestados"] / resumen["total_libros"]
        ) * 100

    except ZeroDivisionError:
        porcentaje = 0

    resumen["porcentaje"] = porcentaje

    print("\n----------------------------------------")
    print("       INFORMACION DE LA BIBLIOTECA")
    print("----------------------------------------")
    print(f"Total de libros       : {resumen['total_libros']}")
    print(f"Libros disponibles    : {resumen['disponibles']}")
    print(f"Libros prestados      : {resumen['prestados']}")
    print(f"Prestamos registrados : {resumen['total_prestamos']}")
    print(f"Prestamos activos     : {resumen['activos']}")
    print(f"Libros prestados (%)  : {porcentaje:.1f}%")
    print("----------------------------------------")

    return resumen


def salir(libros, prestamos):
    guardar_libros(libros)
    guardar_prestamos(prestamos)

    print("\nDatos guardados, asta luego.")

    return 8


def main():
    try:
        libros = cargar_libros()
        prestamos = cargar_prestamos()

    except OSError:
        print("No se pudieron abrir o crear los archivos.")
        print("Revise los permisos de la carpeta.")
        return

    opcion = 0

    while opcion != 8:
        print("""
****************************************
         BIBLIOTECA TEC AZUAY
****************************************
  1 - Agregar libro
  2 - Ver libros
  3 - Buscar libro por titulo
  4 - Prestar libro a estudiante
  5 - Recibir libro devuelto
  6 - Ver lista de prestamos
  7 - Reporte de biblioteca
  8 - Guardar y salir
****************************************
""")

        opcion = leer_entero("Escoja una opcion: ")

        try:
            if opcion == 1:
                registrar_libro(libros)

            elif opcion == 2:
                mostrar_libros(libros)

            elif opcion == 3:
                buscar_libro(libros)

            elif opcion == 4:
                prestar_libro(libros, prestamos)

            elif opcion == 5:
                devolver_libro(libros, prestamos)

            elif opcion == 6:
                mostrar_prestamos(prestamos, libros)

            elif opcion == 7:
                reporte_general(libros, prestamos)

            elif opcion == 8:
                salir(libros, prestamos)

            else:
                print("Esa opcion no existe, escoja del 1 al 8.")

        except OSError:
            print("Ocurrio un problema al guardar los datos.")
            print("Revise la carpeta y vuelva a intentar.")
            opcion = 0


main()