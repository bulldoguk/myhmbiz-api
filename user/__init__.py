__version__ = '0.1.0'

from flask_restx import Api

from .user import api as user
# user
# schools
# store_setup
# order

api = Api(
    title='Mum Shoppe API layer',
    version='1.0',
    description='APIs used to run Mum Shoppe project',
)

api.add_namespace(user, path='/user')
