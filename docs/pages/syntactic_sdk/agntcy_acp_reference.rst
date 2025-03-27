Client Reference API
=============================

ACP Objects
--------------

``ApiClientConfiguration``
***************************************
.. autoclass:: agntcy_acp.ApiClientConfiguration
   :members:
   :inherited-members:

``ACPClient``
*****************************
.. autoclass:: agntcy_acp.ACPClient
   :members:
   :inherited-members:

``AsyncACPClient``
*****************************
.. autoclass:: agntcy_acp.AsyncACPClient
   :members:
   :inherited-members:

``ApiClient``
*****************************
.. autoclass:: agntcy_acp.ApiClient
   :members:
   :inherited-members:

``AsyncApiClient``
*****************************
.. autoclass:: agntcy_acp.AsyncApiClient
   :members:
   :inherited-members:

``ApiResponse``
*****************************
.. autopydantic_model:: agntcy_acp.ApiResponse
   :members:

LangGraph Bindings
-----------------------

``ACPNode``
*****************************
.. autoclass:: agntcy_acp.langgraph.ACPNode
   :members:

``APIBridgeAgentNode``
*****************************
.. autoclass:: agntcy_acp.langgraph.APIBridgeAgentNode
   :members:
   :inherited-members:

``APIBridgeInput``
*****************************
.. autopydantic_model:: agntcy_acp.langgraph.APIBridgeInput
   :members:

``APIBridgeOutput``
*****************************
.. autopydantic_model:: agntcy_acp.langgraph.APIBridgeOutput
   :members:

``add_io_mapped_edge``
*****************************
.. autofunction:: agntcy_acp.langgraph.add_io_mapped_edge

``add_io_mapped_conditional_edge``
****************************************
.. autofunction:: agntcy_acp.langgraph.add_io_mapped_conditional_edge

Exceptions
------------

``ACPDescriptorValidationException``
********************************************
.. autoclass:: agntcy_acp.ACPDescriptorValidationException
   :members:
   :inherited-members:

``ACPRunException``
*****************************
.. autoclass:: agntcy_acp.ACPRunException
   :members:
   :inherited-members:

``ApiTypeError``
*****************************
.. autoclass:: agntcy_acp.ApiTypeError
   :members:
   :inherited-members:

``ApiValueError``
*****************************
.. autoclass:: agntcy_acp.ApiValueError
   :members:
   :inherited-members:

``ApiKeyError``
*****************************
.. autoclass:: agntcy_acp.ApiKeyError
   :members:
   :inherited-members:

``ApiAttributeError``
*****************************
.. autoclass:: agntcy_acp.ApiAttributeError
   :members:
   :inherited-members:

``ApiException``
*****************************
.. autoclass:: agntcy_acp.ApiException
   :members:
   :inherited-members:

``BadRequestException``
*****************************
.. autoclass:: agntcy_acp.BadRequestException
   :members:
   :inherited-members:

``NotFoundException``
*****************************
.. autoclass:: agntcy_acp.NotFoundException
   :members:
   :inherited-members:

``UnauthorizedException``
*****************************
.. autoclass:: agntcy_acp.UnauthorizedException
   :members:
   :inherited-members:

``ForbiddenException``
*****************************
.. autoclass:: agntcy_acp.ForbiddenException
   :members:
   :inherited-members:

``ServiceException``
*****************************
.. autoclass:: agntcy_acp.ServiceException
   :members:
   :inherited-members:

``ConflictException``
************************************
.. autoclass:: agntcy_acp.ConflictException
   :members:
   :inherited-members:

``UnprocessableEntityException``
************************************
.. autoclass:: agntcy_acp.UnprocessableEntityException
   :members:
   :inherited-members:
 
``OpenApiException``
*****************************
.. autoclass:: agntcy_acp.OpenApiException
   :members:
   :inherited-members:
