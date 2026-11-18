# Mercy Pay pour Python

La bibliothèque Python officielle de l'API [Mercy Pay](https://mercy-pay.com) : paiements mobile money et carte. Python 3.10 ou plus, un client synchrone et un client `async`.

```sh
pip install mercy-pay
```

Sur Django, prenez aussi [`mercy-pay-django`](https://github.com/mercy-pay/mercy-pay-django) pour recevoir les webhooks.

## Encaisser un paiement

```python
import os
from mercypay import MercyPay

mercy_pay = MercyPay(os.environ["MERCY_PAY_API_KEY"])

session = mercy_pay.checkout_sessions.create(
    amount=15000,
    currency="XAF",
    description="Commande 4821",
    success_url="https://boutique.example/merci",
    metadata={"order_id": "4821"},
    idempotency_key="order-4821",
)

# Redirigez le client vers session.checkout_url
```

Les montants sont en unités mineures. Chaque objet est un `dict` dont les champs se lisent aussi en attribut : `session.status` ou `session["status"]`.

Avec `asyncio` (FastAPI, aiohttp…) :

```python
from mercypay import AsyncMercyPay

async with AsyncMercyPay(os.environ["MERCY_PAY_API_KEY"]) as mercy_pay:
    payment = await mercy_pay.payments.retrieve("pay_…")
```

## Recevoir les webhooks

```python
from mercypay import SignatureVerificationError, construct_event

# FastAPI
@app.post("/webhooks/mercy-pay")
async def webhook(request: Request):
    try:
        event = construct_event(await request.body(), request.headers.get("MercyPay-Signature"), os.environ["MERCY_PAY_WEBHOOK_SECRET"])
    except SignatureVerificationError:
        raise HTTPException(status_code=400)

    if event.type == "payment.succeeded":
        mark_order_paid(event.data.metadata["order_id"])
    return {"received": True}
```

Passez le corps brut, avant tout décodage JSON. Un même événement peut arriver deux fois : servez-vous de `event.id`.

## Listes

```python
for payment in mercy_pay.payments.list(limit=100, status="succeeded").auto_paging_iter():
    ...  # toutes les pages, chargées au fur et à mesure

page = mercy_pay.payouts.list(limit=20)
page.data, page.has_more
```

En `async` : `async for payment in (await mercy_pay.payments.list()).auto_paging_iter()`.

## Erreurs

```python
from mercypay import ConnectionError, InvalidRequestError, PaymentError

try:
    mercy_pay.payouts.create(**params, idempotency_key=f"payout-{payout_id}")
except InvalidRequestError as error:
    error.code   # validation_failed, insufficient_balance…
    error.param  # le champ en cause
except PaymentError:
    ...  # refusé par l'opérateur ou la banque
except ConnectionError:
    ...  # pas de réponse : relancez avec la même idempotency_key
```

Toutes les erreurs de l'API héritent de `ApiError` (`status`, `type`, `code`, `param`, `request_id`, `errors`). Fiez-vous à `code`, pas au message.

## Nouvelles tentatives et idempotence

Une coupure réseau, un `429` ou une erreur `5xx` sont retentés deux fois. Chaque `POST` porte une `Idempotency-Key`, la même à chaque tentative : un paiement ou un retrait n'est jamais créé en double. Passez la vôtre avec `idempotency_key=` pour couvrir aussi vos propres relances.

## Options

```python
MercyPay(api_key, timeout=30.0, max_retries=2, http_client=httpx.Client(proxy="…"))
```

## Paramètres typés

Chaque méthode décrit les arguments que l'API accepte (`TypedDict`) : votre éditeur les propose, et mypy ou Pyright signalent un argument obligatoire oublié ou une valeur inconnue. Les opérateurs, les pays et les types d'événements sont dans `mercypay.catalog` :

```python
from mercypay import catalog

mercy_pay.payments.create(
    amount=1000,
    currency="XAF",
    country="CMR",
    provider=catalog.MTN_MOMO_CMR,
    phone="237653456789",
    idempotency_key="order-4821",
)
```

## Attendre le résultat

Pour un script ou un test, attendez qu'un paiement ait un statut final :

```python
payment = mercy_pay.payments.wait_for_final_status(payment_id, timeout=60)
session = mercy_pay.checkout_sessions.wait_for_completion(session_id)
```

La lecture se répète, de plus en plus espacée. Passé le délai, `WaitTimeoutError` donne le dernier état dans `last`. Sur un serveur en production, préférez le webhook `payment.succeeded`.

## Sandbox

Une clé `mp_sandbox_…` ne touche pas à l'argent réel.

```python
# Le numéro de test qui produit ce résultat :
phone = mercy_pay.test_helpers.mobile_money_number(catalog.ORANGE_CMR, "insufficient_balance")
```

Les résultats possibles : `succeeded`, `pending`, `payout_failed`, ou un `failure_code` comme `insufficient_balance`. `mercy_pay.test_helpers.trigger_event(type="payment.succeeded")` envoie un événement de test à vos endpoints, et la [CLI](https://docs.mercy-pay.com/developers/cli) relaie les webhooks vers votre ordinateur.

## Développement

```sh
python -m venv .venv && .venv/bin/pip install -e ".[test]"
.venv/bin/pytest
```

`tests/openapi.json` est une copie de la référence de l'API : `python3 scripts/generate.py` régénère les ressources, et un test vérifie que chaque endpoint a sa méthode.
