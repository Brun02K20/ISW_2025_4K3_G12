import { activityStyles } from "@/data/activitiesStyles";
import { Ionicons } from "@expo/vector-icons";
import { Picker } from "@react-native-picker/picker";
import { useLocalSearchParams, useRouter } from "expo-router";
import React, { useEffect, useState } from "react";
import {
  Platform,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import { useSchedules } from "../../contexts/SchedulesContext";
import { Participant, convertApiScheduleToSchedule } from "../../types";

const clothingSizes = ["XS", "S", "M", "L", "XL", "XXL"];

interface ValidationErrors {
  [participantIndex: number]: {
    fullName?: string;
    dni?: string;
    age?: string;
    clothingSize?: string;
  };
}

export default function ParticipantsForm() {
  const router = useRouter();
  const { activityId, scheduleId } = useLocalSearchParams();
  const { schedules, getSchedulesByActivity } = useSchedules();

  const [participantCount, setParticipantCount] = useState(1);
  const [participants, setParticipants] = useState<Participant[]>([
    { fullName: "", dni: "", age: "", clothingSize: "" },
  ]);
  const [errors, setErrors] = useState<ValidationErrors>({});
  const [maxParticipants, setMaxParticipants] = useState(10);
  const [activity, setActivity] = useState<any | null>(null);

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

  // ✅ Calcular cupos según el horario elegido
  useEffect(() => {
    if (!activity) return;
    const apiSchedules = getSchedulesByActivity(activity.name);
    const converted = apiSchedules.map(convertApiScheduleToSchedule);
    const selected = converted.find((s) => s.id === normalizedScheduleId);

    if (selected) {
      setMaxParticipants(selected.availableSpots);
      if (participantCount > selected.availableSpots) {
        setParticipantCount(selected.availableSpots);
        setParticipants(participants.slice(0, selected.availableSpots));
      }
    }
  }, [activity, normalizedScheduleId]);

  const validateField = (index: number, field: keyof Participant, value: string): string | undefined => {
    switch (field) {
      case "fullName":
        if (!value.trim()) return "Este campo es requerido";
        if (value.trim().length < 3) return "El nombre debe tener al menos 3 caracteres";
        break;
      case "dni":
        if (!value.trim()) return "Este campo es requerido";
        if (!/^[0-9]{7,8}$/.test(value)) return "DNI inválido (7 u 8 dígitos)";
        break;
      case "age":
        if (!value.trim()) return "Este campo es requerido";
        const age = parseInt(value);
        if (isNaN(age) || age < 1 || age > 119) return "Edad inválida";
        if (activity?.minAge && age < activity.minAge)
          return `Edad mínima requerida: ${activity.minAge} años`;
        break;
      case "clothingSize":
        if (activity?.requiresSize && (!value || value === "")) return "Este campo es requerido";
        break;
    }
    return undefined;
  };

  const validateAllParticipants = (): boolean => {
    const newErrors: ValidationErrors = {};
    let isValid = true;

    participants.forEach((participant, index) => {
      const pErrors: any = {};
      (["fullName", "dni", "age", "clothingSize"] as (keyof Participant)[]).forEach((field) => {
        const value = participant[field] || "";
        const err = validateField(index, field, value);
        if (err) {
          pErrors[field] = err;
          isValid = false;
        }
      });
      if (Object.keys(pErrors).length > 0) newErrors[index] = pErrors;
    });

    setErrors(newErrors);
    return isValid;
  };

  const handleFieldChange = (index: number, field: keyof Participant, value: string) => {
    const updated = [...participants];
    updated[index] = { ...updated[index], [field]: value };
    setParticipants(updated);

    const err = validateField(index, field, value);
    setErrors((prev) => {
      const newE = { ...prev };
      if (!newE[index]) newE[index] = {};
      if (err) newE[index][field] = err;
      else {
        delete newE[index][field];
        if (Object.keys(newE[index]).length === 0) delete newE[index];
      }
      return newE;
    });
  };

  const handleIncrement = () => {
    if (participantCount < maxParticipants) {
      setParticipantCount(participantCount + 1);
      setParticipants([...participants, { fullName: "", dni: "", age: "", clothingSize: "" }]);
    }
  };

  const handleDecrement = () => {
    if (participantCount > 1) {
      setParticipantCount(participantCount - 1);
      const trimmed = participants.slice(0, -1);
      setParticipants(trimmed);
      setErrors((prev) => {
        const newE = { ...prev };
        delete newE[participantCount - 1];
        return newE;
      });
    }
  };

  const handleContinue = () => {
    if (!validateAllParticipants()) return;
    router.push({
      pathname: "/[activityId]/confirmation",
      params: {
        activityId: normalizedActivityId,
        scheduleId: normalizedScheduleId,
        participants: JSON.stringify(participants),
      },
    });
  };

  if (!activity) return null;

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#1f2937" />
          </TouchableOpacity>
          <Text style={styles.title}>Datos de los Participantes</Text>
          <Text style={styles.subtitle}>Ingresa la información de cada participante</Text>
        </View>

        <View style={styles.content}>
          <View style={styles.activityInfo}>
            <Text style={styles.activityInfoTitle}>Actividad: {activity.name}</Text>
            {activity.minAge && (
              <View style={styles.warningBox}>
                <Ionicons name="information-circle" size={20} color="#92400e" />
                <Text style={styles.warningText}>
                  Edad mínima requerida: {activity.minAge} años
                </Text>
              </View>
            )}
            {activity.requiresSize && (
              <View style={styles.warningBox}>
                <Ionicons name="information-circle" size={20} color="#92400e" />
                <Text style={styles.warningText}>
                  Esta actividad requiere talla de vestimenta
                </Text>
              </View>
            )}
          </View>

          {/* contador */}
          <View style={styles.counterSection}>
            <Text style={styles.counterLabel}>Cantidad de participantes</Text>
            <Text style={styles.counterSubLabel}>Cupos disponibles: {maxParticipants}</Text>
            <View style={styles.counter}>
              <TouchableOpacity onPress={handleDecrement} disabled={participantCount === 1}>
                <Ionicons
                  name="remove"
                  size={24}
                  color={participantCount === 1 ? "#d1d5db" : "#4b5563"}
                />
              </TouchableOpacity>
              <Text style={styles.counterValue}>{participantCount}</Text>
              <TouchableOpacity
                onPress={handleIncrement}
                disabled={participantCount >= maxParticipants}
              >
                <Ionicons
                  name="add"
                  size={24}
                  color={participantCount >= maxParticipants ? "#d1d5db" : "#4b5563"}
                />
              </TouchableOpacity>
            </View>
          </View>

          {/* formulario */}
          {participants.map((p, i) => (
            <View key={i} style={styles.participantCard}>
              <Text style={styles.participantTitle}>Participante {i + 1}</Text>

              {/* Nombre */}
                <View style={styles.inputGroup}>
                <Text style={styles.label}>Nombre completo *</Text>
                <TextInput
                  style={[styles.input, errors[i]?.fullName && styles.inputError]}
                  value={p.fullName}
                  onChangeText={(v) => handleFieldChange(i, "fullName", v)}
                  placeholder="Juan Pérez"
                  placeholderTextColor="#9ca3af"
                />
                {errors[i]?.fullName && <Text style={styles.errorText}>{errors[i].fullName}</Text>}
                </View>

                {/* DNI */}
              <View style={styles.inputGroup}>
                <Text style={styles.label}>DNI *</Text>
                <TextInput
                  style={[styles.input, errors[i]?.dni && styles.inputError]}
                  keyboardType="numeric"
                  value={p.dni}
                  maxLength={8}
                  onChangeText={(v) => handleFieldChange(i, "dni", v)}
                  placeholder="12345678"
                  placeholderTextColor="#9ca3af"
                />
                {errors[i]?.dni && <Text style={styles.errorText}>{errors[i].dni}</Text>}
              </View>

              {/* Edad */}
              <View style={styles.inputGroup}>
                <Text style={styles.label}>Edad *</Text>
                <TextInput
                  style={[styles.input, errors[i]?.age && styles.inputError]}
                  keyboardType="numeric"
                  value={p.age}
                  maxLength={3}
                  onChangeText={(v) => handleFieldChange(i, "age", v)}
                  placeholder="25"
                  placeholderTextColor="#9ca3af"
                />
                {errors[i]?.age && <Text style={styles.errorText}>{errors[i].age}</Text>}
              </View>

              {/* Talle */}
              {activity.requiresSize && (
                <View style={styles.inputGroup}>
                  <Text style={styles.label}>Talla de vestimenta *</Text>
                  <View
                    style={[styles.pickerContainer, errors[i]?.clothingSize && styles.inputError]}
                  >
                    <Picker
                      selectedValue={p.clothingSize}
                      onValueChange={(v) => handleFieldChange(i, "clothingSize", v)}
                      style={styles.picker}
                      dropdownIconColor="#6b7280"
                    >
                      <Picker.Item label="Seleccionar talla" value="" color="#9ca3af" />
                      {clothingSizes.map((s) => (
                        <Picker.Item key={s} label={s} value={s} color="#1f2937" />
                      ))}
                    </Picker>
                  </View>
                  {errors[i]?.clothingSize && (
                    <Text style={styles.errorText}>{errors[i].clothingSize}</Text>
                  )}
                </View>
              )}
            </View>
          ))}
        </View>
      </ScrollView>

      <View style={styles.footer}>
        <TouchableOpacity style={styles.backBtn} onPress={() => router.back()}>
          <Text style={styles.backBtnText}>Volver</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.continueBtn, { backgroundColor: activity.color }]}
          onPress={handleContinue}
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
    backgroundColor: "#f5f5f5",
  },
  scrollView: {
    flex: 1,
  },
  header: {
    padding: 24,
    paddingTop: 16,
    backgroundColor: "#ffffff",
  },
  backButton: {
    marginBottom: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#1f2937",
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: "#6b7280",
  },
  content: {
    padding: 16,
  },
  activityInfo: {
    backgroundColor: "#fef3c7",
    padding: 16,
    borderRadius: 12,
    marginBottom: 24,
  },
  activityInfoTitle: {
    fontSize: 16,
    fontWeight: "600",
    color: "#78350f",
    marginBottom: 8,
  },
  warningBox: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginTop: 8,
  },
  warningText: {
    fontSize: 14,
    color: "#92400e",
    flex: 1,
  },
  counterSection: {
    marginBottom: 24,
  },
  counterLabel: {
    fontSize: 16,
    fontWeight: "600",
    color: "#1f2937",
    marginBottom: 4,
  },
  counterSubLabel: {
    fontSize: 14,
    color: "#6b7280",
    marginBottom: 12,
  },
  counter: {
    flexDirection: "row",
    alignItems: "center",
    gap: 20,
  },
  counterButton: {
    width: 40,
    height: 40,
    borderRadius: 8,
    backgroundColor: "#ffffff",
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1,
    borderColor: "#e5e7eb",
  },
  counterValue: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#1f2937",
    minWidth: 40,
    textAlign: "center",
  },
  participantCard: {
    backgroundColor: "#ffffff",
    borderRadius: 12,
    padding: 20,
    marginBottom: 16,
  },
  participantTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "#1f2937",
    marginBottom: 16,
  },
  inputGroup: {
    marginBottom: 16,
  },
  label: {
    fontSize: 14,
    fontWeight: "500",
    color: "#374151",
    marginBottom: 8,
  },
  required: {
    color: "#ef4444",
  },
  input: {
    backgroundColor: "#f9fafb",
    borderWidth: 1,
    borderColor: "#e5e7eb",
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    color: "#1f2937",
  },
  inputError: {
    borderColor: "#ef4444",
  },
  errorText: {
    color: "#ef4444",
    fontSize: 12,
    marginTop: 4,
  },
  pickerContainer: {
    backgroundColor: "#f9fafb",
    borderWidth: 1,
    borderColor: "#e5e7eb",
    borderRadius: 8,
    overflow: "hidden",
  },
  picker: {
    height: Platform.OS === "ios" ? 180 : 50,
    color: "#1f2937",
  },
  footer: {
    flexDirection: "row",
    padding: 16,
    gap: 12,
    backgroundColor: "#ffffff",
    borderTopWidth: 1,
    borderTopColor: "#e5e7eb",
  },
  backBtn: {
    flex: 1,
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: "center",
    backgroundColor: "#f3f4f6",
  },
  backBtnText: {
    fontSize: 16,
    fontWeight: "600",
    color: "#4b5563",
  },
  continueBtn: {
    flex: 1,
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: "center",
  },
  continueBtnText: {
    fontSize: 16,
    fontWeight: "600",
    color: "#ffffff",
  },
});
