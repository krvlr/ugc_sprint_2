import datetime

import jwt
from functional.settings import test_settings


def get_jwt_token():
    body = {'fresh': False,
            'iat': datetime.datetime.now(tz=datetime.timezone.utc),
            'jti': 'a0565537-7d14-4965-b5eb-a250a0d5e6ec',
            'type': 'access',
            'sub': {'id': '3d868f0d-8f10-4ca0-ac0d-e2836fef5805',
                    'device_info': 'PostmanRuntime/3.0.11-hotfix.2',
                    'is_active': 'True',
                    'is_verified': 'False',
                    'is_admin': 'False',
                    'roles': ['default']},
            'nbf': datetime.datetime.now(tz=datetime.timezone.utc),
            'csrf': '3b49f0e4-8955-4c59-8c0f-282001a49534',
            'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=60)}

    token = jwt.encode(
        body,
        test_settings.secret_key,
        algorithm="HS256"
    )

    return token
