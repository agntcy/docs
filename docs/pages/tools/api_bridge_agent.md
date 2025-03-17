# API Bridge Agnt

## About The Project

The [API Bridge Agnt](https://github.com/agntcy/api-bridge-agnt) project provides a [Tyk](https://tyk.io/) middleware plugin
that allows users to interact with traditional REST APIs using natural language.
It acts as a translator between human language and structured API
requests/responses.

Key features:

- Converts natural language queries into valid API requests based on OpenAPI specifications
- Transforms API responses back into natural language explanations
- Integrates with Tyk API Gateway as a plugin
- Uses Azure OpenAI's GPT models for language processing
- Preserves API schema validation and security while enabling conversational interfaces

This enables developers to build more accessible and user-friendly API interfaces without modifying
the underlying API implementations.

## Getting Started

### Prerequisites

To build the plugin you need those dependenccies
- Go
- Cmake
- Git
- jq

Then get the source code:

```
git clone https://github.com/agntcy/api-bridge-agnt
```

Tyk requires also a redis database. You can deploy it with:

```bash
make start_redis
```

### Local development

Built with:

- [search](https://github.com/kelindar/search) for the semantic router
- [Tyk](https://github.com/TykTechnologies/tyk.git) for the gateway
We use these dependencies inside the project. However, you don't need to download it or to build it, 
everything is managed by the Makefile.

#### Set environment variables

For OpenAI:

```bash
export OPENAI_API_KEY=REPLACE_WITH_YOUR_KEY
export OPENAI_MODEL=gpt-4o-mini
```

For Azure OpenAI:

```bash
export OPENAI_API_KEY=REPLACE_WITH_YOUR_KEY
export OPENAI_ENDPOINT=https://REPLACE_WITH_YOUR_ENDPOINT.openai.azure.com
export OPENAI_MODEL=gpt-4o-mini
```

#### Build the plugin and start tyk locally on [Tyk](http://localhost:8080)

Dependencies are managed so that you can just run:

```bash
make start_tyk
```

This will automatically build "Tyk", "search" and the plugin, then install the plugin and start Tyk gateway

#### Load and configure Tyk with an example API (httpbin.org)

```bash
make load_plugin
```

### Other installation

#### Linux

For linux (ubuntu) you can use:

```bash
TARGET_OS=linux TARGET_ARCH=amd64 SEARCH_LIB=libllama_go.so make start_tyk
```

#### Individual steps for building if needed:

If you need to decompose each task individually, you can split into

```bash
make build_tyk          # build tyk
make build_search_lib   # build the "search" library, used as semantic router
make build_plugin       # build the plugin
make install_plugin     # Install the plugin
```

## Tyk configuration

This plugins relies on [Tyk OAS API Definition](https://tyk.io/docs/api-management/gateway-config-tyk-oas/).
To use it, you need to add the plugin to the `postPlugins` and `responsePlugins`
sections of the `x-tyk-api-gateway` section:

```json
"x-tyk-api-gateway": {
  "middleware": {
    "global": {
      "pluginConfig": {
        "data": {
          "enabled": true,
          "value": {
          }
        },
        "driver": "goplugin"
      },
      "postPlugins": [
        {
          "enabled": true,
          "functionName": "SelectAndRewrite",
          "path": "middleware/agent-bridge-plugin.so"
        },
        {
          "enabled": true,
          "functionName": "RewriteQueryToOas",
          "path": "middleware/agent-bridge-plugin.so"
        }
      ],
      "responsePlugins": [
        {
          "enabled": true,
          "functionName": "RewriteResponseToNl",
          "path": "middleware/agent-bridge-plugin.so"
        }
      ]
    }
  }
}
```
Then add the your OpenAPI specification:

For example, adding the httpbin.org service can be done using the `configs/httpbin.org.oas.json` file.

```bash
curl http://localhost:8080/tyk/apis/oas \
  --header "x-tyk-authorization: foo" \
  --header 'Content-Type: text/plain' \
  -d@configs/httpbin.org.oas.json

curl http://localhost:8080/tyk/reload/group \
  --header "x-tyk-authorization: foo"
```

It's then possible to do a query like this:

```bash
curl http://localhost:8080/httpbin/json \
  --header "X-Nl-Query-Enabled: yes" \
  --header "X-Nl-Response-Type: nl" \
  --header "Content-Type: text/plain" \
  -d "Hello"
```

In this example `http://localhost:8080/httpbin/json`:

- "/httpbin/" is the listen path defined on the x-tyk-api-gateway part of the spec
- "json" is the endpoint on the spec


### Select and rewrite middleware

The first middleware function (`SelectAndRewrite`) is responsible for selecting
the appropriate OpenAPI endpoint based on the request, and then rewriting the
request to match the expected API format.

The content type for this request should be `application/nlq`.

Example:

```bash
curl 'http://localhost:8080/github/' \
  --header 'Content-Type: application/nlq' \
  -d 'List the first issue for the repository named tyk owned by TykTechnologies with the label bug'
```

### Rewrite query

The second middleware function (`RewriteQueryToOas`) is only responsible for
converting the natural language query into a valid API request based on the
selected OpenAPI endpoint.

```{important}
Here you MUST provide the full path of the target API in the request URL.
Rewriting the query will be available only if the content type is not set or is text/plain
```

Two headers are available for this request:

- **X-Nl-Query-Enabled**: `yes` or `no` (default is `no`), to enable or disable the natural language query processing
- **X-Nl-Response-Type**: `nl` or `upstream` (default is `upstream`), to select the response format. `nl` will return the response in natural language, while `upstream` will return the original API response.

Example:

```bash
curl 'http://localhost:8080/gmail/gmail/v1/users/me/messages/send' \
  --header "Authorization: Bearer YOUR_GOOGLE_TOKEN" \
  --header 'Content-Type: text/plain' \
  --header 'X-Nl-Query-Enabled: yes' \
  --header 'X-Nl-Response-Type: nl' \
  --data 'Send an email to "john.doe@example.com". Explain that we are accepting his offer for Agntcy'
```

In this example "http://localhost:8080/gmail/gmail/v1/users/me/messages/send":

- `/gmail/` is the listen path defined on the x-tyk-api-gateway part of the spec
- `gmail/v1/users/me/messages/send` is the endpoint in the specification

### Rewrite response

The third middleware function (`RewriteResponseToNl`) is responsible for
converting the API response into natural language.
It can be used standalone or in combination with the `RewriteQueryToOas` middleware.

## An example with Github

The `configs/api.github.com.gist.deref.oas.json` file is a subset of the Github API, already configured with a few `x-nl-input-examples`:

```bash
curl 'http://localhost:8080/github/' \
  --header 'Content-Type: application/nlq' \
  -d 'List the first issue for the repository named tyk owned by TykTechnologies with the label bug'
```


## An example with Sendgrid API

As a usage example, we will use the API Bridge Agnt to send email via SENGRID API.

### Prerequisites

- Get an API Key for free from sendgrid [sengrid by twilio](https://sendgrid.com/en-us)
- Retreive the open api spec here [tsg_mail_v3.json](https://github.com/twilio/sendgrid-oai/blob/main/spec/json/tsg_mail_v3.json)
- Make sure redis is running (otherwise, use `make start_redis`)
- Make sure you properly export `OPENAI_*` parameters
- Start the plugin as described on "Getting Started" section

### Update the API with tyk middleware settings

Configure Tyk to use the sendgrid API by adding the `x-tyk-api-gateway` extension:

```json
{
  "x-tyk-api-gateway": {
    "info": {
      "id": "tyk-sendgrid-id",
      "name": "Sendgrid Mail API",
      "state": {
        "active": true
      }
    },
    "upstream": {
      "url": "https://api.sendgrid.com"
    },
    "server": {
      "listenPath": {
        "value": "/sendgrid/",
        "strip": true
      }
    },
    "middleware": {
      "global": {
        "pluginConfig": {
          "data": {
            "enabled": true,
            "value": {
            }
          },
          "driver": "goplugin"
        },
        "postPlugins": [
          {
            "enabled": true,
            "functionName": "SelectAndRewrite",
            "path": "middleware/agent-bridge-plugin.so"
          },
          {
            "enabled": true,
            "functionName": "RewriteQueryToOas",
            "path": "middleware/agent-bridge-plugin.so"
          }
        ],
        "responsePlugins": [
          {
            "enabled": true,
            "functionName": "RewriteResponseToNl",
            "path": "middleware/agent-bridge-plugin.so"
          }
        ]
      }
    }
  }
}
```

You have an example of a such configuration in `configs/api.sendgrid.com.oas.json`

### Configure an endpoint to allow plugin to retrieve it

On the same oas file, add a `x-nl-input-examples` element to an endpoint with
sentence that describe how you can use the endpoint with natural language.
For example:

```json
{
  "...": "...",
  "paths": {
    "...": "...",
    "/v3/mail/send": {
      "...": "...",
      "post": {
        "...": "...",
        "x-nl-input-examples": [
          "Send an message to 'test@example.com' including a joke. Please use emojis inside it.",
          "Send an email to 'test@example.com' including a joke. Please use emojis inside it.",
          "Tell to 'test@example.com' that his new car is available.",
          "Write a profesional email to reject the candidate 'John Doe <test@example.com'"
        ]
      }
    }
  },
  "...": "..."
```

You have a configuration example here: `./configs/api.sendgrid.com.oas.json`

### Add the API to tyk configuration

Your OAS API is ready to be integrated on the Tyk plugin:

```bash
curl http://localhost:8080/tyk/apis/oas \
  --header "x-tyk-authorization: foo" \
  --header 'Content-Type: text/plain' \
  -d@configs/api.sendgrid.com.oas.json

curl http://localhost:8080/tyk/reload/group \
  --header "x-tyk-authorization: foo"
```

### Test it !

Replace "agntcy@example.com" with a sender email you have configured on your sendgrid account.

```bash
curl http://localhost:8080/sendgrid/ \
  --header "Authorization: Bearer $SENDGRID_API_KEY" \
  --header 'Content-Type: application/nlq' \
  -d 'Send a message from me (agntcy@example.com) to John Die <j.doe@example.com>. John is french, the message should be a joke using a lot of emojis, something fun about comparing France and Italy'
```

As a result, the receiver (j.doe@example.com) must receive a mail like:
```

Subject: A Little Joke for You! 🇫🇷🇮🇹

Hey John! 😄

I hope you're having a fantastic day! I just wanted to share a little joke with you:

Why did the French chef break up with the Italian chef? 🍽️❤️

Because he couldn't handle all the pasta-bilities! 🍝😂

But don't worry, they still have a "bready" good friendship! 🥖😜

Just remember, whether it's croissants or cannoli, we can all agree that food brings us together! 🍷🍰

Take care and keep smiling! 😊

Best,
agntcy

```

## An example by adding a new API from scratch

Let's say you want to add a new API to your Tyk API Gateway, and make it available over natural language. Here are the steps:

- Create or get the OpenAPI specification for your API.
- Add the `x-tyk-api-gateway` section to your OpenAPI specification.
- Add the `x-nl-input-examples` section to your OpenAPI operations.
- Configure Tyk to use this new API.
- Query your new API with natural language questions.

### Let's choose an API

Let's choose <https://openskynetwork.github.io/opensky-api>.
There is no OpenAPI specification available so we create one.

<details>
<summary>OpenSky Network OpenAPI (Click to expand)</summary>

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "OpenSky Network API",
    "description": "API for accessing flight tracking data from the OpenSky Network",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://opensky-network.org/api"
    }
  ],
  "paths": {
    "/states/all": {
      "get": {
        "operationId": "getStatesAll",
        "summary": "Get all state vectors",
        "description": "Retrieve any state vector of the OpenSky Network",
        "parameters": [
          {
            "name": "time",
            "in": "query",
            "schema": {
              "type": "integer"
            },
            "description": "Unix timestamp to retrieve states for"
          },
          {
            "name": "icao24",
            "in": "query",
            "schema": {
              "type": "string"
            },
            "description": "ICAO24 transponder address in hex"
          },
          {
            "name": "lamin",
            "in": "query",
            "schema": {
              "type": "number",
              "format": "float"
            },
            "description": "Lower bound for latitude"
          },
          {
            "name": "lomin",
            "in": "query",
            "schema": {
              "type": "number",
              "format": "float"
            },
            "description": "Lower bound for longitude"
          },
          {
            "name": "lamax",
            "in": "query",
            "schema": {
              "type": "number",
              "format": "float"
            },
            "description": "Upper bound for latitude"
          },
          {
            "name": "lomax",
            "in": "query",
            "schema": {
              "type": "number",
              "format": "float"
            },
            "description": "Upper bound for longitude"
          },
          {
            "name": "extended",
            "in": "query",
            "schema": {
              "type": "integer"
            },
            "description": "Set to 1 to include aircraft category"
          }
        ],
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StateVector"
                }
              }
            }
          }
        }
      }
    },
    "/states/own": {
      "get": {
        "operationId": "getStatesOwn",
        "summary": "Get own state vectors",
        "description": "Retrieve state vectors for authenticated user's sensors",
        "security": [
          {
            "basicAuth": []
          }
        ],
        "parameters": [
          {
            "name": "time",
            "in": "query",
            "schema": {
              "type": "integer"
            }
          },
          {
            "name": "icao24",
            "in": "query",
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "serials",
            "in": "query",
            "schema": {
              "type": "integer"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StateVector"
                }
              }
            }
          }
        }
      }
    },
    "/flights/all": {
      "get": {
        "operationId": "getFlightsAll",
        "summary": "Get flights in time interval",
        "parameters": [
          {
            "name": "begin",
            "in": "query",
            "required": true,
            "schema": {
              "type": "integer"
            }
          },
          {
            "name": "end",
            "in": "query",
            "required": true,
            "schema": {
              "type": "integer"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/Flight"
                  }
                }
              }
            }
          }
        }
      }
    },
    "/flights/aircraft": {
      "get": {
        "operationId": "getFlightsAircraft",
        "summary": "Get flights by aircraft",
        "description": "Retrieve flights for a particular aircraft within a time interval",
        "parameters": [
          {
            "name": "icao24",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string"
            },
            "description": "Unique ICAO 24-bit address of the transponder in hex string representation (lower case)"
          },
          {
            "name": "begin",
            "in": "query",
            "required": true,
            "schema": {
              "type": "integer"
            },
            "description": "Start of time interval as Unix timestamp (seconds since epoch)"
          },
          {
            "name": "end",
            "in": "query",
            "required": true,
            "schema": {
              "type": "integer"
            },
            "description": "End of time interval as Unix timestamp (seconds since epoch)"
          }
        ],
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/Flight"
                  }
                }
              }
            }
          },
          "404": {
            "description": "No flights found for the given time period"
          }
        }
      }
    },
    "/flights/arrival": {
      "get": {
        "operationId": "getFlightsArrival",
        "summary": "Get arrivals by airport",
        "description": "Retrieve flights that arrived at a specific airport within a given time interval",
        "parameters": [
          {
            "name": "airport",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string"
            },
            "description": "ICAO identifier for the airport"
          },
          {
            "name": "begin",
            "in": "query",
            "required": true,
            "schema": {
              "type": "integer"
            },
            "description": "Start of time interval as Unix timestamp (seconds since epoch)"
          },
          {
            "name": "end",
            "in": "query",
            "required": true,
            "schema": {
              "type": "integer"
            },
            "description": "End of time interval as Unix timestamp (seconds since epoch)"
          }
        ],
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/Flight"
                  }
                }
              }
            }
          },
          "404": {
            "description": "No flights found for the given time period"
          }
        }
      }
    },
    "/flights/departure": {
      "get": {
        "operationId": "getFlightsDeparture",
        "summary": "Get departures by airport",
        "description": "Retrieve flights that departed from a specific airport within a given time interval",
        "parameters": [
          {
            "name": "airport",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string"
            },
            "description": "ICAO identifier for the airport (usually upper case)"
          },
          {
            "name": "begin",
            "in": "query",
            "required": true,
            "schema": {
              "type": "integer"
            },
            "description": "Start of time interval as Unix timestamp (seconds since epoch)"
          },
          {
            "name": "end",
            "in": "query",
            "required": true,
            "schema": {
              "type": "integer"
            },
            "description": "End of time interval as Unix timestamp (seconds since epoch)"
          }
        ],
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/Flight"
                  }
                }
              }
            }
          },
          "404": {
            "description": "No flights found for the given time period"
          }
        }
      }
    },
    "/tracks": {
      "get": {
        "operationId": "getTracks",
        "summary": "Get track by aircraft",
        "description": "Retrieve the trajectory for a certain aircraft at a given time. The trajectory is a list of waypoints\ncontaining position, barometric altitude, true track and an on-ground flag.\nNote: This endpoint is experimental.\n",
        "parameters": [
          {
            "name": "icao24",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string"
            },
            "description": "Unique ICAO 24-bit address of the transponder in hex string representation (lower case)"
          },
          {
            "name": "time",
            "in": "query",
            "required": true,
            "schema": {
              "type": "integer"
            },
            "description": "Unix timestamp. Can be any time between start and end of a known flight. If time = 0, returns live track if there is any ongoing flight."
          }
        ],
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Track"
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "StateVector": {
        "type": "object",
        "properties": {
          "time": {
            "type": "integer"
          },
          "states": {
            "type": "array",
            "items": {
              "type": "array",
              "items": {
                "oneOf": [
                  {
                    "type": "string"
                  },
                  {
                    "type": "number"
                  },
                  {
                    "type": "boolean"
                  },
                  {
                    "type": "array",
                    "items": {
                      "type": "integer"
                    }
                  }
                ]
              }
            }
          }
        }
      },
      "Flight": {
        "type": "object",
        "properties": {
          "icao24": {
            "type": "string"
          },
          "firstSeen": {
            "type": "integer"
          },
          "lastSeen": {
            "type": "integer"
          },
          "callsign": {
            "type": "string"
          }
        }
      },
      "Track": {
        "type": "object",
        "properties": {
          "icao24": {
            "type": "string",
            "description": "Unique ICAO 24-bit address of the transponder in lower case hex string"
          },
          "startTime": {
            "type": "integer",
            "description": "Time of the first waypoint in seconds since epoch"
          },
          "endTime": {
            "type": "integer",
            "description": "Time of the last waypoint in seconds since epoch"
          },
          "callsign": {
            "type": "string",
            "nullable": true,
            "description": "Callsign (8 characters) that holds for the whole track"
          },
          "path": {
            "type": "array",
            "description": "Waypoints of the trajectory",
            "items": {
              "type": "array",
              "minItems": 6,
              "maxItems": 6,
              "items": {
                "oneOf": [
                  {
                    "type": "integer"
                  },
                  {
                    "type": "number"
                  },
                  {
                    "type": "number"
                  },
                  {
                    "type": "number"
                  },
                  {
                    "type": "number"
                  },
                  {
                    "type": "boolean"
                  }
                ]
              }
            }
          }
        }
      }
    },
    "securitySchemes": {
      "basicAuth": {
        "type": "http",
        "scheme": "basic"
      }
    }
  }
}
```

</details>

### Update the API and configure Tyk

Let's add the `x-tyk-api-gateway` extension. You can find more information about
it in the [Tyk OAS API Definition](https://tyk.io/docs/api-management/gateway-config-tyk-oas/).

```json
  "x-tyk-api-gateway": {
    "info": {
      "id": "tyk-opensky-network-id",
      "name": "OpenSky Network API",
      "state": {
        "active": true
      }
    },
    "upstream": {
      "url": "https://opensky-network.org/api"
    },
    "server": {
      "listenPath": {
        "value": "/opensky/",
        "strip": true
      }
    },
    "middleware": {
      "global": {
        "pluginConfig": {
          "data": {
            "enabled": true,
            "value": {}
          },
          "driver": "goplugin"
        },
        "postPlugins": [
          {
            "enabled": true,
            "functionName": "SelectAndRewrite",
            "path": "middleware/agent-bridge-plugin.so"
          },
          {
            "enabled": true,
            "functionName": "RewriteQueryToOas",
            "path": "middleware/agent-bridge-plugin.so"
          }
        ],
        "responsePlugins": [
          {
            "enabled": true,
            "functionName": "RewriteResponseToNl",
            "path": "middleware/agent-bridge-plugin.so"
          }
        ]
      }
    }
  },
