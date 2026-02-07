# Save System Documentation

## Overview

The Gen VI Pokémon Game save system implements a binary save file format compatible with Gen VI game mechanics. The save file contains all player progress, Pokémon data, items, and game flags.

## File Structure

Save files use a structured binary format defined in `save_structure.json`. The total save file size is approximately 65KB (0x10000 bytes).

### Major Sections

1. **Player Data** (0x0000 - 0x00FF)
   - Player name, ID, gender
   - Money and coins
   - Current position and map

2. **Party Pokémon** (0x0100 - 0x0FFF)
   - Up to 6 Pokémon in active party
   - Full stats, moves, EVs, IVs
   - Original trainer information

3. **Pokédex** (0x1000 - 0x1FFF)
   - Seen/Owned bitfields for all species
   - Efficient 1-bit-per-species storage

4. **Bag/Inventory** (0x2000 - 0x2FFF)
   - Items categorized by type
   - TM/HM ownership bitfield
   - Berry storage

5. **PC Boxes** (0x3000 - 0x7FFF)
   - 14 boxes, 30 Pokémon each
   - Custom box names
   - Same structure as party Pokémon

6. **Game Statistics** (0x8000 - 0x8FFF)
   - Badges collected
   - Play time tracking
   - Battle statistics
   - Pokémon caught/evolved

7. **Flags** (0x9000 - 0x9FFF)
   - Story progression flags
   - Event completion tracking
   - Defeated trainers
   - Collected items

8. **Options** (0xA000 - 0xAFFF)
   - Game settings (text speed, battle style, etc.)
   - Audio preferences
   - Control scheme

9. **Checksum** (0xFFFC - 0xFFFF)
   - CRC32 validation for data integrity

## Data Types

### Primitive Types
- `uint8`: 1-byte unsigned integer (0-255)
- `uint16`: 2-byte unsigned integer (0-65535)
- `uint32`: 4-byte unsigned integer (0-4294967295)
- `bool`: 1-byte boolean (0=false, 1=true)
- `string`: Variable-length text, null-terminated
- `bitfield`: Packed bits for efficient flag storage

### Complex Types
- Arrays: Fixed-size collections of elements
- Structures: Nested data with multiple fields

## Pokémon Storage Format

Each Pokémon uses 100 bytes (0x64) and contains:

```
Offset | Size | Field
-------|------|------
0x00   | 2    | Species ID
0x02   | 2    | Held Item
0x04   | 8    | Moves (4 × 2 bytes)
0x0C   | 4    | PP (4 × 1 byte)
0x10   | 1    | PP Bonuses
0x11   | 1    | Friendship
0x12   | 1    | Level
0x13   | 1    | Pokérus Status
0x14   | 2    | Met Location
0x16   | 1    | Met Level
0x17   | 1    | Met Game
0x18   | 1    | Poké Ball Type
0x20   | 15   | Original Trainer Data
0x30   | 12   | Current Stats
0x3C   | 2    | Current HP
0x3E   | 2    | Max HP
0x40   | 4    | Experience Points
0x44   | 6    | EVs (Effort Values)
0x4A   | 6    | IVs (Individual Values)
0x50   | 1    | Status Condition
0x52   | 10   | Nickname
0x5C   | 1    | Is Egg Flag
```

## Save/Load Implementation

### Saving

```python
import struct
import json

def save_game(filename, player_data, party, boxes, flags):
    with open(filename, 'wb') as f:
        # Write player data
        write_player_data(f, player_data)
        
        # Write party Pokémon
        write_party(f, party)
        
        # Write PC boxes
        write_boxes(f, boxes)
        
        # Write flags and options
        write_flags(f, flags)
        
        # Calculate and write checksum
        checksum = calculate_checksum(f)
        f.seek(0xFFFC)
        f.write(struct.pack('<I', checksum))
```

### Loading

```python
def load_game(filename):
    with open(filename, 'rb') as f:
        # Verify checksum
        if not verify_checksum(f):
            raise ValueError("Save file corrupted")
        
        # Read all sections
        player_data = read_player_data(f)
        party = read_party(f)
        boxes = read_boxes(f)
        flags = read_flags(f)
        
    return player_data, party, boxes, flags
```

