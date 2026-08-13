#!/data/data/com.termux/files/usr/bin/bash

usuario=${1:-dev}

while true
do
clear
echo "================================"
echo "            LynaOS"
echo "================================"
echo
echo "Usuario: $usuario"
echo
echo "1) Aplicaciones"
echo "2) Información del sistema"
echo "3) Limpiar pantalla"
echo "4) Reiniciar"
echo "5) Apagar"
echo
read -p "Selecciona una opción: " opcion

case $opcion in

1)
while true
do
clear
echo "================================"
echo "      LynaOS Application Hub"
echo "================================"
echo
echo "1) Files"
echo "2) Editor"
echo "3) Monitor"
echo "4) Settings"
echo "5) Calculator"
echo "6) Calendar"
echo "7) Clock"
echo "8) Store"
echo "9) System Info"
echo "10) Compiler"
echo
echo "0) Volver"
echo

read -p "Selecciona una aplicación: " app

case $app in

1)
while true
do
clear
echo "========== FILES =========="
echo
pwd
echo
ls -lah
echo
echo "0) Volver"
read -p "> " op
[ "$op" = "0" ] && break
done
;;

2)
clear
echo "========== EDITOR =========="
echo
read -p "Archivo: " archivo
nano "$archivo"
;;

3)
top
;;

4)
clear
echo "========== SETTINGS =========="
echo
echo "Sistema: LynaOS"
echo "Versión: 1.0"
echo "Tema: Green"
echo "Shell: LynaShell"
echo
read -p "Enter para volver..."
;;

5)
clear
echo "========== CALCULATOR =========="
echo
read -p "Operación: " op
echo
echo "$op" | bc
echo
read -p "Enter para volver..."
;;

6)
clear
echo "========== CALENDAR =========="
echo
cal
echo
read -p "Enter para volver..."
;;

7)
while true
do
clear
echo "========== CLOCK =========="
echo
date
echo
echo "Ctrl+C para salir"
sleep 1
done
;;

8)
while true
do
clear
echo "========== STORE =========="
echo
echo "1) Actualizar sistema"
echo "2) Instalar paquete"
echo "3) Buscar paquete"
echo "0) Volver"
echo

read -p "> " op

case $op in
1)
pkg update && pkg upgrade
;;
2)
read -p "Paquete: " p
pkg install "$p"
;;
3)
read -p "Buscar: " p
pkg search "$p"
;;
0)
break
;;
esac
done
;;

9)
clear
echo "========== SYSTEM INFO =========="
echo
echo "Sistema : LynaOS"
echo "Versión : 1.0"
echo "Usuario : $usuario"
echo "Fecha   : $(date)"
echo "Base    : Termux"
echo "Shell   : Bash"
echo
read -p "Enter para volver..."
;;

10)

clear

echo "Preparando entorno de compilación..."

command -v python >/dev/null 2>&1 || pkg install -y python
command -v gcc >/dev/null 2>&1 || pkg install -y clang

while true
do

clear

echo "========== COMPILER =========="
echo
echo "1) Bash"
echo "2) Python"
echo "3) C"
echo "4) C++"
echo
echo "0) Volver"
echo

read -p "> " lang

case $lang in

1)
clear
read -p "Archivo Bash: " archivo
bash "$archivo"
echo
read -p "Enter para continuar..."
;;

2)
clear
read -p "Archivo Python: " archivo
python "$archivo"
echo
read -p "Enter para continuar..."
;;

3)
clear
read -p "Archivo C: " archivo

salida=$(basename "$archivo" .c)

gcc "$archivo" -o "$salida"

if [ $? -eq 0 ]
then
echo
echo "Compilación exitosa."
echo
./"$salida"
fi

echo
read -p "Enter para continuar..."
;;

4)
clear
read -p "Archivo C++: " archivo

salida=$(basename "$archivo" .cpp)

g++ "$archivo" -o "$salida"

if [ $? -eq 0 ]
then
echo
echo "Compilación exitosa."
echo
./"$salida"
fi

echo
read -p "Enter para continuar..."
;;

0)
break
;;

*)
echo "Opción inválida"
sleep 1
;;

esac

done
;;

0)
break
;;

*)
echo "Opción inválida"
sleep 1
;;

esac
done
;;

2)
clear
echo "Sistema : LynaOS"
echo "Versión : 1.0"
echo "Usuario : $usuario"
echo
read -p "Enter para volver..."
;;

3)
clear
;;

4)
echo "Reiniciando..."
sleep 1
exec "$0" "$usuario"
;;

5)
echo "Apagando LynaOS..."
sleep 1
exit
;;

*)
echo "Opción inválida"
sleep 1
;;

esac

done
