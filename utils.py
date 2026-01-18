"""
Funciones auxiliares para detección, seguimiento y conteo de coches.
Separadas del programa principal para mejorar claridad y reutilización.
"""

import cv2
import math


# ************************************************************
# CLASE COCHE

class Coche:
    """
    Representa un coche detectado y seguido a lo largo de los frames.
    """
    def __init__(self, centro, dimensiones, id_coche):
        self.centro = centro                  # Centro actual del coche
        self.dimensiones = dimensiones        # (x, y, w, h)
        self.id_coche = id_coche              # Identificador único
        self.sin_deteccion = 0                # Frames sin detectar
        self.contado = False                  # Para no contar dos veces


# ************************************************************
# PREPROCESADO DEL FRAME

def obtener_mascara(frame, fondo, kernel):
    """
    Aplica sustracción de fondo y operaciones morfológicas
    para obtener la máscara de movimiento.
    """
    fgmask = fondo.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    return fgmask


# ************************************************************
# ASOCIACIÓN DE COCHES

def buscar_coche_mas_cercano(centro, coches, max_dist):
    """
    Busca el coche existente más cercano a un centro dado.
    """
    coche_cercano = None
    distancia_min = max_dist

    for coche in coches:
        d = math.hypot(
            centro[0] - coche.centro[0],
            centro[1] - coche.centro[1]
        )
        if d < distancia_min:
            distancia_min = d
            coche_cercano = coche

    return coche_cercano


def procesar_deteccion(centro, bbox, coches, coches_visibles,
                       linea_conteo, contador, id_counter, max_dist):
    """
    Actualiza un coche existente o crea uno nuevo a partir
    de una detección.
    """
    coche = buscar_coche_mas_cercano(centro, coches, max_dist)

    # CASO 1: coche ya existente
    if coche:
        coche.centro = centro
        coche.dimensiones = bbox
        coche.sin_deteccion = 0
        coches_visibles.append(coche)

        # Contar si cruza la línea por primera vez
        if not coche.contado and centro[1] >= linea_conteo:
            contador += 1
            coche.contado = True

    # CASO 2: coche nuevo
    else:
        nuevo = Coche(centro, bbox, id_counter)
        id_counter += 1

        # Si aparece ya pasado la línea, se cuenta
        if centro[1] >= linea_conteo:
            contador += 1
            nuevo.contado = True

        coches.append(nuevo)
        coches_visibles.append(nuevo)

    return contador, id_counter


# ************************************************************
# FILTRADO DE COCHES PERDIDOS

def filtrar_coches(coches, coches_visibles, limite_deteccion):
    """
    Elimina coches que llevan demasiados frames sin detectarse.
    """
    coches_filtrados = []

    for coche in coches:
        if coche in coches_visibles:
            coches_filtrados.append(coche)
        else:
            coche.sin_deteccion += 1
            if coche.sin_deteccion < limite_deteccion:
                coches_filtrados.append(coche)

    return coches_filtrados


# ************************************************************
# DIBUJADO

def dibujar(frame, coches_visibles, linea_conteo, contador):
    """
    Dibuja rectángulos, línea de conteo y contador.
    """
    for coche in coches_visibles:
        x, y, w, h = coche.dimensiones
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.line(frame, (0, linea_conteo),
             (frame.shape[1], linea_conteo), (0, 0, 255), 2)

    cv2.putText(frame, f"Coches detectados: {contador}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)
