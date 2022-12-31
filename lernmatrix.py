"""
    Título del proyecto: RECONOCIMIENTO DE IMÁGENES
    Descripción del proyecto: Implementación del algoritmo Lernmatrix de Steinbuch.
    Autor: Cristian Del Angel Fiscal
    Fecha: 23/12/2022
    Licencia: Ninguna

    Librerías:
    pickle: Para transformar un objeto complejo en una secuencia de bytes.
    numpy: Operar vectores y matrices.
    cv2: Operar imágenes.
"""

import pickle

import numpy as np
import cv2 as cv

class LernMatrix():
    """
        La clase implementa las funciones necesarias para la fase
        de aprendizaje (generar memoria asociativa) y fase de recuperación
        del método de Lernmatrix de Steinbuch.
    """

    def __init__(self) -> None:
        """
            Constructor de la clase.

            Parámetros:
            img_list: Lista que guarda los pixeles de la imagen de entrada
            matriz: Lista que almacena la matriz de aprendizaje
            vector_salida: Lista que almacena el vector de salida, que es de 7 elementos
            clase: Cadena que indica la clase asignada
        """

        self.img_list = []
        self.matriz = []
        self.vector_salida = []
        self.clase = ""

    # ---------------------FASE DE APRENDIZAJE ------------------------

    def calcular_fila_lernmatrix(self, img_list: list) -> list:
        """
            Compara cada una de las clases (filas de la Lernmatrix) con los pixeles 
            de la imagen (columnas de la lernmatrix), para asignarles un valor EPSILON.
            
            Parámetros:
            img_list: Contiene otras listas, que representan las filas de pixeles de la imagen.

            Retorno:
            Lista que representa una de las filas de la Lernmatrix, por cada clase. 
        """

        # Valor arbitrario para EPSILON > 0
        EPSILON = 1

        # Lista con todos los pixeles
        list_matrix_x1 = []

        for fila in img_list:
            # Se unen las listas en una sola
            list_matrix_x1 = list_matrix_x1 + fila

        # Fila de la Lernmatrix con los epsilon
        list_matrix_y1 = []

        for i in list_matrix_x1:
            if i == 255:
                list_matrix_y1.append(EPSILON)
            elif i == 0:
                list_matrix_y1.append(-EPSILON)

        return list_matrix_y1

    def almacenar_matriz(self, lista_pix: list) -> None:
        """
            Escribe un archivo de bytes que almacena la Lernmatrix.

            Parámetros:
            lista_pix: Filas de EPSILON calculadas para todas las clases.
        """
    
        with open('Matriz_aprendizaje', 'wb') as archivo_salida:
            pickle.dump(lista_pix, archivo_salida)

            archivo_salida.close()
        
    def recuperar_matriz(self) -> list:
        """
            Recupera la Lernmatrix del archivo binario.

            Retorno:
            Lista de listas con los valores EPSILON correspondientes.
        """

        with open('Matriz_aprendizaje', 'rb') as archivo_entrada:
            matriz = pickle.load(archivo_entrada)

            archivo_entrada.close()

        return matriz
    
    # --------------------- FASE DE RECUPERACIÓN ------------------------

    def set_pixel_entrada(self, dir_img: str) -> None:
        """
            Lee los pixeles de una imagen, los convierte en una sola lista y
            lo asigna a la variable de la clase img_list.

            Parámetros:
            dir_img: Ruta relativa a la imagen seleccionada por el usuario
        """

        # Escala de grises para obtener 0 ó 255
        img = cv.imread(dir_img, cv.IMREAD_GRAYSCALE)
        img_list = np.array(img).tolist()

        # Lista con todos los pixeles
        list_matrix_x1 = []

        for fila in img_list:
            # Se unen las listas en una sola
            list_matrix_x1 = list_matrix_x1 + fila

        self.img_list = list_matrix_x1

    def set_matriz(self) -> None:
        """
            Recupera la Lernmatrix del archivo binario y asigna la información
            en la variable matriz perteneciente a la clase.
        """

        with open('Matriz_aprendizaje', 'rb') as archivo_entrada:
            self.matriz = pickle.load(archivo_entrada)

            archivo_entrada.close()

    def set_vector_salida(self) -> None:
        """
            Multiplica cada fila de la Lernmatrix con el vector de entrada (pixeles de la imagen),
            luego suma los resultados por cada fila y los almacena en la variable de la clase 
            vector_salida.
        """

        # Se convierte en arreglo numpy para más rapidez en la multiplicación
        vector_entrada = np.array(self.img_list)

        for fila_matriz in self.matriz:
            mult_fila_vect = np.array(fila_matriz) * vector_entrada
            resultado = sum(mult_fila_vect)

            self.vector_salida.append(resultado)

    def set_clase(self) -> None:
        """
            Asocia el índice del elemento más grande en el vector de salida con la
            clase correspondiente, entonces asigna una cadena a la variable clase, para
            indicarle al usuario final a qué clase pertenece la imagen seleccionada.
        """

        max_vector = max(self.vector_salida)
        posicion_max = self.vector_salida.index(max_vector)

        posicion_max += 1

        if posicion_max == 1:
            self.clase = "La imagen corresponde al operador División"
        elif posicion_max == 2:
            self.clase = "La imagen corresponde al operador Suma"
        elif posicion_max == 3:
            self.clase = "La imagen corresponde al operador Resta"
        elif posicion_max == 4:
            self.clase = "La imagen corresponde al operador Or"
        elif posicion_max == 5:
            self.clase = "La imagen corresponde al operador Multiplicación"
        elif posicion_max == 6:
            self.clase = "La imagen corresponde al operador Igualdad"
        elif posicion_max == 7:
            self.clase = "La imagen corresponde al operador And"

    @property
    def get_img_list(self) -> list:
        return self.img_list

    @property
    def get_matriz(self) -> list:
        return self.matriz

    @property
    def get_vector_salida(self) -> list:
        return self.vector_salida

    @property
    def get_clase_asignada(self) -> str:
        return self.clase

