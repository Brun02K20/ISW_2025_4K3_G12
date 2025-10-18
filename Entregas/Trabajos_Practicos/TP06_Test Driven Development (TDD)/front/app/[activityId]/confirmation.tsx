import { Ionicons } from '@expo/vector-icons';
import { useLocalSearchParams, useRouter } from 'expo-router';
import React from 'react';
import {
    Alert,
    SafeAreaView,
    ScrollView,
    StyleSheet,
    Text,
    TouchableOpacity,
    View,
} from 'react-native';
import { activities } from '../../data/activities';
import { Participant } from '../../types';

export default function Confirmation() {
  const router = useRouter();
  const { activityId, scheduleId, participants } = useLocalSearchParams();

  const activity = activities.find(a => a.id === activityId);
  const schedule = activity?.schedules.find(s => s.id === scheduleId);
  const participantsData: Participant[] = participants 
    ? JSON.parse(participants as string) 
    : [];

  if (!activity || !schedule) {
    return null;
  }

  const handleConfirm = () => {
    Alert.alert(
      '¡Reserva Confirmada!',
      `Tu reserva para ${activity.name} ha sido confirmada exitosamente.`,
      [
        {
          text: 'OK',
          onPress: () => router.push('/'),
        },
      ]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView}>
        <View style={styles.header}>
          <View style={styles.successIcon}>
            <Ionicons name="checkmark-circle" size={64} color="#16a34a" />
          </View>
          <Text style={styles.title}>Confirma tu Reserva</Text>
          <Text style={styles.subtitle}>Revisa los detalles antes de confirmar</Text>
        </View>

        <View style={styles.content}>
          {/* Activity Details */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Detalles de la Actividad</Text>
            <View style={styles.detailCard}>
              <View style={styles.detailRow}>
                <Text style={styles.detailLabel}>Actividad:</Text>
                <Text style={styles.detailValue}>{activity.name}</Text>
              </View>
              <View style={styles.detailRow}>
                <Ionicons name="time-outline" size={20} color="#6b7280" />
                <Text style={styles.detailValue}>Horario: {schedule.time}</Text>
              </View>
              <View style={styles.detailRow}>
                <Ionicons name="people-outline" size={20} color="#6b7280" />
                <Text style={styles.detailValue}>
                  {participantsData.length} {participantsData.length === 1 ? 'participante' : 'participantes'}
                </Text>
              </View>
            </View>
          </View>

          {/* Participants Details */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Participantes</Text>
            {participantsData.map((participant, index) => (
              <View key={index} style={styles.participantCard}>
                <Text style={styles.participantNumber}>Participante {index + 1}</Text>
                <View style={styles.participantDetails}>
                  <View style={styles.participantRow}>
                    <Ionicons name="person-outline" size={18} color="#6b7280" />
                    <Text style={styles.participantText}>{participant.fullName}</Text>
                  </View>
                  <View style={styles.participantRow}>
                    <Ionicons name="card-outline" size={18} color="#6b7280" />
                    <Text style={styles.participantText}>DNI: {participant.dni}</Text>
                  </View>
                  <View style={styles.participantRow}>
                    <Ionicons name="calendar-outline" size={18} color="#6b7280" />
                    <Text style={styles.participantText}>{participant.age} años</Text>
                  </View>
                  {participant.clothingSize && (
                    <View style={styles.participantRow}>
                      <Ionicons name="shirt-outline" size={18} color="#6b7280" />
                      <Text style={styles.participantText}>Talla: {participant.clothingSize}</Text>
                    </View>
                  )}
                </View>
              </View>
            ))}
          </View>

          {/* Important Info */}
          <View style={styles.infoBox}>
            <Ionicons name="information-circle" size={24} color="#3b82f6" />
            <View style={styles.infoTextContainer}>
              <Text style={styles.infoTitle}>Información importante</Text>
              <Text style={styles.infoText}>
                • Llega 15 minutos antes del horario seleccionado{'\n'}
                • Trae documento de identidad{'\n'}
                • Sigue las instrucciones del personal
              </Text>
            </View>
          </View>
        </View>
      </ScrollView>

      <View style={styles.footer}>
        <TouchableOpacity style={styles.backBtn} onPress={() => router.back()}>
          <Text style={styles.backBtnText}>Volver</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.confirmBtn, { backgroundColor: activity.color }]}
          onPress={handleConfirm}
        >
          <Text style={styles.confirmBtnText}>Confirmar Reserva</Text>
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
  scrollView: {
    flex: 1,
  },
  header: {
    padding: 24,
    paddingTop: 16,
    backgroundColor: '#ffffff',
    alignItems: 'center',
  },
  successIcon: {
    marginBottom: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#6b7280',
    textAlign: 'center',
  },
  content: {
    padding: 16,
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 12,
  },
  detailCard: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
  },
  detailRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
    gap: 8,
  },
  detailLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#4b5563',
  },
  detailValue: {
    fontSize: 16,
    color: '#1f2937',
  },
  participantCard: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
  },
  participantNumber: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 12,
  },
  participantDetails: {
    gap: 8,
  },
  participantRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  participantText: {
    fontSize: 15,
    color: '#4b5563',
  },
  infoBox: {
    flexDirection: 'row',
    backgroundColor: '#eff6ff',
    borderRadius: 12,
    padding: 16,
    gap: 12,
  },
  infoTextContainer: {
    flex: 1,
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1e40af',
    marginBottom: 8,
  },
  infoText: {
    fontSize: 14,
    color: '#1e40af',
    lineHeight: 20,
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
  confirmBtn: {
    flex: 1,
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
  },
  confirmBtnText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#ffffff',
  },
});