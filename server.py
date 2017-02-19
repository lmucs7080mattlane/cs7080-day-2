from flask import Flask, request, abort, jsonify, render_template_string
app = Flask(__name__)

animal_id_counter = 0
def generate_animal_id():
    global animal_id_counter
    animal_id_counter += 1
    return str(animal_id_counter)

animals = {
    generate_animal_id(): {
        'name': 'dave',
        'species': 'deer',
        'eats': 'grass'
    },
    generate_animal_id(): {
        'name': 'bob',
        'species': 'bear',
        'eats': 'salmon'
    }
}

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

def return_error(code):
    return ('', code)

def return_empty_success():
    return return_error(200)

@app.route('/animals/', methods = ['GET', 'POST'])
def handle_animals():
    if request.method == 'GET':
        return jsonify(animals)
    elif request.method == 'POST':
        # This should insert a new animal with a new
        # animal id (created using generate_animal_id) and
        # then return the animal_id to the requester
        new_animal_id = generate_animal_id()
        # The new animal comes from the 'body' of the request
        # and can be retrieved using 'request.get_json()'
        my_new_animal = request.get_json()
        # You can check if it is a valid animal using the
        # function is_animal(possible_animal)
        if not is_animal(my_new_animal):
            # If the request did not contain a valid animal,
            # return a 400 or 'BadRequest' error code using
            # the return_error method e.g. 'return return_error(400)'
            return return_error(400)
        animals[new_animal_id] = my_new_animal
        return new_animal_id

@app.route('/animals/<animal_id>', methods = ['GET', 'PUT', 'DELETE'])
def handle_animal(animal_id):
    if request.method == 'GET':
        # This should return the single animal from the
        # animals dictionary that has the same animal_id.
        #
        # If there is no matching animal, return a 404
        # or 'NotFoundError' using the return_error function
        raise NotImplementedError()
    elif request.method == 'PUT':
        # This should update an existing animal with a new animal.
        # The animal to be updated should be identified by the
        # animal_id.
        #
        # If there is no matching animal, return a 404
        # or 'NotFoundError' using the return_error function
        #
        # The new animal comes from the 'body' of the request
        # and can be retrieved using 'request.get_json()'
        #
        # You can check if it is a valid animal using the
        # function is_animal(possible_animal)
        #
        # If the request did not contain a valid animal,
        # return a 400 or 'BadRequest' error code using
        # the return_error method e.g. 'return return_error(400)'
        raise NotImplementedError()
    elif request.method == 'DELETE':
        # This should delete an existing animal from the
        # animals dictionary.
        # The animal to be updated should be identified by the
        # animal_id.
        #
        # If there is no matching animal, return a 404
        # or 'NotFoundError' using the return_error function
        #
        # If there is a match and the animal is deleted
        # call 'return return_empty_success()'
        raise NotImplementedError()

@app.route('/', methods = ['GET'])
def get_webpage():
    html = '''
    <table>
       <tr>
            <th> ID </th>
            <td> species </td>
            <td> name </td>
            <td> eat </td>
       </tr>
    {% for key, value in animals.items() %}
       <tr>
            <th> {{ key }} </th>
            <td> {{ value['specIES'] }} </td>
            <td> {{ value['namez'] }} </td>
            <td> {{ value['foods'] }} </td>
       </tr>
    {% endfor %}
    </table>
    '''
    return render_template_string(html, animals=animals)


if __name__ == '__main__':
    app.run()