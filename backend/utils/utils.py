from flask import abort

from backend.models.currency import Currency
from backend.models.expense import Expense
from backend.models.tricount import Tricount
from backend.models.user import User
from backend.services.balance import compute_balances
from backend.services.settlement import compute_settlements


def tricount_to_dict(tricount: Tricount) -> dict:
    return {
        "id": tricount.id,
        "owner_auth_id": tricount.owner_auth_id,
        "name": tricount.name,
        "currency": tricount.currency.value,
        "users": [
            {
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "auth_id": u.auth_id,
            }
            for u in tricount.users
        ],
        "expenses": [
            {
                "id": e.id,
                "description": e.description,
                "amount": e.amount,
                "currency": e.currency.value,
                "payer_id": e.payer_id,
                "participants_ids": e.participants_ids,
                "weights": e.weights,
            }
            for e in tricount.expenses
        ],
    }


def tricount_from_dict(data: dict) -> Tricount:
    tricount = Tricount(
        id=data["id"],
        owner_auth_id=data.get("owner_auth_id", ""),
        name=data["name"],
        currency=Currency(data["currency"]),
    )

    for u in data.get("users", []):
        user = User(
            id=u["id"],
            name=u["name"],
            email=u.get("email"),
            auth_id=u.get("auth_id"),
        )
        tricount.users.append(user)

    for e in data.get("expenses", []):
        expense = Expense(
            id=e["id"],
            description=e["description"],
            amount=e["amount"],
            currency=Currency(e["currency"]),
            payer_id=e["payer_id"],
            participants_ids=e["participants_ids"],
            weights=e.get("weights", {}),
        )
        tricount.expenses.append(expense)

    return tricount


def get_tricount_from_id(
    tricount_id: str, tricounts: list[Tricount]
) -> Tricount:
    t = next((t for t in tricounts if t.id == tricount_id), None)
    if not t:
        abort(404, "Not found")

    return t


def get_tricount_from_id_with_permissions(
    tricount_id: str,
    tricounts: list[Tricount],
    user_auth_id: str,
    owner_needed: bool = False,
) -> Tricount:
    t = get_tricount_from_id(tricount_id, tricounts=tricounts)

    if not (
        t.owner_auth_id == user_auth_id
        or (
            any(u.auth_id == user_auth_id for u in t.users)
            and not owner_needed
        )
    ):
        abort(403, "Forbidden")

    return t


def tricount_with_balances_to_dict(tricount: Tricount) -> dict:
    balances = compute_balances(tricount)
    settlements_raw = compute_settlements(balances)

    return {
        "id": tricount.id,
        "name": tricount.name,
        "currency": tricount.currency.value,
        "users": [
            {
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "auth_id": u.auth_id,
            }
            for u in tricount.users
        ],
        "expenses": [
            {
                "id": e.id,
                "description": e.description,
                "amount": e.amount,
                "currency": e.currency.value,
                "payer_id": e.payer_id,
                "participants_ids": e.participants_ids,
                "weights": e.weights,
            }
            for e in tricount.expenses
        ],
        "balances": balances,
        "settlements": [
            {"from": f, "to": t, "amount": amount}
            for (f, t, amount) in settlements_raw
        ],
    }
