"""Generates src/mercypay/_resources.py (one sync and one async class per resource) from
scripts/operations.json and the API reference copy (tests/openapi.json).
Run: python3 scripts/generate.py"""
import json
import os
import re

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = json.load(open(os.path.join(root, "tests/openapi.json")))
ops = json.load(open(os.path.join(root, "scripts/operations.json")))
catalog = json.load(open(os.path.join(root, "tests/catalog.json")))
shared_params = spec["components"].get("parameters", {})


def py_type(prop):
    if "$ref" in prop:
        return "Dict[str, Any]"
    if "const" in prop:
        return f"Literal[{json.dumps(prop['const'])}]"
    t = prop.get("type", "any")
    types = t if isinstance(t, list) else [t]
    out = []
    nullable = "null" in types
    for one in types:
        if one == "string":
            enum = [e for e in prop.get("enum", []) if e is not None]
            out.append("Literal[" + ", ".join(json.dumps(e) for e in enum) + "]" if enum else "str")
        elif one == "integer":
            out.append("int")
        elif one == "number":
            out.append("float")
        elif one == "boolean":
            out.append("bool")
        elif one == "array":
            out.append(f"List[{py_type(prop.get('items', {})) if prop.get('items') else 'Any'}]")
        elif one in ("object", "any"):
            out.append("Dict[str, Any]")
    kind = out[0] if len(out) == 1 else ("Union[" + ", ".join(out) + "]" if out else "Any")
    return f"Optional[{kind}]" if nullable else kind


def params_of(definition):
    fields, groups = [], {}
    required = set()
    for p in definition.get("parameters", []):
        p = shared_params[p["$ref"].split("/")[-1]] if "$ref" in p else p
        if p["in"] != "query":
            continue
        name = p["name"][:-2] if p["name"].endswith("[]") else p["name"]
        group = re.match(r"^(\w+)\[(\w+)\]$", name)
        if group:
            groups.setdefault(group.group(1), []).append(group.group(2))
        else:
            fields.append((name, py_type(p.get("schema", {}))))
    body = definition.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
    required = set(body.get("required", []))
    for name, prop in body.get("properties", {}).items():
        fields.append((name, py_type(prop)))
    for group in groups:
        fields.append((group, "Dict[str, str]"))
    return fields, required

summary, is_list = {}, {}
for path, methods in spec["paths"].items():
    for verb, d in methods.items():
        ok = next((r for s, r in d["responses"].items() if s.startswith("2")), {})
        schema = ok.get("content", {}).get("application/json", {}).get("schema", {})
        summary[d["operationId"]] = d.get("summary", "")
        is_list[d["operationId"]] = schema.get("properties", {}).get("object", {}).get("const") == "list" or schema.get("properties", {}).get("data", {}).get("type") == "array"


