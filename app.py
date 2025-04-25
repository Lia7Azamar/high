from flask import Flask, jsonify, render_template
import math, random

app = Flask(__name__)

# Coordenadas
coord = {
    'Jiloyork': (19.916012, -99.580580),
    'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844),
    'Guadalajara': (20.677754472859146, -103.34625354877137),
    'Monterrey': (25.69161110159454, -100.321838480256),
    'QuintanaRoo': (21.163111924844458, -86.80231502121464),
    'Michohacan': (19.701400113725654, -101.20829680213464),
    'Aguascalientes': (21.87641043660486, -102.26438663286967),
    'CDMX': (19.432713075976878, -99.13318344772986),
    'QRO': (20.59719437542255, -100.38667040246602)
}

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def evalua_ruta(ruta):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancia(coord[ruta[i]], coord[ruta[i+1]])
    total += distancia(coord[ruta[-1]], coord[ruta[0]])
    return round(total, 2)

def hill_climbing():
    ruta = list(coord.keys())
    random.shuffle(ruta)
    mejora = True
    while mejora:
        mejora = False
        dist_actual = evalua_ruta(ruta)
        for i in range(len(ruta)):
            for j in range(i + 1, len(ruta)):
                ruta_tmp = ruta[:]
                ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
                dist = evalua_ruta(ruta_tmp)
                if dist < dist_actual:
                    ruta = ruta_tmp[:]
                    mejora = True
                    dist_actual = dist
                    break
    return ruta

@app.route("/")
def index():
    return render_template("index.html")  # esto carga el HTML automáticamente

@app.route("/tsp")
def tsp():
    ruta = hill_climbing()
    distancia_total = evalua_ruta(ruta)
    return jsonify({"ruta": ruta, "distancia_total": distancia_total})

if __name__ == '__main__':
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get("PORT", 5000)))

