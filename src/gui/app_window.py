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
from config.settings import APP_CONFIG, DEPOSITO_ID

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
            return

        try:
            logo_path = os.path.join(BASE_DIR, "assets", "images", "enthraLogo.png")
            if not os.path.exists(logo_path):
                return

            imagen = Image.open(logo_path)
            imagen = imagen.resize((100, 40), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(imagen)

            logo_label = tk.Label(parent, image=self.logo, bg=COLORS['bg_main'])
            logo_label.pack(pady=10)

        except Exception:
            pass

    def add_hover_effect(self, button, color_normal, color_hover):
        button.bind("<Enter>", lambda e: button.config(bg=color_hover))
        button.bind("<Leave>", lambda e: button.config(bg=color_normal))

    def print_welcome_message(self):
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
        print("=" * 70)
        print("Sistema de troquelado - Modo Completo A2")
        print("=" * 70)
        print("\n📋 PROCESO IMPLEMENTADO:")
        print("   1. Transferencia de materias primas entre depósitos")
        print("   2. Actualización de SEnsamblesDetalle con campos completos")
        print("   3. Incremento de contadores en SSistema")
        print("   4. Movimiento de existencias (origen → destino)")
        print("   5. Creación de orden de ensamble")
        print("   6. Registro de operación de transferencia")
        print("\n" + "=" * 70)
        print("INSTRUCCIONES:")
        print("=" * 70)
        print("1. Haga clic en 'Cargar Archivo Excel' para seleccionar el archivo")
        print("2. Haga clic en 'Procesar troquelado' para iniciar")
        print("3. Las órdenes se emiten y quedan listas para cerrar en A2")
        print("=" * 70 + "\n")

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
            print(f"✓ Archivo cargado: {filename}\n")
        else:
            print("✗ No se seleccionó ningún archivo\n")

    def limpiar_consola(self):
        self.console.delete(1.0, tk.END)
        print("Consola limpia\n")

    def iniciar_procesamiento(self):
        if not self.excel_path:
            print("✗ ERROR: No hay archivo Excel cargado\n")
            return

        if self.processing:
            print("⚠ Ya hay un proceso en ejecución\n")
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
        cur = None

        try:
            print("=" * 70)
            print("INICIANDO PROCESO DE TROQUELADO")
            print("=" * 70 + "\n")

            # Leer archivo Excel
            df = self.excel_handler.read_excel(self.excel_path)
            print(f"✓ Productos en archivo: {len(df)}\n")

            # Validar columnas
            if 'FT_CODIGOPRODUCTO' not in df.columns or 'NO_FABRICADOS' not in df.columns:
                raise Exception("El archivo Excel debe contener las columnas 'FT_CODIGOPRODUCTO' y 'NO_FABRICADOS'")

            # Conectar a BD
            conn = self.db_connection.connect()
            cur = conn.cursor()
            print(f"✓ Conexión establecida (Depósito: {DEPOSITO_ID})\n")

            # Validar depósito destino
            try:
                deposito_destino = self.db_queries.get_deposito_destino(cur)

                if deposito_destino == DEPOSITO_ID:
                    raise Exception(
                        f"❌ CONFIGURACIÓN INVÁLIDA:\n"
                        f"   Depósito origen ({DEPOSITO_ID}) = Depósito destino ({deposito_destino})\n"
                        f"   Corrija en BD: UPDATE SSistema SET DEPOSITO_ENSAMBLEDESTINO = '2'\n"
                    )

                print(f"✓ Depósito destino: {deposito_destino}\n")

            except Exception as e:
                print(f"{'='*70}")
                print("❌ ERROR DE CONFIGURACIÓN")
                print(f"{'='*70}")
                print(str(e))
                print(f"{'='*70}\n")
                raise Exception("No se puede continuar: Configuración de depósito inválida")

            # Procesar cada producto
            print("=" * 70)
            print("PROCESANDO PRODUCTOS")
            print("=" * 70 + "\n")

            exitosos = 0
            fallidos = 0
            productos_fallidos = []

            for idx, row in df.iterrows():
                try:
                    FT_CODIGOPRODUCTO = str(row["FT_CODIGOPRODUCTO"]).strip().zfill(8)
                    NO_FABRICADOS = float(row["NO_FABRICADOS"])

                    print(f"[{idx + 1}/{len(df)}] Procesando: {FT_CODIGOPRODUCTO} (Cantidad: {NO_FABRICADOS})")

                    # Verificar producto
                    prod_ini = self.db_queries.get_producto_existencia(cur, FT_CODIGOPRODUCTO)
                    if not prod_ini:
                        raise Exception(f"Producto no existe en depósito {DEPOSITO_ID}")

                    # Obtener fórmula
                    materias = self.db_queries.get_materias_primas(cur, FT_CODIGOPRODUCTO)
                    if not materias or len(materias) == 0:
                        raise Exception("Sin fórmula de ensamble")

                    print(f"   ✓ Fórmula: {len(materias)} materia(s) prima(s)")

                    # Validar stock
                    faltantes = []
                    for mp in materias:
                        consumo = NO_FABRICADOS * mp.FED_CANTIDAD
                        if mp.FT_EXISTENCIA < consumo:
                            faltantes.append(mp.FED_PRODUCTO)

                    if faltantes:
                        raise Exception(f"Stock insuficiente: {', '.join(faltantes)}")

                    print(f"   ✓ Stock validado")

                    # Procesar ensamble
                    documento = self.db_queries.procesar_ensamble_completo(
                        cur, FT_CODIGOPRODUCTO, NO_FABRICADOS
                    )

                    # Commit
                    conn.commit()

                    print(f"   ✅ PROCESADO - Doc: {documento}\n")
                    exitosos += 1

                except Exception as e:
                    conn.rollback()
                    print(f"   ❌ ERROR: {str(e)}\n")
                    fallidos += 1
                    productos_fallidos.append({
                        'codigo': FT_CODIGOPRODUCTO,
                        'error': str(e)
                    })

            # Resumen final
            print("=" * 70)
            print("RESUMEN FINAL")
            print("=" * 70)
            print(f"Total productos: {len(df)}")
            print(f"Exitosos: {exitosos}")
            print(f"Fallidos: {fallidos}")

            if exitosos > 0:
                print(f"\n✅ {exitosos} órdenes emitidas correctamente")
                print("⚠️  Recordar cerrar las órdenes desde A2")

            if fallidos > 0:
                print(f"\n❌ Productos con errores:")
                for pf in productos_fallidos:
                    print(f"   • {pf['codigo']}: {pf['error'][:50]}...")

            print("\n" + "=" * 70 + "\n")

        except Exception as e:
            print(f"{'='*70}")
            print("❌ ERROR CRÍTICO")
            print(f"{'='*70}")
            print(f"{e}\n")

            if conn:
                try:
                    conn.rollback()
                    print("⚠️  Cambios revertidos (ROLLBACK)\n")
                except:
                    pass

        finally:
            if cur:
                try:
                    cur.close()
                except:
                    pass

            if conn:
                try:
                    self.db_connection.close(conn)
                except:
                    pass

            self.root.after(0, self.finalizar_procesamiento)

    def finalizar_procesamiento(self):
        self.progress.stop()
        self.btn_cargar.config(state=tk.NORMAL)
        self.btn_procesar.config(state=tk.NORMAL)
        self.processing = False
        print("✓ Sistema listo\n")