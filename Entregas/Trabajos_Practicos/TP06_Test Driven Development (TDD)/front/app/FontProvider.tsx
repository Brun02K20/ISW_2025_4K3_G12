import { Montserrat_400Regular, Montserrat_500Medium, Montserrat_600SemiBold, Montserrat_700Bold } from '@expo-google-fonts/montserrat';
import { useFonts } from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';
import React, { ReactNode, useEffect } from 'react';
import { StyleSheet, Text, TextInput } from 'react-native';

SplashScreen.preventAutoHideAsync();

interface FontProviderProps {
  children: ReactNode;
}

export default function FontProvider({ children }: FontProviderProps) {
  const [fontsLoaded] = useFonts({
    'Montserrat-Regular': Montserrat_400Regular,
    'Montserrat-Medium': Montserrat_500Medium,
    'Montserrat-SemiBold': Montserrat_600SemiBold,
    'Montserrat-Bold': Montserrat_700Bold,
  });

  useEffect(() => {
    if (fontsLoaded) {
      SplashScreen.hideAsync();
      
      // Aplicar fuente por defecto a todos los Text
      const defaultFontFamily = { fontFamily: 'Montserrat-Regular' };
      const oldTextRender = (Text as any).render;
      const oldTextInputRender = (TextInput as any).render;

      // @ts-ignore
      Text.render = function (props: any, ref: any) {
        return oldTextRender.call(this, {
          ...props,
          style: StyleSheet.flatten([defaultFontFamily, props.style]),
        }, ref);
      };

      // @ts-ignore  
      TextInput.render = function (props: any, ref: any) {
        return oldTextInputRender.call(this, {
          ...props,
          style: StyleSheet.flatten([defaultFontFamily, props.style]),
        }, ref);
      };
    }
  }, [fontsLoaded]);

  if (!fontsLoaded) {
    return null;
  }

  return <>{children}</>;
}