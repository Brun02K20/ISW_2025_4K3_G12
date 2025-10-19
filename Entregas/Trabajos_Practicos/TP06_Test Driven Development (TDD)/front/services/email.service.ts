import emailjs from "emailjs-com";

export interface Visitante {
  nombre: string;
  dni: number;
  edad: number;
  talle: string;
}

export interface InscripcionData {
  id_horario: number;
    nombre_actividad: string;
  visitantes: Visitante[];
  acepta_terminos: boolean;
}

/**
 * Envía la inscripción por correo usando EmailJS.
 */
export const sendInscriptionEmail = async (data: InscripcionData) => {
  if (!data) throw new Error("No hay datos para enviar el correo.");

  const visitantes = data.visitantes.map((v, i) => ({
    index: i + 1,
    nombre: v.nombre,
    dni: v.dni,
    edad: v.edad,
    talle: v.talle,
  }));

  const templateParams = {
    id_horario: data.id_horario,
    activity_name: data.nombre_actividad,
    acepta_terminos: data.acepta_terminos ? "Sí" : "No",
    visitantes,
    email: "bvirinni@gmail.com",
  };

  try {
    const result = await emailjs.send(
      "service_wznr9rd", // tu Service ID
      "template_82kyvau", // tu Template ID
      templateParams,
      "TCtZk6pPoeJ9_o-5o", // tu Public Key
    );

    console.log("✅ Correo enviado correctamente:", result.text);
    return { success: true, message: "Inscripción enviada con éxito." };
  } catch (error) {
    console.error("❌ Error al enviar el correo:", error);
    return { success: false, message: "No se pudo enviar el correo." };
  }
};