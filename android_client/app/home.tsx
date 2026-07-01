import AsyncStorage from "@react-native-async-storage/async-storage";
import { useEffect, useState } from "react";
import { Text, View } from "react-native";

export default function Home() {
  const [loggedUser, setLoggedUser] = useState<any>(null);

  useEffect(() => {
    const loadUser = async () => {
      const data = await AsyncStorage.getItem("loggedUser");

      if (data) {
        setLoggedUser(JSON.parse(data));
      }
    };

    loadUser();
  }, []);

  return (
    <View style={{ flex: 1, justifyContent: "center", padding: 20 }}>
      <Text style={{ fontSize: 28, marginBottom: 20 }}>
        {loggedUser?.username || "Loading..."}
      </Text>

      <Text style={{ fontSize: 20 }}>
        Weight: {loggedUser?.dailyPlan?.weight ?? "N/A"}
      </Text>

      <Text style={{ fontSize: 20 }}>
        Waist: {loggedUser?.dailyPlan?.waist ?? "N/A"}
      </Text>

      <Text style={{ fontSize: 20 }}>
        Thighs: {loggedUser?.dailyPlan?.thighs ?? "N/A"}
      </Text>
    </View>
  );
}