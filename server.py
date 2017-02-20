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
        # If there is no matching animal, return a 404
        # or 'NotFoundError' using the return_error function
        if animal_id not in animals:
            return return_error(404)
        return jsonify(animals[animal_id])
    elif request.method == 'PUT':
        # This should update an existing animal with a new animal.
        # The animal to be updated should be identified by the
        # animal_id.
        #
        # If there is no matching animal, return a 404
        # or 'NotFoundError' using the return_error function
        if animal_id not in animals:
            return return_error(404)
        # The new animal comes from the 'body' of the request
        # and can be retrieved using 'request.get_json()'
        updated_animal = request.get_json()
        if not is_animal(updated_animal):
            # You can check if it is a valid animal using the
            # function is_animal(possible_animal)
            # If the request did not contain a valid animal,
            # return a 400 or 'BadRequest' error code using
            # the return_error method e.g. 'return return_error(400)'
            return return_error(400)

        animals[animal_id] = updated_animal
        return return_empty_success() # This returns the 200 Success Message
    elif request.method == 'DELETE':
        # This should delete an existing animal from the
        # animals dictionary.
        # The animal to be updated should be identified by the
        # animal_id.
        #
        # If there is no matching animal, return a 404
        # or 'NotFoundError' using the return_error function
        if animal_id not in animals:
            return return_error(404)
        #
        # If there is a match and the animal is deleted
        del animals[animal_id]
        # call 'return return_empty_success()'
        return return_empty_success()

@app.route('/', methods = ['GET'])
def get_webpage():
    html = '''
    <!doctype html>
    <title>jQuery Example</title>
    <script type="text/javascript"
      src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.0/jquery.min.js"></script>
    <script type="text/javascript">
      var $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
    </script>
    <script type="text/javascript">
        $(function() {
            // Once every 500 milliseconds,
            // call GET /animals/ and update
            // the table caled 'animals'
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
                    setTimeout(update_table, 500);
                });
            };
            setTimeout(update_table, 500);

            // Watch the new animal form for submissions
            // When we see a form submission, call POST /animals/
            // with the form's data
            $( "#new_animal_form" ).submit(function(event) {
                event.preventDefault(); // Stop the form from submitting normally

                var $form = $(this); // Get the form

                // Get the data from the form
                var name = $form.find( "input[name='name']" ).val();
                var species = $form.find( "input[name='species']" ).val();
                var eats = $form.find( "input[name='eats']" ).val();

                // The REST API address
                var url = "/animals/"

                // Send the data using the /animals/ POST method
                $.ajax(
                    {
                        url:url,
                        type:"POST",
                        data: JSON.stringify({
                            name: name,
                            species: species,
                            eats: eats
                        }),
                        contentType: "application/json; charset=utf-8",
                        dataType: "json",
                        success: function(){ return; }
                    }
                );
            });
        });
    </script>

    <h1>Add an Animal:</h1>
    <form action="/animals/" id="new_animal_form">
        Name:<input type="text" name="name" placeholder="name of animal"><br/>
        Species:<input type="text" name="species" placeholder="species"><br/>
        Eats:<input type="text" name="eats" placeholder="what food the animal eats"><br/>
        <input type="submit" value="add animal">
    </form>

    <h1>Current Animals</h1>
    <p>
    Every 0.5 seconds (or 500ms) the update_table javascript function is called.
    This function empties the table of all contents and then calls the
    GET /animals/ route. It then generates a whole new table based on what
    animals were received in the GET /animals/ response.
    </p>

    <table id="animals"> </table>

    <script type="text/javascript">
    </script>
    '''
    return render_template_string(html, animals=animals)

if __name__ == '__main__':
    app.run()