import json
import random
import time
import tkinter as tk
from tkinter import messagebox

ARCHIVO = "preguntas1.json"
NUM_PREGUNTAS = 5
CONT_VINICIALES = 3
PUNTOS_POR_ACIERTO = 10
FUENTE_PREGUNTA = ("Times New Roman", 16, "bold")


def cargar_preguntas(ruta=ARCHIVO):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo '{ruta}'.")
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"El archivo '{ruta}' no tiene un formato JSON válido.")
    return None


class Juego(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QUIZ DE CULTURA GENERAL")
        self.geometry("520x380")
        self.resizable(False, False)
        self.config(bg="#ADD0ED")

        self.preguntas = []
        self.indice = 0
        self.puntos = 0
        self.vidas = CONT_VINICIALES
        self.inicio_tiempo = 0
        self.opcion = tk.IntVar(value=-1)

        # Corrección 1: nombre correcto del método
        self.pantalla_inicio()

    def limpiar(self):
        for w in self.winfo_children():
            w.destroy()

    def pantalla_inicio(self):
        self.limpiar()
        self.config(bg="#ADD0ED")
        tk.Label(self, text="QUIZ CULTURA GENERAL",
                 font=("Times New Roman", 26, "bold"),
                 bg="#ADD0ED", fg="#120cd2").pack(pady=(80, 10))
        tk.Label(self, text="¡Pon a prueba tus conocimientos!",
                 font=("Times New Roman", 14),
                 fg="#120cd2", bg="#ADD0ED").pack(pady=5)
        tk.Button(self, text="Comenzar", font=("Times New Roman", 14),
                  fg="#062046", bg="#138CB7",
                  command=self.comenzar).pack(pady=30)

    def comenzar(self):
        todas = cargar_preguntas()
        if todas is None:
            return
        if len(todas) < NUM_PREGUNTAS:
            messagebox.showerror(
                "Error",
                f"El archivo tiene solo {len(todas)} preguntas. Se necesitan al menos {NUM_PREGUNTAS}.",
            )
            return
        self.preguntas = random.sample(todas, NUM_PREGUNTAS)
        self.indice = 0
        self.puntos = 0
        self.vidas = CONT_VINICIALES
        self.inicio_tiempo = time.time()
        self.vista_juego()

    def vista_juego(self):
        self.limpiar()
        self.config(bg="#ADD0ED")
        self.opcion.set(-1)
        p = self.preguntas[self.indice]

        tk.Label(self, text=f"Pregunta {self.indice + 1} de {len(self.preguntas)}",
                 font=("Times New Roman", 11),
                 fg="#120cd2", bg="#ADD0ED").grid(row=0, column=0, sticky="w", padx=20, pady=(15, 0))
        tk.Label(self, text=f"Puntaje: {self.puntos}   Vidas: {self.vidas}",
                 font=("Times New Roman", 11),
                 fg="#120cd2", bg="#ADD0ED").grid(row=0, column=1, sticky="e", padx=20, pady=(15, 0))

        tk.Label(self, text=p["pregunta"],
                 font=FUENTE_PREGUNTA,
                 wraplength=470,
                 bg="#ADD0ED",
                 justify="left").grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        for i, texto in enumerate(p["opciones"]):
            tk.Radiobutton(self, text=texto, variable=self.opcion, value=i,
                           font=("Times New Roman", 12), bg="#ADD0ED").grid(row=2 + i, column=0, columnspan=2,
                                                                           sticky="w", padx=40, pady=3)

        tk.Button(self, text="Responder", font=("Times New Roman", 12),
                  fg="#062046",
                  bg="#138CB7",
                  command=self.responder).grid(row=7, column=0, columnspan=2, pady=20)

    def responder(self):
        if self.opcion.get() == -1:
            messagebox.showwarning("Aviso", "Selecciona una opción.")
            return

        if self.opcion.get() == self.preguntas[self.indice]["correcta"]:
            self.puntos += PUNTOS_POR_ACIERTO
        else:
            self.vidas -= 1

        self.indice += 1
        if self.vidas == 0 or self.indice >= len(self.preguntas):
            self.vista_resultados()
        else:
            self.vista_juego()

    def vista_resultados(self):
        tiempo_total = time.time() - self.inicio_tiempo
        self.limpiar()
        self.config(bg="#ADD0ED")

        if self.vidas == 0:
            motivo = "Te quedaste sin vidas"
        else:
            motivo = "¡Terminaste todas las preguntas!"

        tk.Label(self, text="Resultados", font=("Times New Roman", 26, "bold"),
                 fg="#120cd2",
                 bg="#ADD0ED").pack(pady=(40, 10))
        tk.Label(self, text=motivo,
                 font=("Times New Roman", 12),
                 fg="#120cd2",
                 bg="#ADD0ED").pack()
        tk.Label(self, text=f"Puntaje: {self.puntos}",
                 font=("Times New Roman", 14),
                 fg="#120cd2",
                 bg="#ADD0ED").pack(pady=5)
        tk.Label(self, text=f"Vidas restantes: {self.vidas}",
                 font=("Times New Roman", 14),
                 fg="#120cd2",
                 bg="#ADD0ED").pack(pady=5)
        tk.Label(self, text=f"Tiempo total: {tiempo_total:.1f} segundos",
                 font=("Times New Roman", 14),
                 fg="#120cd2",
                 bg="#ADD0ED").pack(pady=5)

        # Corrección 2: nombre correcto del método en el botón
        tk.Button(self, text="Jugar de nuevo",
                  font=("Times New Roman", 12),
                  fg="#062046",
                  bg="#138CB7",
                  command=self.pantalla_inicio).pack(pady=(25, 5))
        tk.Button(self, text="Salir", font=("Times New Roman", 12),
                  fg="#062046",
                  bg="#138CB7",
                  command=self.salir).pack()

    def salir(self):
        if messagebox.askyesno("Salir", "¿Seguro que quieres salir?"):
            self.destroy()


if __name__ == "__main__":
    Juego().mainloop()