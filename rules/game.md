# Game Development
*Game engine and development rules*

## Base Rules (Game:Base)
**Trigger:** {game_engine_markers}

- **Frame-Budget**: 16ms (60fps) or 8ms (120fps) target
- **Asset-LOD**: Level of detail + streaming
- **Save-Versioned**: Migration support for old saves
- **Determinism**: Fixed timestep for multiplayer/replay
- **Input-System**: Input actions, rebindable keys
- **Object-Pool**: Reuse frequently spawned objects

## Unity (Game:Unity)
**Trigger:** {unity_markers}

- **Prefab-Usage**: Use prefabs for reusable objects, avoid scene-only objects
- **ScriptableObjects**: Use ScriptableObjects for data containers and configuration
- **Assembly-Definition**: Split code into assemblies for faster compilation
- **Addressables**: Use Addressables for asset management (not Resources.Load)
- **ECS-Performance**: Use ECS/DOTS for performance-critical systems
- **IL2CPP**: Use IL2CPP for production builds (better performance)
- **UI-Toolkit**: Use UI Toolkit for runtime UI, UGUI for legacy support
- **Input-System**: Use new Input System, not legacy Input.GetKey
- **Async-UniTask**: Use UniTask for async/await (faster than coroutines)
- **Serialization**: [SerializeField] for private fields, avoid public fields

## Unreal (Game:Unreal)
**Trigger:** {unreal_markers}

- **Blueprint-Cpp-Balance**: Gameplay logic in Blueprint, performance in C++
- **UPROPERTY-Always**: All reflected properties use UPROPERTY macro
- **GC-Aware**: Use TWeakObjectPtr for non-owning references to avoid GC issues
- **Asset-Soft-Refs**: Use soft references for large assets to avoid memory bloat
- **Data-Assets**: Use Data Assets for configuration, not hardcoded values
- **Enhanced-Input**: Use Enhanced Input System, not legacy input
- **Niagara**: Use Niagara for particles (not Cascade)
- **Common-UI**: Use Common UI for cross-platform UI
- **Live-Coding**: Enable Live Coding for faster iteration
- **Gameplay-Abilities**: Use Gameplay Ability System for complex abilities

## Godot (Game:Godot)
**Trigger:** {godot_markers}

- **Scene-Composition**: Composition over inheritance via scene instancing
- **Signal-Decoupling**: Use signals for loose coupling between nodes
- **Autoload-Minimal**: Minimal autoloads, prefer dependency injection
- **Resource-Custom**: Custom resources for data (not dictionaries)
- **Export-Vars**: Use @export for inspector-editable variables
- **Typed-GDScript**: Use static typing for performance and IDE support
- **Node-Groups**: Use groups for batch operations
- **Scene-Unique**: Use %NodeName for scene-unique node access
- **Tween-Animation**: Use Tweens for procedural animation
- **Physics-Layers**: Configure collision layers/masks properly
