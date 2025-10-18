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
import { activitiesInfo } from "../../data/activities";
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
  const { getSchedulesByActivity } = useSchedules();
  const [participantCount, setParticipantCount] = useState(1);
  const [participants, setParticipants] = useState<Participant[]>([
    { fullName: "", dni: "", age: "", clothingSize: "" },
  ]);
  const [errors, setErrors] = useState<ValidationErrors>({});
  const [maxParticipants, setMaxParticipants] = useState(10);

  // Ensure params are strings
  const normalizedActivityId = Array.isArray(activityId)
    ? activityId[0]
    : activityId;
  const normalizedScheduleId = Array.isArray(scheduleId)
    ? scheduleId[0]
    : scheduleId;

  const activity = activitiesInfo.find((a) => a.id === normalizedActivityId);

  // Obtener el horario seleccionado y calcular cupos disponibles
  useEffect(() => {
    if (activity) {
      const apiSchedules = getSchedulesByActivity(activity.name);
      const schedules = apiSchedules.map(convertApiScheduleToSchedule);
      const selectedSchedule = schedules.find(
        (s) => s.id === normalizedScheduleId
      );

      if (selectedSchedule) {
        // El máximo de participantes es el número de cupos disponibles
        setMaxParticipants(selectedSchedule.availableSpots);

        // Si ya había más participantes seleccionados, ajustar
        if (participantCount > selectedSchedule.availableSpots) {
          setParticipantCount(selectedSchedule.availableSpots);
          setParticipants(
            participants.slice(0, selectedSchedule.availableSpots)
          );
        }
      }
    }
  }, [activity, normalizedScheduleId]);

  const validateField = (
    index: number,
    field: keyof Participant,
    value: string
  ): string | undefined => {
    switch (field) {
      case "fullName":
        if (!value.trim()) return "Este campo es requerido";
        if (value.trim().length < 3)
          return "El nombre debe tener al menos 3 caracteres";
        break;
      case "dni":
        if (!value.trim()) return "Este campo es requerido";
        if (!/^[0-9]{7,8}$/.test(value))
          return "DNI inválido (debe tener 7 u 8 dígitos)";
        break;
      case "age":
        if (!value.trim()) return "Este campo es requerido";
        const age = parseInt(value);
        if (isNaN(age) || age < 1 || age > 119) return "Edad inválida";
        // Validar edad mínima de la actividad
        if (activity?.minAge && age < activity.minAge) {
          return `Edad mínima requerida: ${activity.minAge} años`;
        }
        break;
      case "clothingSize":
        if (activity?.requiresSize && (!value || value === "")) {
          return "Este campo es requerido";
        }
        break;
    }
    return undefined;
  };

  const validateAllParticipants = (): boolean => {
    const newErrors: ValidationErrors = {};
    let isValid = true;

    participants.forEach((participant, index) => {
      const participantErrors: any = {};

      const fullNameError = validateField(
        index,
        "fullName",
        participant.fullName
      );
      if (fullNameError) {
        participantErrors.fullName = fullNameError;
        isValid = false;
      }

      const dniError = validateField(index, "dni", participant.dni);
      if (dniError) {
        participantErrors.dni = dniError;
        isValid = false;
      }

      const ageError = validateField(index, "age", participant.age);
      if (ageError) {
        participantErrors.age = ageError;
        isValid = false;
      }

      if (activity?.requiresSize) {
        const sizeError = validateField(
          index,
          "clothingSize",
          participant.clothingSize || ""
        );
        if (sizeError) {
          participantErrors.clothingSize = sizeError;
          isValid = false;
        }
      }

      if (Object.keys(participantErrors).length > 0) {
        newErrors[index] = participantErrors;
      }
    });

    setErrors(newErrors);
    return isValid;
  };

  const handleFieldChange = (
    index: number,
    field: keyof Participant,
    value: string
  ) => {
    const newParticipants = [...participants];
    newParticipants[index] = { ...newParticipants[index], [field]: value };
    setParticipants(newParticipants);

    // VALIDAR INMEDIATAMENTE (cambio principal #1)
    const error = validateField(index, field, value);
    setErrors((prev) => {
      const newErrors = { ...prev };
      if (!newErrors[index]) newErrors[index] = {};

      if (error) {
        newErrors[index][field] = error;
      } else {
        delete newErrors[index][field];
        if (Object.keys(newErrors[index]).length === 0) {
          delete newErrors[index];
        }
      }
      return newErrors;
    });
  };

  const handleFieldBlur = (
    index: number,
    field: keyof Participant,
    valueOverride?: string
  ) => {
    // Usar el valor override si se proporciona, sino tomar del estado actual
    const value =
      valueOverride !== undefined
        ? valueOverride
        : participants[index][field] || "";
    const error = validateField(index, field, value);

    setErrors((prev) => {
      const newErrors = { ...prev };
      if (!newErrors[index]) newErrors[index] = {};

      if (error) {
        newErrors[index][field] = error;
      } else {
        delete newErrors[index][field];
        if (Object.keys(newErrors[index]).length === 0) {
          delete newErrors[index];
        }
      }
      return newErrors;
    });
  };

  const handleIncrement = () => {
    // Limitar al máximo de cupos disponibles (cambio principal #2)
    if (participantCount < maxParticipants) {
      setParticipantCount(participantCount + 1);
      setParticipants([
        ...participants,
        { fullName: "", dni: "", age: "", clothingSize: "" },
      ]);
    }
  };

  const handleDecrement = () => {
    if (participantCount > 1) {
      setParticipantCount(participantCount - 1);
      const newParticipants = [...participants];
      newParticipants.pop();
      setParticipants(newParticipants);

      // Limpiar errores del participante eliminado
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[participantCount - 1];
        return newErrors;
      });
    }
  };

  const handleContinue = () => {
    const isValid = validateAllParticipants();

    if (isValid) {
      router.push({
        pathname: "/[activityId]/confirmation",
        params: {
          activityId: normalizedActivityId as string,
          scheduleId: normalizedScheduleId,
          participants: JSON.stringify(participants),
        },
      });
    }
  };

  if (!activity) {
    return null;
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView}>
        <View style={styles.header}>
          <TouchableOpacity
            onPress={() => router.back()}
            style={styles.backButton}
          >
            <Ionicons name="arrow-back" size={24} color="#1f2937" />
          </TouchableOpacity>
          <Text style={styles.title}>Datos de los Participantes</Text>
          <Text style={styles.subtitle}>
            Ingresa la información de cada participante
          </Text>
        </View>

        <View style={styles.content}>
          <View style={styles.activityInfo}>
            <Text style={styles.activityInfoTitle}>
              Actividad: {activity.name}
            </Text>
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

          <View style={styles.counterSection}>
            <Text style={styles.counterLabel}>Cantidad de participantes</Text>
            <Text style={styles.counterSubLabel}>
              Cupos disponibles: {maxParticipants}
            </Text>
            <View style={styles.counter}>
              <TouchableOpacity
                style={styles.counterButton}
                onPress={handleDecrement}
                disabled={participantCount === 1}
              >
                <Ionicons
                  name="remove"
                  size={24}
                  color={participantCount === 1 ? "#d1d5db" : "#4b5563"}
                />
              </TouchableOpacity>
              <Text style={styles.counterValue}>{participantCount}</Text>
              <TouchableOpacity
                style={styles.counterButton}
                onPress={handleIncrement}
                disabled={participantCount >= maxParticipants}
              >
                <Ionicons
                  name="add"
                  size={24}
                  color={
                    participantCount >= maxParticipants ? "#d1d5db" : "#4b5563"
                  }
                />
              </TouchableOpacity>
            </View>
          </View>

          {participants.map((participant, index) => (
            <View key={index} style={styles.participantCard}>
              <Text style={styles.participantTitle}>
                Participante {index + 1}
              </Text>

              <View style={styles.inputGroup}>
                <Text style={styles.label}>
                  Nombre completo <Text style={styles.required}>*</Text>
                </Text>
                <TextInput
                  style={[
                    styles.input,
                    errors[index]?.fullName && styles.inputError,
                  ]}
                  placeholder="Juan Pérez"
                  placeholderTextColor="#9ca3af"
                  value={participant.fullName}
                  onChangeText={(value) =>
                    handleFieldChange(index, "fullName", value)
                  }
                  onBlur={() => handleFieldBlur(index, "fullName")}
                />
                {errors[index]?.fullName && (
                  <Text style={styles.errorText}>{errors[index].fullName}</Text>
                )}
              </View>

              <View style={styles.inputGroup}>
                <Text style={styles.label}>
                  DNI <Text style={styles.required}>*</Text>
                </Text>
                <TextInput
                  style={[
                    styles.input,
                    errors[index]?.dni && styles.inputError,
                  ]}
                  placeholder="12345678"
                  placeholderTextColor="#9ca3af"
                  keyboardType="numeric"
                  value={participant.dni}
                  onChangeText={(value) =>
                    handleFieldChange(index, "dni", value)
                  }
                  onBlur={() => handleFieldBlur(index, "dni")}
                  maxLength={8}
                />
                {errors[index]?.dni && (
                  <Text style={styles.errorText}>{errors[index].dni}</Text>
                )}
              </View>

              <View style={styles.inputGroup}>
                <Text style={styles.label}>
                  Edad <Text style={styles.required}>*</Text>
                </Text>
                <TextInput
                  style={[
                    styles.input,
                    errors[index]?.age && styles.inputError,
                  ]}
                  placeholder="25"
                  placeholderTextColor="#9ca3af"
                  keyboardType="numeric"
                  value={participant.age}
                  onChangeText={(value) =>
                    handleFieldChange(index, "age", value)
                  }
                  onBlur={() => handleFieldBlur(index, "age")}
                  maxLength={3}
                />
                {errors[index]?.age && (
                  <Text style={styles.errorText}>{errors[index].age}</Text>
                )}
              </View>

              {activity.requiresSize && (
                <View style={styles.inputGroup}>
                  <Text style={styles.label}>
                    Talla de vestimenta <Text style={styles.required}>*</Text>
                  </Text>
                  <View
                    style={[
                      styles.pickerContainer,
                      errors[index]?.clothingSize && styles.inputError,
                    ]}
                  >
                    <Picker
                      selectedValue={participant.clothingSize}
                      onValueChange={(value) => {
                        // Actualizamos el valor
                        handleFieldChange(index, "clothingSize", value);

                        // Validamos inmediatamente
                        const error = validateField(
                          index,
                          "clothingSize",
                          value
                        );
                        setErrors((prev) => {
                          const newErrors = { ...prev };
                          if (!newErrors[index]) newErrors[index] = {};

                          if (error) {
                            newErrors[index].clothingSize = error;
                          } else {
                            delete newErrors[index].clothingSize;
                            if (Object.keys(newErrors[index]).length === 0)
                              delete newErrors[index];
                          }

                          return newErrors;
                        });
                      }}
                      style={styles.picker}
                      dropdownIconColor="#6b7280"
                    >
                      <Picker.Item
                        label="Seleccionar talla"
                        value=""
                        color="#9ca3af"
                      />
                      {clothingSizes.map((size) => (
                        <Picker.Item
                          key={size}
                          label={size}
                          value={size}
                          color="#1f2937"
                        />
                      ))}
                    </Picker>
                  </View>
                  {errors[index]?.clothingSize && (
                    <Text style={styles.errorText}>
                      {errors[index].clothingSize}
                    </Text>
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
