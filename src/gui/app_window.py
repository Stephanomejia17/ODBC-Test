"""
Interfaz gráfica principal del sistema
"""
import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import threading
import sys

from database.connection import DatabaseConnection
from database.queries import DatabaseQueries
from utils.excel_handler import ExcelHandler
from utils.console_redirector import ConsoleRedirector
from assets.styles.colors import COLORS
from config.settings import APP_CONFIG

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class FabricacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_CONFIG['window_title'])
        self.root.geometry(f"{APP_CONFIG['window_width']}x{APP_CONFIG['window_height']}")
        self.root.configure(bg=COLORS['bg_main'])

        # Variables
        self.excel_path = None
        self.processing = False
        self.db_connection = DatabaseConnection()
        self.db_queries = DatabaseQueries()
        self.excel_handler = ExcelHandler()

        # Configuración de la interfaz
        self.setup_ui()

    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg=COLORS['bg_main'], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Logo arriba
        self.add_logo(main_frame)

        # Título
        title = tk.Label(
            main_frame,
            text="Sistema de troquelado",
            font=("Arial", 18, "bold"),
            bg=COLORS['bg_main'],
            fg=COLORS['text_primary']
        )
        title.pack(pady=(0, 10))

        # Frame para botones
        button_frame = tk.Frame(main_frame, bg=COLORS['bg_main'])
        button_frame.pack(fill=tk.X, pady=(0, 15))

        # Botón cargar Excel
        self.btn_cargar = tk.Button(
            button_frame,
            text="📁 Cargar archivo de excel",
            command=self.cargar_excel,
            font=("Arial", 12, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['button_text'],
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.btn_cargar.pack(side=tk.LEFT, padx=(0, 10))
        self.add_hover_effect(self.btn_cargar, COLORS['primary'], COLORS['primary_hover'])

        # Botón procesar
        self.btn_procesar = tk.Button(
            button_frame,
            text="▶ Procesar troquelado",
            command=self.iniciar_procesamiento,
            font=("Arial", 12, "bold"),
            bg=COLORS['primary'],
            fg=COLORS['button_text'],
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.btn_procesar.pack(side=tk.LEFT, padx=(0, 10))
        self.add_hover_effect(self.btn_procesar, COLORS['primary'], COLORS['primary_hover'])

        # Botón limpiar consola
        btn_limpiar = tk.Button(
            button_frame,
            text="🗑 Limpiar",
            command=self.limpiar_consola,
            font=("Arial", 12, "bold"),
            bg=COLORS['neutral'],
            fg=COLORS['button_text'],
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_limpiar.pack(side=tk.RIGHT)
        self.add_hover_effect(btn_limpiar, COLORS['neutral'], COLORS['neutral_hover'])

        # Label del archivo cargado
        self.lbl_archivo = tk.Label(
            main_frame,
            text="Ningún archivo seleccionado",
            font=("Arial", 10),
            bg=COLORS['bg_main'],
            fg=COLORS['text_secondary'],
            anchor="w"
        )
        self.lbl_archivo.pack(fill=tk.X, pady=(0, 10))

        # Barra de progreso
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(fill=tk.X, pady=(0, 15))

        # Frame para consola
        console_frame = tk.LabelFrame(
            main_frame,
            text="Consola de Logs",
            font=("Arial", 11, "bold"),
            bg=COLORS['bg_main'],
            fg=COLORS['text_primary'],
            padx=10,
            pady=10
        )
        console_frame.pack(fill=tk.BOTH, expand=True)

        # Área de texto con scroll para consola
        self.console = scrolledtext.ScrolledText(
            console_frame,
            font=("Consolas", 10),
            bg=COLORS['bg_console'],
            fg=COLORS['text_console'],
            insertbackground="white",
            wrap=tk.WORD,
            state=tk.NORMAL
        )
        self.console.pack(fill=tk.BOTH, expand=True)

        # Redirigir stdout a la consola
        sys.stdout = ConsoleRedirector(self.console)

        # Mensaje de bienvenida
        self.print_welcome_message()

    def add_logo(self, parent):
        if not PIL_AVAILABLE:
            print("⚠ PIL/Pillow no está instalado. Logo deshabilitado.")
            return

        try:
            logo_path = os.path.join(BASE_DIR, "assets", "images", "enthraLogo.png")

            if not os.path.exists(logo_path):
                print(f"⚠ Logo no encontrado en: {logo_path}")
                return

            imagen = Image.open(logo_path)
            imagen = imagen.resize((100, 40), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(imagen)

            logo_label = tk.Label(
                parent,
                image=self.logo,
                bg=COLORS['bg_main']
            )
            logo_label.pack(pady=10)
            print(f"✓ Logo cargado correctamente")

        except Exception as e:
            print(f"⚠ Error al cargar logo: {e}")

    def add_hover_effect(self, button, color_normal, color_hover):
        button.bind("<Enter>", lambda e: button.config(bg=color_hover))
        button.bind("<Leave>", lambda e: button.config(bg=color_normal))

    def print_welcome_message(self):
        # Logo ASCII de enthra
        print("""                                              
                                               ###                                          
                                      ###      ###                                          
                                      ###      ###                                          
      #########    ### ########   ############ ### ########    ###########  ###########     
    #####   #####  ######   ####    ########   #####    ####   #####    #  ####     ####    
   ####       #### ####       ###     ###      ####       ###  ###            ##########    
   ############### ####       ###     ###      ###        ###  ###         #############    
   ###             ####       ###     ###      ###        ###  ###        ###        ###    
   #####      ##   ####       ###     ###      ###        ###  ###        ###       ####    
     ############  ####       ###      ####### ###        ###  ###         #############    
         ###                              ##                                   ##                                                                                
        """)
        print("=" * 60)
        print("Sistema de troquelado - Listo para usar")
        print("=" * 60)
        print("\n1. Haga clic en 'Cargar Archivo Excel' para seleccionar el archivo")
        print("2. Haga clic en 'Procesar troquelado' para iniciar\n")

    def cargar_excel(self):
        excel_path = filedialog.askopenfilename(
            title="Seleccione el archivo Excel",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )

        if excel_path:
            self.excel_path = excel_path
            filename = excel_path.split("/")[-1]
            self.lbl_archivo.config(
                text=f"Archivo cargado: {filename}",
                fg=COLORS['text_success']
            )
            self.btn_procesar.config(state=tk.NORMAL)
            print(f"\n✓ Archivo cargado: {filename}")
        else:
            print("\n✗ No se seleccionó ningún archivo")

    def limpiar_consola(self):
        self.console.delete(1.0, tk.END)
        print("Consola limpia\n")

    def iniciar_procesamiento(self):
        if not self.excel_path:
            print("\n✗ ERROR: No hay archivo Excel cargado")
            return

        if self.processing:
            print("\n⚠ Ya hay un proceso en ejecución")
            return

        self.btn_cargar.config(state=tk.DISABLED)
        self.btn_procesar.config(state=tk.DISABLED)
        self.progress.start()
        self.processing = True

        thread = threading.Thread(target=self.procesar_fabricacion)
        thread.daemon = True
        thread.start()

    def procesar_fabricacion(self):
        conn = None
        try:
            print("\n" + "=" * 60)
            print("INICIANDO PROCESO DE TROQUELADO")
            print("=" * 60 + "\n")

            # Leer Excel
            print("📄 Leyendo archivo Excel...")
            df = self.excel_handler.read_excel(self.excel_path)
            print(f"✓ Archivo leído correctamente: {len(df)} productos encontrados\n")

            # Conectar a base de datos
            print("🔌 Conectando a base de datos...")
            conn = self.db_connection.connect()
            cur = conn.cursor()
            print("✓ Conexión establecida\n")

            # Procesar cada producto
            exitosos = 0
            fallidos = 0

            for idx, row in df.iterrows():
                FT_CODIGOPRODUCTO = row["FT_CODIGOPRODUCTO"].strip().zfill(8)
                NO_FABRICADOS = int(row["NO_FABRICADOS"])

                print("=" * 60)
                print(f"📦 Procesando producto {idx + 1}/{len(df)}: {FT_CODIGOPRODUCTO}")
                print(f"   Cantidad a fabricar: {NO_FABRICADOS}")

                try:
                    prod_ini = self.db_queries.get_producto_existencia(cur, FT_CODIGOPRODUCTO)
                    if not prod_ini:
                        raise Exception(f"Producto {FT_CODIGOPRODUCTO} no existe en depósito 1")

                    print(f"   Stock inicial: {prod_ini.FT_EXISTENCIA}")

                    materias = self.db_queries.get_materias_primas(cur, FT_CODIGOPRODUCTO)
                    if not materias:
                        raise Exception(f"Producto {FT_CODIGOPRODUCTO} no tiene ensambles")

                    print(f"   Materias primas requeridas: {len(materias)}")

                    for mp in materias:
                        consumo_total = int(NO_FABRICADOS * mp.FED_CANTIDAD)
                        print(f"   - {mp.FED_PRODUCTO}: Stock={mp.FT_EXISTENCIA}, Consumo={consumo_total}")

                        if mp.FT_EXISTENCIA - consumo_total < 0:
                            raise Exception(
                                f"STOCK INSUFICIENTE | "
                                f"Materia prima: {mp.FED_PRODUCTO} | "
                                f"Stock actual: {mp.FT_EXISTENCIA} | "
                                f"Consumo requerido: {consumo_total}"
                            )

                    self.db_queries.actualizar_producto_terminado(cur, FT_CODIGOPRODUCTO, NO_FABRICADOS)

                    for mp in materias:
                        consumo_total = int(NO_FABRICADOS * mp.FED_CANTIDAD)
                        self.db_queries.descontar_materia_prima(cur, mp.FED_PRODUCTO, consumo_total)

                    conn.commit()
                    print("   ✓ Troquelado aplicado correctamente")
                    exitosos += 1

                except Exception as e:
                    conn.rollback()
                    print("   ✗ OPERACIÓN CANCELADA PARA ESTE PRODUCTO")
                    print(f"   Error: {e}")
                    fallidos += 1

                print("")

            # Resumen final
            print("=" * 60)
            print("PROCESO FINALIZADO")
            print("=" * 60)
            print(f"✓ Productos procesados exitosamente: {exitosos}")
            print(f"✗ Productos con errores: {fallidos}")
            print(f"📊 Total productos: {len(df)}")
            print("=" * 60 + "\n")

        except Exception as e:
            print(f"\n❌ ERROR CRÍTICO: {e}\n")

        finally:
            if conn:
                self.db_connection.close(conn)
            # Rehabilitar botones
            self.root.after(0, self.finalizar_procesamiento)

    def finalizar_procesamiento(self):
        self.progress.stop()
        self.btn_cargar.config(state=tk.NORMAL)
        self.btn_procesar.config(state=tk.NORMAL)
        self.processing = False