import { API_BASE_URL } from "@/constants/url";

export interface VisitanteInscripcion {
  nombre: string;
  dni: number;
  edad: number;
  talle: string;
}

export interface InscripcionApiData {
  id_horario: number;
  visitantes: VisitanteInscripcion[];
  acepta_terminos: boolean;
}

export interface InscripcionResponse {
  success: boolean;
  message: string;
  data?: any;
}

/**
 * Envía la inscripción a la API del backend.
 */
export const createInscripcion = async (
  data: InscripcionApiData
): Promise<InscripcionResponse> => {
  try {
    // URL de la API en localhost
    const API_URL = `${API_BASE_URL}/inscripciones`;

    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const responseData = await response.json();
      return {
        success: true,
        message: "Inscripción registrada correctamente",
        data: responseData,
      };
    } else {
      // Manejar errores específicos según el código de estado
      const errorData = await response.json().catch(() => ({ detail: "Error desconocido" }));

      const userMessage = errorData.detail && errorData.detail[0] ? errorData.detail[0].msg : "Error desconocido";
      
      return {
        success: false,
        message: userMessage,
      };
    }
  } catch (error) {
    console.error("❌ Error al enviar inscripción:", error);
    
    if (error instanceof TypeError && error.message.includes("fetch")) {
      return {
        success: false,
        message: "No se pudo conectar con el servidor. Verifica que la API esté en funcionamiento en http://localhost:8080",
      };
    }
    
    return {
      success: false,
      message: "No se pudo conectar con el servidor. Verifica tu conexión a internet.",
    };
  }
};