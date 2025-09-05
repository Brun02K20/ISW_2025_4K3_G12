# 📋 Plan de Gestión de Configuración SCM - ISW_2025_4K3_G12

## 1. 📖 Introducción
**Propósito:**  
Definir cómo se gestionan los documentos del proyecto, el control de cambios, la estructura de carpetas y los ítems de configuración para el repositorio ISW_2025_4K3_G12.

---

## 2. 📍 Línea Base

### 2.1 🏷️ Criterio de creación
Se establecerá la **Línea de Base** del proyecto luego de recibir retroalimentación (es decir, calificación) por parte del equipo docente del curso luego de Trabajos Prácticos evaluables. Esto nos permitiría marcar un hito importante para alcanzar el objetivo que tenemos en esta materia, alcanzar la Aprobación Directa.

### 2.2 🔖 Identificación
Las líneas base se identificarán con la siguiente etiqueta: `LB-G12-<NroLineaBase>`

---

## 3. 📦 Ítems de Configuración

### 3.1 📚 Glosario de Siglas

| Sigla | Significado |
|-------|-------------|
| ISW | Ingeniería y Calidad de Software |
| CED | Casos de Estudio y Documentación |
| MA | Material Auxiliar |
| TP | Trabajo Práctico |
| TIG | Trabajo de Investigación en Grupo |
| EXT | Extensión del Archivo |
| TMP | Template / Plantilla |
| B | Bibliografía |
| IFS | Introducción a la Ingeniería de Software |
| LYK | Lean y Kanban |
| PA | Pensamiento Ágil |
| TS | Testing de Software |
| PRC | Parcial |
| G12 | Grupo 12 |
| LB | Línea Base |
| P | Presentacion |
| CR | Cronograma de la materia |

### 3.2 📝 Reglas de Nombrado y Ubicaciones

| Ítem | Regla de Nombrado | Ubicación |
|------|------------------|-----------|
| Bibliografía | `ISW_B_<NombreLibro>.pdf` | `Documentacion/Bibliografia/Material_Bibliografia` |
| Presentaciones | `ISW_P_<NombrePresentación>.pdf` | `Documentacion/Presentaciones` |
| Resúmenes Propios | `ISW_Resumen_Parc<NroParcial><Autor><Año>.<ext>` | `Documentacion/Resumenes` |
| Clases Grabadas | `ISW_Links_ClasesGrabadas_<Curso>_<Año>.<ext>` | `Documentacion/Presentaciones/Clases_Grabadas` |
| Ejercicios Resueltos | `ISW_ER_<NombreArchivo>_<Año>.<ext>` | `Ejercicios_Resueltos` |
| Trabajos Prácticos | `ISW_TP_<NumeroTP>.<ext>` | `Entregas/Trabajos_Practicos/<TrabajoPractico>` |
| Trabajo De Investigación | `ISW_TIG_<NombreTrabajoInvestigacionGrupal>_<Curso>.<ext>` | `Entregas/Investigaciones/<TrabajoDeInvestigacion>` |
| Cronograma de la Materia | `ISW_CR_2025_4K3.ext` | `/ (raíz del proyecto)` |

### 3.3 📁 Estructura de Carpetas
```
ISW_2025_4K3_G12/
├── 📂 Documentacion/
│   ├── 📂 Bibliografia/
│   │    └──📂 Material_Bibliografico/
│   └── 📂 Resumenes/
|   └── 📂 Notas_Clases/
│   └── 📂 Presentaciones/
│       └── 📂 Clases_Grabadas/
├── 📂 Ejercicios_Resueltos/
└── 📂 Entregas/
    ├── 📂 Investigaciones/
    └── 📂 Trabajos_Practicos/
```

---

## 4. 🔄 Control de Cambios
**Sistema de control:** Git / GitHub

**Reglas para los commits:**  
- 📄 docs: agregar [nombre del documento] → para nuevos documentos  
- 🔄 docs: actualizar [nombre del documento] → para modificaciones  
- 📁 chore: agregar carpeta [nombre de la carpeta] → para nuevas carpetas vacías  
- 🐛 fix: [descripción del arreglo] → para correcciones en documentos o archivos existentes  
- ✨ func: [descripción de nueva funcionalidad] → para agregar funcionalidades no relacionadas a código, por ejemplo plantillas o scripts auxiliares

**Pull Requests (PR):**  
- 🔍 Cada nuevo documento o carpeta se sube mediante PR para revisión  
- ✅ PR aprobado → documento/carpeta queda en el repositorio  
- 🗑️ Opcional: borrar la rama remota después del merge  

**Ramas:**  
- 🌿 Basadas en main  
- 📋 Formato: [tipo]/[descripcion_corta]  
- 📝 Ejemplos:  
  - docs/Documentacion_Bibliografia_Material_Bibliográfico  
  - chore/Nueva_Carpeta_Resumenes_Propios  

**🎥 TUTORIAL:** [https://youtu.be/LjfTYkcAQSc](https://youtu.be/LjfTYkcAQSc)

---

## 5. 📤 Procedimiento de Subida de Documentos y Carpetas

1. 📂 Crear o identificar la carpeta donde se subirá el documento.  
2. ➕ Si la carpeta no existe, crearla y agregar .gitkeep.  
3. ⬆️ Subir el documento a la carpeta correspondiente.  
4. 💾 Realizar commit siguiendo las convenciones (docs: o chore:).  
5. 🔄 Abrir un Pull Request para revisión.  

---

## 6. 🛠️ Mantenimiento del Documento

- 👥 **Responsables:** Bruno Laszlo Virinni 89639; Juan Esteban Liendo 91274; Martin Horacio Castro Monzón 91429  
- 🔄 Actualizar el plan si hay cambios en la estructura de carpetas, reglas de nombrado o procedimientos.  

---

## 7. 📝 Procedimiento de Control de Cambios Detallado

1. 📂 Crear carpeta/documento siguiendo la estructura y reglas de nombrado.  
2. 🌿 Crear rama remota siguiendo la convención [tipo]/[descripcion_corta].  
3. 💾 Subir cambios y realizar commit según las reglas.  
4. 🔍 Abrir PR para revisión y aprobación.  
5. ✅ Hacer merge a main y borrar rama remota si ya no es necesaria.
|
