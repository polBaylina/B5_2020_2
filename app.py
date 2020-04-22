from flask import Flask
from flask_restful import Resource, Api, reqparse
from data import events, artists

app = Flask(__name__)
api = Api(app)


class Artist(Resource):

    def get(self, id):
        artist = next(filter(lambda x: x['id'] == id, artists), None)
        return {'artist': artist}, 200 if artist else 404

    def post(self, id=None):
        if id is None:
            id = len(artists)
        parser = reqparse.RequestParser()  # create parameters parser from request

        # define al input parameters need and its type
        parser.add_argument('name', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('country', type=str)
        parser.add_argument('genre', type=str, action="append")
        # action = "append" is needed to determine that is a list of strings

        data = parser.parse_args()
        artist = {'id': id,
                  "name": data['name'],
                  "country": data['country'],
                  "genre": data['genre']
                  }
        artists.append(artist)

        return artist, 201

    def delete(self, id):
        if id < len(artists):
            artists.pop(id)
            return {'message': "User deleted correctly"}, 200
        else:
            return {'message': "User not found"}, 406

    def put(self, id):
        if id == len(artists) or id > len(artists):
            self.post(id)
            return artists[id], 201
        else:
            parser = reqparse.RequestParser()  # create parameters parser from request

            # define al input parameters need and its type
            parser.add_argument('country', type=str)
            parser.add_argument('genre', type=str,
                                action="append")  # action = "append" is needed to determine that is a list of strings

            data = parser.parse_args()
            artist = {
                "country": data['country'],
                "genre": data['genre']
            }
            artists[id].update(artist)
            return artist, 200

class Event(Resource):

    def get(self, id):
        event = next(filter(lambda x: x['id'] == id, events), None)
        return {'artist': event}, 200 if event else 404

    def post(self, id=None):
        if id is None:
            id = len(events)
        parser = reqparse.RequestParser()  # create parameters parser from request

        # define al input parameters need and its type
        parser.add_argument('place', type=str, required=True, help="This field cannot be left blanck")
        parser.add_argument('city', type=str)
        parser.add_argument('country', type=str)
        parser.add_argument('date', type=str)
        # action = "append" is needed to determine that is a list of strings

        data = parser.parse_args()

        event = {'id': id,
                 "place": data['place'],
                 "city": data['city'],
                 'country': data['country'],
                 'date': data['date'],
                 'artists': []
                 }
        events.append(event)

        return event, 201

    def delete(self, id):
        if id < len(events):
            events.pop(id)
            return {'message': "Event deleted correctly"}, 200
        else:
            return {'message': "Event not found"}, 406

    def put(self, id):
        if id == len(events) or id > len(events):
            self.post(id)
            return events[id], 201
        else:
            parser = reqparse.RequestParser()  # create parameters parser from request

            # define al input parameters need and its type
            parser.add_argument('place', type=str, required=True, help="This field cannot be left blanck")
            parser.add_argument('city', type=str)
            parser.add_argument('country', type=str)
            parser.add_argument('date', type=str)

            data = parser.parse_args()
            event = {
                "place": data['place'],
                "city": data['city'],
                'country': data['country'],
                'date': data['date']
            }
            events[id].update(event)
            return event, 200


class ArtistsList(Resource):

    def get(self):
        return {'artists': artists}


class EventList(Resource):

    def get(self):
        return {'events': events}


api.add_resource(Artist, '/artist/<int:id>', '/artist')
api.add_resource(Event, '/event/<int:id>', '/event')

api.add_resource(ArtistsList, '/artists')
api.add_resource(EventList, '/events')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
