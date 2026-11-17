from datetime import date


ARCHIVO_LIBROS = "libros.txt"
ARCHIVO_PRESTAMOS = "prestamos.txt"


class Libro:
    def __init__(self, codigo, titulo, autor, estado):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.estado = estado

    def mostrar(self):
        print(
            f"{self.codigo:<8}"
            f"{self.titulo:<34}"
            f"{self.autor:<28}"
            f"{self.estado}"
        )

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def __str__(self):
        return (
            f"Codigo: {self.codigo}, "
            f"titulo: {self.titulo}, "
            f"autor: {self.autor}, "
            f"estado: {self.estado}"
        )


class Prestamo:
    def __init__(self, numero, codigo_libro, estudiante, fecha, estado):
        self.numero = numero
        self.codigo_libro = codigo_libro
        self.estudiante = estudiante
        self.fecha = fecha
        self.estado = estado

    def mostrar(self, titulo):
        print(
            f"{self.numero:<8}"
            f"{titulo:<34}"
            f"{self.estudiante:<30}"
            f"{self.fecha:<14}"
            f"{self.estado}"
        )

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def __str__(self):
        return (
            f"Prestamo: {self.numero}, "
            f"codigo del libro: {self.codigo_libro}, "
            f"estudiante: {self.estudiante}, "
            f"fecha: {self.fecha}, "
            f"estado: {self.estado}"
        )


def guardar_libros(libros):
    with open(ARCHIVO_LIBROS, "w", encoding="utf-8") as archivo:
        for libro in libros:
            archivo.write(
                f"{libro.codigo},{libro.titulo},"
                f"{libro.autor},{libro.estado}\n"
            )

    return len(libros)


def guardar_prestamos(prestamos):
    with open(ARCHIVO_PRESTAMOS, "w", encoding="utf-8") as archivo:
        for prestamo in prestamos:
            archivo.write(
                f"{prestamo.numero},{prestamo.codigo_libro},"
                f"{prestamo.estudiante},{prestamo.fecha},"
                f"{prestamo.estado}\n"
            )

    return len(prestamos)