## Checksum Validation

The save file uses CRC32 for integrity checking:

```python
import zlib

def calculate_checksum(file_handle):
    file_handle.seek(0)
    data = file_handle.read(0xFFFC)  # Read everything except checksum
    return zlib.crc32(data) & 0xFFFFFFFF

def verify_checksum(file_handle):
    calculated = calculate_checksum(file_handle)
    file_handle.seek(0xFFFC)
    stored = struct.unpack('<I', file_handle.read(4))[0]
    return calculated == stored
```

## Bitfield Management

Flags and Pokédex data use bitfields for efficient storage:

```python
def set_flag(bitfield, flag_id):
    """Set a specific bit to 1"""
    byte_index = flag_id // 8
    bit_index = flag_id % 8
    bitfield[byte_index] |= (1 << bit_index)

def get_flag(bitfield, flag_id):
    """Get the value of a specific bit"""
    byte_index = flag_id // 8
    bit_index = flag_id % 8
    return bool(bitfield[byte_index] & (1 << bit_index))

def clear_flag(bitfield, flag_id):
    """Clear a specific bit to 0"""
    byte_index = flag_id // 8
    bit_index = flag_id % 8
    bitfield[byte_index] &= ~(1 << bit_index)
```

## Backup and Recovery

The game maintains multiple save slots:

1. **Primary Save** (`save1.sav`)
2. **Backup Save** (`save2.sav`)
3. **Auto-save** (`autosave.sav`)

When saving:
1. Write to temporary file
2. Verify checksum
3. Copy primary to backup
4. Move temporary to primary

This prevents data loss if saving is interrupted.

## Platform-Specific Notes

### Big Endian vs Little Endian

The save format uses **little-endian** byte order. When porting to big-endian platforms:

```python
import sys

def write_uint16(f, value):
    if sys.byteorder == 'big':
        value = ((value & 0xFF) << 8) | ((value >> 8) & 0xFF)
    f.write(struct.pack('<H', value))
```

### Save Location

Default save locations by platform:
- **Windows**: `%APPDATA%/GenVIPokemon/save/`
- **macOS**: `~/Library/Application Support/GenVIPokemon/`
- **Linux**: `~/.local/share/genvipokemon/`
- **PS Vita**: `ux0:data/genvipokemon/`
- **Unity**: `Application.persistentDataPath`

## Security Considerations

1. **Checksum**: Detects accidental corruption
2. **Validation**: Check value ranges on load
3. **Sanitization**: Ensure strings are null-terminated
4. **Backup**: Multiple save slots prevent data loss

⚠️ **Note**: This system does NOT provide encryption or cheat protection. For competitive play, implement additional security measures.

## Migration and Compatibility

When updating the save format:

1. Increment `save_format_version`
2. Implement migration function
3. Keep backward compatibility for one version

```python
def migrate_save(old_data, old_version, new_version):
    if old_version == "0.9" and new_version == "1.0":
        # Add new fields with defaults
        old_data["new_field"] = default_value
    return old_data
```

## Testing Save System

```python
def test_save_load():
    # Create test data
    player = create_test_player()
    party = create_test_party()
    
    # Save
    save_game("test.sav", player, party, [], {})
    
    # Load
    loaded_player, loaded_party, _, _ = load_game("test.sav")
    
    # Verify
    assert player == loaded_player
    assert party == loaded_party
    print("Save/load test passed!")
```

## Performance

- **Save time**: ~50ms for full save
- **Load time**: ~100ms for full save
- **Memory**: ~1MB runtime, 65KB disk
- **Autosave**: Every 5 minutes or major event

## Troubleshooting

### Common Issues

1. **Corrupted Save**
   - Check checksum
   - Restore from backup
   - Check disk space

2. **Invalid Data**
   - Validate ranges after loading
   - Sanitize user-provided values
   - Check for null pointers

3. **Performance Issues**
   - Use memory-mapped files for large saves
   - Cache frequently accessed data
   - Defer saving non-critical data

## Future Enhancements

- Cloud save synchronization
- Compressed save format
- Delta encoding for efficient updates
- Cross-platform save file compatibility
- Save file encryption (optional)
