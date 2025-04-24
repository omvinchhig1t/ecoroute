// EcoFriendlyRouteFinder.tsx
import React, { useState, useEffect } from "react";
import {
  View,
  TextInput,
  Button,
  StyleSheet,
  Alert,
  Linking,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Text,
} from "react-native";
import * as Location from "expo-location";

const BACKEND_URL = "https://ecofriendlyrouteproject.onrender.com";

const testBackend = async () => {
  try {
    const response = await fetch(`${BACKEND_URL}/ping`);
    const data = await response.text();
    Alert.alert("Backend Response", data);
  } catch (error) {
    Alert.alert("Error", "Failed to reach backend");
    console.error(error);
  }
};

const EcoFriendlyRouteFinder = () => {
  const [source, setSource] = useState("");
  const [destination, setDestination] = useState("");
  const [locationGranted, setLocationGranted] = useState(false);

  useEffect(() => {
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      setLocationGranted(status === "granted");
    })();
  }, []);

  const useCurrentLocationAsSource = async () => {
    if (!locationGranted) {
      Alert.alert("Permission Denied", "Location permission not granted.");
      return;
    }

    const location = await Location.getCurrentPositionAsync({});
    const { latitude, longitude } = location.coords;
    setSource(`${latitude},${longitude}`);
  };

  const openMap = async (mode: "eco" | "shortest") => {
    if (!source || !destination) {
      Alert.alert("Error", "Please enter both source and destination.");
      return;
    }

    const mapUrl = `${BACKEND_URL}/show_map?source=${encodeURIComponent(
      source
    )}&destination=${encodeURIComponent(destination)}&mode=${mode}`;

    const supported = await Linking.canOpenURL(mapUrl);
    supported ? Linking.openURL(mapUrl) : Alert.alert("Error", "Can't open map.");
  };

  return (
    <KeyboardAvoidingView
      style={{ flex: 1 }}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <ScrollView contentContainerStyle={styles.container}>
        <Text style={styles.title}>Eco-Friendly Route Finder</Text>

        <TextInput
          style={styles.input}
          placeholder="Enter Source (or use GPS)"
          placeholderTextColor="#666"
          value={source}
          onChangeText={setSource}
        />
        <Button title="Use Current Location" onPress={useCurrentLocationAsSource} />

        <TextInput
          style={styles.input}
          placeholder="Enter Destination"
          placeholderTextColor="#666"
          value={destination}
          onChangeText={setDestination}
        />

        <View style={styles.buttonGroup}>
          <Button title="Eco-Friendly Route" onPress={() => openMap("eco")} />
          <View style={{ height: 10 }} />
          <Button title="Shortest Route" onPress={() => openMap("shortest")} />
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
    justifyContent: "center",
    backgroundColor: "#f0f8ff",
    flexGrow: 1,
  },
  title: {
    fontSize: 22,
    marginBottom: 20,
    fontWeight: "bold",
    textAlign: "center",
  },
  input: {
    height: 45,
    borderColor: "#ccc",
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 12,
    backgroundColor: "#fff",
    color: "#000",
    borderRadius: 8,
  },
  buttonGroup: {
    marginTop: 20,
  },
});

export default EcoFriendlyRouteFinder;