```

### Configure Tyk with this new API

```shell
curl http://localhost:8080/tyk/apis/oas \
  --header "x-tyk-authorization: foo" \
  --header 'Content-Type: text/plain' \
  -d@configs/opensky_network.json

curl http://localhost:8080/tyk/reload/group --header "x-tyk-authorization: foo"
```

- Tyk is now listening on the `/opensky/` path.
- You can now query the `/opensky/` path using a natural language query, by
  adding the `application/nlq` HTTP Content-Type header, and your query as body.

```shell
curl http://localhost:8080/opensky/ \
  --header 'Content-Type: application/nlq' \
  -d 'Get flights from 12pm to 1pm on March 11th 2025'

Here are the flights that were recorded between 12 PM and 1 PM on March 11th, 2025:

1. **Flight DESET** (ICAO24: 3d34ab)
   - Departure Airport: EDEN
   - Arrival Airport: EDVK
   - First Seen: 12:54 PM
   - Last Seen: 1:03 PM
   - Horizontal Distance from Departure Airport: 9,544 meters
   - Vertical Distance from Departure Airport: 1,181 meters

2. **Flight THD120** (ICAO24: 88530e)
   - Departure Airport: VTBS
   - Arrival Airport: Not specified
   - First Seen: 12:47 PM
   - Last Seen: 12:54 PM
   - Horizontal Distance from Departure Airport: 2,237 meters
   - Vertical Distance from Departure Airport: 432 meters

