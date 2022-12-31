"""
    Título del proyecto: GUI RECONOCIMIENTO DE IMÁGENES
    Descripción del proyecto: Interfaz que permite seleccionar una imágen por el usuario para asociarla a una clase.
    Autor: Cristian Del Angel Fiscal
    Fecha: 25/12/2022
    Licencia: Ninguna

    Librerías:
    tkinter: Kit de herramientas GUI.
    PIL: Procesamiento de imágenes directamente en python.
    lernmatrix: Funcionalidades para trabajar con algoritmo Lernamtrix de Steinbuch.
"""

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo

from PIL import ImageTk, Image

from lernmatrix import LernMatrix

class Aplicacion():
    """
        Interfaz Gráfica de Usuario que permite elegir al usuario alguna imágen
        y la procesa para darle una respuesta al usuario de la clase que le fue 
        asignada por el algoritmo.
    """

    def __init__(self, raiz) -> None:
        """
            Constructor de la clase.

            Parámetros:
            raiz: Widget principal de la GUI
        """

        frm_base = raiz
        frm_base.title('Enfoque asociativo')
        frm_base.geometry('230x130')
        frm_base.resizable(False, False)

        # Referencia y escalado de imágen de portada
        img = ImageTk.PhotoImage(Image.open('img_1.png').resize((230, 130)))
        lbl_img = ttk.Label(frm_base, image=img)
        lbl_img.place(x=0, y=0)

        l_info = ttk.Label(
            frm_base, 
            text='Memoria asociativa: \nLernmatrix',
            background='white'
        )
        l_info.grid(row=0, column=0, padx=5, pady=5)

        l_info = ttk.Label(
            frm_base, 
            text='Elija una imagen, con ruido o sin ruido,\ny verifique si es asociada correctamente.',
            background='white'
        )
        l_info.grid(row=2, column=0, padx=5, pady=5)

        btn_elegir_img = ttk.Button(frm_base, text='Elegir imagen', command=self.elegir_img)
        btn_elegir_img.grid(row=4, column=0, padx=5, pady=5)

        # Se necestia hacer referencia a la imágen, ya que si no es borrada de memoría
        lbl_img.image = img

    def elegir_img(self) -> None:
        """
            Permite seleccionar una imágen del explorador de archivos del usuario,
            y luego la ruta al archivo la envía a otro método.
        """

        dir_img = askopenfilename(
            title='Selecciona una imagen',
            filetypes=(('Imagen BMP', '*.bmp'), ('Imagen PNG', '*.png'))
        )

        self.asociar_img(dir_img)

    def asociar_img(self, dir_img) -> None:
        """
            Calcula todos los parámetros necesarios del algoritmo Lernmatrix, y al
            término muestra en una ventana emergente la clase asignada por el algoritmo.

            Parámetros:
            dir_img: Ruta relativa de una imágen.
        """

        controlador = LernMatrix()
        controlador.set_pixel_entrada(dir_img)
        controlador.set_matriz()
        controlador.set_vector_salida()
        controlador.set_clase()

        print(controlador.vector_salida)
        print(controlador.get_clase_asignada)

        showinfo(
            'Operación aritmetica asociada',
            controlador.get_clase_asignada
        )

if __name__ == '__main__':
    raiz = Tk()
    Aplicacion(raiz)
    raiz.mainloop()