# Week 2 — Distributed Tracing

## Class Summary Tasks

## Honeycomb.io

Instrument our backend flask application to use Open Telemetry (OTEL) with Honeycomb.io as the provider

> For implementation our OTEL to backend using [Installation instraction OTEL for Python](https://docs.honeycomb.io/getting-data-in/opentelemetry/python/)

Just add to `requirements.txt` following line of code, notice we working with `/backend-flask/` directory 

```sh
opentelemetry-api 
opentelemetry-sdk 
opentelemetry-exporter-otlp-proto-http 
opentelemetry-instrumentation-flask 
opentelemetry-instrumentation-requests
```

> Install this dependencies

```sh
pip install -r requirements.txt
```

> Next add this line to `app.py` 

```sh
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
```

> Initialize tracing and an exporter that can send data to Honeycomb

```sh
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
```

> Initialize automatic instrumentation with Flask

```sh
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
```

> Add following ENV VARIABLES to our `docker-compose.yml`

```sh
OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"
OTEL_SERVICE_NAME: "${HONEYCOMB_SERVICE_NAME}"
```

> Grab your [API KEY](assets/api-key-honeycomb.jpg) and export to the ENV VAR

```sh
export HONEYCOMB_API_KEY="<your API key>"
export HONEYCOMB_SERVICE_NAME="Cruddur"
gp env HONEYCOMB_API_KEY="<your API key>"
gp env HONEYCOMB_SERVICE_NAME="Cruddur"
```

> Up your application with `docker-compose.yml"

```sh
docker compose up
```

> Go `PORT` tab make public ports `3000, 4567`, go 4567 link, paste at the end URL `/api/activities/home`

Update your page few times for generate some data

> If All is Fine you should get some spans

![Honeycomb.io data](assets/1_home-activity-span.jpg)

> Adding Attributes and Nested Spans

For getting information, for example, how your services is working when recieving api call and how long it lasted

```sh
...

with tracer.start_as_current_span("home-activities-data") as outer_span:
    outer_span.set_attribute("outer", True)
    span = trace.get_current_span()
    span.set_attribute("app.hubabuba", now.isoformat())
    ...
    
    with tracer.start_as_current_span("home-result-activities") as inner_span:
        inner_span.set_attribute("inner", True)
        span = trace.get_current_span()
        span.set_attribute("app.hubabuba", now.isoformat())
    ...
# `return results` end your home_activities.py service file
```

> If you generate new data you'll get sub spans with attribute value

![Nested Spans](assets/2_home-activity-nested-span.jpg)