[...]
```

Here is what happened behind the scenes:

1. **Content-Type Detection**: The system recognizes the `application/nlq` content type
2. **Operation Matching**:
   - Compares your query ("Get flights from 12pm to 1pm on March 11th 2025")
     against the `x-nl-input-examples` or the operation description
   - Identifies the closest matching operation (`getFlightsAll` in this case, ie `GET /flights/all`)
3. **Parameter Extraction**:
   - An LLM extracts relevant parameters from your query
   - Builds a proper API request
4. **Request Transformation**:
   - Converts the natural query to a proper HTTP request
   - Forwards the request to the upstream API (`GET /flights/all?start=1678560000&end=1678563600` for example)
5. **Response Handling**:
   - Receives the raw API response
   - Returns the JSON response with the flight data

Without any code you were able to query the OpenSky Network API and retrieve flight data.

### Improving the operation matching

When the `description` field provided in the operation definition are poorly
written or missing, it's possible to improve the selection of the operation by
providing examples of queries that should match the operation.

This is done by adding the `x-nl-input-examples` field to the operation definition.

For example, you could provide the following examples which could help improve the operation matching:

In the OpenAPI specification, add the `x-nl-output-examples` field to the operation definition:

```{code-block} json
---
lineno-start: 123
emphasize-lines: 7-11
---
{
"paths": {
  "/flights/all": {
    "get": {
      "operationId": "getFlightsAll",
      "summary": "Get flights in time interval",
      "x-nl-input-examples": [
         "Get flights from 12pm to 1pm on March 11th 2025",
         "Donne moi les vols de 12h à 13h le 11 mars 2025",
         "List of flights from 12pm to 1pm on March 11th 2025"
      ]
      "parameters": [
        {
          "name": "begin",
          "in": "query",
          "required": true,
          "schema": {
            "type": "integer"
          }
        },
        {
          "name": "end",
          "in": "query",
          "required": true,
          "schema": {
            "type": "integer"
          }
        }
      ],
      "responses": {
        "200": {
          "description": "Successful response",
          "content": {
            "application/json": {
              "schema": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/Flight"
                }
              }
            }
          }
        }
      }
    }
  }
}
```
