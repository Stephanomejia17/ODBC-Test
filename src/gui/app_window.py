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
        cur = None

        try:
            print("\n" + "=" * 70)
            print("INICIANDO PROCESO DE TROQUELADO")
            print("Modo: REPLICACIÓN COMPLETA DE A2")
            print("=" * 70 + "\n")

            # ================================================================
            # PASO 1: LEER ARCHIVO EXCEL
            # ================================================================
            print("📄 PASO 1: Leyendo archivo Excel...")
            print("-" * 70)
            df = self.excel_handler.read_excel(self.excel_path)
            print(f"✓ Archivo leído correctamente")
            print(f"✓ Productos encontrados: {len(df)}")
            print(f"✓ Columnas requeridas: FT_CODIGOPRODUCTO, NO_FABRICADOS")

            # Validar columnas requeridas
            if 'FT_CODIGOPRODUCTO' not in df.columns or 'NO_FABRICADOS' not in df.columns:
                raise Exception("El archivo Excel debe contener las columnas 'FT_CODIGOPRODUCTO' y 'NO_FABRICADOS'")

            print("")

            # ================================================================
            # PASO 2: CONECTAR A BASE DE DATOS
            # ================================================================
            print("🔌 PASO 2: Conectando a base de datos...")
            print("-" * 70)
            conn = self.db_connection.connect()
            cur = conn.cursor()
            print("✓ Conexión establecida exitosamente")
            print(f"✓ Depósito de trabajo: {DEPOSITO_ID}")

            # Obtener depósito destino CON VALIDACIÓN
            try:
                deposito_destino = self.db_queries.get_deposito_destino(cur)
                print(f"✓ Depósito destino (producción): {deposito_destino}")

                # Validación adicional de seguridad
                if deposito_destino == DEPOSITO_ID:
                    raise Exception(
                        f"\n❌ CONFIGURACIÓN INVÁLIDA DETECTADA:\n"
                        f"   Depósito origen ({DEPOSITO_ID}) = Depósito destino ({deposito_destino})\n"
                        f"   Las transferencias DEBEN ser entre depósitos DIFERENTES\n"
                        f"\n   Por favor, corrija la configuración en la base de datos:\n"
                        f"   UPDATE SSistema SET DEPOSITO_ENSAMBLEDESTINO = '2'\n"
                        f"   (Use un depósito diferente a {DEPOSITO_ID})\n"
                    )

            except Exception as e:
                error_msg = str(e)
                print(f"\n{'='*70}")
                print("❌ ERROR DE CONFIGURACIÓN")
                print('='*70)
                print(error_msg)
                print('='*70)
                raise Exception("No se puede continuar: Configuración de depósito inválida")

            print("")

            # ================================================================
            # PASO 3: PROCESAR CADA PRODUCTO
            # ================================================================
            print("📦 PASO 3: Procesando productos...")
            print("=" * 70 + "\n")

            exitosos = 0
            fallidos = 0
            productos_fallidos = []

            for idx, row in df.iterrows():
                try:
                    # Normalizar código de producto
                    FT_CODIGOPRODUCTO = str(row["FT_CODIGOPRODUCTO"]).strip().zfill(8)
                    NO_FABRICADOS = float(row["NO_FABRICADOS"])

                    print("┌" + "─" * 68 + "┐")
                    print(f"│ PRODUCTO {idx + 1}/{len(df)}: {FT_CODIGOPRODUCTO}".ljust(69) + "│")
                    print("├" + "─" * 68 + "┤")
                    print(f"│ Cantidad a fabricar: {NO_FABRICADOS}".ljust(69) + "│")
                    print("└" + "─" * 68 + "┘\n")

                    # --------------------------------------------------------
                    # 3.1: Verificar existencia del producto
                    # --------------------------------------------------------
                    print("   [1/6] Verificando producto terminado...")
                    prod_ini = self.db_queries.get_producto_existencia(cur, FT_CODIGOPRODUCTO)

                    if not prod_ini:
                        raise Exception(
                            f"El producto {FT_CODIGOPRODUCTO} no existe en el depósito {DEPOSITO_ID}"
                        )

                    print(f"   ✓ Producto encontrado")
                    print(f"   ✓ Stock actual: {prod_ini.FT_EXISTENCIA:.2f} unidades")

                    # --------------------------------------------------------
                    # 3.2: Obtener fórmula de ensamble (materias primas)
                    # --------------------------------------------------------
                    print(f"\n   [2/6] Obteniendo fórmula de ensamble...")
                    materias = self.db_queries.get_materias_primas(cur, FT_CODIGOPRODUCTO)

                    if not materias or len(materias) == 0:
                        raise Exception(
                            f"El producto {FT_CODIGOPRODUCTO} no tiene fórmula de ensamble definida "
                            f"(no hay materias primas activas en SEnsamblesDetalle)"
                        )

                    print(f"   ✓ Fórmula encontrada: {len(materias)} materia(s) prima(s)")

                    # Mostrar fórmula
                    print(f"\n   📋 Composición del producto:")
                    total_consumo_valor = 0
                    for mp in materias:
                        consumo_unitario = mp.FED_CANTIDAD
                        consumo_total = NO_FABRICADOS * consumo_unitario

                        # Calcular costo
                        try:
                            costo_mp = self.db_queries.get_costo_producto(cur, mp.FED_PRODUCTO, DEPOSITO_ID)
                            valor_consumo = consumo_total * costo_mp
                            total_consumo_valor += valor_consumo
                        except:
                            costo_mp = 0
                            valor_consumo = 0

                        print(f"      • {mp.FED_PRODUCTO}")
                        print(f"        - Por unidad: {consumo_unitario:.4f}")
                        print(f"        - Consumo total: {consumo_total:.4f}")
                        print(f"        - Costo unitario: ${costo_mp:,.2f}")
                        print(f"        - Valor total: ${valor_consumo:,.2f}")

                    print(f"\n   💰 Valor total de materias primas: ${total_consumo_valor:,.2f}")

                    # --------------------------------------------------------
                    # 3.3: Validar disponibilidad de materias primas
                    # --------------------------------------------------------
                    print(f"\n   [3/6] Validando disponibilidad de stock...")

                    faltantes = []
                    for mp in materias:
                        consumo_total = NO_FABRICADOS * mp.FED_CANTIDAD

                        if mp.FT_EXISTENCIA < consumo_total:
                            faltante = consumo_total - mp.FT_EXISTENCIA
                            faltantes.append({
                                'codigo': mp.FED_PRODUCTO,
                                'disponible': mp.FT_EXISTENCIA,
                                'requerido': consumo_total,
                                'faltante': faltante
                            })
                            print(f"   ❌ {mp.FED_PRODUCTO}: Stock={mp.FT_EXISTENCIA:.2f}, Requerido={consumo_total:.2f}, Falta={faltante:.2f}")
                        else:
                            print(f"   ✓ {mp.FED_PRODUCTO}: Stock={mp.FT_EXISTENCIA:.2f}, Requerido={consumo_total:.2f} ✓")

                    if faltantes:
                        mensaje_error = f"STOCK INSUFICIENTE - Faltan {len(faltantes)} materia(s) prima(s):\n"
                        for f in faltantes:
                            mensaje_error += f"      • {f['codigo']}: Falta {f['faltante']:.2f} unidades\n"
                        raise Exception(mensaje_error)

                    print(f"   ✓ Stock suficiente para todas las materias primas")

                    # --------------------------------------------------------
                    # 3.4: Obtener siguiente número de documento
                    # --------------------------------------------------------
                    print(f"\n   [4/6] Generando número de documento...")
                    doc_orden = self.db_queries.get_siguiente_documento(
                        cur, 'SEnsamblesOrden', 'FEO_DOCUMENTO'
                    )
                    doc_operacion = self.db_queries.get_siguiente_documento(
                        cur, 'SOperacionInv', 'FTI_DOCUMENTO'
                    )
                    print(f"   ✓ Documento orden: {doc_orden}")
                    print(f"   ✓ Documento operación: {doc_operacion}")

                    # --------------------------------------------------------
                    # 3.5: Procesar ensamble completo (6 operaciones)
                    # --------------------------------------------------------
                    print(f"\n   [5/6] Procesando ensamble completo...")
                    print(f"   ⚙️  Replicando comportamiento de A2...")
                    print(f"   📝 Operaciones a realizar:")
                    print(f"      1. INSERT en SDetalleInv (Transferencia)")
                    print(f"      2. INSERT en SEnsamblesDetalle (Detalles)")
                    print(f"      3. UPDATE en SSistema (contadores)")
                    print(f"      4. UPDATE en SinvDep (ambos depósitos)")
                    print(f"      5. INSERT en SEnsamblesOrden")
                    print(f"      6. INSERT en SOperacionInv")
                    print("")

                    documento = self.db_queries.procesar_ensamble_completo(
                        cur, FT_CODIGOPRODUCTO, NO_FABRICADOS
                    )

                    # --------------------------------------------------------
                    # 3.6: Commit de la transacción
                    # --------------------------------------------------------
                    print(f"\n   [6/6] Confirmando transacción...")
                    conn.commit()
                    print(f"   ✅ Transacción confirmada exitosamente")

                    # Resumen del producto
                    print(f"\n   ╔════════════════════════════════════════════════════════════╗")
                    print(f"   ║  ✅ PRODUCTO PROCESADO EXITOSAMENTE                        ║")
                    print(f"   ╠════════════════════════════════════════════════════════════╣")
                    print(f"   ║  Producto: {FT_CODIGOPRODUCTO}                                  ║")
                    print(f"   ║  Cantidad: {NO_FABRICADOS}                                          ║")
                    print(f"   ║  Documento: {documento}                                    ║")
                    print(f"   ║  Materias primas: {len(materias)}                                     ║")
                    print(f"   ║  Valor: ${total_consumo_valor:,.2f}".ljust(61) + "║")
                    print(f"   ║  Estado: EMITIDA (lista para cerrar en A2)                ║")
                    print(f"   ╚════════════════════════════════════════════════════════════╝")

                    exitosos += 1

                except Exception as e:
                    # Rollback de la transacción
                    conn.rollback()

                    print(f"\n   ╔════════════════════════════════════════════════════════════╗")
                    print(f"   ║  ❌ ERROR AL PROCESAR PRODUCTO                             ║")
                    print(f"   ╠════════════════════════════════════════════════════════════╣")
                    print(f"   ║  Producto: {FT_CODIGOPRODUCTO}                                  ║")
                    print(f"   ║  Transacción revertida (ROLLBACK)                         ║")
                    print(f"   ╚════════════════════════════════════════════════════════════╝")
                    print(f"\n   📋 Detalle del error:")

                    error_msg = str(e)
                    # Dividir mensaje largo en líneas
                    for line in error_msg.split('\n'):
                        if line.strip():
                            print(f"      {line}")

                    fallidos += 1
                    productos_fallidos.append({
                        'codigo': FT_CODIGOPRODUCTO,
                        'error': str(e)
                    })

                print("\n")

            # ================================================================
            # PASO 4: RESUMEN FINAL
            # ================================================================
            print("\n" + "=" * 70)
            print("RESUMEN FINAL DEL PROCESO")
            print("=" * 70)
            print(f"\n📊 Estadísticas:")
            print(f"   • Total productos en Excel: {len(df)}")
            print(f"   • Productos procesados exitosamente: {exitosos}")
            print(f"   • Productos con errores: {fallidos}")

            if exitosos > 0:
                print(f"\n✅ Operaciones completadas para {exitosos} producto(s):")
                print(f"   • Materias primas transferidas entre depósitos")
                print(f"   • Órdenes de ensamble emitidas")
                print(f"   • Inventarios actualizados correctamente")
                print(f"   • Contadores del sistema incrementados")
                print(f"\n⚠️  IMPORTANTE:")
                print(f"   Las órdenes están EMITIDAS y deben cerrarse desde A2 para:")
                print(f"   • Generar el informe de producción")
                print(f"   • Incrementar el stock del producto terminado")
                print(f"   • Completar el ciclo de fabricación")

            if fallidos > 0:
                print(f"\n❌ Productos con errores ({fallidos}):")
                for pf in productos_fallidos:
                    print(f"   • {pf['codigo']}: {pf['error'][:80]}...")

            print("\n" + "=" * 70)

            if exitosos == len(df):
                print("🎉 PROCESO COMPLETADO EXITOSAMENTE")
            elif exitosos > 0:
                print("⚠️  PROCESO COMPLETADO CON ADVERTENCIAS")
            else:
                print("❌ PROCESO COMPLETADO CON ERRORES")

            print("=" * 70 + "\n")

        except Exception as e:
            print(f"\n" + "=" * 70)
            print("❌ ERROR CRÍTICO EN EL PROCESO")
            print("=" * 70)
            print(f"\n{e}\n")

            import traceback
            print("📋 Traceback completo:")
            print("-" * 70)
            traceback.print_exc()
            print("-" * 70)

            if conn:
                try:
                    conn.rollback()
                    print("\n⚠️  Se ha revertido cualquier cambio pendiente (ROLLBACK)")
                except:
                    pass

        finally:
            # Cerrar cursor y conexión
            if cur:
                try:
                    cur.close()
                    print("\n🔌 Cursor cerrado")
                except:
                    pass

            if conn:
                try:
                    self.db_connection.close(conn)
                    print("🔌 Conexión a base de datos cerrada")
                except:
                    pass

            # Finalizar en el hilo principal
            self.root.after(0, self.finalizar_procesamiento)

    def finalizar_procesamiento(self):
        self.progress.stop()
        self.btn_cargar.config(state=tk.NORMAL)
        self.btn_procesar.config(state=tk.NORMAL)
        self.processing = False
        print("\n✓ Sistema listo para procesar nuevos archivos\n")