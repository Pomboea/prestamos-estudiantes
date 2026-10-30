#!/bin/sh
# Regenera los .accdb desde las bases locales (requiere Java 17+ y los jar de Jackcess en ./lib)
python exportar_definicion.py
CP=lib/jackcess-4.0.8.jar:lib/commons-lang3-3.17.0.jar:lib/commons-logging-1.3.4.jar
javac -cp $CP -d . GenerarAccess.java VerificarAccess.java
java -cp $CP:. GenerarAccess prestamos.def ../prestamos.accdb
java -cp $CP:. GenerarAccess prestamos_aux.def ../prestamos_aux.accdb
java -cp $CP:. VerificarAccess ../prestamos.accdb
python generar_sql_access.py
