# 🐧 LynaOS

**LynaOS** es un sistema operativo experimental basado en Linux y diseñado para ejecutarse en **Termux**.

Actualmente se encuentra en desarrollo activo. El objetivo es construir un entorno operativo propio, modular y ligero, con sus propias aplicaciones, shell y herramientas de sistema.

## 🚀 LynaOS 0.4

**Estado:** Stable  
**Versión:** 0.4
**Licencia:** MIT  
**Plataforma:** Termux / Android

LynaOS 0.4 es la cuarta versión pública del proyecto.

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
- Cómo instalar desde una instalación nueva:
Si todavía no tienes LynaOS:
cd ~/LynaOS-Installer
./installer.sh
Seleccionas Instalar LynaOS, y después:
cd ~/LynaOS
./boot.sh
🛠️ Si boot.sh no tiene permisos
Puedes solucionarlo con:
chmod +x ~/LynaOS/boot.sh
Y volver a ejecutar:
~/LynaOS/boot.sh

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
