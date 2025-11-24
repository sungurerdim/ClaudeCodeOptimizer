---
name: mobile-development
description: Build offline-first mobile apps with cache-first data layer, battery-efficient location and networking, app store compliance (iOS ATT, Android runtime permissions), and FlatList virtualization
keywords: [mobile, offline-first, battery optimization, app store, iOS, Android, ATT, AsyncStorage, FlatList, React Native]
category: performance
related_commands:
  action_types: [audit, fix, optimize]
  categories: [performance]
pain_points: [1, 6, 11]
---

# Skill: Mobile Development
**Domain**: iOS/Android
**Purpose**: Build offline-first mobile apps with battery optimization and app store compliance for reliable, performant mobile experiences.

> **Standards:** Format defined in [STANDARDS_SKILLS.md](../STANDARDS_SKILLS.md)  
> **Discovery:** See [STANDARDS_COMMANDS.md](../STANDARDS_COMMANDS.md#18-command-discovery-protocol)


## Core Techniques
- **Offline-First**: Cache data locally, sync when connected, queue operations
- **Battery Optimization**: Batch network requests, coarse location, limit background tasks
- **App Store Compliance**: ATT permissions (iOS), runtime permissions (Android), privacy labels
- **Performance**: FlatList virtualization, memoization, native modules for heavy tasks

## Patterns

### ✅ Good: Offline-First Data Layer
```javascript
class OfflineDataManager {
  async getData(key) {
    const cached = await AsyncStorage.getItem(key);
    if (cached) return JSON.parse(cached);

    const isOnline = await NetInfo.fetch().then(s => s.isConnected);
    if (isOnline) {
      const data = await fetch(`/api/${key}`).then(r => r.json());
      await AsyncStorage.setItem(key, JSON.stringify(data));
      return data;
    }
    throw new Error('Data unavailable offline');
  }

  async saveData(key, data) {
    await AsyncStorage.setItem(key, JSON.stringify(data));
    this.syncQueue.push({ key, data });
    if (await isOnline()) await this.syncPendingOperations();
  }
}
```
**Why**: Cache-first strategy works offline, syncs when connected

### ✅ Good: Battery-Efficient Location
```javascript
navigator.geolocation.watchPosition(callback, error, {
  enableHighAccuracy: false,  // Network/WiFi, not GPS
  distanceFilter: 100,        // Update only if moved 100m
  interval: 60000             // Check every 60s
});
```
**Why**: Coarse location + distance filter reduces battery drain 90%

### ✅ Good: Batch Network Requests
```javascript
setInterval(async () => {
  await fetch('/api/batch', {
    method: 'POST',
    body: JSON.stringify({ updates: pendingUpdates })
  });
  pendingUpdates = [];
}, 30000);  // Every 30s, not 1s
```
**Why**: 30s batching vs 1s polling reduces battery drain 97%

### ✅ Good: iOS ATT Permission
```javascript
import { requestTrackingPermissionsAsync } from 'expo-tracking-transparency';

const { status } = await requestTrackingPermissionsAsync();
if (status === 'granted') {
  // Can use IDFA for ads
}
```
**Why**: Required for iOS 14.5+ if tracking users

### ✅ Good: FlatList Virtualization
```javascript
<FlatList
  data={items}
  renderItem={({ item }) => <ItemComponent item={item} />}
  keyExtractor={item => item.id}
  windowSize={10}
  removeClippedSubviews={true}
  getItemLayout={(data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index
  })}
/>
```
**Why**: Virtualizes long lists for 60 FPS scrolling

### ❌ Bad: No Offline Support
```javascript
async function loadData() {
  const data = await fetch('/api/data').then(r => r.json());
  return data;  // Crashes if offline
}
```
**Why**: Network errors crash app without fallback

### ❌ Bad: Continuous High-Accuracy GPS
```javascript
navigator.geolocation.watchPosition(callback, error, {
  enableHighAccuracy: true,
  distanceFilter: 0,
  interval: 1000
});
```
**Why**: Drains battery in 2-3 hours

### ❌ Bad: Missing iOS Permissions
```javascript
// No ATT request before tracking
```
**Why**: App Store rejection

## Checklist
- [ ] Local database (SQLite/Realm) for offline
- [ ] Sync queue for pending operations
- [ ] Network state listener
- [ ] Batch network requests (>30s intervals)
- [ ] Coarse location (enableHighAccuracy: false)
- [ ] Background tasks <30s (iOS limit)
- [ ] FlatList for long lists
- [ ] Memoization (memo, useMemo, useCallback)
- [ ] iOS: ATT permission requested
- [ ] iOS: Sign in with Apple (if third-party auth)
- [ ] Android: Runtime permissions
- [ ] Android: Target API 33+
---

---

