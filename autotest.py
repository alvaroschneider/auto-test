import json
import random
import os
import sys
from cryptography.fernet import Fernet
from datetime import datetime

# 🔐 Clave generada desde encriptar_preguntas.py
CLAVE = b'eBe0oSpQ7AilDsT28_VsKced70-8I1fOEMlu63lRIq0='

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_preguntas_encriptadas(path):
    fernet = Fernet(CLAVE)
    with open(path, 'rb') as f:
        datos_encriptados = f.read()
    datos = fernet.decrypt(datos_encriptados).decode()
    return json.loads(datos)

def guardar_log(puntaje, cantidad, respuestas_incorrectas):
    ahora = datetime.now().strftime("%y%m%d_%H%M")
    nombre_archivo = f"log_respuestas_{ahora}.txt"

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(f"AutoTest - Resultado del {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        f.write(f"\nPreguntas respondidas: {cantidad}")
        f.write(f"\nPuntaje: {puntaje}/{cantidad} ({round((puntaje / cantidad) * 100)}%)")

        if respuestas_incorrectas:
            f.write("\n\nPreguntas incorrectas:")
            for pregunta, opciones, correcta in respuestas_incorrectas:
                f.write(f"\n\n\nPregunta: {pregunta}")
                for idx, opcion in enumerate(opciones):
                    f.write(f"\n{chr(65 + idx)}. {opcion}")
                f.write(f"\n\n✅ Respuesta correcta: {correcta}")
        else:
            f.write("\n🎉 ¡Todas las respuestas fueron correctas!")

    # Mostrar mensaje de resultado
    print(f"📝 Resultado guardado en: {nombre_archivo}")

def realizar_test(preguntas, cantidad):
    puntaje = 0
    respuestas_incorrectas = []

    random.shuffle(preguntas)
    preguntas = preguntas[:cantidad]

    # Mostrar preguntas
    for i, pregunta in enumerate(preguntas, start=1):
        limpiar_pantalla()
        print(f"Pregunta {i}:\n\n{pregunta['pregunta']}")

        opciones = list(enumerate(pregunta["opciones"]))
        random.shuffle(opciones)

        for idx, (original_idx, opcion) in enumerate(opciones):
            if original_idx == pregunta["respuesta_correcta"]:
                nueva_respuesta_correcta = idx
            print(f"{chr(65 + idx)}. {opcion}")

        # respuesta = input("\nTu respuesta (A/B/C): ").strip().upper()

        # Validar input hasta que sea A, B o C
        while True:
            respuesta = input("\nTu respuesta (A/B/C): ").strip().upper()
            if respuesta in ['A', 'B', 'C']:
                break
            print("❗ Entrada inválida. Por favor, ingresá A, B o C.")

        if respuesta and ord(respuesta) - 65 == nueva_respuesta_correcta:
            print("\n✅ ¡Correcto!")
            puntaje += 1
        else:
            correcta = opciones[nueva_respuesta_correcta][1]
            print(f"\n❌ Incorrecto. Respuesta correcta: {chr(65 + nueva_respuesta_correcta)}. {correcta}")
            respuestas_incorrectas.append((pregunta["pregunta"], pregunta["opciones"], correcta))

        input("\nPresioná Enter para continuar...")

    limpiar_pantalla()
    porcentaje = round((puntaje / cantidad) * 100)
    print(f"🏁 Test finalizado.")
    print(f"✅ Puntaje: {puntaje}/{cantidad} ({porcentaje}%)")

    guardar_log(puntaje, cantidad, respuestas_incorrectas)

    if respuestas_incorrectas:
        print("\n📘 Repaso de respuestas incorrectas:")
        for pregunta, opciones, correcta in respuestas_incorrectas:
            print(f"\nPregunta: {pregunta}")
            for idx, opcion in enumerate(opciones):
                print(f"{chr(65 + idx)}. {opcion}")
            print(f"✅ Respuesta correcta: {correcta}")

if __name__ == "__main__":
    preguntas = cargar_preguntas_encriptadas("preguntas.enc")
    try:
        cantidad = int(sys.argv[1])
        if cantidad < 1 or cantidad > len(preguntas):
            raise ValueError
    except (IndexError, ValueError):
        cantidad = len(preguntas)
        print(f"ℹ️ Ejecutando con todas las preguntas disponibles ({cantidad}).")
        input("Presioná Enter para comenzar...")

    realizar_test(preguntas, cantidad)