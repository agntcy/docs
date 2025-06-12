# Getting Started with API Bridge Agent

For a detailed description on the API Bridge Agent, see [API Bridge Agent documentation](../tools/api_bridge_agent.md).

### Prerequisites

To build the plugin you need the following dependencies:
- Go
- CMake
- Git
- jq

Get the source code by running the following command:

```
git clone https://github.com/agntcy/api-bridge-agnt
```

Tyk requires also a Redis database. Deploy it with the following command:

```shell
make start_redis
```

### Local Development

Built with:

- [Search](https://github.com/kelindar/search) for the semantic router.
- [Tyk](https://github.com/TykTechnologies/tyk.git) for the gateway.
We use these dependencies inside the project. However, you don't need to download it or to build it,
everything is managed by the Makefile.

#### Set Environment Variables

For OpenAI:

```shell
export OPENAI_API_KEY=REPLACE_WITH_YOUR_KEY
export OPENAI_MODEL=gpt-4o-mini
```

For Azure OpenAI:

```shell
export OPENAI_API_KEY=REPLACE_WITH_YOUR_KEY
export OPENAI_ENDPOINT=https://REPLACE_WITH_YOUR_ENDPOINT.openai.azure.com
export OPENAI_MODEL=gpt-4o-mini
```

#### Build the Plugin and Start Tyk Locally on [Tyk](http://localhost:8080)

Dependencies are managed so that you can just run:

```shell
make start_tyk
```

This will automatically build "Tyk", "search" and the plugin, then install the plugin and start Tyk gateway.

#### Load and Configure Tyk with an Example API (httpbin.org)

```shell
make load_plugin
```

### Other Installation

#### Linux

For Linux (Ubuntu) you can use:

```shell
TARGET_OS=linux TARGET_ARCH=amd64 SEARCH_LIB=libllama_go.so make start_tyk
```

#### Individual Steps for Building if Needed:

If you need to decompose each task individually, you can split into:

```shell
make build_tyk          # build tyk
make build_search_lib   # build the "search" library, used as semantic router
make build_plugin       # build the plugin
make install_plugin     # Install the plugin
```

## Tyk Configuration

This plugin relies on [Tyk OAS API Definition](https://tyk.io/docs/api-management/gateway-config-tyk-oas/).

You need to apply some configuration when:
- you add a new service
- you want to activate the new cross-api interface
- you want to activate the mcp interface
- you add the support for a new MCP server

### Adding a new Service

Add the plugin to the `postPlugins` and `responsePlugins` sections of the `x-tyk-api-gateway` section:

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

Then add your OpenAPI specification:

For example, adding the httpbin.org service can be done using the `configs/httpbin.org.oas.json` file.

```shell
curl http://localhost:8080/tyk/apis/oas \
  --header "x-tyk-authorization: foo" \
  --header 'Content-Type: text/plain' \
  -d@configs/httpbin.org.oas.json

curl http://localhost:8080/tyk/reload/group \
  --header "x-tyk-authorization: foo"
```

It's then possible to do a query like this:

```shell
curl http://localhost:8080/httpbin/json \
  --header "X-Nl-Query-Enabled: yes" \
  --header "X-Nl-Response-Type: nl" \
  --header "Content-Type: text/plain" \
  -d "Hello"
```

In this example `http://localhost:8080/httpbin/json`:

- "/httpbin/" is the listen path defined on the `x-tyk-api-gateway` part of the specification
- "json" is the endpoint on the specification

### Activate the new Cross-API interface

The new Cross-API interface, available at the `/aba/` endpoint, is not activated by default.

To activate it, use the provided `configs/api-bridge-agent.oas.json` file:
then restart

```shell
curl http://localhost:8080/tyk/apis/oas \
  --header 'x-tyk-authorization: foo' \
  --header 'Content-Type: text/plain' \
  -d@configs/api-bridge-agent.oas.json

curl http://localhost:8080/tyk/reload/group --header 'x-tyk-authorization: foo'
```

It's then possible to do a query like this:

```shell
curl http://localhost:8080/aba/ \
  --header "Content-Type: application/nlq" \
  -d "Send email to <john.doe@gmail.com>. The content is 'Hello from Mr Smith', The subject is 'This is a test' and the reply-to address is <mr.smith@gmail.com>. No BCC, no CC"
```

If you have a service that support action to send an email, the Cross-API interface will route this request to that service.
Otherwise, a "404 Not found" will be answered.

Note: it is possible to change the listen path `/aba/` by editing the `configs/api-bridge-agent.oas.json` file before activate it.

### Activate the new MCP interface

The new MCP interface, available across the `/mcp/` endpoint, is not activated by default.

To activate it, use the provided `configs/mcp.oas.json` file

```shell
curl http://localhost:8080/tyk/apis/oas \
  --header 'x-tyk-authorization: foo' \
  --header 'Content-Type: text/plain' \
  -d@configs/mcp.oas.json

curl http://localhost:8080/tyk/reload/group --header 'x-tyk-authorization: foo'

curl http://localhost:8080/mcp/init
```

Note: do not change the listen path `/mcp/` on the `configs/mcp.oas.json` file. It is used internally.

### Adding support for a new MCP server

You have to edit the `configs/mcp.oas.json` file, then reload the Tyk configuration.

Inside the `configs/mcp.oas.json` file, add the new MCP server to the `mcpServers` list.
A valid configuration need a `command` and `args`, or a SSE address. This is some examples of such configuration:

```json
"mcpServers": {
  "weather": {
    "command": "poetry",
    "args": [
      "run",
      "python",
      "../../../mcp/weather/weather.py"
    ]
  },
  "git": {
    "command": "poetry",
    "args": [
      "run",
      "python",
      "../../../mcp/servers/git/src/mcp_server_git/server.py",
      "--repository",
      "/media/sf_vmshared/my_repository"
    ]
  },
  "github": {
    "command": "docker",
    "args": [
      "run",
      "-i",
      "--rm",
      "-e",
      "GITHUB_PERSONAL_ACCESS_TOKEN",
      "ghcr.io/github/github-mcp-server"
    ],
    "env": ["GITHUB_PERSONAL_ACCESS_TOKEN=${GITHUB_PERSONAL_ACCESS_TOKEN}"]
  },
  "resend": {
    "command": "node",
    "args": [
      ".../mcp/mcp-send-email/build/index.js",
      "--key=<MAY KEY>",
      "--sender=john.doe@resend.dev"
    ]
  },
  "weather-sse": {
    "sse": "http://127.0.0.1:8000/sse"
  },
}
```

then refresh Tyk with the new configuration:

```shell
curl http://localhost:8080/tyk/apis/oas \
  --header 'x-tyk-authorization: foo' \
  --header 'Content-Type: text/plain' \
  -d@configs/mcp.oas.json

curl http://localhost:8080/tyk/reload/group --header 'x-tyk-authorization: foo'

curl http://localhost:8080/mcp/init
```

### Using API Bridge Agent

When using API Bridge Agent, you *MUST* use the content type `application/nlq` on your request

```shell
curl http://localhost:8080/aba/ \
  --header "Content-Type: application/nlq" \
  -d "Send email to <john.doe@gmail.com>. The content is "Hello from Mr Smith", The subject is "This is a test" and
  the reply-to address is <mr.smith@gmail.com>. No BCC, no CC"
```

## An Example with Github

The `configs/api.github.com.gist.deref.oas.json` file is a subset of the Github API, already configured with a few `x-nl-input-examples`:

```shell
curl 'http://localhost:8080/github/' \
  --header 'Content-Type: application/nlq' \
  -d 'List the first issue for the repository named tyk owned by TykTechnologies with the label bug'
```


## An Example with Sendgrid API

As a usage example, we will use the API Bridge Agent to send email via SENGRID API.

### Prerequisites

- Get an API Key for free from sendgrid [sengrid by twilio](https://sendgrid.com/en-us).
- Retreive the open api spec here [tsg_mail_v3.json](https://github.com/twilio/sendgrid-oai/blob/main/spec/json/tsg_mail_v3.json).
- Make sure redis is running (otherwise, use `make start_redis`).
- Make sure you properly export `OPENAI_*` parameters.
- Start the plugin as described on "Getting Started" section.

### Update the API with Tyk middleware settings

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

### Configure an Endpoint to Allow Plugin to Retrieve It

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

### Add the API to Tyk configuration

Your OAS API is ready to be integrated on the Tyk plugin:

```shell
curl http://localhost:8080/tyk/apis/oas \
  --header "x-tyk-authorization: foo" \
  --header 'Content-Type: text/plain' \
  -d@configs/api.sendgrid.com.oas.json

curl http://localhost:8080/tyk/reload/group \
  --header "x-tyk-authorization: foo"
```

### Test It!

Replace "agntcy@example.com" with a sender email you have configured on your sendgrid account.

```shell
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

1. **Content-Type Detection**: The system recognizes the `application/nlq` content type.
2. **Operation Matching**:
   - Compares your query ("Get flights from 12pm to 1pm on March 11th 2025")
     against the `x-nl-input-examples` or the operation description.
   - Identifies the closest matching operation (`getFlightsAll` in this case, ie `GET /flights/all`).
3. **Parameter Extraction**:
   - An LLM extracts relevant parameters from your query.
   - Builds a proper API request.
4. **Request Transformation**:
   - Converts the natural query to a proper HTTP request.
   - Forwards the request to the upstream API (`GET /flights/all?start=1678560000&end=1678563600` for example).
5. **Response Handling**:
   - Receives the raw API response.
   - Returns the JSON response with the flight data.

Without any code you were able to query the OpenSky Network API and retrieve flight data.

### Improving the Operation Matching

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

## An Example with a new MCP Server

In this exemple, we have already activated MCP support
We want to add a new MCP server (weather) in addition to the existing one (the default one) github.

1- create a MCP server

create a folder `mcp-weather`, then inside this folder create a file `weather.py` and copy paste the following content:

<details>
<summary>weather.py content (Click to expand)</summary>

```python
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

```

</details>

Then, still inside the `mcp-weather` folder, create a file `pyproject.toml` with content:

```
[project]
name = "weather"
version = "0.1.0"
description = "A simple MCP weather server"
requires-python = ">=3.10"
dependencies = [
    "httpx>=0.28.1",
    "mcp[cli]>=1.2.0",
]

[build-system]
requires = [ "hatchling",]
build-backend = "hatchling.build"

[project.scripts]
weather = "weather:main"

```

Use poetry to install dependencies.

```shell
poetry install
```

2- update the API Bridge Agent configuration. Add the following "weather" entry on the mcpServers list inside the `configs/mcp.oas.json` file:

```json
              "mcpServers": {
                ...
                "weather": {
                  "command": "poetry",
                  "args": [
                    "run",
                    "python",
                    "<path_to>/mcp-weather/weather.py"
                  ]
                }
              }
```

3- reload the config

```shell
curl http://localhost:8080/tyk/apis/oas \
  --header 'x-tyk-authorization: foo' \
  --header 'Content-Type: text/plain' \
  -d@configs/mcp.oas.json

curl http://localhost:8080/tyk/reload/group --header 'x-tyk-authorization: foo'

curl http://localhost:8080/mcp/init
```

4- You can request API Bridge Agent with

```shell
curl 'http://localhost:8080/mcp/'  \
  --header 'Content-Type: application/nlq'  \
  -d "give me the weather forecast in california"
```

and you will receive a response that looks like
```
Here's the weather forecast for California:

### Today:
- **Temperature:** 66°F
- **Wind:** 5 mph S
- **Forecast:** A slight chance of rain after 5 PM. Partly sunny. High near 66, with temperatures falling to around 64 in the afternoon. Chance of precipitation is 20%. New rainfall amounts less than a tenth of an inch possible.

### Tonight:
- **Temperature:** 48°F
- **Wind:** 0 to 5 mph ENE
- **Forecast:** A chance of rain. Mostly cloudy. Low around 48, with temperatures rising to around 50 overnight. Chance of precipitation is 50%. New rainfall amounts less than a tenth of an inch possible.

### Saturday:
- **Temperature:** 60°F
- **Wind:** 0 to 5 mph SSW
- **Forecast:** A chance of rain before 11 AM, then showers and thunderstorms likely between 11 AM and 5 PM, then a chance of rain. Mostly cloudy, with a high near 60. Chance of precipitation is 70%. New rainfall amounts between a tenth and quarter of an inch possible.

### Saturday Night:
- **Temperature:** 48°F
- **Wind:** 0 to 5 mph NE
- **Forecast:** A chance of rain before 5 AM. Mostly cloudy, with a low around 48. Chance of precipitation is 50%. New rainfall amounts less than a tenth of an inch possible.

### Sunday:
- **Temperature:** 65°F
- **Wind:** 0 to 5 mph SW
- **Forecast:** Partly sunny, with a high near 65.

```
