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

export interface InscripcionErrorResponse {
  detail: Array<{
    type: string;
    loc: unknown[]; // puede haber cualquier cosa aca adentro
    msg: string;
    input: any;
    url: string;
  }>;
}

/**
 * Envía la inscripción a la API del backend.
 */
export const createInscripcion = async (
  data: InscripcionApiData
): Promise<InscripcionResponse | InscripcionErrorResponse> => {
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
      const errorData: InscripcionErrorResponse = await response.json();
      console.error("❌ Error en la inscripción:", errorData);
      let userMessage = "";

      switch (response.status) {
        case 400:
          // Errores de validación (CupoInsuficienteError, TerminosNoAceptadosError, TalleRequeridoError)
          userMessage = "Oops! Parece que hubo un problema con los datos enviados. Por favor, revisa la información e intenta nuevamente.";
          break;
        case 404:
          // Horario o visitante no encontrado
          userMessage = "Oops! Parece que hubo un problema con los datos enviados. Por favor, revisa la información e intenta nuevamente.";
          break;
        case 409:
          // Inscripción duplicada
          userMessage = "Oops! Parece que hubo un problema con los datos enviados. Por favor, revisa la información e intenta nuevamente.";
          break;
        case 500:
          userMessage = "Error interno del servidor. Por favor, intenta nuevamente más tarde.";
          break;
        default:
          userMessage = "Oops! Parece que hubo un problema con los datos enviados. Por favor, revisa la información e intenta nuevamente.";
      }

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