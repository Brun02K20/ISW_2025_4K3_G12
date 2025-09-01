# Plan de Gestión de Configuración SCM - ISW_2025_4K3_G12

## 1. Introducción
*Propósito:*  
Definir cómo se gestionan los documentos del proyecto, el control de cambios, la estructura de carpetas y los ítems de configuración para el repositorio ISW_2025_4K3_G12.

---

## 2. Control de Cambios
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

## 3. Procedimiento de Subida de Documentos y Carpetas

1. Crear o identificar la carpeta donde se subirá el documento.  
2. Si la carpeta no existe, crearla y agregar .gitkeep.  
3. Subir el documento a la carpeta correspondiente.  
4. Realizar commit siguiendo las convenciones (docs: o chore:).  
5. Abrir un Pull Request para revisión.  

---

## 4. Mantenimiento del Documento

- Responsable: Bruno Virinni 89639  
- Actualizar el plan si hay cambios en la estructura de carpetas, reglas de nombrado o procedimientos.  

  
---

## 5. Procedimiento de Control de Cambios Detallado

1. Crear carpeta/documento siguiendo la estructura y reglas de nombrado.  
2. Crear rama remota siguiendo la convención [tipo]/[descripcion_corta].  
3. Subir cambios y realizar commit según las reglas.  
4. Abrir PR para revisión y aprobación.  
5. Hacer merge a main y borrar rama remota si ya no es necesaria.