def snake(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def attribute(service):
    base = service if service in ("Account", "ProviderStatus", "BillingPortal") else service + "s"
    return snake(base)


definitions = {d["operationId"]: d for methods in spec["paths"].values() for d in methods.values()}


def pascal(name):
    return name[0].upper() + name[1:]


plines = ['"""Généré par scripts/generate.py depuis la référence de l\'API. Ne pas modifier à la main.', "", "What each operation accepts, for your editor and your type checker.", '"""', "",
          "from typing import Any, Dict, List, Literal, Optional, Union", "", "from typing_extensions import Required, TypedDict", "", ""]
for o in ops:
    fields, required = params_of(definitions[o["operationId"]])
    entries = ", ".join(f'"{n}": ' + (f"Required[{t}]" if n in required else t) for n, t in fields)
    plines.append(f'{pascal(o["operationId"])}Params = TypedDict("{pascal(o["operationId"])}Params", {{{entries}}}, total=False)')
    plines.append("")
open(os.path.join(root, "src/mercypay/_params.py"), "w").write("\n".join(plines).rstrip() + "\n")

countries = catalog["countries"]
clines = ['"""Généré par scripts/generate.py depuis le catalogue Mercy Pay. Ne pas modifier à la main.', "",
          "The open countries, their mobile money operators and the webhook event types. A new operator",
          "may appear before this list knows it: any code stays accepted.", '"""', "",
          "from typing import Dict, List", "", ""]
clines.append("COUNTRIES: Dict[str, Dict[str, object]] = " + json.dumps({c["code"]: {"name": c["name"], "currency": c["currency"], "providers": {p["code"]: p["name"] for p in c["providers"]}} for c in countries}, ensure_ascii=False, indent=4))
clines.append("")
clines.append("EVENT_TYPES: List[str] = " + json.dumps(catalog["event_types"], indent=4))
clines.append("")
for c in countries:
    for p in c["providers"]:
        clines.append(f'{p["code"]} = "{p["code"]}"')
open(os.path.join(root, "src/mercypay/catalog.py"), "w").write("\n".join(clines).rstrip() + "\n")

services = {}
for o in ops:
    services.setdefault(o["service"], []).append(o)

lines = ['"""Généré par scripts/generate.py depuis la référence de l\'API. Ne pas modifier à la main."""', "",
         "from typing import TYPE_CHECKING, Any, Optional", "", "from typing_extensions import Unpack", "", "from . import _params", "from ._helpers import WaitMixin, AsyncWaitMixin",
         "from ._client import encode_id", "from ._object import MercyPayObject", "from ._page import AsyncPage, Page", "",
         "if TYPE_CHECKING:", "    from ._client import AsyncTransport, SyncTransport", "", ""]

for asynchronous in (False, True):
    for service, items in services.items():
        cls = ("Async" if asynchronous else "") + attribute(service).title().replace("_", "") + "Resource"
        transport = "AsyncTransport" if asynchronous else "SyncTransport"
        extras = os.path.join(root, "scripts/extras", f"{cls}.py")
        mixin = ("AsyncWaitMixin" if asynchronous else "WaitMixin") if os.path.exists(extras) else ""
        lines.append(f"class {cls}({mixin}):" if mixin else f"class {cls}:")
        lines.append(f'    def __init__(self, transport: "{transport}") -> None:')
        lines.append("        self._transport = transport")
        lines.append("")
        for o in items:
            method = "list" if o["method"] == "all" else snake(o["method"])
            ids = [snake(i) for i in o["ids"]]
            args = ["self"] + [f"{i}: str" for i in ids]
            post = o["http"] == "POST"
            if post:
                args.append("*")
                args.append("idempotency_key: Optional[str] = None")
            args.append(f"**params: Unpack[_params.{pascal(o['operationId'])}Params]")
            path = ("f\"" + re.sub(r"\{\}", lambda m, it=iter(ids): "{encode_id(" + next(it) + ")}", o["path"]) + "\"") if ids else json.dumps(o["path"])
            listing = is_list[o["operationId"]]
            page = ("AsyncPage" if asynchronous else "Page") if listing else "MercyPayObject"
            prefix = "async " if asynchronous else ""
            wait = "await " if asynchronous else ""
            lines.append(f"    {prefix}def {method}({', '.join(args)}) -> {page}:")
            lines.append(f'        """{summary[o["operationId"]]}. {o["http"]} /api/v1/{o["path"].replace("{}", "{id}")}"""')
            if listing:
                lines.append(f"        return {wait}self._list({path}, params)")
            else:
                key = ", idempotency_key" if post else ", None"
                lines.append(f"        body = {wait}self._transport.request(\"{o['http']}\", {path}, params{key})")
                lines.append("        return MercyPayObject(body.get(\"data\", body) if isinstance(body.get(\"data\", body), dict) else {})")
            lines.append("")
        if os.path.exists(extras):
            lines += [line.rstrip() for line in open(extras).read().rstrip().splitlines()] + [""]
        if any(is_list[o["operationId"]] for o in items):
            if asynchronous:
                lines += [f"    async def _list(self, path: str, params: Any) -> AsyncPage:",
                          "        body = await self._transport.request(\"GET\", path, params)",
                          "",
                          "        async def fetch(next_params: Any) -> AsyncPage:",
                          "            return await self._list(path, next_params)",
                          "",
                          "        return AsyncPage(body, fetch, dict(params))", ""]
            else:
                lines += [f"    def _list(self, path: str, params: Any) -> Page:",
                          "        body = self._transport.request(\"GET\", path, params)",
                          "        return Page(body, lambda next_params: self._list(path, next_params), dict(params))", ""]
        lines.append("")

attrs = [(attribute(s), attribute(s).title().replace("_", "") + "Resource") for s in services]
open(os.path.join(root, "src/mercypay/_resources.py"), "w").write("\n".join(lines).rstrip() + "\n")
open(os.path.join(root, "scripts/attributes.json"), "w").write(json.dumps(attrs, indent=1))
print(len(services), "resources,", len(ops), "operations")
