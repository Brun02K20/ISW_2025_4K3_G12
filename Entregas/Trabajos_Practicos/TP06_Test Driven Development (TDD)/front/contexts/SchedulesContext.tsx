import { API_BASE_URL } from '@/constants/url';
import React, { createContext, ReactNode, useContext, useState } from 'react';
import { ApiSchedule } from '../types';

interface SchedulesContextType {
  schedules: ApiSchedule[];
  loading: boolean;
  error: string | null;
  fetchSchedules: () => Promise<void>;
  getSchedulesByActivity: (activityName: string) => ApiSchedule[];
}

const SchedulesContext = createContext<SchedulesContextType | undefined>(undefined);

export const SchedulesProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [schedules, setSchedules] = useState<ApiSchedule[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchSchedules = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`${API_BASE_URL}/horarios`);

      if (!response.ok) {
        throw new Error('Error al cargar los horarios');
      }

      const data: ApiSchedule[] = await response.json();
      setSchedules(data);
    } catch (err) {
      console.error('Error fetching schedules:', err);
      setError('No se pudieron cargar los horarios. Por favor, intenta de nuevo.');
      setSchedules([]);
    } finally {
      setLoading(false);
    }
  };

  const getSchedulesByActivity = (activityName: string): ApiSchedule[] => {
    return schedules.filter(
      (schedule) =>
        schedule.actividad.nombre.toLowerCase() === activityName.toLowerCase() &&
        schedule.estado === 'activo'
    );
  };

  return (
    <SchedulesContext.Provider
      value={{
        schedules,
        loading,
        error,
        fetchSchedules,
        getSchedulesByActivity,
      }}
    >
      {children}
    </SchedulesContext.Provider>
  );
};

export const useSchedules = (): SchedulesContextType => {
  const context = useContext(SchedulesContext);
  if (!context) {
    throw new Error('useSchedules must be used within a SchedulesProvider');
  }
  return context;
};