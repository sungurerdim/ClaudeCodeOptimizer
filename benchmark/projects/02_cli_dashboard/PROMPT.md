# Project: System Monitor TUI Dashboard

Build a terminal-based system monitoring dashboard using Python and Textual.

## Requirements

### Core Features
1. **Real-time System Stats**
   - CPU usage per core (bar charts)
   - Memory usage (used/available/cached)
   - Disk usage for each mount point
   - Network I/O (bytes sent/received per second)

2. **Process List**
   - Sortable table: PID, Name, CPU%, MEM%, Status
   - Filter by name (search box)
   - Kill process by selecting + pressing 'k'
   - Refresh every 2 seconds

3. **Resource History**
   - CPU history graph (last 60 seconds)
   - Memory history graph (last 60 seconds)
   - Sparkline visualization

4. **Alerts Panel**
   - Show warnings when CPU > 80% for 10+ seconds
   - Show warnings when Memory > 90%
   - Show warnings when Disk > 95%
   - Alert history with timestamps

5. **Configuration**
   - YAML config file for thresholds
   - Config hot-reload (watch file changes)
   - Custom refresh intervals per widget

### Technical Requirements
- Textual for TUI framework
- psutil for system metrics
- YAML for configuration
- Async architecture for non-blocking updates
- Graceful shutdown (Ctrl+C)
- Cross-platform (Linux, macOS, Windows)
- Tests with pytest

### Project Structure
```
sysmon/
├── src/
│   ├── main.py           # Entry point
│   ├── app.py            # Textual app
│   ├── config.py         # Configuration
│   ├── collectors/       # Metric collectors
│   │   ├── cpu.py
│   │   ├── memory.py
│   │   ├── disk.py
│   │   └── network.py
│   ├── widgets/          # Custom widgets
│   │   ├── cpu_widget.py
│   │   ├── process_table.py
│   │   ├── alerts.py
│   │   └── sparkline.py
│   └── utils/
├── tests/
├── config.yaml
└── pyproject.toml
```

### Keyboard Shortcuts
```
q       - Quit
r       - Force refresh
k       - Kill selected process
/       - Search processes
Tab     - Switch focus between panels
1-4     - Quick jump to panels
?       - Help
```

## Success Criteria
- Smooth 60fps rendering
- CPU usage of monitor itself < 5%
- All metrics update correctly
- Process kill works with confirmation
- Alerts fire and display properly
- Config changes apply without restart
