import { activityStyles } from '@/data/activitiesStyles';
import { Ionicons } from '@expo/vector-icons';
import { useLocalSearchParams, useRouter } from 'expo-router';
import React, { useEffect, useState } from 'react';
import {
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import { useSchedules } from '../../contexts/SchedulesContext';
import { Schedule, convertApiScheduleToSchedule } from '../../types';

export default function SelectSchedule() {
  const router = useRouter();
  const { activityId } = useLocalSearchParams();
  const { schedules } = useSchedules();

  const [selectedSchedule, setSelectedSchedule] = useState<string | null>(null);
  const [filteredSchedules, setFilteredSchedules] = useState<Schedule[]>([]);
  const [activity, setActivity] = useState<{
    id: string;
    name: string;
    description: string;
    color: string;
    icon: string;
  } | null>(null);

  // Normalizamos activityId
  const normalizedActivityId = Array.isArray(activityId) ? activityId[0] : activityId;

  useEffect(() => {
    if (!normalizedActivityId || schedules.length === 0) return;

    // Buscar la actividad por ID dentro de los schedules
    const relatedSchedules = schedules.filter(
      (s) => s.actividad.id.toString() === normalizedActivityId && s.estado === 'activo'
    );

    if (relatedSchedules.length === 0) return;

    const actividad = relatedSchedules[0].actividad;

    // Buscar icono y color desde activityStyles
    const style = activityStyles[actividad.nombre] || { icon: '❓', color: '#9ca3af' };

    // Setear actividad actual
    setActivity({
      id: actividad.id.toString(),
      name: actividad.nombre,
      description: actividad.descripcion,
      color: style.color,
      icon: style.icon,
    });

    // Convertir y ordenar los horarios
    const convertedSchedules = relatedSchedules
      .map(convertApiScheduleToSchedule)
      .sort((a, b) => a.time.localeCompare(b.time));

    setFilteredSchedules(convertedSchedules);
  }, [schedules, normalizedActivityId]);

  const handleContinue = () => {
    if (selectedSchedule) {
      router.push({
        pathname: '/[activityId]/participants',
        params: { activityId: normalizedActivityId, scheduleId: selectedSchedule },
      });
    }
  };

  if (!activity) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>Actividad no encontrada</Text>
          <TouchableOpacity style={styles.backBtn} onPress={() => router.back()}>
            <Text style={styles.backBtnText}>Volver</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#1f2937" />
          </TouchableOpacity>
          <Text style={styles.title}>Selecciona el Horario</Text>
          <Text style={styles.subtitle}>
            Elige un horario disponible para {activity.name}
          </Text>
        </View>

        <View style={styles.content}>
          <View style={styles.selectedActivity}>
            <Text style={styles.labelText}>Actividad seleccionada:</Text>
            <Text style={styles.activityNameText}>{activity.icon} {activity.name}</Text>
          </View>

          <Text style={styles.sectionTitle}>Horarios disponibles:</Text>

          {filteredSchedules.length === 0 ? (
            <View style={styles.emptyContainer}>
              <Ionicons name="calendar-outline" size={48} color="#9ca3af" />
              <Text style={styles.emptyText}>No hay horarios disponibles</Text>
            </View>
          ) : (
            filteredSchedules.map((schedule) => (
              <TouchableOpacity
                key={schedule.id}
                style={[
                  styles.scheduleCard,
                  selectedSchedule === schedule.id && styles.scheduleCardSelected,
                  schedule.status === 'full' && styles.scheduleCardDisabled,
                ]}
                onPress={() =>
                  schedule.status === 'available' && setSelectedSchedule(schedule.id)
                }
                disabled={schedule.status === 'full'}
              >
                <View style={styles.scheduleLeft}>
                  <Ionicons
                    name="time-outline"
                    size={24}
                    color={schedule.status === 'full' ? '#d1d5db' : '#6b7280'}
                  />
                  <Text
                    style={[
                      styles.timeText,
                      schedule.status === 'full' && styles.timeTextDisabled,
                    ]}
                  >
                    {schedule.time}
                  </Text>
                </View>

                <View style={styles.scheduleRight}>
                  <Ionicons
                    name="people-outline"
                    size={16}
                    color={schedule.status === 'full' ? '#ef4444' : '#6b7280'}
                  />
                  {schedule.status === 'available' ? (
                    <View style={styles.spotsAvailable}>
                      <Text style={styles.spotsText}>{schedule.availableSpots} cupos</Text>
                    </View>
                  ) : (
                    <View style={styles.spotsFull}>
                      <Text style={styles.spotsFullText}>Completo</Text>
                    </View>
                  )}
                </View>
              </TouchableOpacity>
            ))
          )}
        </View>
      </ScrollView>

      <View style={styles.footer}>
        <TouchableOpacity style={styles.backBtn} onPress={() => router.back()}>
          <Text style={styles.backBtnText}>Volver</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[
            styles.continueBtn,
            !selectedSchedule && styles.continueBtnDisabled,
            { backgroundColor: activity.color },
          ]}
          onPress={handleContinue}
          disabled={!selectedSchedule}
        >
          <Text style={styles.continueBtnText}>Continuar</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  errorText: {
    fontSize: 18,
    color: '#991b1b',
    marginBottom: 16,
  },
  scrollView: {
    flex: 1,
  },
  header: {
    padding: 24,
    paddingTop: 16,
    backgroundColor: '#ffffff',
  },
  backButton: {
    marginBottom: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#6b7280',
  },
  content: {
    padding: 16,
  },
  selectedActivity: {
    backgroundColor: '#fef3c7',
    padding: 16,
    borderRadius: 12,
    marginBottom: 24,
  },
  labelText: {
    fontSize: 14,
    color: '#92400e',
    marginBottom: 4,
  },
  activityNameText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#78350f',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 16,
  },
  emptyContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 40,
  },
  emptyText: {
    marginTop: 12,
    fontSize: 16,
    color: '#6b7280',
  },
  scheduleCard: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#ffffff',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  scheduleCardSelected: {
    borderColor: '#3b82f6',
    backgroundColor: '#eff6ff',
  },
  scheduleCardDisabled: {
    backgroundColor: '#f9fafb',
  },
  scheduleLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  timeText: {
    fontSize: 20,
    fontWeight: '600',
    color: '#1f2937',
  },
  timeTextDisabled: {
    color: '#d1d5db',
  },
  scheduleRight: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  spotsAvailable: {
    backgroundColor: '#d1fae5',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  spotsText: {
    color: '#065f46',
    fontSize: 14,
    fontWeight: '600',
  },
  spotsFull: {
    backgroundColor: '#fee2e2',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  spotsFullText: {
    color: '#991b1b',
    fontSize: 14,
    fontWeight: '600',
  },
  footer: {
    flexDirection: 'row',
    padding: 16,
    gap: 12,
    backgroundColor: '#ffffff',
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
  },
  backBtn: {
    flex: 1,
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
    backgroundColor: '#f3f4f6',
  },
  backBtnText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#4b5563',
  },
  continueBtn: {
    flex: 1,
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
  },
  continueBtnDisabled: {
    opacity: 0.5,
  },
  continueBtnText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#ffffff',
  },
});