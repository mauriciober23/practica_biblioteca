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
    hay_invalidos = False

    try:
        with open(ARCHIVO_LIBROS, "r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                if linea.strip() == "":
                    continue

                datos = linea.strip().split(",")

                try:
                    if len(datos) != 4:
                        raise ValueError("se necesitan exactamente 4 campos")

                    codigo = int(datos[0])
                    titulo = datos[1].strip()
                    autor = datos[2].strip()
                    estado = datos[3].strip()

                    if codigo <= 0:
                        raise ValueError("el codigo debe ser positivo")

                    if titulo == "" or autor == "":
                        raise ValueError("titulo y autor son obligatorios")

                    if estado not in ("Disponible", "Prestado"):
                        raise ValueError(
                            "el estado debe ser Disponible o Prestado"
                        )

                    libros.append(
                        Libro(codigo, titulo, autor, estado)
                    )

                except ValueError as error:
                    hay_invalidos = True
                    print(
                        f"{ARCHIVO_LIBROS}, linea {numero_linea}: "
                        f"registro ignorado ({error})."
                    )

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
        print("Se crearon los tres libros iniciales.")

    if hay_invalidos:
        print(
            f"Advertencia: al guardar {ARCHIVO_LIBROS}, "
            "las lineas invalidas ignoradas no se conservaran."
        )

    return libros


def cargar_prestamos():
    prestamos = []
    hay_invalidos = False

    try:
        with open(ARCHIVO_PRESTAMOS, "r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                if linea.strip() == "":
                    continue

                datos = linea.strip().split(",")

                try:
                    if len(datos) != 5:
                        raise ValueError("se necesitan exactamente 5 campos")

                    numero = int(datos[0])
                    codigo_libro = int(datos[1])
                    estudiante = datos[2].strip()
                    fecha = datos[3].strip()
                    estado = datos[4].strip()

                    if numero <= 0 or codigo_libro <= 0:
                        raise ValueError(
                            "numero y codigo deben ser positivos"
                        )

                    if estudiante == "" or fecha == "":
                        raise ValueError(
                            "estudiante y fecha son obligatorios"
                        )

                    if estado not in ("Activo", "Devuelto"):
                        raise ValueError(
                            "el estado debe ser Activo o Devuelto"
                        )

                    prestamos.append(
                        Prestamo(
                            numero,
                            codigo_libro,
                            estudiante,
                            fecha,
                            estado
                        )
                    )

                except ValueError as error:
                    hay_invalidos = True
                    print(
                        f"{ARCHIVO_PRESTAMOS}, linea {numero_linea}: "
                        f"registro ignorado ({error})."
                    )

    except FileNotFoundError:
        guardar_prestamos(prestamos)

    if hay_invalidos:
        print(
            f"Advertencia: al guardar {ARCHIVO_PRESTAMOS}, "
            "las lineas invalidas ignoradas no se conservaran."
        )

    return prestamos


def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))

        except ValueError:
            print("Dato incorrecto, ingrese un numero entero.")


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()

        if texto == "":
            print("Este dato no puede quedar vacio.")

        elif "," in texto:
            print("No coloque comas, vuelva a escribir.")

        else:
            return texto


def buscar_por_codigo(libros, codigo):
    for libro in libros:
        if libro.codigo == codigo:
            return libro

    return None


def comprobar_coherencia(libros, prestamos):
    correcto = True

    for prestamo in prestamos:
        libro = buscar_por_codigo(libros, prestamo.codigo_libro)

        if libro is None:
            print(
                f"Advertencia en {ARCHIVO_PRESTAMOS}: "
                f"el prestamo {prestamo.numero} refiere al libro "
                f"{prestamo.codigo_libro}, que no existe "
                f"en {ARCHIVO_LIBROS}."
            )
            correcto = False

    for libro in libros:
        activos = 0

        for prestamo in prestamos:
            if prestamo.codigo_libro == libro.codigo:
                if prestamo.estado == "Activo":
                    activos += 1

        if libro.estado == "Prestado" and activos != 1:
            print(
                f"Advertencia: el libro {libro.codigo} esta Prestado "
                f"y tiene {activos} prestamos activos. "
                "Debe tener exactamente uno."
            )
            correcto = False

        elif libro.estado == "Disponible" and activos > 0:
            print(
                f"Advertencia: el libro {libro.codigo} "
                f"esta Disponible y tiene {activos} prestamos activos."
            )
            correcto = False

    if not correcto:
        print(
            "Los registros se mantienen con sus estados actuales. "
            "Las operaciones y la salida guardaran los datos "
            "que estan en memoria."
        )

    return correcto


