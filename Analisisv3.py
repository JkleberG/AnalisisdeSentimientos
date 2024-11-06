import tkinter as tk
from tkinter import messagebox
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from PIL import Image, ImageTk
from concurrent.futures import ThreadPoolExecutor

# Configuración de análisis de sentimiento
analyzer = SentimentIntensityAnalyzer()
executor = ThreadPoolExecutor(max_workers=4)  # Limitar el número de hilos paralelos

# === Capa de Utilidades ===
class TranslationService:
    def __init__(self):
        self.translator = Translator()

    def translate_to_english(self, text):
        return self.translator.translate(text, dest='en').text

# === Capa de Lógica de Negocio ===
class SentimentAnalysisService:
    def analyze_sentiment(self, text):
        sentiment_scores = analyzer.polarity_scores(text)
        compound_score = sentiment_scores['compound']
        if compound_score > 0:
            return "Positivo"
        elif compound_score < 0:
            return "Negativo"
        else:
            return "Neutral"

# === Capa de Presentación (Interfaz de Usuario) ===
class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Análisis Emocional con NLP")
        self.translation_service = TranslationService()
        self.sentiment_service = SentimentAnalysisService()
        self.setup_ui()

    def setup_ui(self):
        self.center_window(600, 400)
        self.master.configure(bg="#F0F0F0")
        
        tk.Label(self.master, text="Análisis Emocional con NLP", bg="#F0F0F0", font=("Arial", 18, "bold")).pack(pady=20)
        
        # Cuadro de texto
        self.entrada_texto = tk.Text(self.master, width=40, height=5, font=("Arial", 14), wrap="word", borderwidth=2, relief=tk.GROOVE)
        self.entrada_texto.pack(pady=10)

        # Frame para botones
        frame_botones = tk.Frame(self.master, bg="#F0F0F0")
        frame_botones.pack(pady=10)

        # Botones de analizar y vaciar
        tk.Button(frame_botones, text="Analizar", command=self.iniciar_analisis, width=12, height=2, bg="#5CB85C", fg="white", relief=tk.GROOVE, font=("Arial", 12)).pack(side="left", padx=5)
        self.boton_vaciar = tk.Button(frame_botones, text="Vaciar", command=self.vaciar_texto, width=12, height=2, bg="#FF6347", fg="white", relief=tk.GROOVE, font=("Arial", 12))
        self.boton_vaciar.pack_forget()

        # Etiqueta de resultado
        self.etiqueta_resultado = tk.Label(self.master, text="", bg="#F0F0F0", font=("Arial", 16, "bold"))
        self.etiqueta_resultado.pack(pady=10)

        # Botón de ayuda con icono
        self.icono_ayuda = self.load_help_icon(r"C:\Users\JENS\Documents\Uni\Semestre10\Ingeniria y Fundamentos\Proyecto\Help.jpg")
        tk.Button(self.master, image=self.icono_ayuda, command=self.mostrar_ayuda, bg="#D3D3D3", relief=tk.GROOVE).pack(pady=10)

    def center_window(self, width, height):
        x_pos = (self.master.winfo_screenwidth() - width) // 2
        y_pos = (self.master.winfo_screenheight() - height) // 2
        self.master.geometry(f"{width}x{height}+{x_pos}+{y_pos}")

    def load_help_icon(self, path):
        img = Image.open(path)
        img = img.resize((30, 30), Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    def iniciar_analisis(self):
        texto_ingresado = self.entrada_texto.get("1.0", tk.END).strip()
        if not texto_ingresado:
            messagebox.showerror("Error", "Campo vacío. Por favor, ingresa texto.")
            return
        
        # Ejecutar traducción y análisis de sentimiento en paralelo
        future_translation = executor.submit(self.translation_service.translate_to_english, texto_ingresado)
        future_translation.add_done_callback(self.realizar_analisis)

    def realizar_analisis(self, future):
        texto_traducido = future.result()
        future_analysis = executor.submit(self.sentiment_service.analyze_sentiment, texto_traducido)
        future_analysis.add_done_callback(self.mostrar_resultado)

    def mostrar_resultado(self, future):
        resultado_sentimiento = future.result()
        self.etiqueta_resultado.config(text=f"\nSentimiento: {resultado_sentimiento}")
        self.boton_vaciar.pack(side="left", padx=10)

    def vaciar_texto(self):
        self.entrada_texto.delete("1.0", tk.END)
        self.etiqueta_resultado.config(text="")
        self.boton_vaciar.pack_forget()

    def mostrar_ayuda(self):
        self.master.withdraw()
        AyudaWindow(self.master)

class AyudaWindow:
    def __init__(self, parent):
        self.ayuda_window = tk.Toplevel(parent)
        self.ayuda_window.title("Ventana de Ayuda")
        self.center_window(500, 300)

        tk.Label(self.ayuda_window, text="Sistema de Análisis basado en NLP usando programación paralela y arquitectura por capas para la evaluación de textos de usuarios", font=("Arial", 16, "bold"), fg="black", bg="#5CB85C", wraplength=480).pack(pady=20)
        tk.Button(self.ayuda_window, text="Volver a Inicio", command=self.volver_inicio, width=12, height=2, bg="#5CB85C", fg="white", relief=tk.GROOVE, font=("Arial", 12)).pack(pady=10)

    def center_window(self, width, height):
        x_pos = (self.ayuda_window.winfo_screenwidth() - width) // 2
        y_pos = (self.ayuda_window.winfo_screenheight() - height) // 2
        self.ayuda_window.geometry(f"{width}x{height}+{x_pos}+{y_pos}")

    def volver_inicio(self):
        self.ayuda_window.destroy()
        root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
