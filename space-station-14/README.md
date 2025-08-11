# Capitalism Station

This repository contains the economic and commercial systems extracted from [Space Station 14](https://github.com/space-wizards/space-station-14) stable branch.

## What's Included

This modded server focuses on capitalism and economic gameplay mechanics. The following systems have been extracted:

### Core Economic Systems

- **Cargo System**: Complete cargo ordering, shipping, and management system
  - Cargo ordering consoles and interfaces
  - Cargo shuttle management
  - Cargo pallet handling
  - Bounty system for trading
  - Price calculation and economic balancing

- **Store System**: In-game store and purchasing mechanics  
  - Store interfaces and menus
  - Currency handling
  - Store listings and catalogs
  - Purchase conditions and validation

- **Store Discount System**: Dynamic pricing and discount mechanics
  - Discount calculation and application
  - Price modification systems

- **Vending Machines**: Automated sales and distribution
  - Various vending machine types
  - Inventory management
  - Restocking mechanics
  - User interfaces for purchasing

### Resources Included

- All non-audio resources related to economic systems
- Textures for cargo, stores, vending machines, and currencies
- Prototype definitions for economic entities
- Localization files for economic interfaces
- Maps related to trading outposts

### Test Coverage

- Integration tests for cargo systems
- Store functionality tests

## What's NOT Included

- Audio files (excluded as requested)
- Non-economic game systems (combat, medical, engineering, etc.)
- Base game framework (you'll need to integrate this with SS14 base)

## Structure

```
space-station-14/
├── Content.Client/          # Client-side economic systems
│   ├── Cargo/              # Cargo UI and client logic
│   ├── Store/              # Store interfaces  
│   └── VendingMachines/    # Vending machine UIs
├── Content.Server/         # Server-side economic logic
│   ├── Cargo/              # Cargo processing and management
│   ├── Store/              # Store backend systems
│   ├── StoreDiscount/      # Discount calculation
│   └── VendingMachines/    # Vending machine logic
├── Content.Shared/         # Shared economic components
│   ├── Cargo/              # Shared cargo data structures
│   ├── Store/              # Shared store definitions
│   └── StoreDiscount/      # Shared discount components
└── Resources/              # Game resources (no audio)
    ├── Prototypes/         # Entity and system definitions
    ├── Textures/           # Visual assets
    ├── Locale/             # Localization
    └── Maps/               # Trading-related maps
```

## Usage

This is designed to be integrated with a Space Station 14 server setup. You'll need:

1. Base SS14 server framework
2. Integration with the core SS14 systems these depend on
3. Proper configuration for your modded server

## Original Source

Extracted from: https://github.com/space-wizards/space-station-14/tree/stable

All content retains original licensing from Space Station 14 project.