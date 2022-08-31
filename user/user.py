from flask import request
from flask_restx import Namespace, Resource, fields

api = Namespace('user', description='User related operations')

user_model = api.model('user', {
    "guid": fields.String(required=False, description='Internal GUID'),
    "given_name": fields.String(required=False, description='oAuth provided'),
    "picture": fields.String(required=False, description='oAuth provided'),
    "locale": fields.String(required=False, description='Used in i18n, defaults to en'),
    "hd": fields.String(required=False, description='Used to identify superusers, must have email_verified'),
    "extended_info": fields.Boolean(required=False, description='Added by system as flag that we have extended data '
                                                                'on this user'),
    "some_new_data": fields.String(required=False, description='Test field to show passing extended data back'),
    "superAdmin": fields.Boolean(default=False,readonly=True)
})

user_example = {
    "guid": "3b6598c6-6d4f-4293-ac66-9f564dc302e8",
    "given_name": "Gary",
    "picture": "https://lh3.googleusercontent.com/a-/AOh14GhuErhFmR0i2t-vF8aSdLtI1LP4aR65Os2oioYXKJc=s96-c",
    "email": "gary@myhmbiz.com",
    "locale": "en",
    "hd": "myhmbiz.com",
    "extended_info": True,
    "superAdmin": False
}


@api.route('/')
class User(Resource):
    """Create/update user"""

    @api.response(403, "Forbidden")
    @api.response(400, 'User with the given name already exists')
    @api.response(500, 'Internal Server error')
    @api.response(201, 'User updated successfully')
    @api.marshal_with(user_model)
    @api.expect(user_model)
    def post(self):
        """Create a new entity"""
        try:
            result = add_or_update(request.json)
            return result, 201
        except:
            return 'Failed user update', 500


@api.route('/<guid>')
class UserUpdate(Resource):
    @api.param('guid', 'The user identifier - unique in our system')
    @api.response(404, 'User not found')
    @api.doc('get_user')
    @api.marshal_with(user_model)
    @api.response(500, 'Internal Server error')
    def get(self, id):
        """Fetch a user given their identifier"""
        return user_example, 200

    def patch(self, id):
        """Update user details"""
        return "User updated", 201