def registrar_libro(libros):
    print("\nREGISTRAR NUEVO LIBRO")

    codigo = 1

    for libro in libros:
        if libro.codigo >= codigo:
            codigo = libro.codigo + 1

    titulo = leer_texto("Nombre del libro: ")
    autor = leer_texto("Nombre del autor: ")

    nuevo_libro = Libro(
        codigo,
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
    print("\nLISTA DE LIBROS")
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
        print("No hay libros para mostrar.")

    print("-" * 90)
    print(f"Se muestran {len(libros)} libros.")

    return len(libros)


def buscar_libro(libros):
    print("\nBUSCAR UN LIBRO")

    palabra = leer_texto("Palabra que desea buscar: ").lower()
    encontrados = []

    for libro in libros:
        if palabra in libro.titulo.lower():
            encontrados.append(libro)

    if len(encontrados) == 0:
        print("No se encontro un titulo con esa palabra.")
    else:
        mostrar_libros(encontrados)

    return len(encontrados)


def prestar_libro(libros, prestamos):
    print("\nPRESTAR UN LIBRO")

    codigo = leer_entero("Escriba el codigo: ")
    libro = buscar_por_codigo(libros, codigo)

    if libro is None:
        print("Ese codigo no esta registrado.")
        return False

    if libro.estado != "Disponible":
        print("El libro no esta disponible para prestarlo.")
        return False

    numero = 1

    for prestamo in prestamos:
        if prestamo.numero >= numero:
            numero = prestamo.numero + 1

    estudiante = leer_texto("Estudiante que recibe el libro: ")

    nuevo_prestamo = Prestamo(
        numero,
        codigo,
        estudiante,
        str(date.today()),
        "Activo"
    )

    prestamos.append(nuevo_prestamo)
    libro.cambiar_estado("Prestado")

    guardar_libros(libros)
    guardar_prestamos(prestamos)

    print("\nPrestamo realizado.")
    print(f"Libro entregado: {libro.titulo}")
    print(nuevo_prestamo)

    return True


def devolver_libro(libros, prestamos):
    print("\nDEVOLVER UN LIBRO")

    codigo = leer_entero("Codigo del libro que devuelve: ")
    libro = buscar_por_codigo(libros, codigo)

    if libro is None:
        print("Ese libro no existe.")
        return False

    if libro.estado != "Prestado":
        print("El libro ya esta disponible.")
        return False

    prestamo_activo = None

    for prestamo in prestamos:
        if prestamo.codigo_libro == codigo:
            if prestamo.estado == "Activo":
                prestamo_activo = prestamo
                break

    if prestamo_activo is None:
        print("No se encontro un prestamo activo para este libro.")
        return False

    prestamo_activo.cambiar_estado("Devuelto")
    libro.cambiar_estado("Disponible")

    guardar_libros(libros)
    guardar_prestamos(prestamos)

    print(f"Devolucion registrada: {libro.titulo}")
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

    for prestamo in prestamos:
        libro = buscar_por_codigo(libros, prestamo.codigo_libro)
        titulo = "Libro no encontrado"

        if libro is not None:
            titulo = libro.titulo

        prestamo.mostrar(titulo)

    if len(prestamos) == 0:
        print("Aun no se realizan prestamos.")

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

    print("\nDatos guardados. Hasta luego.")

    return 8


def main():
    try:
        libros = cargar_libros()
        prestamos = cargar_prestamos()

    except (OSError, UnicodeError) as error:
        print(f"No se pudieron cargar los archivos: {error}")
        return

    comprobar_coherencia(libros, prestamos)

    opcion = 0

    while opcion != 8:
        print("""
****************************************
         BIBLIOTECA TEC AZUAY
****************************************
  1. Registrar libro
  2. Mostrar libros
  3. Buscar por titulo
  4. Prestar libro
  5. Devolver libro
  6. Mostrar prestamos
  7. Reporte general
  8. Guardar y salir
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
                print("Opcion incorrecta. Escoja del 1 al 8.")

        except OSError as error:
            print(f"No se pudieron guardar los datos: {error}")
            print("Los cambios siguen en memoria. Intente guardar otra vez.")
            opcion = 0


if __name__ == "__main__":
    main()