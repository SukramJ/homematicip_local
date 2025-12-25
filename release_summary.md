# Version 1.90.2 -

## What's Changed

### New Features

- **HmIP-WRCD Text Display**: Full support for the wall-mount remote control with display via NotifyEntity, including services for sending text with icons, colors, sounds, and alignment options
- **HmIP-MP3P Sound Player**: Full support for the combination signalling device with services for sound playback (play_sound, stop_sound) and LED control (set_sound_led) with colors, brightness, and timing options
- **Siren Control**: Automatic select entities for siren tone and light pattern selection with full translations (no manual InputHelper setup required)
- **Reauthentication**: Added reauthentication flow to update expired credentials without removing the integration
- **Reconfigure Flow**: Quick reconfiguration of connection settings without full re-setup
- **Air Quality Sensors**: New entity descriptions for DIRT_LEVEL and SMOKE_LEVEL sensors

### Improvements

- **Configuration Experience**: Enhanced config flow with improved error messages, progress indicators (Step X of Y), and menu-based navigation
- **Error Handling**: Reduced log flooding during connection issues with improved error handling decorator for entity actions
- **Translations**: Fixed naming of untranslated entities and improved translation coverage for press events

### Bug Fixes

- **Services**: Fixed `set_schedule_simple_weekday` service
- **Translations**: Fixed translation issues

### Developer Experience

- **Code Quality**: Strict mypy type checking, consistent use of keyword-only arguments, removed legacy code from config flow
- **Testing**: Comprehensive test coverage improvements for config flow, services, lights, and updates
- **Documentation**: Added comprehensive CLAUDE.md for AI assistants with development guidelines and project structure
