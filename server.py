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
    <!doctype html>
    <title>jQuery Example</title>
    <script type="text/javascript"
      src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script type="text/javascript">
      var $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
    </script>
    <script type="text/javascript">
        $(function() {
            var update_table = function() {
                $.getJSON($SCRIPT_ROOT + '/animals/', {}, function(data) {
                    $("#animals").empty();
                    $("#animals").append(`
                        <tr>
                            <th> KEY </th>
                            <td> species </td>
                            <td> name </td>
                            <td> eats </td>
                        </tr>
                    `);
                    for (var key in data){
                        $("#animals").append(`
                            <tr>
                                <th> ` + key + `</th>
                                <td> ` + data[key].species +` </td>
                                <td> ` + data[key].name +` </td>
                                <td> ` + data[key].eats +` </td>
                            </tr>
                        `);
                    }
                    setTimeout(update_table, 1000);
                });
            };

            setTimeout(update_table, 1000);
        });
    </script>

    <p>
    Every 1 second (or 1000ms) the update_table javascript function is called.
    This function empties the table of all contents and then calls the
    GET /animals/ route. It then generates a whole new table based on what
    animals were received in the GET /animals/ response.
    </p>

    <br/><br/>
    <table id="animals"/>
    '''
    return render_template_string(html, animals=animals)


if __name__ == '__main__':
    app.run()