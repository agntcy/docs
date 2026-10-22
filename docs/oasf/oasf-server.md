# Open Agentic Schema Framework Server

The Open Agentic Schema Framework (OASF) schema server is an HTTP server that
provides a convenient way to browse and use the OASF schema.
It also validates records and objects against the schema, which is useful
during development.

You can access the OASF schema server, which is running the latest released
schema, at [schema.oasf.outshift.com](https://schema.oasf.outshift.com).

The server source code and its Helm chart live in
[agntcy/oasf-server](https://github.com/agntcy/oasf-server), and the schema in
[agntcy/oasf](https://github.com/agntcy/oasf).
The server is versioned independently of the schema, and one server release
serves every supported schema version.
See the
[changelog](https://github.com/agntcy/oasf-server/blob/main/CHANGELOG.md) for
the schema versions each release supports.

## Artifacts

| Artifact | Location |
| --- | --- |
| Server image | `ghcr.io/agntcy/oasf-server:<server version>`, for example `v2.0.0` |
| Schema images | `ghcr.io/agntcy/oasf-schema:<schema version>`, for example `1.1.0` |
| Helm chart | `oci://ghcr.io/agntcy/oasf-server/helm-charts/oasf` |

The server image does not contain a schema: mount one at `/app/schema`, from a
schema image or from a local directory.
Schema images contain only the schema, under `/schema`.

Server images up to `v1.x` bundled a single schema version, for example
`ghcr.io/agntcy/oasf-server:v1.1.3` for schema 1.1.0.
They remain available, but no longer receive fixes.
Schema 0.7.0 is deprecated: server `v2` and later don't support it, and it is
no longer served at schema.oasf.outshift.com.

## Run the Server Locally

To preview schema changes, run the pinned server release against your local
checkout of [agntcy/oasf](https://github.com/agntcy/oasf):

```shell
git clone https://github.com/agntcy/oasf.git
cd oasf
task server:up
```

The server serves the local `schema/` directory at
[`localhost:8080`](http://localhost:8080).
Run `task server:reload` in another terminal to reload the schema whenever a
file under `schema/` changes, and `task server:down` to stop the server.

To run a released schema with Docker, copy the schema image into a volume and
mount that volume in the server:

```shell
docker run --rm -v oasf-schema:/app/schema ghcr.io/agntcy/oasf-schema:1.1.0 cp -R /schema/. /app/schema
docker run --rm -p 8080:8080 -v oasf-schema:/app/schema:ro ghcr.io/agntcy/oasf-server:v2.0.0
```

## Deploy with Helm

The `oasf` chart runs one server per schema version, all from the same server
image, each with its schema mounted from an `oasf-schema` image:

```yaml
image:
  repository: ghcr.io/agntcy/oasf-server
  tag: v2.0.0
schema:
  mount: initContainer # or imageVolume, on Kubernetes 1.35+
  versions:
    - schema: 1.1.0
      default: true
    - schema: 1.0.0
    - schema: 0.8.0
```

```shell
helm install oasf oci://ghcr.io/agntcy/oasf-server/helm-charts/oasf -f values.yaml
```

Each version is served under `/<version>/`, `/api/<version>/`,
`/schema/<version>/` and `/sample/<version>/`, and the default version also
without the version segment.
To upgrade the server, change `image.tag`; no new chart release is needed.

Chart `v1.x`, published as `oci://ghcr.io/agntcy/oasf/helm-charts/oasf`, ran a
different server image per schema version from `image.versions`.
Chart `v2` replaces it with `schema.versions`, as above.

## Develop the Server

To build, test and deploy the server itself, for example in a local Kind
cluster with `task up`, see the
[oasf-server README](https://github.com/agntcy/oasf-server/blob/main/README.md).

## Protocol Buffer Definitions

The [`proto`](https://github.com/agntcy/oasf/tree/main/proto) directory of
agntcy/oasf contains the Protocol Buffer (`.proto`) files defining our data
objects and APIs.
The full proto module, generated language stubs and its versions are hosted at
the Buf Schema Registry:
[https://buf.build/agntcy/oasf](https://buf.build/agntcy/oasf)