def cargar_libros():
    libros = []

    try:
        with open(ARCHIVO_LIBROS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if linea.strip() != "":
                    datos = linea.strip().split(",")

                    try:
                        if len(datos) == 4:
                            libro = Libro(
                                int(datos[0]),
                                datos[1],
                                datos[2],
                                datos[3]
                            )

                            libros.append(libro)
                        else:
                            print("Una linea de libros esta incompleta.")

                    except ValueError:
                        print("Hay un codigo incorrecto en libros.txt.")

    except FileNotFoundError:
        libros.append(
            Libro(
                1,
                "Python para todos",
                "Charles Severance",
                "Disponible"
            )
        )

        libros.append(
            Libro(
                2,
                "Aprende Java",
                "Ana Torres",
                "Disponible"
            )
        )

        libros.append(
            Libro(
                3,
                "Bases de datos",
                "Carlos Mora",
                "Disponible"
            )
        )

        guardar_libros(libros)
        print("Se agregaron los tres libros iniciales.")

    return libros


def cargar_prestamos():
    prestamos = []

    try:
        with open(ARCHIVO_PRESTAMOS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if linea.strip() != "":
                    datos = linea.strip().split(",")

                    try:
                        if len(datos) == 5:
                            prestamo = Prestamo(
                                int(datos[0]),
                                int(datos[1]),
                                datos[2],
                                datos[3],
                                datos[4]
                            )

                            prestamos.append(prestamo)
                        else:
                            print("Una linea de prestamos esta incompleta.")

                    except ValueError:
                        print("Hay un numero incorrecto en prestamos.txt.")

    except FileNotFoundError:
        guardar_prestamos(prestamos)

    return prestamos


def leer_entero(mensaje):
    while True:
        try:
            numero = int(input(mensaje))
            return numero

        except ValueError:
            print("Ingrese un numero entero, vuelva a intentar.")


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()

        if texto == "":
            print("Debe escribir este dato.")

        elif "," in texto:
            print("El texto no puede tener comas.")

        else:
            return texto


def buscar_por_codigo(libros, codigo):
    for libro in libros:
        if libro.codigo == codigo:
            return libro

    return None


def registrar_libro(libros):
    print("\nAGREGAR UN LIBRO")

    siguiente_codigo = 1

    for libro in libros:
        if libro.codigo >= siguiente_codigo:
            siguiente_codigo = libro.codigo + 1

    titulo = leer_texto("Titulo del libro: ")
    autor = leer_texto("Autor del libro: ")

    nuevo_libro = Libro(
        siguiente_codigo,
        titulo,
        autor,
        "Disponible"
    )

    libros.append(nuevo_libro)
    guardar_libros(libros)

    print("\nLibro registrado.")
    print(nuevo_libro)

    return nuevo_libro


def mostrar_libros(libros):
    print("\nCATALOGO DE LA BIBLIOTECA")
    print("-" * 90)

    print(
        f"{'Codigo':<8}"
        f"{'Titulo':<34}"
        f"{'Autor':<28}"
        f"{'Estado'}"
    )

    print("-" * 90)

    for libro in libros:
        libro.mostrar()

    if len(libros) == 0:
        print("No hay libros registrados.")

    print("-" * 90)
    print(f"Cantidad de libros: {len(libros)}")

    return len(libros)


def buscar_libro(libros):
    print("\nBUSQUEDA POR TITULO")

    palabra = leer_texto("Palabra que desea buscar: ").lower()
    encontrados = []

    for libro in libros:
        if palabra in libro.titulo.lower():
            encontrados.append(libro)

    if len(encontrados) == 0:
        print("No se encontraron libros con esa palabra.")
    else:
        mostrar_libros(encontrados)

    return len(encontrados)


def prestar_libro(libros, prestamos):
    print("\nNUEVO PRESTAMO")

    codigo = leer_entero("Codigo del libro: ")
    libro = buscar_por_codigo(libros, codigo)

    if libro is None:
        print("No existe un libro con ese codigo.")
        return False

    if libro.estado != "Disponible":
        print("El libro ya esta prestado.")
        return False

    siguiente_numero = 1

    for prestamo in prestamos:
        if prestamo.numero >= siguiente_numero:
            siguiente_numero = prestamo.numero + 1

    estudiante = leer_texto("Nombre del estudiante: ")

    nuevo_prestamo = Prestamo(
        siguiente_numero,
        codigo,
        estudiante,
        str(date.today()),
        "Activo"
    )

    prestamos.append(nuevo_prestamo)
    libro.cambiar_estado("Prestado")

    guardar_libros(libros)
    guardar_prestamos(prestamos)

    print("\nPrestamo registrado.")
    print(f"Libro: {libro.titulo}")
    print(nuevo_prestamo)

    return True


def devolver_libro(libros, prestamos):
    print("\nDEVOLUCION DE LIBRO")

    codigo = leer_entero("Codigo del libro que devuelve: ")
    libro = buscar_por_codigo(libros, codigo)

    if libro is None:
        print("El codigo ingresado no existe.")
        return False

    if libro.estado != "Prestado":
        print("Ese libro ya esta disponible.")
        return False

    prestamo_activo = None

    for prestamo in prestamos:
        if prestamo.codigo_libro == codigo:
            if prestamo.estado == "Activo":
                prestamo_activo = prestamo
                break

    if prestamo_activo is None:
        print("No se encontro un prestamo activo para ese libro.")
        return False

    libro.cambiar_estado("Disponible")
    prestamo_activo.cambiar_estado("Devuelto")

    guardar_libros(libros)
    guardar_prestamos(prestamos)

    print(f"Libro devuelto: {libro.titulo}")
    print("La devolucion se guardo correctamente.")

    return True


def mostrar_prestamos(prestamos, libros):
    print("\nHISTORIAL DE PRESTAMOS")
    print("-" * 105)

    print(
        f"{'Numero':<8}"
        f"{'Libro':<34}"
        f"{'Estudiante':<30}"
        f"{'Fecha':<14}"
        f"{'Estado'}"
    )

    print("-" * 105)

    for prestamo in prestamos:
        libro = buscar_por_codigo(libros, prestamo.codigo_libro)
        titulo = "Libro sin informacion"

        if libro is not None:
            titulo = libro.titulo

        prestamo.mostrar(titulo)

    if len(prestamos) == 0:
        print("Todavia no hay prestamos registrados.")

    print("-" * 105)
    print(f"Cantidad de prestamos: {len(prestamos)}")

    return len(prestamos)


def reporte_general(libros, prestamos):
    disponibles = 0
    prestados = 0
    activos = 0

    for libro in libros:
        if libro.estado == "Disponible":
            disponibles += 1
        elif libro.estado == "Prestado":
            prestados += 1

    for prestamo in prestamos:
        if prestamo.estado == "Activo":
            activos += 1

    try:
        porcentaje = prestados * 100 / len(libros)

    except ZeroDivisionError:
        porcentaje = 0

    print("\n========================================")
    print("         REPORTE DE BIBLIOTECA")
    print("========================================")
    print(f"Libros registrados: {len(libros)}")
    print(f"Libros disponibles: {disponibles}")
    print(f"Libros prestados: {prestados}")
    print(f"Prestamos registrados: {len(prestamos)}")
    print(f"Prestamos activos: {activos}")
    print(f"Porcentaje de libros prestados: {porcentaje:.1f}%")
    print("========================================")

    return porcentaje


def salir(libros, prestamos):
    guardar_libros(libros)
    guardar_prestamos(prestamos)

    print("\nInformacion guardada, asta luego.")

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
  1. Registrar libro
  2. Mostrar libros
  3. Buscar libro
  4. Prestar libro
  5. Devolver libro
  6. Mostrar prestamos
  7. Reporte general
  8. Guardar y salir
****************************************
""")

        opcion = leer_entero("Ingrese una opcion: ")

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
                print("Opcion incorrecta, ingrese del 1 al 8.")

        except OSError:
            print("No se pudieron guardar los datos.")
            print("Revise la carpeta y vuelva a intentar.")
            opcion = 0


main()