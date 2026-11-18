# Journal des changements

## 0.2.0 (18 novembre 2026)

- Arguments typés pour chaque méthode (`TypedDict`), générés depuis la référence de l'API. Nouvelle dépendance : `typing-extensions`.
- Nouveau : `mercy_pay.embed_domains`, pour les sites autorisés du paiement intégré.
- Nouveau : `mercypay.catalog` (pays, opérateurs, types d'événements).
- Nouveau : `payments.wait_for_final_status()` et `checkout_sessions.wait_for_completion()`, aussi en async.
- Nouveau : `test_helpers.mobile_money_numbers()` et `test_helpers.mobile_money_number()`.

## 0.1.0 (16 novembre 2026)

- Première version : client pour toute l'API v1, pagination, erreurs typées, nouvelles tentatives et vérification des webhooks.
