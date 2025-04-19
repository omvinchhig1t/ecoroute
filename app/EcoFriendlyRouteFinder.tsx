import React, { useState } from "react";
import {
  View,
  TextInput,
  Button,
  StyleSheet,
  Alert,
  Linking,
} from "react-native";

const EcoFriendlyRouteFinder = () => {
  const [source, setSource] = useState("");
  const [destination, setDestination] = useState("");

  const BACKEND_URL = "https://ecofriendlyrouteproject.onrender.com"; // 👈 Replace with your IP

  const openMapInBrowser = async () => {
    if (!source || !destination) {
      Alert.alert("Error", "Please enter both source and destination.");
      return;
    }

    const mapUrl = `${BACKEND_URL}/show_map?source=${encodeURIComponent(source)}&destination=${encodeURIComponent(destination)}}`;

    // console.log(mapUrl);
    const supported = await Linking.canOpenURL(mapUrl);

    if (supported) {
      Linking.openURL(mapUrl);
    } else {
      Alert.alert("Error", "Can't open map link.");
    }
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Enter Source (e.g. Mumbai)"
        placeholderTextColor="#666"
        value={source}
        onChangeText={setSource}
      />
      <TextInput
        style={styles.input}
        placeholder="Enter Destination (e.g. Pune)"
        placeholderTextColor="#666"
        value={destination}
        onChangeText={setDestination}
      />
      <Button title="View Eco Route" onPress={openMapInBrowser} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: "center",
    backgroundColor: "#fff",
  },
  input: {
    height: 40,
    borderColor: "gray",
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 10,
    backgroundColor: "#fff",
    color: "#000",
  },
});

export default EcoFriendlyRouteFinder;
