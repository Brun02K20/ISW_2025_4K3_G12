import { activityStyles } from "@/data/activitiesStyles";
import { sendInscriptionEmail } from "@/services/email.service";
import { createInscripcion } from "@/services/inscripcion.service";
import { Ionicons } from '@expo/vector-icons';
import Checkbox from 'expo-checkbox';
import { useLocalSearchParams, useRouter } from 'expo-router';
import React, { useEffect, useState } from 'react';
import {
  ActivityIndicator,
  Modal,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import { useSchedules } from '../../contexts/SchedulesContext';
import { ApiSchedule, Participant } from '../../types';

export default function Confirmation() {
  const router = useRouter();
  const { activityId, scheduleId, participants } = useLocalSearchParams();
  const { getSchedulesByActivity, fetchSchedules, schedules } = useSchedules();
  
  const [aceptaTerminos, setAceptaTerminos] = useState(false);
  const [sending, setSending] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const [showErrorModal, setShowErrorModal] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [selectedSchedule, setSelectedSchedule] = useState<ApiSchedule | null>(null);
  const [activity, setActivity] = useState<any | null>(null);

  // Normalize params
  const normalizedActivityId = Array.isArray(activityId) ? activityId[0] : activityId;
  const normalizedScheduleId = Array.isArray(scheduleId) ? scheduleId[0] : scheduleId;

  // ✅ Obtenemos la actividad directamente desde schedules (API)
    useEffect(() => {
      if (!schedules || schedules.length === 0) return;
  
      // Agrupar actividades únicas igual que en SelectActivity
      const grouped = new Map<number, any>();
  
      for (const s of schedules) {
        const { actividad } = s;
        if (!grouped.has(actividad.id)) grouped.set(actividad.id, actividad);
      }
  
      const foundActivity = grouped.get(Number(normalizedActivityId));
      if (foundActivity) {
        const style = activityStyles[foundActivity.nombre] || { color: "#9ca3af", icon: "❓" };
        setActivity({
          id: foundActivity.id.toString(),
          name: foundActivity.nombre,
          minAge: foundActivity.edad,
          requiresSize: foundActivity.requiere_talle,
          color: style.color,
        });
      }
    }, [schedules, normalizedActivityId]);


  const participantsData: Participant[] = participants 
    ? JSON.parse(participants as string) 
    : [];

  // Obtener horario seleccionado del contexto
  useEffect(() => {
    if (activity) {
      const apiSchedules = getSchedulesByActivity(activity.name);
      const schedule = apiSchedules.find(s => s.id === parseInt(normalizedScheduleId));

      if (schedule) {
        setSelectedSchedule(schedule);
      }
    }
  }, [activity, normalizedScheduleId]);

  if (!activity || !selectedSchedule) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>Error al cargar la información</Text>
          <TouchableOpacity style={styles.backBtn} onPress={() => router.back()}>
            <Text style={styles.backBtnText}>Volver</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  const handleConfirm = async () => {
    if (!aceptaTerminos) {
      alert("Debes aceptar los Términos y Condiciones antes de continuar.");
      return;
    }

    // Preparar datos para ambos servicios
    const visitantesData = participantsData.map((p) => ({
      nombre: p.fullName,
      dni: Number(p.dni),
      edad: Number(p.age),
      talle: p.clothingSize || "",
    }));

    // Datos para la API (sin activity_name)
    const apiData = {
      id_horario: Number(normalizedScheduleId) || 0,
      visitantes: visitantesData,
      acepta_terminos: aceptaTerminos,
    };

    // Datos para el email (con activity_name)
    const emailData = {
      id_horario: Number(normalizedScheduleId) || 0,
      hora_inicio: selectedSchedule.hora_inicio,
      hora_fin: selectedSchedule.hora_fin,
      nombre_actividad: activity.name,
      visitantes: visitantesData,
      acepta_terminos: aceptaTerminos,
    };

    try {
      setSending(true);

      // 1. Enviar a la API
      const apiResponse = await createInscripcion(apiData);

      if (!apiResponse.success) {
        // Si la API falla, mostrar modal de error
        setErrorMessage(apiResponse.message);
        setShowErrorModal(true);
        return;
      }

      // 2. Si la API fue exitosa, enviar el email
      const emailResponse = await sendInscriptionEmail(emailData);

      if (!emailResponse.success) {
        // Si el email falla, avisar pero considerar la reserva exitosa
        console.warn("⚠️ Inscripción guardada pero el email falló:", emailResponse.message);
      }

      // 3. Actualizar los horarios en el contexto global
      await fetchSchedules();

      // 4. Mostrar modal de éxito
      setShowSuccessModal(true);

    } catch (error) {
      console.error("Error al confirmar reserva:", error);
      setShowErrorModal(true);
    } finally {
      setSending(false);
    }
  };

  const handleCloseModal = () => {
    setShowSuccessModal(false);
    router.push('/');
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#1f2937" />
          </TouchableOpacity>
          <View style={styles.headerIcon}>
            <Ionicons name="checkmark-circle-outline" size={64} color={activity.color} />
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
                <View style={[styles.activityIcon, { backgroundColor: activity.color + '20' }]}>
                    <Text style={styles.activityEmoji}>
                    {activityStyles[activity.name]?.icon ?? '❓'}
                    </Text>
                </View>
                <View style={styles.activityDetails}>
                  <Text style={styles.activityName}>{activity.name}</Text>
                  <Text style={styles.activityDescription}>{activity.description}</Text>
                </View>
              </View>
              
              <View style={styles.divider} />
              
              <View style={styles.infoRow}>
                <Ionicons name="time-outline" size={20} color="#6b7280" />
                <Text style={styles.infoText}>Horario: {selectedSchedule.hora_inicio}</Text>
              </View>
              
              <View style={styles.infoRow}>
                <Ionicons name="people-outline" size={20} color="#6b7280" />
                <Text style={styles.infoText}>
                  {participantsData.length} {participantsData.length === 1 ? 'participante' : 'participantes'}
                </Text>
              </View>

              {activity.minAge && (
                <View style={styles.infoRow}>
                  <Ionicons name="information-circle-outline" size={20} color="#6b7280" />
                  <Text style={styles.infoText}>Edad mínima: {activity.minAge} años</Text>
                </View>
              )}
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
              <Text style={styles.infoTextDetail}>
                • Llega 15 minutos antes del horario seleccionado{'\n'}
                • Trae documento de identidad{'\n'}
                • Sigue las instrucciones del personal
              </Text>
            </View>
          </View>

          {/* Terms and Conditions */}
          <View style={styles.termsContainer}>
            <Checkbox
              value={aceptaTerminos}
              onValueChange={setAceptaTerminos}
              color={aceptaTerminos ? activity.color : "#9ca3af"}
            />
            <Text style={styles.termsText}>
              Acepto los{" "}
              <Text style={[styles.termsLink, { color: activity.color }]}>
                Términos y Condiciones
              </Text>
            </Text>
          </View>
        </View>
      </ScrollView>

      <View style={styles.footer}>
        <TouchableOpacity 
          style={styles.backBtn} 
          onPress={() => router.back()}
          disabled={sending}
        >
          <Text style={styles.backBtnText}>Volver</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[
            styles.confirmBtn, 
            { backgroundColor: activity.color },
            (sending || !aceptaTerminos) && styles.confirmBtnDisabled
          ]}
          onPress={handleConfirm}
          disabled={sending || !aceptaTerminos}
        >
          {sending ? (
            <ActivityIndicator color="#ffffff" />
          ) : (
            <Text style={styles.confirmBtnText}>Confirmar Reserva</Text>
          )}
        </TouchableOpacity>
      </View>

      {/* Success Modal */}
      <Modal
        visible={showSuccessModal}
        transparent={true}
        animationType="fade"
        onRequestClose={handleCloseModal}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={[styles.modalIconContainer, { backgroundColor: activity.color + '20' }]}>
              <Ionicons name="checkmark-circle" size={80} color={activity.color} />
            </View>
            
            <Text style={styles.modalTitle}>¡Reserva Confirmada!</Text>
            <Text style={styles.modalMessage}>
              Tu reserva para <Text style={styles.modalActivityName}>{activity.name}</Text> ha sido confirmada exitosamente.
            </Text>
            <Text style={styles.modalSubMessage}>
              Recibirás un correo de confirmación con todos los detalles.
            </Text>
            
            <TouchableOpacity 
              style={[styles.modalButton, { backgroundColor: activity.color }]}
              onPress={handleCloseModal}
            >
              <Text style={styles.modalButtonText}>Aceptar</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>

      {/* Error Modal */}
      <Modal
        visible={showErrorModal}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setShowErrorModal(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalIconContainerError}>
              <Ionicons name="close-circle" size={80} color="#dc2626" />
            </View>
            
            <Text style={styles.modalTitleError}>Error al Confirmar</Text>
            <Text style={styles.modalMessage}>
              {errorMessage}
            </Text>
            <Text style={styles.modalSubMessage}>
              Por favor, intenta nuevamente o contacta con soporte si el problema persiste.
            </Text>
            
            <View style={styles.modalButtonsRow}>
              <TouchableOpacity 
                style={styles.modalButtonSecondary}
                onPress={() => setShowErrorModal(false)}
              >
                <Text style={styles.modalButtonSecondaryText}>Volver</Text>
              </TouchableOpacity>
              <TouchableOpacity 
                style={styles.modalButtonError}
                onPress={() => {
                  setShowErrorModal(false);
                  handleConfirm();
                }}
              >
                <Text style={styles.modalButtonText}>Reintentar</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
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
  backButton: {
    alignSelf: 'flex-start',
    marginBottom: 16,
  },
  headerIcon: {
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
    borderRadius: 16,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  detailRow: {
    flexDirection: 'row',
    gap: 16,
  },
  activityIcon: {
    width: 56,
    height: 56,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  activityEmoji: {
    fontSize: 32,
  },
  activityDetails: {
    flex: 1,
  },
  activityName: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 4,
  },
  activityDescription: {
    fontSize: 14,
    color: '#6b7280',
    lineHeight: 20,
  },
  divider: {
    height: 1,
    backgroundColor: '#e5e7eb',
    marginVertical: 16,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    paddingVertical: 8,
  },
  infoText: {
    fontSize: 16,
    color: '#4b5563',
  },
  participantCard: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
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
    marginBottom: 24,
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
  infoTextDetail: {
    fontSize: 14,
    color: '#1e40af',
    lineHeight: 20,
  },
  termsContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    backgroundColor: '#ffffff',
    padding: 16,
    borderRadius: 12,
  },
  termsText: {
    flex: 1,
    fontSize: 15,
    color: '#4b5563',
  },
  termsLink: {
    fontWeight: '600',
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
    marginBottom: 20,
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
  confirmBtnDisabled: {
    opacity: 0.5,
  },
  confirmBtnText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#ffffff',
  },
  // Modal styles
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  modalContent: {
    backgroundColor: '#ffffff',
    borderRadius: 24,
    padding: 32,
    alignItems: 'center',
    maxWidth: 400,
    width: '100%',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 16,
    elevation: 8,
  },
  modalIconContainer: {
    width: 120,
    height: 120,
    borderRadius: 60,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
  },
  modalTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 12,
    textAlign: 'center',
  },
  modalMessage: {
    fontSize: 16,
    color: '#4b5563',
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 8,
  },
  modalActivityName: {
    fontWeight: '600',
    color: '#1f2937',
  },
  modalSubMessage: {
    fontSize: 14,
    color: '#6b7280',
    textAlign: 'center',
    marginBottom: 24,
  },
  modalButton: {
    paddingVertical: 14,
    paddingHorizontal: 48,
    borderRadius: 12,
    minWidth: 200,
  },
  modalButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#ffffff',
    textAlign: 'center',
  },
  // Error Modal styles
  modalIconContainerError: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#fee2e2',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
  },
  modalTitleError: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#991b1b',
    marginBottom: 12,
    textAlign: 'center',
  },
  modalButtonsRow: {
    flexDirection: 'row',
    gap: 12,
    width: '100%',
  },
  modalButtonSecondary: {
    flex: 1,
    paddingVertical: 14,
    paddingHorizontal: 24,
    borderRadius: 12,
    backgroundColor: '#f3f4f6',
  },
  modalButtonSecondaryText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#4b5563',
    textAlign: 'center',
  },
  modalButtonError: {
    flex: 1,
    paddingVertical: 14,
    paddingHorizontal: 24,
    borderRadius: 12,
    backgroundColor: '#dc2626',
  },
});