if __name__ == '__main__':
    aprendizaje = LernMatrix()

    """# IMREAD_GRAYSCALE para obtener 0 o 255
    # Calculamos la fila de la imagen Division
    img = cv.imread('Division.bmp', cv.IMREAD_GRAYSCALE)
    img_list = np.array(img).tolist()
    fila_c1_div = aprendizaje.calcular_fila_lernmatrix(img_list)

    # Calculamos la fila de la imagen Suma
    img = cv.imread('Suma.bmp', cv.IMREAD_GRAYSCALE)
    img_list = np.array(img).tolist()
    fila_c2_sum = aprendizaje.calcular_fila_lernmatrix(img_list)

    # Calculamos la fila de la imagen Resta
    img = cv.imread('Resta.bmp', cv.IMREAD_GRAYSCALE)
    img_list = np.array(img).tolist()
    fila_c3_rest = aprendizaje.calcular_fila_lernmatrix(img_list)

    # Calculamos la fila de la imagen Or
    img = cv.imread('Or.bmp', cv.IMREAD_GRAYSCALE)
    img_list = np.array(img).tolist()
    fila_c4_or = aprendizaje.calcular_fila_lernmatrix(img_list)

    # Calculamos la fila de la imagen Multiplicacion
    img = cv.imread('Multiplicacion.bmp', cv.IMREAD_GRAYSCALE)
    img_list = np.array(img).tolist()
    fila_c5_multi = aprendizaje.calcular_fila_lernmatrix(img_list)

    # Calculamos la fila de la imagen Igualdad
    img = cv.imread('Igualdad.bmp', cv.IMREAD_GRAYSCALE)
    img_list = np.array(img).tolist()
    fila_c6_igual = aprendizaje.calcular_fila_lernmatrix(img_list)

    # Calculamos la fila de la imagen And
    img = cv.imread('And.bmp', cv.IMREAD_GRAYSCALE)
    img_list = np.array(img).tolist()
    fila_c7_and = aprendizaje.calcular_fila_lernmatrix(img_list)

    matriz_aprendizaje = []
    matriz_aprendizaje.append(fila_c1_div)
    matriz_aprendizaje.append(fila_c2_sum)
    matriz_aprendizaje.append(fila_c3_rest)
    matriz_aprendizaje.append(fila_c4_or)
    matriz_aprendizaje.append(fila_c5_multi)
    matriz_aprendizaje.append(fila_c6_igual)
    matriz_aprendizaje.append(fila_c7_and)

    aprendizaje.almacenar_matriz(matriz_aprendizaje)"""

    matriz = aprendizaje.recuperar_matriz()

    print(len(matriz))

    for elemento in matriz:
        print(len(elemento))
        print(elemento)