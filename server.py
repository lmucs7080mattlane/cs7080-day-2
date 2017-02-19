from flask import Flask, request, abort, jsonify, render_template_string
app = Flask(__name__)

animals = {}

animal_id_counter = 0;
def generate_animal_id():
    global animal_id_counter
    animal_id_counter += 1
    return str(animal_id_counter)

def is_animal(possible_animal):
    if type(possible_animal) != dict:
        return False
    if len(possible_animal.keys()) != 3:
        return False
    if 'name' not in possible_animal:
        return False
    if 'species' not in possible_animal:
        return False
    if 'eats' not in possible_animal:
        return False
    return True

@app.route('/animals/', methods = ['GET'])
def get_animals():
    return jsonify(animals)

@app.route('/animals/<animal_id>', methods = ['GET'])
def get_animal(animal_id):
    if animal_id not in animals:
        abort(404)
    return jsonify(animals[animal_id])

@app.route('/animals/', methods = ['POST'])
def post_animal():
    animal_id = generate_animal_id()
    request_content = request.get_json()
    if not is_animal(request_content):
        abort(400)
    animals[animal_id] = request_content
    return jsonify(animal_id)

@app.route('/animals/<animal_id>', methods = ['PUT'])
def put_animal(animal_id):
    if animal_id not in animals:
        abort(404)
    request_content = request.get_json()
    if not is_animal(request_content):
        abort(400)
    animals[animal_id] = request_content
    return '', 200

@app.route('/animals/<animal_id>', methods = ['DELETE'])
def delete_animal(animal_id):
    if animal_id not in animals:
        abort(404)
    del animals[animal_id]
    return '', 200

@app.route('/', methods = ['GET'])
def get_webpage():
    html = '''
    <table>
       <tr>
            <th> KEY </th>
            <td> species </td>
            <td> name </td>
            <td> eat </td>
       </tr>
    {% for key, value in animals.items() %}
       <tr>
            <th> {{ key }} </th>
            <td> {{ value['species'] }} </td>
            <td> {{ value['name'] }} </td>
            <td> {{ value['eats'] }} </td>
       </tr>
    {% endfor %}
    </table>
    '''
    return render_template_string(html, animals=animals)


if __name__ == '__main__':
    app.run()