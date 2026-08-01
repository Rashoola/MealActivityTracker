import AsyncStorage from "@react-native-async-storage/async-storage";
import { useRouter } from "expo-router";
import { useState } from "react";
import { Alert, Button, Text, TextInput, View } from "react-native";

export default function Login() {
  const router = useRouter();

  const [user, setUser] = useState(null);

  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    // Replace with your computer's IP address
    const url = "http://192.168.0.17:8000/api/users/login/";

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          identifier,
          password,
        }),
      });

      if (!response.ok) {
        Alert.alert("Login failed", "Check your username and password.");
        return;
      }

      const data = await response.json();

      console.log("Logged in user:", data);

      await AsyncStorage.setItem(
        "loggedUser",
        JSON.stringify(data)
      );

      Alert.alert("Success", "Logged in successfully.");

      generateDailyPlan(data);

      router.push("/home");
    } catch (error) {
      console.error(error);
      Alert.alert(
        "Connection Error",
        "Could not connect to the server."
      );
    }
  };

  const generateDailyPlan = async (loggedUser: any) => {
  if (loggedUser.daily_plan_generated) {
    console.log("Daily plan already generated.");
    return;
  }

  const url = `http://192.168.0.17:8000/api/users/${loggedUser.id}/generate-daily-plan/`;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const errorData = await response.text();
      console.error("Generate plan error:", errorData);
      Alert.alert("Error", "Could not generate daily plan.");
      return;
    }

    const data = await response.json();

    console.log("Generated daily plan:", data);

    // Update stored user so it doesn't generate again
    const updatedUser = {
      ...loggedUser,
      daily_plan_generated: true,
    };

    await AsyncStorage.setItem(
      "loggedUser",
      JSON.stringify(updatedUser)
    );

  } catch (error) {
    console.error(error);
    Alert.alert(
      "Connection Error",
      "Could not connect to the server."
    );
  }
};

  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        padding: 20,
      }}
    >
      <Text
        style={{
          fontSize: 28,
          marginBottom: 20,
        }}
      >
        Login
      </Text>

      <TextInput
        placeholder="Username"
        value={identifier}
        onChangeText={setIdentifier}
        autoCapitalize="none"
        style={{
          borderWidth: 1,
          padding: 10,
          marginBottom: 10,
          borderRadius: 5,
        }}
      />

      <TextInput
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
        style={{
          borderWidth: 1,
          padding: 10,
          marginBottom: 20,
          borderRadius: 5,
        }}
      />

      <Button title="Login" onPress={handleLogin} />
    </View>
  );
}