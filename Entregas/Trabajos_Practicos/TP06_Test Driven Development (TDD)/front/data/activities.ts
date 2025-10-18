// Actividades hardcodeadas (sin horarios)
export interface ActivityInfo {
  id: string;
  name: string;
  description: string;
  icon: string;
  requiresSize: boolean;
  minAge: number | null;
  color: string;
}

export const activitiesInfo: ActivityInfo[] = [
  {
    id: 'tirolesa',
    name: 'Tirolesa',
    description: 'Deslízate por las copas de los árboles en una experiencia emocionante de aventura extrema',
    icon: '🪂',
    requiresSize: true,
    minAge: 8,
    color: '#16a34a',
  },
  {
    id: 'safari',
    name: 'Safari',
    description: 'Recorre el parque en vehículos especiales y observa la fauna local en su hábitat natural',
    icon: '🦁',
    requiresSize: false,
    minAge: null,
    color: '#d97706',
  },
  {
    id: 'balestra',
    name: 'Balestra',
    description: 'Practica tiro con ballesta en nuestro campo especializado con instructores certificados',
    icon: '🏹',
    requiresSize: true,
    minAge: 12,
    color: '#dc2626',
  },
  {
    id: 'jardineria',
    name: 'Jardinería',
    description: 'Aprende técnicas de cultivo sustentable y participa en el cuidado de nuestro vivero ecológico',
    icon: '🌱',
    requiresSize: false,
    minAge: null,
    color: '#65a30d',
  },
];

// Helper para obtener info de actividad por nombre
export const getActivityInfoByName = (name: string): ActivityInfo | undefined => {
  const normalizedName = name.toLowerCase();
  return activitiesInfo.find(
    (activity) => activity.name.toLowerCase() === normalizedName
  );
};