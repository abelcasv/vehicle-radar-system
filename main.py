import cv2
from utils import *

# ************************************************************
# CONFIGURACIÓN

VIDEO_PATH = "trafico.mp4"

min_area = 2800
max_dist = 120
limite_deteccion = 5

linea_y1 = 400
linea_y2 = 900
linea_conteo = 550


def main():
    # Inicialización de vídeo y estructuras
    video = cv2.VideoCapture(VIDEO_PATH)

    fondo = cv2.createBackgroundSubtractorMOG2(
        history=500,
        varThreshold=40,
        detectShadows=False
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    coches = []
    contador_coches = 0
    id_counter = 1

    # ************************************************************
    # BUCLE PRINCIPAL

    while True:
        ret, frame = video.read()
        if not ret:
            break

        fgmask = obtener_mascara(frame, fondo, kernel)
        contours, _ = cv2.findContours(
            fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        coches_visibles = []

        for cnt in contours:
            if cv2.contourArea(cnt) < min_area:
                continue

            x, y, w, h = cv2.boundingRect(cnt)
            centro = (x + w/2, y + h/2)

            # Zona de interés
            if not (linea_y1 < centro[1] < linea_y2):
                continue

            contador_coches, id_counter = procesar_deteccion(
                centro,
                (x, y, w, h),
                coches,
                coches_visibles,
                linea_conteo,
                contador_coches,
                id_counter,
                max_dist
            )

        coches = filtrar_coches(coches, coches_visibles, limite_deteccion)
        dibujar(frame, coches_visibles, linea_conteo, contador_coches)

        cv2.imshow("Conteo de coches", frame)
        if cv2.waitKey(2) & 0xFF == 27:
            break

    # ************************************************************
    # LIMPIEZA

    video.release()
    cv2.destroyAllWindows()
    print(f"Total coches: {contador_coches}")


if __name__ == "__main__":
    main()