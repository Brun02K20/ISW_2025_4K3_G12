import { activityStyles } from '@/data/activitiesStyles';
import { useRouter } from 'expo-router';
import React, { useEffect, useState } from 'react';
import {
  ActivityIndicator,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import { useSchedules } from '../contexts/SchedulesContext';

interface ActivityWithScheduleCount {
  id: string;
  name: string;
  description: string;
  icon: string;
  requiresSize: boolean;
  minAge: number | null;
  color: string;
  availableSchedulesCount: number;
}

export default function SelectActivity() {
  const router = useRouter();
  const { schedules, loading, error, fetchSchedules } = useSchedules();
  const [activities, setActivities] = useState<ActivityWithScheduleCount[]>([]);

  // Fetch solo si no hay datos
  useEffect(() => {
    if (schedules.length === 0 && !loading) {
      fetchSchedules();
    }
  }, []);

  // Procesar actividades una sola vez por cambio de schedules
  useEffect(() => {
    if (schedules.length === 0) return;

    // Agrupar por id de actividad
    const grouped = new Map<number, { actividad: any; horarios: typeof schedules }>();

    for (const schedule of schedules) {
      const { actividad } = schedule;
      if (!grouped.has(actividad.id)) {
        grouped.set(actividad.id, { actividad, horarios: [] });
      }
      grouped.get(actividad.id)!.horarios.push(schedule);
    }

    // Construir la lista de actividades únicas
    const uniqueActivities: ActivityWithScheduleCount[] = Array.from(grouped.values()).map(
      ({ actividad, horarios }) => {
        // Contar horarios disponibles activos
        const availableSchedulesCount = horarios.filter(
          (s) => s.estado === 'activo' && s.cupo_total - s.cupo_ocupado > 0
        ).length;

        // Buscar estilo (icono/color) desde el mapa
        const style = activityStyles[actividad.nombre] || { icon: '❓', color: '#9ca3af' };

        return {
          id: actividad.id.toString(),
          name: actividad.nombre,
          description: actividad.descripcion,
          requiresSize: actividad.requiere_talle,
          minAge: actividad.edad,
          icon: style.icon,
          color: style.color,
          availableSchedulesCount,
        };
      }
    );

    setActivities(uniqueActivities);
  }, [schedules]);

  // Mostrar loading
  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#16a34a" />
          <Text style={styles.loadingText}>Cargando actividades...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView}>
        <View style={styles.header}>
          <Text style={styles.title}>Selecciona tu Actividad</Text>
          <Text style={styles.subtitle}>Elige la actividad que deseas realizar</Text>
        </View>

        {error && (
          <View style={styles.errorContainer}>
            <Text style={styles.errorText}>{error}</Text>
            <TouchableOpacity style={styles.retryButton} onPress={fetchSchedules}>
              <Text style={styles.retryButtonText}>Reintentar</Text>
            </TouchableOpacity>
          </View>
        )}

        <View style={styles.activitiesContainer}>
          {activities.map((activity) => (
            <View key={activity.id} style={styles.activityCard}>
              <View style={styles.cardHeader}>
                <View style={[styles.iconContainer, { backgroundColor: activity.color + '20' }]}>
                  <Text style={styles.icon}>{activity.icon}</Text>
                </View>
                {activity.availableSchedulesCount > 0 ? (
                  <View style={styles.badge}>
                    <Text style={styles.badgeText}>Disponible</Text>
                  </View>
                ) : (
                  <View style={styles.badgeUnavailable}>
                    <Text style={styles.badgeUnavailableText}>Sin horarios</Text>
                  </View>
                )}
              </View>

              <Text style={styles.activityName}>{activity.name}</Text>
              <Text style={styles.activityDescription}>{activity.description}</Text>

              <View style={styles.infoContainer}>
                {activity.minAge && (
                  <Text style={styles.infoText}>• Edad mínima: {activity.minAge} años</Text>
                )}
                {activity.requiresSize && (
                  <Text style={styles.infoText}>• Requiere talla de vestimenta</Text>
                )}
                <Text style={styles.infoText}>
                  • {activity.availableSchedulesCount} horario
                  {activity.availableSchedulesCount !== 1 ? 's' : ''} disponible
                  {activity.availableSchedulesCount !== 1 ? 's' : ''}
                </Text>
              </View>

              <TouchableOpacity
                style={[
                  styles.selectButton,
                  { backgroundColor: activity.color },
                  activity.availableSchedulesCount === 0 && styles.selectButtonDisabled,
                ]}
                onPress={() =>
                  router.push({
                    pathname: '/[activityId]/schedule',
                    params: { activityId: activity.id },
                  })
                }
                disabled={activity.availableSchedulesCount === 0}
              >
                <Text style={styles.selectButtonText}>
                  {activity.availableSchedulesCount === 0 ? 'No disponible' : 'Seleccionar'}
                </Text>
              </TouchableOpacity>
            </View>
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollView: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  loadingText: {
    marginTop: 12,
    fontSize: 16,
    color: '#6b7280',
  },
  errorContainer: {
    margin: 16,
    padding: 16,
    backgroundColor: '#fee2e2',
    borderRadius: 12,
    alignItems: 'center',
  },
  errorText: {
    color: '#991b1b',
    fontSize: 14,
    textAlign: 'center',
    marginBottom: 12,
  },
  retryButton: {
    backgroundColor: '#dc2626',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
  retryButtonText: {
    color: '#ffffff',
    fontWeight: '600',
  },
  header: {
    padding: 24,
    paddingTop: 16,
    backgroundColor: '#ffffff',
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
  activitiesContainer: {
    padding: 16,
  },
  activityCard: {
    backgroundColor: '#ffffff',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  iconContainer: {
    width: 56,
    height: 56,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  icon: {
    fontSize: 32,
  },
  badge: {
    backgroundColor: '#d1fae5',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  badgeText: {
    color: '#065f46',
    fontSize: 13,
    fontWeight: '600',
  },
  badgeUnavailable: {
    backgroundColor: '#fee2e2',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  badgeUnavailableText: {
    color: '#991b1b',
    fontSize: 13,
    fontWeight: '600',
  },
  activityName: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 8,
  },
  activityDescription: {
    fontSize: 15,
    color: '#6b7280',
    lineHeight: 22,
    marginBottom: 16,
  },
  infoContainer: {
    marginBottom: 16,
  },
  infoText: {
    fontSize: 14,
    color: '#4b5563',
    marginBottom: 4,
  },
  selectButton: {
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
  },
  selectButtonDisabled: {
    opacity: 0.5,
  },
  selectButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
});