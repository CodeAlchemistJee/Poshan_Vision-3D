import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function App() {
  const [pendingScans, setPendingScans] = useState(0);

  // Check how many scans are saved offline when the app opens
  useEffect(() => {
    checkOfflineQueue();
  }, []);

  const checkOfflineQueue = async () => {
    try {
      const existingData = await AsyncStorage.getItem('@offline_scans');
      let scans = existingData ? JSON.parse(existingData) : [];
      setPendingScans(scans.length);
    } catch (e) {
      console.log("Error reading data", e);
    }
  };

  // 1. Simulate the camera taking a scan and saving it OFFLINE
  const handleTakeScan = async () => {
    try {
      // Fake data that the AI will eventually generate
      const newScan = {
        id: Date.now().toString(),
        height_cm: 65.4,
        status: "Healthy",
        timestamp: new Date().toISOString()
      };

      // Get existing scans, add the new one, and save back to local storage
      const existingData = await AsyncStorage.getItem('@offline_scans');
      let scans = existingData ? JSON.parse(existingData) : [];
      scans.push(newScan);
      
      await AsyncStorage.setItem('@offline_scans', JSON.stringify(scans));
      
      Alert.alert("Success", "Scan saved locally in offline queue!");
      checkOfflineQueue(); // Update the counter on the screen
      
    } catch (e) {
      Alert.alert("Error", "Failed to save scan");
    }
  };

  // 2. Clear the queue (We will add the Cloud Sync logic here later)
  const handleSyncData = async () => {
    if (pendingScans === 0) {
      Alert.alert("Up to Date", "No offline scans to sync.");
      return;
    }
    
    // For now, just clear the local storage to simulate a successful sync
    await AsyncStorage.removeItem('@offline_scans');
    Alert.alert("Sync Complete", "Data pushed to the cloud!");
    checkOfflineQueue();
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Poshan-Vision 3D</Text>
        <Text style={styles.subtitle}>Anganwadi Worker Portal</Text>
      </View>

      <View style={styles.statusCard}>
        <Text style={styles.statusText}>Offline Scans Pending: {pendingScans}</Text>
      </View>

      <TouchableOpacity style={styles.scanButton} onPress={handleTakeScan}>
        <Text style={styles.scanButtonText}>📸 Take New Scan</Text>
      </TouchableOpacity>

      <TouchableOpacity 
        style={[styles.syncButton, pendingScans === 0 && styles.syncButtonDisabled]} 
        onPress={handleSyncData}
      >
        <Text style={styles.syncButtonText}>☁️ Sync to Cloud</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F0FDF4', // Very light health-tech green
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  header: {
    marginBottom: 50,
    alignItems: 'center',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#166534', // Dark green
  },
  subtitle: {
    fontSize: 16,
    color: '#15803D',
    marginTop: 5,
  },
  statusCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 15,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    marginBottom: 40,
    width: '100%',
    alignItems: 'center',
  },
  statusText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#374151',
  },
  scanButton: {
    backgroundColor: '#22C55E',
    paddingVertical: 18,
    paddingHorizontal: 40,
    borderRadius: 30,
    width: '100%',
    alignItems: 'center',
    marginBottom: 15,
  },
  scanButtonText: {
    color: 'white',
    fontSize: 20,
    fontWeight: 'bold',
  },
  syncButton: {
    backgroundColor: '#10B981',
    paddingVertical: 18,
    paddingHorizontal: 40,
    borderRadius: 30,
    width: '100%',
    alignItems: 'center',
  },
  syncButtonDisabled: {
    backgroundColor: '#A7F3D0',
  },
  syncButtonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
});