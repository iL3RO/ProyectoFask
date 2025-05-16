from flask import Flask, render_template, request, abort
import json

app = Flask(__name__)

# Cargar datos de motocicletas
with open('motocicletas.json', 'r', encoding='utf-8') as f:
    motos_data = json.load(f)

# Obtener lista única de ciudades
ciudades = sorted(set(moto['ciudad'] for moto in motos_data))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar')
def buscar():
    return render_template('buscar.html', ciudades=ciudades)

@app.route('/resultados', methods=['POST'])
def resultados():
    modelo = request.form.get('modelo', '').strip().lower()
    ciudad = request.form.get('ciudad', '')
    
    motos_filtradas = [
        moto for moto in motos_data
        if (not modelo or moto['detalles']['modelo'].lower().startswith(modelo)) and
        (not ciudad or moto['ciudad'] == ciudad)
    ]
    
    return render_template('resultados.html', motos=motos_filtradas)

@app.route('/moto/<id_moto>')
def moto_detail(id_moto):
    moto = next((moto for moto in motos_data if moto['id_moto'] == id_moto), None)
    if not moto:
        abort(404)
    return render_template('moto_detail.html', moto=moto)

if __name__ == '__main__':
    app.run(debug=True)
