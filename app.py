from flask import Flask, request, jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

app = Flask(__name__)

db = PostgresqlDatabase(
    'pets',
    user='postgres',
    password='postgres',
    host='localhost'
    port=5432
)


class BaseModel(Model):
    class Meta:
        database = db


class Pet(BaseModel):
    name = CharField()
    type = CharField()
    photo = CharField()
    personality = TextField()


db.connect()
db.create_tables([Pet])
db.create_tables([Pet])

Pet(name='Fido', type='dog', photo='https://www.petmd.com/sites/default/files/petmd-dog-behavior/image-gallery/dog-behavior-6.jpg',
    personality='Loves to play fetch').save()
Pet(name='Lo Mein', type='cat', photo='https://www.petmd.com/sites/default/files/petmd-cat-behavior/images/cat-behavior-6.jpg',
    personality='Loves to cuddle').save()

app = Flask(__name__)


@app.route('/pet/', methods=['GET', 'POST'])
@app.route('/pet/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
      if id:
        return jsonify(
          model_to_dict(
            Pet.get(
              Pet.id == id
            )
          )
        )
      else:
        pets_list = []
        for pet in Pet.select():
          pets_list.append(model_to_dict(pet))
        return jsonify(pets_list)

    if request.method == 'POST':
        new_pet = dict_to_model(Pet, request.json())
        new_pet.save()
        return jsonify({"success": True})

    if request.method == 'PUT':
        data = request.get_json()
        Pet.update(data).where(Pet.id == id).execute()
        return "Pet " + str(id) + " has been updated."

    if request.method == 'DELETE':
        Pet.delete().where(Pet.id == id).execute()
        return "Pet " + str(id) + " has been deleted."

app.run(debug=True, port=6000)
