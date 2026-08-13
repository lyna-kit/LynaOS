# 🐧 LynaOS

**LynaOS** es un sistema operativo experimental basado en Linux y diseñado para ejecutarse en **Termux**.

Actualmente se encuentra en desarrollo activo. El objetivo es construir un entorno operativo propio, modular y ligero, con sus propias aplicaciones, shell y herramientas de sistema.

## 🚀 LynaOS 0.2

**Estado:** Development  
**Versión:** 0.2  
**Licencia:** MIT  
**Plataforma:** Termux / Android

LynaOS 0.2 es la primera versión pública del proyecto.

### Características

- 🖥️ Sistema base de LynaOS
- 🐚 LynaBash
- 📁 Gestor de archivos — LynaFiles
- 🧮 Calculadora — LynaCalc
- ⚙️ Ajustes — LynaSettings
- 📦 Tienda de aplicaciones — LynaStore
- 🎵 Reproductor de música — LynaFM
- 🌐 Navegador de texto — Shelly
- 🔧 Sistema de arranque
- 🧠 Componentes experimentales de kernel
- 👤 Sistema de usuarios
- 📋 Sistema de versiones y builds
- 🔄 Sistema inicial de actualización

## 📂 Estructura

```text
LynaOS/
├── apps/
│   ├── lynacalc/
│   ├── lynafiles/
│   ├── lynafm/
│   ├── lynasettings/
│   ├── lynastore/
│   └── shelly/
│
├── boot/
│   ├── init.sh
│   ├── services.sh
│   └── startup.sh
│
├── etc/
│   └── lyna.conf
│
├── kernel/
│   ├── kernel.sh
│   ├── memory.sh
│   └── process.sh
│
├── shell/
│   └── lynashell.sh
│
├── system/
│   ├── build.py
│   ├── changelog.json
│   ├── login.sh
│   ├── update.py
│   └── version.py
│
├── boot.sh
├── lynaapps.py
└── lynaos.py
