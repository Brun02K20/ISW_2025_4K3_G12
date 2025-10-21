// app/(tabs)/index.tsx
import { Ionicons } from '@expo/vector-icons';
import React, { useState } from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';

interface Activity {
  id: string;
  name: string;
  icon: keyof typeof Ionicons.glyphMap;
  availableSlots: number;
  requiresSize: boolean;
  color: string;
}

const activities: Activity[] = [
  {
    id: '1',
    name: 'Tirolesa',
    icon: 'arrow-forward',
    availableSlots: 4,
    requiresSize: true,
    color: '#10b981',
  },
  {
    id: '2',
    name: 'Escalada',
    icon: 'trending-up',
    availableSlots: 3,
    requiresSize: false,
    color: '#3b82f6',
  },
  {
    id: '3',
    name: 'Kayak',
    icon: 'boat',
    availableSlots: 3,
    requiresSize: true,
    color: '#06b6d4',
  },
  {
    id: '4',
    name: 'Senderismo',
    icon: 'walk',
    availableSlots: 3,
    requiresSize: false,
    color: '#8b5cf6',
  },
];

export default function HomeScreen() {
  const [selectedActivity, setSelectedActivity] = useState<string | null>(null);

  const handleActivityPress = (activityId: string) => {
    setSelectedActivity(activityId);
    // Aquí navegarías a la pantalla de detalles/reserva
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <ScrollView style={styles.scrollView}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>Parque Aventura</Text>
          <Text style={styles.subtitle}>
            Reserva tu lugar en nuestras actividades
          </Text>
        </View>

        {/* Activities Grid */}
        <View style={styles.activitiesContainer}>
          {activities.map((activity) => (
            <TouchableOpacity
              key={activity.id}
              style={[
                styles.activityCard,
                selectedActivity === activity.id && styles.activityCardSelected,
              ]}
              onPress={() => handleActivityPress(activity.id)}
              activeOpacity={0.7}
            >
              {/* Icon Circle */}
              <View
                style={[
                  styles.iconCircle,
                  { backgroundColor: activity.color + '20' },
                ]}
              >
                <Ionicons
                  name={activity.icon}
                  size={32}
                  color={activity.color}
                />
              </View>

              {/* Activity Info */}
              <View style={styles.activityInfo}>
                <Text style={styles.activityName}>{activity.name}</Text>

                {/* Badges */}
                <View style={styles.badgesContainer}>
                  {activity.requiresSize && (
                    <View style={styles.badge}>
                      <Ionicons name="shirt-outline" size={12} color="#6b7280" />
                      <Text style={styles.badgeText}>
                        Requiere talla de vestimenta
                      </Text>
                    </View>
                  )}
                  <View style={styles.badge}>
                    <Ionicons name="time-outline" size={12} color="#6b7280" />
                    <Text style={styles.badgeText}>
                      {activity.availableSlots} horarios disponibles
                    </Text>
                  </View>
                </View>
              </View>

              {/* Arrow */}
              <Ionicons
                name="chevron-forward"
                size={20}
                color="#9ca3af"
                style={styles.arrow}
              />
            </TouchableOpacity>
          ))}
        </View>

        {/* Info Section */}
        <View style={styles.infoSection}>
          <View style={styles.infoCard}>
            <Ionicons name="information-circle" size={24} color="#3b82f6" />
            <Text style={styles.infoText}>
              Selecciona una actividad para ver los horarios disponibles y
              realizar tu reserva
            </Text>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
  },
  scrollView: {
    flex: 1,
  },
  header: {
    padding: 24,
    paddingTop: 16,
    backgroundColor: '#ffffff',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#111827',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#6b7280',
    lineHeight: 24,
  },
  activitiesContainer: {
    padding: 16,
  },
  activityCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffffff',
    borderRadius: 16,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  activityCardSelected: {
    borderWidth: 2,
    borderColor: '#3b82f6',
  },
  iconCircle: {
    width: 60,
    height: 60,
    borderRadius: 30,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 16,
  },
  activityInfo: {
    flex: 1,
  },
  activityName: {
    fontSize: 18,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 8,
  },
  badgesContainer: {
    gap: 6,
  },
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  badgeText: {
    fontSize: 13,
    color: '#6b7280',
  },
  arrow: {
    marginLeft: 8,
  },
  infoSection: {
    padding: 16,
    paddingTop: 8,
  },
  infoCard: {
    flexDirection: 'row',
    backgroundColor: '#eff6ff',
    borderRadius: 12,
    padding: 16,
    gap: 12,
  },
  infoText: {
    flex: 1,
    fontSize: 14,
    color: '#1e40af',
    lineHeight: 20,
  },
});