import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { SchedulesProvider } from "../contexts/SchedulesContext";
import FontProvider from "./FontProvider";

export default function RootLayout() {
  return (
    <FontProvider>
      <SchedulesProvider>
        <StatusBar style="dark" />
        <Stack screenOptions={{ headerShown: false }}>
          <Stack.Screen name="index" />
          <Stack.Screen name="[activityId]/schedule" />
          <Stack.Screen name="[activityId]/participants" />
          <Stack.Screen name="[activityId]/confirmation" />
        </Stack>
      </SchedulesProvider>
    </FontProvider>
  );
}
