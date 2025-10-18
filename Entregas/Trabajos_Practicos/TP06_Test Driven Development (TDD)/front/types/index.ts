// Tipos para la API
export interface ApiSchedule {
  id: number;
  id_actividad: number;
  hora_inicio: string;
  hora_fin: string;
  cupo_total: number;
  cupo_ocupado: number;
  estado: string;
  actividad: {
    id: number;
    nombre: string;
    requiere_talle: boolean;
  };
  estado_horario: {
    nombre: string;
    descripcion: string;
  };
}

// Tipos internos de la app
export interface Activity {
  id: string;
  name: string;
  description: string;
  icon: string;
  requiresSize: boolean;
  minAge: number | null;
  color: string;
  schedules: Schedule[];
}

export interface Schedule {
  id: string;
  time: string;
  availableSpots: number;
  status: 'available' | 'full';
}

export interface Participant {
  fullName: string;
  dni: string;
  age: string;
  clothingSize?: string;
}

export interface BookingData {
  activity: Activity;
  schedule: Schedule;
  participants: Participant[];
}

// Helper para convertir horarios de API a formato interno
export const convertApiScheduleToSchedule = (
  apiSchedule: ApiSchedule
): Schedule => {
  const availableSpots = apiSchedule.cupo_total - apiSchedule.cupo_ocupado;
  return {
    id: apiSchedule.id.toString(),
    time: apiSchedule.hora_inicio,
    availableSpots: availableSpots,
    status: availableSpots > 0 ? 'available' : 'full',
  };
};