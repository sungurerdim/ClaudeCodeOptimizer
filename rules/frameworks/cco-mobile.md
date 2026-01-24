# Mobile
*Mobile application development rules*

**Trigger:** Flutter/ReactNative/iOS/Android detected

## Base Mobile Rules
- **Offline-Cache**: Offline-first with local storage
- **Deep-Link**: Handle deep links properly
- **Push-Permission**: Request permissions gracefully
- **Battery-Aware**: Minimize battery drain

## Flutter (Mobile:Flutter)
**Trigger:** {flutter_manifest}, {dart_ext}

- **Widget-Const**: Use const constructors
- **State-Provider**: Provider/Riverpod for state
- **Platform-Channel**: Platform channels for native APIs
- **Build-Modes**: Different configs for debug/release

## React Native (Mobile:ReactNative)
**Trigger:** {rn_deps}

- **Native-Modules**: TurboModules/New Architecture for performance
- **Metro-Optimize**: Optimize Metro bundler config
- **Hermes-Enable**: Hermes engine for Android
- **Workflow-Match**: Choose managed (Expo) or bare based on native module needs

## iOS Native (Mobile:iOS)
**Trigger:** {ios_project}, {ios_deps}, {swift_ext}

- **SwiftUI-Modern**: SwiftUI over UIKit when possible
- **Combine-Reactive**: Combine for reactive patterns
- **App-Privacy**: Privacy manifest and descriptions
- **TestFlight-Beta**: TestFlight for beta testing

## Android Native (Mobile:Android)
**Trigger:** {android_build}, {android_manifest}

- **Compose-Modern**: Jetpack Compose over XML layouts
- **ViewModel-State**: ViewModel + StateFlow for state
- **WorkManager-Background**: WorkManager for background work
- **R8-Shrink**: Enable R8 code shrinking

## Kotlin Multiplatform (Mobile:KMP)
**Trigger:** {kmp_config}, {kmp_dirs}

- **Expect-Actual**: Shared expect/actual declarations
- **Ktor-Networking**: Ktor for shared networking
- **SqlDelight-DB**: SqlDelight for shared database
- **KMM-Modules**: Separate shared and platform modules
