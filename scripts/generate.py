"""Generates src/mercypay/_resources.py (one sync and one async class per resource) from
scripts/operations.json and the API reference copy (tests/openapi.json).
Run: python3 scripts/generate.py"""
import json
import os
import re

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = json.load(open(os.path.join(root, "tests/openapi.json")))
ops = json.load(open(os.path.join(root, "scripts/operations.json")))

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


services = {}
for o in ops:
    services.setdefault(o["service"], []).append(o)

lines = ['"""Généré par scripts/generate.py depuis la référence de l\'API. Ne pas modifier à la main."""', "",
         "from typing import TYPE_CHECKING, Any, Optional", "",
         "from ._client import encode_id", "from ._object import MercyPayObject", "from ._page import AsyncPage, Page", "",
         "if TYPE_CHECKING:", "    from ._client import AsyncTransport, SyncTransport", "", ""]

for asynchronous in (False, True):
    for service, items in services.items():
        cls = ("Async" if asynchronous else "") + attribute(service).title().replace("_", "") + "Resource"
        transport = "AsyncTransport" if asynchronous else "SyncTransport"
        lines.append(f"class {cls}:")
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
            args.append("**params: Any")
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
