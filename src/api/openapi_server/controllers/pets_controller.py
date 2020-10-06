import connexion
import six

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.pet import Pet  # noqa: E501
from openapi_server import util


def list_pets(limit=None):  # noqa: E501
    """List all pets

     # noqa: E501

    :param limit: How many items to return at one time (max 100)
    :type limit: int

    :rtype: List[Pet]
    """
    return 'do some magic!'
