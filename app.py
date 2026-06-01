<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MIND MUSCLE - Sistema de Control y Evaluación</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    
    <style>
        /* ==========================================================================
           ESTILOS GENERALES Y DISEÑO DE INTERFAZ (SISTEMA DE DISEÑO OSCURO)
           ========================================================================== */
        :root {
            --bg-principal: #0a0c10;
            --bg-secundario: #121620;
            --bg-tarjeta: #1a1f2c;
            --texto-claro: #f1f5f9;
            --texto-mutado: #94a3b8;
            --color-marca: #00e5ff;
            --color-marca-hover: #00b8d4;
            --color-exito: #22c55e;
            --color-alerta: #eab308;
            --color-error: #ef4444;
            --color-neutro: #64748b;
            --borde-suave: rgba(255, 255, 255, 0.08);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Arial', sans-serif;
        }

        body {
            background-color: var(--bg-principal);
            color: var(--texto-claro);
            line-height: 1.6;
            padding-bottom: 60px;
        }

        .contenedor-global {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Encabezado Principal Estilo MM247 */
        header {
            background: linear-gradient(135deg, var(--bg-secundario) 0%, #1e2538 100%);
            padding: 30px 20px;
            border-radius: 16px;
            margin-bottom: 30px;
            border: 1px solid var(--borde-suave);
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        header h1 {
            font-size: 2.5rem;
            font-weight: 900;
            letter-spacing: 2px;
            color: #ffffff;
            text-transform: uppercase;
            margin-bottom: 5px;
        }

        header p {
            color: var(--color-marca);
            font-size: 1.1rem;
            font-weight: 600;
        }

        /* Sistema de Navegación */
        nav {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }

        .btn-nav {
            background-color: var(--bg-secundario);
            color: var(--texto-claro);
            border: 1px solid var(--borde-suave);
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .btn-nav:hover, .btn-nav.activo {
            background-color: var(--color-marca);
            color: var(--bg-principal);
            border-color: var(--color-marca);
            box-shadow: 0 0 15px rgba(0, 229, 255, 0.4);
        }

        /* Secciones del Enrutador */
        .seccion-app {
            display: none;
            animation: fadeIn 0.4s ease-in-out forwards;
        }

        .seccion-app.activa {
            display: block;
        }

        /* Tarjetas y Contenedores Base */
        .tarjeta-panel {
            background-color: var(--bg-secundario);
            border: 1px solid var(--borde-suave);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 25px;
        }

        .titulo-seccion {
            font-size: 1.8rem;
            margin-bottom: 20px;
            border-bottom: 2px solid var(--borde-suave);
            padding-bottom: 10px;
            color: #ffffff;
        }

        /* Estilos de Formularios y Cuestionarios */
        .grupo-formulario {
            margin-bottom: 20px;
        }

        .grupo-formulario label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: var(--texto-claro);
        }

        .control-formulario {
            width: 100%;
            background-color: var(--bg-tarjeta);
            border: 1px solid var(--borde-suave);
            color: #ffffff;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }

        .control-formulario:focus {
            outline: none;
            border-color: var(--color-marca);
        }

        /* Opciones Múltiples Especiales */
        .opciones-bloque {
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
            margin-top: 10px;
        }

        .opcion-item {
            background-color: var(--bg-tarjeta);
            border: 1px solid var(--borde-suave);
            padding: 15px;
            border-radius: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.2s ease;
        }

        .opcion-item:hover {
            border-color: rgba(0, 229, 255, 0.5);
            background-color: rgba(255, 255, 255, 0.02);
        }

        .opcion-item input[type="radio"] {
            accent-color: var(--color-marca);
            width: 18px;
            height: 18px;
        }

        /* Botones de Acción */
        .btn-accion {
            background-color: var(--color-marca);
            color: var(--bg-principal);
            border: none;
            padding: 14px 28px;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            display: inline-block;
            text-align: center;
        }

        .btn-accion:hover {
            background-color: var(--color-marca-hover);
            box-shadow: 0 0 20px rgba(0, 229, 255, 0.5);
        }

        /* Alertas de Confirmación Exclusivas */
        .bloque-exito-id {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(34, 197, 94, 0.2) 100%);
            border: 2px dashed var(--color-exito);
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            margin-top: 20px;
        }

        .token-id {
            font-size: 2.2rem;
            font-weight: 900;
            color: var(--color-marca);
            letter-spacing: 4px;
            margin: 15px 0;
            text-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
        }

        /* ==========================================================================
           REESTRUCTURA DEL DASHBOARD ADMIN (VISTA DE LISTA COMPLETA)
           ========================================================================== */
        .tabla-alumnos-contenedor {
            overflow-x: auto;
            margin-top: 20px;
        }

        .tabla-alumnos {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            background-color: var(--bg-tarjeta);
            border-radius: 12px;
            overflow: hidden;
        }

        .tabla-alumnos th {
            background-color: #1e2538;
            color: #ffffff;
            padding: 16px 20px;
            font-weight: bold;
            font-size: 0.95rem;
            text-transform: uppercase;
            border-bottom: 2px solid var(--borde-suave);
        }

        .tabla-alumnos td {
            padding: 16px 20px;
            border-bottom: 1px solid var(--borde-suave);
            vertical-align: middle;
        }

        .tabla-alumnos tr:last-child td {
            border-bottom: none;
        }

        .tabla-alumnos tr:hover {
            background-color: rgba(255, 255, 255, 0.02);
        }

        .col-id {
            font-family: 'Courier New', monospace;
            font-weight: bold;
            color: var(--color-marca);
        }

        /* Barra de Progreso Dinámica Automatizada */
        .contenedor-barra-progreso {
            width: 100%;
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            height: 14px;
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .llenado-barra {
            height: 100%;
            border-radius: 20px;
            transition: width 0.5s ease-in-out;
            width: 0%;
        }

        /* Colores Condicionales de Estado */
        .barra-avance { background-color: var(--color-exito); }
        .barra-retroceso { background-color: var(--color-error); }
        .barra-lento { background-color: var(--color-alerta); }
        .barra-vacia { background-color: var(--color-neutro); }

        .etiqueta-estado {
            font-size: 0.85rem;
            font-weight: bold;
            display: block;
            margin-bottom: 4px;
        }

        .btn-tabla-reporte {
            background-color: #1e2538;
            color: var(--color-marca);
            border: 1px solid var(--color-marca);
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            font-size: 0.85rem;
            transition: all 0.2s ease;
            white-space: nowrap;
        }

        .btn-tabla-reporte:hover {
            background-color: var(--color-marca);
            color: var(--bg-principal);
            box-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
        }

        /* Panel Dinámico Detalle del Reporte de Alumno */
        .panel-detalle-alumno {
            background-color: var(--bg-tarjeta);
            border: 1px solid rgba(0, 229, 255, 0.2);
            border-radius: 12px;
            padding: 25px;
            margin-top: 30px;
            display: none;
        }

        .cuadricula-comparativa {
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
            margin-bottom: 25px;
        }

        @media(min-width: 768px) {
            .cuadricula-comparativa {
                grid-template-columns: 1fr 1fr;
            }
        }

        .bloque-columna-reporte {
            background-color: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--borde-suave);
            border-radius: 8px;
            padding: 20px;
        }

        .area-descargas {
            background-color: #1a1f2c;
            padding: 20px;
            border-radius: 8px;
            border-top: 2px solid var(--color-marca);
            margin-top: 25px;
            display: flex;
            flex-direction: column;
            gap: 15px;
            align-items: center;
        }

        @media(min-width: 600px) {
            .area-descargas {
                flex-direction: row;
                justify-content: space-between;
            }
        }

        .btn-descarga-pdf {
            background: linear-gradient(135deg, #ff1744 0%, #d50000 100%);
            color: #ffffff;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .btn-descarga-pdf:hover {
            transform: scale(1.03);
        }

        /* Animación Fade In */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

    <div class="contenedor-global">
        
        <header>
            <h1>MIND MUSCLE</h1>
            <p>Plataforma Inteligente de Nutrición y Gestión MM247</p>
        </header>

        <nav>
            <button class="btn-nav activo" onclick="irASeccion('sec-inicial')">Cuestionario Inicial (1)</button>
            <button class="btn-nav" onclick="irASeccion('sec-seguimiento')">Cuestionario de Avance (2)</button>
            <button class="btn-nav" onclick="irASeccion('sec-admin')">Panel de Administración</button>
        </nav>

        <div id="sec-inicial" class="seccion-app activa">
            <div class="tarjeta-panel">
                <h2 class="titulo-seccion">Registro Inicial del Alumno - Cuestionario 1</h2>
                <form id="formulario-registro-inicial" onsubmit="procesarCuestionarioUno(event)">
                    <div class="grupo-formulario">
                        <label for="c1-nombre">Nombre Completo:</label>
                        <input type="text" id="c1-nombre" class="control-formulario" required placeholder="Ej. Juan Pérez">
                    </div>
                    <div class="grupo-formulario">
                        <label for="c1-peso">Peso Corporal Actual (kg):</label>
                        <input type="number" id="c1-peso" step="0.1" class="control-formulario" required placeholder="Ej. 80">
                    </div>
                    <div class="grupo-formulario">
                        <label for="c1-objetivo">Meta u Objetivo Principal:</label>
                        <input type="text" id="c1-objetivo" class="control-formulario" required placeholder="Ej. Definición muscular extrema / Aumento de fuerza">
                    </div>
                    <div class="grupo-formulario">
                        <label for="c1-experiencia">Nivel de Experiencia en el Gimnasio:</label>
                        <select id="c1-experiencia" class="control-formulario">
                            <option value="Principiante">Principiante (Menos de 1 año)</option>
                            <option value="Intermedio">Intermedio (1 a 3 años)</option>
                            <option value="Avanzado">Avanzado (Más de 3 años entrenando)</option>
                        </select>
                    </div>
                    <button type="submit" class="btn-accion">Finalizar Registro y Generar ID</button>
                </form>

                <div id="bloque-confirmacion-id" style="display: none;" class="bloque-exito-id">
                    <h3>¡Cuestionario Guardado Exitosamente!</h3>
                    <p>Se ha generado el identificador único del alumno para ligar su progreso:</p>
                    <div id="id-generado-pantalla" class="token-id">MM-9999</div>
                    <p style="color: var(--texto-mutado);">Guarda este ID. Lo necesitarás obligatoriamente para realizar tus cuestionarios de avance.</p>
                </div>
            </div>
        </div>

        <div id="sec-seguimiento" class="seccion-app">
            <div class="tarjeta-panel">
                <h2 class="titulo-seccion">Evaluación y Métricas de Seguimiento - Cuestionario 2</h2>
                
                <div id="compuerta-id-acceso">
                    <p style="margin-bottom: 15px; color: var(--texto-mutated);">Por favor, introduce tu ID Único de Alumno para poder ingresar al cuestionario comparativo.</p>
                    <div class="grupo-formulario" style="max-width: 400px;">
                        <label for="input-acceso-id">ID de Alumno (Ej: MM-1234):</label>
                        <input type="text" id="input-acceso-id" class="control-formulario" placeholder="Escribe tu ID aquí...">
                    </div>
                    <button type="button" class="btn-accion" style="max-width: 400px;" onclick="validarAccesoCuestionarioDos()">Validar Identificación</button>
                    <p id="error-validacion-id" style="color: var(--color-error); margin-top: 10px; display: none; font-weight: bold;">El ID ingresado no coincide con ningún alumno registrado.</p>
                </div>

                <form id="formulario-avance-dos" style="display: none;" onsubmit="procesarCuestionarioDos(event)">
                    <div style="background-color: rgba(0,229,255,0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid var(--color-marca);">
                        <strong>Alumno Identificado:</strong> <span id="nombre-alumno-activo" style="color: var(--color-marca);"></span> 
                        <br><strong>ID Vinculado:</strong> <span id="id-alumno-activo" style="font-family: monospace;"></span>
                    </div>

                    <div class="grupo-formulario">
                        <label>1. ¿Cómo ha evolucionado tu peso en relación con tu meta inicial?</label>
                        <div class="opciones-bloque">
                            <label class="opcion-item">
                                <input type="radio" name="p2-peso" value="opt-avance" required>
                                Cambió exactamente en la dirección deseada (Avance óptimo).
                            </label>
                            <label class="opcion-item">
                                <input type="radio" name="p2-peso" value="opt-lento">
                                Ha cambiado muy poco o se encuentra estancado (Avance muy lento).
                            </label>
                            <label class="opcion-item">
                                <input type="radio" name="p2-peso" value="opt-retroceso">
                                Se movió en la dirección opuesta a mis metas (Retroceso).
                            </label>
                        </div>
                    </div>

                    <div class="grupo-formulario">
                        <label>2. En tus entrenamientos diarios, tus niveles de fuerza y cargas manejadas:</label>
                        <div class="opciones-bloque">
                            <label class="opcion-item">
                                <input type="radio" name="p2-fuerza" value="opt-avance" required>
                                Incrementaron notablemente en la mayoría de ejercicios.
                            </label>
                            <label class="opcion-item">
                                <input type="radio" name="p2-fuerza" value="opt-lento">
                                Se mantienen iguales, sin cambios significativos.
                            </label>
                            <label class="opcion-item">
                                <input type="radio" name="p2-fuerza" value="opt-retroceso">
                                Siento menos fuerza o mayor fatiga al entrenar.
                            </label>
                        </div>
                    </div>

                    <div class="grupo-formulario">
                        <label>3. ¿Qué nivel de apego has tenido a las pautas macro-nutricionales enviadas?</label>
                        <div class="opciones-bloque">
                            <label class="opcion-item">
                                <input type="radio" name="p2-dieta" value="opt-avance" required>
                                Excelente. Cumplimiento total de proteínas y calorías diarias.
                            </label>
                            <label class="opcion-item">
                                <input type="radio" name="p2-dieta" value="opt-lento">
                                Regular. Fallas constantes los fines de semana o comidas libres.
                            </label>
                            <label class="opcion-item">
                                <input type="radio" name="p2-dieta" value="opt-retroceso">
                                Nulo o muy bajo. No he podido seguir el plan de alimentación.
                            </label>
                        </div>
                    </div>

                    <button type="submit" class="btn-accion">Enviar Evaluación</button>
                </form>

                <div id="confirmacion-cuestionario-dos" style="display: none;" class="bloque-exito-id">
                    <h3 style="color: var(--color-exito);">¡Evaluación Enviada Correctamente!</h3>
                    <p style="margin-top: 10px;">Tus respuestas e historial métrico han sido enviados de forma privada a la base de datos del entrenador.</p>
                    <p style="color: var(--texto-mutado); font-size: 0.9rem; margin-top: 5px;">Nota de Privacidad: Las métricas calculadas y resultados analíticos solo son accesibles en el panel del Administrador / Coach.</p>
                </div>
            </div>
        </div>

        <div id="sec-admin" class="seccion-app">
            <div class="tarjeta-panel">
                <h2 class="titulo-seccion">Dashboard de Control Administrativo</h2>
                <p style="color: var(--texto-mutado); margin-bottom: 20px;">Vista unificada y detallada de alumnos inscritos en el sistema MM247:</p>
                
                <div class="tabla-alumnos-contenedor">
                    <table class="tabla-alumnos">
                        <thead>
                            <tr>
                                <th>ID Alumno</th>
                                <th>Nombre</th>
                                <th>Punto de Inicio</th>
                                <th>Meta Definida</th>
                                <th style="width: 30%;">Estatus de Rendimiento y Avance</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody id="cuerpo-tabla-alumnos">
                            </tbody>
                    </table>
                </div>

                <div id="contenedor-detalle-alumno" class="panel-detalle-alumno">
                    <h3 id="detalle-titulo" style="font-size: 1.5rem; margin-bottom: 15px; color: #ffffff;">Reporte Evolutivo: Juan Pérez</h3>
                    
                    <div class="cuadricula-comparativa">
                        <div class="bloque-columna-reporte">
                            <h4 style="color: var(--color-marca); margin-bottom: 10px;">Registro Inicial (Cuestionario 1)</h4>
                            <p><strong>Peso Base:</strong> <span id="det-peso-inicial">0</span> kg</p>
                            <p><strong>Meta Establecida:</strong> <span id="det-meta-inicial">N/A</span></p>
                            <p><strong>Nivel de Entrada:</strong> <span id="det-nivel-inicial">N/A</span></p>
                            <div style="margin-top: 15px; background: rgba(255,255,255,0.03); padding: 10px; border-radius: 6px;">
                                <strong style="display:block; margin-bottom:4px; font-size:0.9rem;">Macros Base Programados:</strong>
                                <span style="font-size: 0.85rem;" id="det-macros-calculados">Proteína: --g | Grasa: --g</span>
                            </div>
                        </div>

                        <div class="bloque-columna-reporte">
                            <h4 style="color: var(--color-marca); margin-bottom: 10px;">Evolución de Métricas (Cuestionario 2)</h4>
                            <div id="det-bloque-c2-vacio" style="color: var(--texto-mutado); font-style: italic;">
                                El alumno aún no ha contestado la evaluación de seguimiento número 2.
                            </div>
                            <div id="det-bloque-c2-datos" style="display: none;">
                                <p><strong>Evolución de Peso:</strong> <span id="det-c2-peso">--</span></p>
                                <p><strong>Métricas de Fuerza:</strong> <span id="det-c2-fuerza">--</span></p>
                                <p><strong>Cumplimiento Plan:</strong> <span id="det-c2-dieta">--</span></p>
                                <p><strong>Estado General:</strong> <span id="det-c2-estado" style="font-weight: bold;">--</span></p>
                            </div>
                        </div>
                    </div>

                    <div class="area-descargas">
                        <div>
                            <h4 style="margin-bottom: 5px;">Módulo de Exportación Oficial</h4>
                            <p style="font-size: 0.85rem; color: var(--texto-mutado);" id="texto-conteo-hojas">Reporte estándar estructurado de 3 hojas configuradas.</p>
                        </div>
                        <button class="btn-descarga-pdf" onclick="ejecutarDescargaReportes()">Descargar Reporte Completo (.PDF)</button>
                    </div>
                </div>

            </div>
        </div>

    </div>

    <script>
        // Simulación Sólida de Base de Datos Local Integrada con Firebase Estructura
        let baseDatosAlumnos = [
            {
                id: "MM-1024",
                nombre: "Carlos Mendoza",
                peso: 85,
                meta: "Definición Muscular",
                experiencia: "Intermedio",
                macros: { proteina: 170, grasa: 85 },
                cuestionarioDos: {
                    peso: "opt-avance",
                    fuerza: "opt-avance",
                    dieta: "opt-avance",
                    resultadoMétrica: "AVANCE"
                }
            },
            {
                id: "MM-3051",
                nombre: "Mariana Rojas",
                peso: 62,
                meta: "Aumento Masa Muscular",
                experiencia: "Principiante",
                macros: { proteina: 124, grasa: 62 },
                cuestionarioDos: {
                    peso: "opt-lento",
                    fuerza: "opt-avance",
                    dieta: "opt-lento",
                    resultadoMétrica: "LENTO"
                }
            },
            {
                id: "MM-4492",
                nombre: "Rodrigo Silva",
                peso: 98,
                meta: "Recomposición Corporal",
                experiencia: "Avanzado",
                macros: { proteina: 196, grasa: 98 },
                cuestionarioDos: null // Aún no responde cuestionario 2
            }
        ];

        let alumnoSeleccionadoParaReporte = null;

        // Controlador de Rutas/Vistas
        function irASeccion(idSeccion) {
            document.querySelectorAll('.seccion-app').forEach(sec => {
                sec.classList.remove('activa');
            });
            document.querySelectorAll('.btn-nav').forEach(btn => {
                btn.classList.remove('activo');
            });
            
            document.getElementById(idSeccion).classList.add('activa');
            
            // Buscar y prender clase activo en botón correcto
            const botones = document.querySelectorAll('.btn-nav');
            if (idSeccion === 'sec-inicial') botones[0].classList.add('activo');
            if (idSeccion === 'sec-seguimiento') botones[1].classList.add('activo');
            if (idSeccion === 'sec-admin') {
                botones[2].classList.add('activo');
                renderizarTablaAdmin();
            }
        }

        // Procesador de Formulario Cuestionario 1
        function procesarCuestionarioUno(e) {
            e.preventDefault();
            
            const nombre = document.getElementById('c1-nombre').value;
            const peso = parseFloat(document.getElementById('c1-peso').value);
            const meta = document.getElementById('c1-objetivo').value;
            const experiencia = document.getElementById('c1-experiencia').value;
            
            // Regla de negocio inmutable de macronutrientes: 2g proteína y 1g grasa por kg
            const proteinasCalculadas = Math.round(peso * 2);
            const grasasCalculadas = Math.round(peso * 1);
            
            // Generador de ID Único Alfa-Numérico
            const numeroAleatorio = Math.floor(1000 + Math.random() * 9000);
            const idNuevo = `MM-${numeroAleatorio}`;
            
            const nuevoAlumno = {
                id: idNuevo,
                nombre: nombre,
                peso: peso,
                meta: meta,
                experiencia: experiencia,
                macros: { proteina: proteinasCalculadas, grasa: grasasCalculadas },
                cuestionarioDos: null
            };
            
            baseDatosAlumnos.push(nuevoAlumno);
            
            // Mostrar confirmación gráfica al usuario
            document.getElementById('id-generado-pantalla').innerText = idNuevo;
            document.getElementById('bloque-confirmacion-id').style.display = 'block';
            
            // Limpiar campos de formulario
            document.getElementById('formulario-registro-inicial').reset();
        }

        // Validación de ingreso para Cuestionario 2
        function validarAccesoCuestionarioDos() {
            const idIngresado = document.getElementById('input-acceso-id').value.trim().toUpperCase();
            const alumnoEncontrado = baseDatosAlumnos.find(al => al.id === idIngresado);
            
            if (alumnoEncontrado) {
                document.getElementById('error-validacion-id').style.display = 'none';
                document.getElementById('compuerta-id-acceso').style.display = 'none';
                
                // Cargar datos en el formulario activo
                document.getElementById('nombre-alumno-activo').innerText = alumnoEncontrado.nombre;
                document.getElementById('id-alumno-activo').innerText = alumnoEncontrado.id;
                document.getElementById('formulario-avance-dos').setAttribute('data-id-alumno', alumnoEncontrado.id);
                
                document.getElementById('formulario-avance-dos').style.display = 'block';
            } else {
                document.getElementById('error-validacion-id').style.display = 'block';
            }
        }

        // Procesamiento de Cuestionario 2 (Evaluación de avance)
        function procesarCuestionarioDos(e) {
            e.preventDefault();
            
            const idAlumno = document.getElementById('formulario-avance-dos').getAttribute('data-id-alumno');
            const alumno = baseDatosAlumnos.find(al => al.id === idAlumno);
            
            if (!alumno) return;
            
            // Obtener selecciones de opción múltiple
            const rPeso = document.querySelector('input[name="p2-peso"]:checked').value;
            const rFuerza = document.querySelector('input[name="p2-fuerza"]:checked').value;
            const rDieta = document.querySelector('input[name="p2-dieta"]:checked').value;
            
            // Sistema de Puntuación para calificar las métricas
            let scoreAvance = 0;
            if (rPeso === 'opt-avance') scoreAvance += 2;
            if (rFuerza === 'opt-avance') scoreAvance += 2;
            if (rDieta === 'opt-avance') scoreAvance += 2;
            
            if (rPeso === 'opt-lento') scoreAvance += 1;
            if (rFuerza === 'opt-lento') scoreAvance += 1;
            if (rDieta === 'opt-lento') scoreAvance += 1;
            
            let estatusCalculado = "LENTO";
            if (scoreAvance >= 5) estatusCalculado = "AVANCE";
            if (scoreAvance <= 2) estatusCalculado = "RETROCESO";
            
            // Guardar respuestas de manera privada en base de datos
            alumno.cuestionarioDos = {
                peso: rPeso,
                fuerza: rFuerza,
                dieta: rDieta,
                resultadoMétrica: estatusCalculado
            };
            
            // Interfaz: Limpiar y mostrar confirmación cuidando la no exposición de resultados
            document.getElementById('formulario-avance-dos').style.display = 'none';
            document.getElementById('confirmacion-cuestionario-dos').style.display = 'block';
        }

        // Renderizado del Dashboard Administrativo en Lista
        function renderizarTablaAdmin() {
            const cuerpoTabla = document.getElementById('cuerpo-tabla-alumnos');
            cuerpoTabla.innerHTML = '';
            
            baseDatosAlumnos.forEach(alumno => {
                const fila = document.createElement('tr');
                
                // Determinar el estado para armar la barra de progreso
                let colorBarraClase = "barra-vacia";
                let porcentajeAncho = "100%";
                let textoEstatus = "No Evaluado (Falta C2)";
                
                if (alumno.cuestionarioDos) {
                    if (alumno.cuestionarioDos.resultadoMétrica === 'AVANCE') {
                        colorBarraClase = "barra-avance";
                        porcentajeAncho = "100%";
                        textoEstatus = "Avance Correcto";
                    } else if (alumno.cuestionarioDos.resultadoMétrica === 'LENTO') {
                        colorBarraClase = "barra-lento";
                        porcentajeAncho = "50%";
                        textoEstatus = "Avance Muy Lento";
                    } else if (alumno.cuestionarioDos.resultadoMétrica === 'RETROCESO') {
                        colorBarraClase = "barra-retroceso";
                        porcentajeAncho = "25%";
                        textoEstatus = "Retroceso Detectado";
                    }
                } else {
                    porcentajeAncho = "0%";
                }
                
                fila.innerHTML = `
                    <td class="col-id">${alumno.id}</td>
                    <td style="font-weight: 600;">${alumno.nombre}</td>
                    <td>${alumno.peso} kg</td>
                    <td><span style="font-size:0.9rem; color:var(--texto-mutado);">${alumno.meta}</span></td>
                    <td>
                        <span class="etiqueta-estado">${textoEstatus}</span>
                        <div class="contenedor-barra-progreso">
                            <div class="llenado-barra ${colorBarraClase}" style="width: ${porcentajeAncho};"></div>
                        </div>
                    </td>
                    <td>
                        <button class="btn-tabla-reporte" onclick="verDetalleAlumnoReporte('${alumno.id}')">Ver Reporte</button>
                    </td>
                `;
                
                cuerpoTabla.appendChild(fila);
            });
        }

        // Cargar Visualización de Detalle de Reporte para el Administrador
        function verDetalleAlumnoReporte(idAlumno) {
            const alumno = baseDatosAlumnos.find(al => al.id === idAlumno);
            if (!alumno) return;
            
            alumnoSeleccionadoParaReporte = alumno;
            
            document.getElementById('detalle-titulo').innerText = `Análisis de Seguimiento: ${alumno.nombre}`;
            document.getElementById('det-peso-inicial').innerText = alumno.peso;
            document.getElementById('det-meta-inicial').innerText = alumno.meta;
            document.getElementById('det-nivel-inicial').innerText = alumno.experiencia;
            document.getElementById('det-macros-calculados').innerText = `Proteína: ${alumno.macros.proteina}g | Grasa: ${alumno.macros.grasa}g`;
            
            const bloqueVacio = document.getElementById('det-bloque-c2-vacio');
            const bloqueDatos = document.getElementById('det-bloque-c2-datos');
            const textoConteoHojas = document.getElementById('texto-conteo-hojas');
            
            if (alumno.cuestionarioDos) {
                bloqueVacio.style.display = 'none';
                bloqueDatos.style.display = 'block';
                
                // Mapeo amigable de respuestas
                document.getElementById('det-c2-peso').innerText = mapearTextoOpcion(alumno.cuestionarioDos.peso);
                document.getElementById('det-c2-fuerza').innerText = mapearTextoOpcion(alumno.cuestionarioDos.fuerza);
                document.getElementById('det-c2-dieta').innerText = mapearTextoOpcion(alumno.cuestionarioDos.dieta);
                document.getElementById('det-c2-estado').innerText = alumno.cuestionarioDos.resultadoMétrica;
                
                // Condición de color de texto para estatus
                if (alumno.cuestionarioDos.resultadoMétrica === 'AVANCE') document.getElementById('det-c2-estado').style.color = 'var(--color-exito)';
                if (alumno.cuestionarioDos.resultadoMétrica === 'LENTO') document.getElementById('det-c2-estado').style.color = 'var(--color-alerta)';
                if (alumno.cuestionarioDos.resultadoMétrica === 'RETROCESO') document.getElementById('det-c2-estado').style.color = 'var(--color-error)';
                
                textoConteoHojas.innerText = "Estructura Avanzada detectada: se descargarán 4 hojas PDF (3 Base + Reporte de Avance).";
            } else {
                bloqueVacio.style.display = 'block';
                bloqueDatos.style.display = 'none';
                textoConteoHojas.innerText = "Reporte estándar estructurado: se descargarán 3 hojas PDF (Cuestionario 1).";
            }
            
            document.getElementById('contenedor-detalle-alumno').style.display = 'block';
            // Scroll suave automático al reporte
            document.getElementById('contenedor-detalle-alumno').scrollIntoView({ behavior: 'smooth' });
        }

        // Auxiliar Traductor de Opciones
        function mapearTextoOpcion(valor) {
            if (valor === 'opt-avance') return 'Favorable / Incremento Positivo';
            if (valor === 'opt-lento') return 'Estable / Sin Cambios Visibles';
            if (valor === 'opt-retroceso') return 'Desfavorable / Alerta';
            return valor;
        }

        // Módulo de exportación e Impresión jsPDF
        function ejecutarDescargaReportes() {
            if (!alumnoSeleccionadoParaReporte) return;
            
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            
            const al = alumnoSeleccionadoParaReporte;
            
            // HOJA 1: Portada del Alumno e ID Oficial
            doc.setFillColor(10, 12, 16);
            doc.rect(0, 0, 210, 297, 'F');
            doc.setTextColor(255, 255, 255);
            doc.setFontSize(26);
            doc.text("MIND MUSCLE", 105, 80, { align: 'center' });
            doc.setFontSize(14);
            doc.setTextColor(0, 229, 255);
            doc.text("INFORME DE CONTROL INTEGRAL MM247", 105, 95, { align: 'center' });
            
            doc.setDrawColor(0, 229, 255);
            doc.setLineWidth(1);
            doc.line(40, 110, 170, 110);
            
            doc.setTextColor(255, 255, 255);
            doc.setFontSize(12);
            doc.text(`Alumno: ${al.nombre}`, 105, 130, { align: 'center' });
            doc.setFontSize(16);
            doc.setTextColor(0, 229, 255);
            doc.text(`ID EXCLUSIVO: ${al.id}`, 105, 150, { align: 'center' });
            
            // HOJA 2: Detalles Cuestionario 1 e Indicadores Base
            doc.addPage();
            doc.setFillColor(255, 255, 255);
            doc.rect(0, 0, 210, 297, 'F');
            doc.setTextColor(10, 12, 16);
            doc.setFontSize(18);
            doc.text("HOJA 2: EXPEDIENTE CLÍNICO DE APERTURA", 20, 30);
            doc.setFontSize(11);
            doc.text(`ID Alumno impreso: ${al.id}`, 20, 42);
            doc.text(`Peso Inicial del Sujeto: ${al.peso} kg`, 20, 55);
            doc.text(`Meta Declarada: ${al.meta}`, 20, 68);
            doc.text(`Nivel Técnico de Entrada en Sala: ${al.experiencia}`, 20, 81);
            
            // HOJA 3: Planeación Macro-Nutricional Inmutable
            doc.addPage();
            doc.setFontSize(18);
            doc.text("HOJA 3: PLANIFICACIÓN Y DISTRIBUCIÓN DE MACROS", 20, 30);
            doc.setFontSize(11);
            doc.text(`ID de Control: ${al.id}`, 20, 42);
            doc.text("Estrategia Nutricional Basada en Carga Corporal Metodología MM247:", 20, 60);
            doc.text(`- Requerimiento de Proteína Configurado (2g/kg): ${al.macros.proteina} gramos diarios`, 25, 75);
            doc.text(`- Requerimiento de Lípidos Línea Base (1g/kg): ${al.macros.grasa} gramos diarios`, 25, 90);
            
            // HOJA 4 CONDICIONAL: Reporte de Avance Extensible
            if (al.cuestionarioDos) {
                doc.addPage();
                doc.setFontSize(18);
                doc.setTextColor(10, 12, 16);
                doc.text("HOJA 4: ANALÍTICA DE AVANCE Y RETROALIMENTACIÓN", 20, 30);
                doc.setFontSize(11);
                doc.text(`ID de Rastreo Cruzado: ${al.id}`, 20, 42);
                
                doc.text("Métricas Comparativas Evaluadas por el Sistema:", 20, 60);
                doc.text(`Evolución en Variable Peso: ${mapearTextoOpcion(al.cuestionarioDos.peso)}`, 25, 75);
                doc.text(`Rendimiento y Desempeño en Fuerza: ${mapearTextoOpcion(al.cuestionarioDos.fuerza)}`, 25, 90);
                doc.text(`Nivel de Disciplina y Apego Nutricional: ${mapearTextoOpcion(al.cuestionarioDos.dieta)}`, 25, 105);
                
                doc.setFontSize(14);
                doc.text(`DIAGNÓSTICO FINAL DEL ENTRENADOR: ${al.cuestionarioDos.resultadoMétrica}`, 20, 130);
            }
            
            // Guardar archivo final oficial con nomenclatura solicitada
            doc.save(`avance_${al.id}.pdf`);
        }
    </script>
</body>
</html>
