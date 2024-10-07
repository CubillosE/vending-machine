import os
import tkinter as tk

import matplotlib.pyplot as plt
import networkx as nx
from PIL import Image, ImageTk


class VendingMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Máquina Expendedora")
        self.root.geometry("979x979")
        # ALFABETO
        self.alfabeto = {"0", "1"}
        # ESTADO INICIAL
        self.estado_inicial = "q0"
        # ESTADOS DE ACEPTACION
        self.estados_aceptacion = {
            "q4",
            "q5",
            "q7",
            "q8",
            "q11",
            "q12",
            "q14",
            "q15",
            "q19",
            "q20",
            "q22",
            "q23",
            "q26",
            "q27",
            "q29",
            "q30",
        }
        # TRANSICIONES
        self.transiciones = {
            "q0": {"0": "q1", "1": "q16"},
            "q1": {"0": "q2", "1": "q9"},
            "q2": {"0": "q3", "1": "q6"},
            "q3": {"0": "q4", "1": "q5"},
            "q6": {"0": "q7", "1": "q8"},
            "q9": {"0": "q10", "1": "q13"},
            "q10": {"0": "q11", "1": "q12"},
            "q13": {"0": "q14", "1": "q15"},
            "q16": {"1": "q17", "0": "q24"},
            "q17": {"1": "q18", "0": "q21"},
            "q18": {"1": "q19", "0": "q20"},
            "q21": {"1": "q22", "0": "q23"},
            "q24": {"1": "q25", "0": "q28"},
            "q25": {"1": "q26", "0": "q27"},
            "q28": {"1": "q29", "0": "q30"},
        }
        self.productos = {
            "0000": "Barra de Cereal",
            "0001": "Crackers",
            "0010": "Snickers",
            "0011": "Frutos Rojos",
            "0100": "Agua",
            "0101": "Pepsi",
            "0110": "Coca-Cola",
            "0111": "Monsters",
            "1000": "Margaritas Pollo",
            "1001": "Tostacos",
            "1010": "Detodito",
            "1011": "Doritos",
            "1100": "Burrito",
            "1101": "Ensalada",
            "1110": "Sandwich",
            "1111": "Lasaña",
        }
        # GRAMATICA
        self.gramatica = "./images/Gramatica.jpeg"
        # TABLA DE TRANSICION
        self.tabla = "./images/Tabla.jpeg"
        self.setup_ui()

    def setup_ui(self):
        imagen_fondo = Image.open("images/vending machine.png").resize(
            (979, 979), Image.LANCZOS
        )
        self.fondo = ImageTk.PhotoImage(imagen_fondo)
        tk.Label(self.root, image=self.fondo).place(x=0, y=0, relwidth=1, relheight=1)

        fondo_recortado = imagen_fondo.crop((505, 730, 605, 830))
        self.fondo_recortado_tk = ImageTk.PhotoImage(fondo_recortado)
        self.canvas_imagen = tk.Canvas(
            self.root, width=100, height=100, highlightthickness=0
        )
        self.canvas_imagen.place(x=505, y=730)
        self.canvas_imagen.create_image(
            0, 0, anchor="nw", image=self.fondo_recortado_tk
        )

        self.entrada_texto = tk.Entry(
            self.root, font=("Arial", 14), width=18, justify="center"
        )
        self.entrada_texto.place(x=708, y=758)
        self.entrada_texto.bind("<Return>", self.capturar_entradas)

    def validar_entrada(self, entrada):
        return len(entrada) == 4 and set(entrada).issubset(self.alfabeto)

    def mostrar_imagen_producto(self, producto):
        ruta_imagen = f"images/{producto}.png"
        if os.path.exists(ruta_imagen):
            imagen_producto = Image.open(ruta_imagen).resize((100, 100), Image.LANCZOS)
            imagen_producto_tk = ImageTk.PhotoImage(imagen_producto)
            self.canvas_imagen.delete("all")
            self.canvas_imagen.create_image(
                0, 0, anchor="nw", image=self.fondo_recortado_tk
            )
            self.canvas_imagen.create_image(0, 0, anchor="nw", image=imagen_producto_tk)
            self.canvas_imagen.image = imagen_producto_tk
        else:
            print(f"No se encontró la imagen para el producto {producto}")

    def graficar_automata(self, camino):
        G = nx.DiGraph()

        for origen, destinos in self.transiciones.items():
            for simbolo, destino in destinos.items():
                G.add_edge(origen, destino, label=simbolo)

        G.add_edge("start", self.estado_inicial, label="")

        nodo_actual = self.estado_inicial
        camino_aristas = []
        nodos_visitados = [nodo_actual]

        for simbolo in camino:
            nodo_siguiente = self.transiciones.get(nodo_actual, {}).get(simbolo)
            if nodo_siguiente:
                camino_aristas.append((nodo_actual, nodo_siguiente))
                nodo_actual = nodo_siguiente
                nodos_visitados.append(nodo_actual)

        pos = self._hierarchy_pos(G, root="start")
        node_colors = []
        node_shapes = []
        for node in G.nodes():
            if node == "start":
                node_colors.append("white")
            elif node in nodos_visitados and node in self.estados_aceptacion:
                node_colors.append("green")
                node_shapes.append("doublecircle")
            elif node in nodos_visitados:
                node_colors.append("green")
                node_shapes.append("circle")
            elif node in self.estados_aceptacion:
                node_colors.append("blue")
                node_shapes.append("doublecircle")
            else:
                node_colors.append("skyblue")
                node_shapes.append("circle")

        edge_colors = [
            "green" if edge in camino_aristas else "black" for edge in G.edges()
        ]

        plt.figure(figsize=(10, 6))
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=node_colors,
            node_size=1200,
            font_size=12,
            arrowsize=20,
            edge_color=edge_colors,
        )
        nx.draw_networkx_nodes(
            G, pos, node_color=node_colors, node_size=1200, node_shape="o", linewidths=2
        )
        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels={(u, v): d["label"] for u, v, d in G.edges(data=True)},
            font_color="red",
            font_size=10,
        )
        plt.title(f"Grafo del Automata - Entrada: {camino}", fontsize=16)
        plt.axis("off")
        plt.savefig("./images/grafo_automata.png")
        plt.close()

    def _hierarchy_pos(
        self, G, root=None, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5
    ):
        if root is None:
            root = list(G.nodes())[0]
        pos = {root: (xcenter, vert_loc)}
        children = list(G.neighbors(root))
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos.update(
                    self._hierarchy_pos(
                        G,
                        child,
                        width=dx,
                        vert_gap=vert_gap,
                        vert_loc=vert_loc - vert_gap,
                        xcenter=nextx,
                    )
                )
        return pos

    def mostrar_tabla_y_gramatica(self):
        ventana_info = tk.Toplevel(self.root)
        ventana_info.title("Automata, Gramática y Tabla")
        ventana_info.configure(bg="white")
        ventana_info.geometry("1400x800")

        frame_principal = tk.Frame(ventana_info, bg="white")
        frame_principal.pack(padx=10, pady=10, fill="both", expand=True)

        img_grafo = Image.open("./images/grafo_automata.png").resize(
            (900, 700), Image.LANCZOS
        )
        img_grafo_tk = ImageTk.PhotoImage(img_grafo)
        label_grafo = tk.Label(frame_principal, image=img_grafo_tk)
        label_grafo.image = img_grafo_tk
        label_grafo.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        img_table = Image.open(self.tabla).resize((400, 300), Image.LANCZOS)
        img_table_tk = ImageTk.PhotoImage(img_table)
        label_table = tk.Label(frame_principal, image=img_table_tk)
        label_table.image = img_table_tk
        label_table.grid(row=0, column=1, padx=10, pady=10)

        img_grammar = Image.open(self.gramatica).resize((400, 250), Image.LANCZOS)
        img_grammar_tk = ImageTk.PhotoImage(img_grammar)
        label_grammar = tk.Label(frame_principal, image=img_grammar_tk)
        label_grammar.image = img_grammar_tk
        label_grammar.grid(row=1, column=1, padx=10, pady=10)

        ventana_info.mainloop()

    def capturar_entradas(self, event=None):
        try:
            entrada_usuario = self.entrada_texto.get()
            if self.validar_entrada(entrada_usuario):
                producto = self.productos.get(entrada_usuario, "Producto no encontrado")
                self.entrada_texto.delete(0, tk.END)
                self.mostrar_imagen_producto(producto)
                self.graficar_automata(entrada_usuario)
                self.mostrar_tabla_y_gramatica()
            else:
                print(
                    "No pertenece al automata. Debe ser una secuencia de 4 dígitos que solo contenga 0 y 1."
                )
            if self.root.winfo_exists():
                self.entrada_texto.delete(0, tk.END)
        except tk.TclError:
            print(
                "La aplicación principal se ha cerrado. No se puede continuar con la operación."
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = VendingMachineApp(root)
    root.mainloop()
