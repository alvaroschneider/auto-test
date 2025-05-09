import json
import random
import os
import sys
from cryptography.fernet import Fernet
from datetime import datetime

# 🔐 Clave generada desde encriptar_preguntas.py
CLAVE = b'j4l5iNXVMlA1HKfjLvxDROJ19hEXbP1hZPy-uYjQlW0='

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
            for pregunta, opciones, correctas, seleccionadas in respuestas_incorrectas:
                f.write(f"\n\n\nPregunta: {pregunta}")
                for idx, opcion in enumerate(opciones):
                    f.write(f"\n{chr(65 + idx)}. {opcion}")
                f.write(f"\n\n✅ Respuesta correcta(s): {', '.join(correctas)}")
                f.write(f"\n❌ Tu respuesta: {', '.join(seleccionadas)}")
        else:
            f.write("\n🎉 ¡Todas las respuestas fueron correctas!")

    print(f"\n📝 Resultado guardado en: {nombre_archivo}")

def realizar_test(preguntas, cantidad):
    puntaje = 0
    respuestas_incorrectas = []

    random.shuffle(preguntas)
    preguntas = preguntas[:cantidad]

    for i, pregunta in enumerate(preguntas, start=1):
        limpiar_pantalla()
        print(f"Pregunta {i}:")

        if len(pregunta["respuestas_correctas"]) > 1:
            print("💡 Tiene más de una respuesta correcta.\n")

        print(f"\n{pregunta['pregunta']}")

        opciones = list(enumerate(pregunta["opciones"]))
        random.shuffle(opciones)

        # Mapeo de índice nuevo a letra
        letra_por_indice = {idx: chr(65 + idx) for idx in range(len(opciones))}

        # Determinar las letras correctas luego de mezclar
        correctas_indices = []
        for idx, (original_idx, _) in enumerate(opciones):
            if original_idx in pregunta["respuestas_correctas"]:
                correctas_indices.append(letra_por_indice[idx])

        for idx, (_, opcion) in enumerate(opciones):
            print(f"{letra_por_indice[idx]}. {opcion}")

        # Validar entrada
        while True:
            entrada = input("\nTu respuesta (ej. A o A,C): ").strip().upper()
            seleccionadas = [x.strip() for x in entrada.split(",") if x.strip()]
            if all(sel in letra_por_indice.values() for sel in seleccionadas):
                break
            print("❌ Entrada inválida. Usá letras como A, B, C o A,C.")

        if sorted(seleccionadas) == sorted(correctas_indices):
            print("\n✅ ¡Correcto!")
            puntaje += 1
        else:
            print(f"\n❌ Incorrecto. Respuesta correcta(s): {', '.join(sorted(correctas_indices))}")
            respuestas_incorrectas.append(
                (
                    pregunta["pregunta"],
                    [op[1] for op in opciones],
                    sorted(correctas_indices),
                    sorted(seleccionadas)
                )
            )

        input("\nPresioná Enter para continuar...")

    limpiar_pantalla()
    porcentaje = round((puntaje / cantidad) * 100)
    print(f"🏁 Test finalizado.")
    print(f"✅ Puntaje: {puntaje}/{cantidad} ({porcentaje}%)")

    guardar_log(puntaje, cantidad, respuestas_incorrectas)

    if respuestas_incorrectas:
        print("\n📘 Repaso de respuestas incorrectas:")
        for pregunta, opciones, correctas, seleccionadas in respuestas_incorrectas:
            print(f"\nPregunta: {pregunta}")
            for idx, opcion in enumerate(opciones):
                print(f"{chr(65 + idx)}. {opcion}")
            print(f"✅ Respuesta correcta(s): {', '.join(correctas)}")
            print(f"❌ Tu respuesta: {', '.join(seleccionadas)}")

    return respuestas_incorrectas

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

    respuestas_incorrectas = realizar_test(preguntas, cantidad)

    if respuestas_incorrectas:
        input("\nPresioná Enter para volver a intentar solo las preguntas incorrectas...")
        preguntas_reintento = []
        for pregunta_texto, opciones, _, _ in respuestas_incorrectas:
            for p in preguntas:
                if p["pregunta"] == pregunta_texto:
                    preguntas_reintento.append(p)
                    break
        realizar_test(preguntas_reintento, len(preguntas_reintento))
