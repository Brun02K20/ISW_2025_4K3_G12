# Plan de Gestión de Configuración SCM - ISW_2025_4K3_G12

## 📑 Índice

### 📌 Para Clientes
- [1. Información General del Repositorio - ISW_2025_4K3_G12](#1-información-general-del-repositorio---isw_2025_4k3_g12)
- [2. Integrantes](#2-integrantes)
- [3. Línea Base](#3-línea-base)
  - [3.1 Criterio de creación](#31-criterio-de-creación)
  - [3.2 Identificación](#32-identificación)
- [4. Ítems de Configuración](#4-ítems-de-configuración)
  - [4.1 Glosario de Siglas](#41-glosario-de-siglas)
  - [4.2 Reglas de Nombrado y Ubicaciones](#42-reglas-de-nombrado-y-ubicaciones)
  - [4.3 Estructura de Carpetas](#43-estructura-de-carpetas)
- [5. Uso del Proyecto](#5-uso-del-proyecto)

### 🛠️ Para el Equipo de Desarrollo
- [6. Control de Cambios](#6-control-de-cambios)
- [7. Procedimiento de Subida](#7-procedimiento-de-subida-de-documentos-y-carpetas)
- [8. Mantenimiento del Documento](#8-mantenimiento-del-documento)
- [9. Procedimiento de Cambios](#9-procedimiento-de-control-de-cambios-detallado)

--- 

## ℹ️ 1. Información General del Repositorio - ISW_2025_4K3_G12
Repositorio del Grupo N°12 con los contenidos; trabajos prácticos; consignas; y entregables desarrollados en la materia “Ingeniería y Calidad de Software” en la Universidad Tecnológica Nacional, Facultad Regional Córdoba. El repositorio estará estructurado a base de directorios y contenidos - con una nomenclatura variante de la conocida "snake case", dicha variante consiste en tener la primer letra de cada palabra en mayúsculas.

*Propósito para el equipo de desarrollo:*  
Definir cómo se gestionan los documentos del proyecto, el control de cambios, la estructura de carpetas y los ítems de configuración para el repositorio ISW_2025_4K3_G12.

---

## 👥 2. Integrantes

| Legajo | Apellido, Nombre | Perfil |
|--------|-----------------------------|---------------------------------------------|
| 89639  | Virinni, Bruno Laszlo             | [Brun02K20](https://github.com/Brun02K20) |
| 90263  | Höhlke, Augusto             | [AugusHo](https://github.com/AugusHo) |
| 91274  | Liendo, Juan Esteban        | [juan-lien-do](https://github.com/juan-lien-do) |
| 89767  | Chaile, Emmanuel Ricardo    | [emmach02](https://github.com/emmach02) |
| 75721  | Freytes Oviedo, Agustin     | [Agustin-98](https://github.com/Agustin-98) |
| 91429  | Castro Monzon, Martin       | [martinxr250](https://github.com/martinxr250) |
| 76860  | Silvestri, Brian            | [BrianSilvestri](https://github.com/BrianSilvestri) |
| 88618  | Barrionuevo, Daniel         | [DanielSiri](https://github.com/DanielSiri) |
| 90297  | Cornejo, Francisco          | [CornejoFrancisco](https://github.com/CornejoFrancisco) |
| 85194  | Guillén, Lucas Martin       | [MartinG94](https://github.com/MartinG94) |

---
## 💼 3. Línea Base

### 🏷️ 3.1 Criterio de creación
Se establecerá la **Línea de Base** del proyecto luego de recibir la devolución (calificación) de cada uno de los Trabajos Prácticos – ya sea evaluable o no evaluable – debido a que estos tienen la aprobación (nuevamente, calificación) de los clientes (profesores).

### 🔖 3.2 Identificación
Las líneas base se identificarán con la siguiente etiqueta: ```LB-G12-<NroLineaBase>```

---
## 📦 4. Ítems de Configuración

### 🧾 4.1 Glosario de Siglas

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

---

### 📚 4.2 Reglas de Nombrado y Ubicaciones

| Ítem | Regla de Nombrado | Ubicación |
|------|------------------|-----------|
| Bibliografía | `ISW_B_<NombreLibro>.pdf` | `Documentacion/Bibliografia/Material_Bibliografia` |
| Presentaciones | `ISW_P_<NombrePresentación>.pdf` | `Documentacion/Presentaciones` |
| Resúmenes Propios | `ISW_Resumen_Parc<NroParcial><Autor><Año>.<ext>` | `Documentacion/Bibliografia/Resumenes_Propios` |
| Clases Grabadas | `ISW_Links_ClasesGrabadas_<Curso>_<Año>.<ext>` | `Documentacion/Presentaciones/Clases_Grabadas` |
| Ejercicios Resueltos | `ISW_ER_<NombreArchivo>_<Año>.<ext>` | `Ejercicios_Resueltos` |
| Trabajos Prácticos | `ISW_TP_<NumeroTP>.<ext>` | `Entregas/Trabajos_Practicos/<TrabajoPractico>` |
| Trabajo De Investigación | `ISW_TIG_<NombreTrabajoInvestigacionGrupal>_<Curso>.<ext>` | `Entregas/Investigaciones/<TrabajoDeInvestigacion>` |
| Cronograma de la Materia | `ISW_CR_2025_4K3_archivo.ext` | `/ (raíz del proyecto)` |

---

### 📁 4.3 Estructura de Carpetas
```bash
ISW_2025_4K3_G12/
├── Documentacion/
│   ├── Bibliografia/
│   │   ├── Material_Bibliografico/
│   │   └── Resumenes_Propios/
│   └── Presentaciones/
│       └── Clases_Grabadas/
├── Ejercicios_Resueltos/
└── Entregas/
    ├── Investigaciones/
    └── Trabajos_Practicos/
```

---

## 💻 5. Uso del Proyecto

Para poder utilizar este proyecto, siga los siguientes pasos:

1. **Abra la terminal de su sistema operativo**:  
   - **Windows:** CMD o PowerShell. También puede usar **Git Bash** si lo tiene instalado.  
   - **Linux:** Terminal (Ctrl + Alt + T en la mayoría de distribuciones)  
   - **macOS:** Aplicación **Terminal** (ubicada en Aplicaciones > Utilidades)  


2. **Navegue al directorio donde quiera descargar el repositorio.** Por ejemplo:  

   ```bash
   cd ruta/del/directorio
   ```
  
3. **Asegúrese de tener instalado Git en su computadora para poder usar el sistema de control de versiones.**
   ```bash
   git --version
   ```

4. **Clone el repositorio usando el siguiente comando:**
  ```bash
   git clone https://github.com/Brun02K20/ISW_2025_4K3_G12.git
   ```

=======

## 6. Control de Cambios
*Sistema de control:* Git / GitHub

*Reglas para los commits:*  
- docs: agregar [nombre del documento] → para nuevos documentos  
- docs: actualizar [nombre del documento] → para modificaciones  
- chore: agregar carpeta [nombre de la carpeta] → para nuevas carpetas vacías  
- fix: [descripción del arreglo] → para correcciones en documentos o archivos existentes  
- func: [descripción de nueva funcionalidad] → para agregar funcionalidades no relacionadas a código, por ejemplo plantillas o scripts auxiliares

*Pull Requests (PR):*  
- Cada nuevo documento o carpeta se sube mediante PR para revisión  
- PR aprobado → documento/carpeta queda en el repositorio  
- Opcional: borrar la rama remota después del merge  

*Ramas:*  
- Basadas en main  
- Formato: [tipo]/[descripcion_corta]  
- Ejemplos:  
docs/Documentacion_Bibliografia_Material_Bibliografia
chore/Nueva_Carpeta_Resumenes_Propios


*TUTORIAL: * https://youtu.be/ip6aTgxfQ7Q
---

## 7. Procedimiento de Subida de Documentos y Carpetas

1. Crear o identificar la carpeta donde se subirá el documento.  
2. Si la carpeta no existe, crearla y agregar .gitkeep.  
3. Subir el documento a la carpeta correspondiente.  
4. Realizar commit siguiendo las convenciones (docs: o chore:).  
5. Abrir un Pull Request para revisión.  

---

## 8. Mantenimiento del Documento

- Responsables: Bruno Laszlo Virinni 89639; Juan Esteban Liendo 91274; Martin Horacio Castro Monzón 91429 
- Actualizar el plan si hay cambios en la estructura de carpetas, reglas de nombrado o procedimientos.  
  
---

## 5. Procedimiento de Control de Cambios Detallado

1. Crear carpeta/documento siguiendo la estructura y reglas de nombrado.  
2. Crear rama remota siguiendo la convención [tipo]/[descripcion_corta].  
3. Subir cambios y realizar commit según las reglas.  
4. Abrir PR para revisión y aprobación.  
5. Hacer merge a main y borrar rama remota si ya no es necesaria.
