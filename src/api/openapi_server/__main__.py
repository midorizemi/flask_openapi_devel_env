#!/usr/bin/env python3

import connexion

from openapi_server import encoder
from openapi_server.database import db


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'Swagger Petstore'},
                pythonic_params=True)
    app.run(port=8001)
    db.init_app(app)


if __name__ == '__main__':
    main()
