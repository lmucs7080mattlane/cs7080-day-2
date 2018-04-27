from flask import Flask, request, abort, jsonify, render_template_string
from pymongo import MongoClient
from bson.objectid import ObjectId
app = Flask(__name__)


# http://docs.mongodb.com/getting-started/python/client/
mongo_database = None
mongo_animals_collection = None
def connect_to_mongo():
    global mongo_database
    global mongo_animals_collection
    client = MongoClient('mongodb://mongo:27017/animals')
    # Cheap and easy command to test the connection
    client.admin.command('ismaster')
    mongo_database = client.get_default_database()
    mongo_animals_collection = mongo_database.animals
connect_to_mongo()


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

def get_all_animals():
    db_animals = [animal for animal in mongo_animals_collection.find()]
    animals = {}
    for animal in db_animals:
        animal_id = str(animal['_id'])
        del animal['_id']
        animals[animal_id] = animal
    return animals

@app.route('/animals/', methods = ['GET', 'POST'])
def handle_animals():
    if request.method == 'GET':
        animals = get_all_animals()
        return jsonify(animals)

    elif request.method == 'POST':
        # This should insert a new animal and return a new animal id
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

        # TODO Challenge: Insert the new animal into the database animals collection
        # The insert_one method will be your friend here.
        # Note: insert_one returns an object with an 'inserted_id' property,
        #       which is the inserted object's '_id' field.
        #       This would be good to return as the object's id.
        #       However, you will need to the convert the property field from
        #       the ObjectId type to a string type using the str() function
        #       Once converted to a string, you need to remember to jsonify
        #       the string.
        result = mongo_animals_collection.insert_one(
            my_new_animal
        )
        return jsonify(str(result.inserted_id))

@app.route('/animals/<animal_id>', methods = ['GET', 'PUT', 'DELETE'])
def handle_animal(animal_id):
    animal_id = ObjectId(animal_id)
    if request.method == 'GET':
        # This should return the single matching
        # animal from mongodb.
        # If there is no matching animal, return a 404
        # or 'NotFoundError' using the return_error function

        # TODO Challenge: Find the animal in the database using the find_one method
        # and the '_id' property.
        # Note: You will need to convert the animal_id, which is a string, into
        #       an ObjectId type, which is the type of '_id'. For more details, see:
        #       http://api.mongodb.com/python/current/tutorial.html#querying-by-objectid
        my_animal = mongo_animals_collection.find_one(
            {'_id': animal_id}
        )
        if my_animal is None:
            return return_error(404)
        del my_animal['_id'] # Keep this line
        return jsonify(my_animal)

    elif request.method == 'PUT':
        # This should update an existing animal with a new animal.
        # The animal to be updated should be identified by the
        # animal_id.

        my_animal = mongo_animals_collection.find_one(
            {'_id': animal_id}
        )


        if my_animal is None:
            # If there is no matching animal, return a 404
            # or 'NotFoundError' using the return_error function
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

        # TODO Challenge: Update the animal in the database using the update_one
        # method and the '_id' property.
        # http://api.mongodb.com/python/current/api/pymongo/collection.html?highlight=update#pymongo.collection.Collection.update_one
        mongo_animals_collection.update_one(
            {'_id': animal_id},
            {'$set': updated_animal}
        )

        return return_empty_success() # This returns the 200 Success Message
    elif request.method == 'DELETE':
        # This should delete an existing animal from mongodb
        # The animal to be deleted should be identified by the
        # animal_id.

        my_animal = mongo_animals_collection.find_one(
            {'_id': animal_id}
        )

        # If there is no matching animal, return a 404
        # or 'NotFoundError' using the return_error function
        if my_animal is None:
            return return_error(404)


        mongo_animals_collection.remove(
            {'_id': animal_id}
        )

        return return_empty_success()

@app.route('/species/', methods = ['GET'])
def handle_species():
    # TODO Challenge:
    # 1) Get all of the animals
    # 2) Build a list of all species with no duplicates.

    all_animals = get_all_animals()

    species = []

    for animal in all_animals.values():
        if animal['species'] not in species:
            species.append(animal['species'])

    return jsonify(species)

@app.route('/species/<species_id>/members', methods = ['GET'])
def handle_species_id_members(species_id):

    all_animals = get_all_animals()

    animal_names = []

    for animal in all_animals.values():
        if animal['species'] == species_id:
            animal_names.append(animal['name'])

    return jsonify(animal_names)

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
            // call GET /animals/ and GET /SPECIES and update
            // the table caled 'animals'
            var update_table = function() {
                $.getJSON($SCRIPT_ROOT + '/animals/', {}, function(data) {
                    $("#animals").empty();
                    $("#animals").append(`
                        <tr>
                            <th> ID </th>
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

                    $.getJSON($SCRIPT_ROOT + '/species/', {}, function(data) {
                        $("#species").empty();
                        var $table = `<tr>
                                <th> Species: </th>`;
                        for (var key in data){
                            $table = $table + `
                                <td> ` + data[key] + ` </td>
                            `;
                        }
                        $table = $table + `
                                </tr>
                        `
                        $("#species").append($table);

                        setTimeout(update_table, 500);
                    });
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
    </script>e is contained in the branch.

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
    This function empties the tables of all contents and then calls the
    GET /animals/ and GET /species/ route. It then generates whole new tables
    based on what animals and species received in the
    GET /animals/ and GET /species/ response.
    </p>

    <table id="animals"> </table>
    <br/>

    <h1>Current Species</h1>
    <table id="species"> </table>

    <script type="text/javascript">
    </script>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run()