import pytest
import requests
from playwright.sync_api import sync_playwright
from config import BASE_URL, EMAIL, PASSWORD


# ---------------- UI FIXTURES ----------------

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headed mode
        yield browser
        browser.close()


@pytest.fixture()
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture()
def login(page):
    page.goto(BASE_URL)
    page.get_by_role("link", name="Вхід").click()
    page.get_by_role("textbox", name="Email").fill(EMAIL)
    page.get_by_role("textbox", name="Пароль").fill(PASSWORD)
    page.get_by_role("button", name="Увійти").click()
    return page


# ---------------- API FIXTURES ----------------

@pytest.fixture(scope="session")
def auth_token():
    """Отримує токен авторизації через API e-tender"""
    url = "https://stg-api.e-tender.ua/api/TokenAuth/Authenticate"  # фіксований API endpoint
    headers = {"Content-Type": "application/json"}
    payload = {
        "userNameOrEmailAddress": EMAIL,
        "password": PASSWORD
    }

    response = requests.post(url, json=payload, headers=headers)
    print(f"🔹 Auth status: {response.status_code}")
    print(f"🔹 Response body: {response.text[:300]}")  # для дебагу

    if response.status_code != 200:
        raise Exception(f"❌ Auth failed ({response.status_code}): {response.text}")

    token = response.json().get("result", {}).get("accessToken")
    if not token:
        raise ValueError("Auth token not found in response")

    print(f"✅ Auth token отримано: {token[:20]}...")
    return token


@pytest.fixture()
def create_tender(auth_token):
    """Створює тестову закупівлю через API перед тестом"""
    url = "https://stg-api.e-tender.ua/api/services/app/tender/CreateTender"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "type": 0,
        "isClosed": False,
        "tenderPeriod": {
            "startDate": "2025-10-17T09:11:43+03:00",
            "endDate": "2025-10-31T18:00:00+02:00"
        },
        "title": "Закупівля test",
        "internalTenderNumber": "1",
        "description": "",
        "lots": [
            {
                "CpvId": 325,
                "AdditionalCpvIds": [473, 950],
                "budgetLimitationType": 0,
                "isPublicBudget": True,
                "value": {
                    "CurrencyId": 0,
                    "valueAddedTaxIncluded": False
                },
                "Title": "Закупівля test",
                "isBidCurrencyPosible": False,
                "isOutsource": False,
                "isBidAnalogPosible": False,
                "isPutGuarantee": False,
                "formula": 2,
                "auctionMode": 0,
                "auctionPeriod": {
                    "startDate": "2025-11-28T18:00:00+02:00",
                    "endDate": "2025-11-28T18:30:00+02:00"
                },
                "auctionPresentationSetting": 0,
                "auctionCountRounds": 3,
                "auctionStepPer": 2,
                "auctionRoundDurationMinutes": 10,
                "auctionAdditionalRoundDurationMinutes": 7,
                "prolongateAuctionIfTheBestPrice": False,
                "auctionProlongationDurationMinutes": 2,
                "isAuctionProlongation": False,
                "auctionTimeToExtend": 2,
                "isAuctionChangeBestPrice": False,
                "denySamePrice": False,
                "isClosedLastRoundAuction": False,
                "items": [
                    {
                        "title": "Vfnthsfk",
                        "quantity": 10,
                        "unit": {
                            "id": 105,
                            "nameUK": "Ящик",
                            "symbolUK": "ящ"
                        },
                        "isPriority": True
                    }
                ],
                "Cpv": {
                    "id": 325,
                    "code": "14000000-1",
                    "description": "Гірнича продукція, неблагородні метали та супутня продукція",
                    "hasChildren": True,
                    "isOpen": False,
                    "rank": 2,
                    "numberOfChildren": 8
                },
                "AdditionalCpvs": [
                    {
                        "id": 473,
                        "code": "15000000-8",
                        "description": "Продукти харчування, напої, тютюн та супутня продукція",
                        "hasChildren": True,
                        "isOpen": False,
                        "rank": 2,
                        "numberOfChildren": 9
                    },
                    {
                        "id": 950,
                        "code": "16000000-5",
                        "description": "Сільськогосподарська техніка",
                        "hasChildren": True,
                        "isOpen": False,
                        "rank": 2,
                        "numberOfChildren": 7
                    }
                ],
                "documents": []
            }
        ],
        "creatorOrganization": {
            "id": 118,
            "organizationId": 118,
            "value": "Тест Тест"
        },
        "edocInitiator": {"id": 179, "value": "Діхтяр Віталій"},
        "edocExpert": {"id": 179, "value": "Діхтяр Віталій"},
        "auctionPlaningMode": 1,
        "isNeedDuplicateDocs": False,
        "isTemplate": False,
        "documents": []
    }

    response = requests.post(url, json=payload, headers=headers)
    print(f"🔹 CreateTender status: {response.status_code}")
    print(f"🔹 Response body: {response.text[:300]}")

    if response.status_code != 200:
        raise Exception(f"❌ CreateTender failed ({response.status_code}): {response.text}")

    tender_id = response.json().get("result", {}).get("tenderId") or response.json().get("result", {}).get("id")
    print(f"🧩 Тендер створено: ID = {tender_id}")
    yield tender_id

    # 🗑️ Видалення тендера після тесту
    delete_url = "https://stg-api.e-tender.ua/api/services/app/tender/DeleteTender"
    delete_payload = {"tenderId": tender_id}
    del_response = requests.post(delete_url, json=delete_payload, headers=headers)
    print(f"🗑️ DeleteTender status: {del_response.status_code}")

@pytest.fixture()
def delete_tender(auth_token):
    """Дає можливість вручну видаляти тендери з тестів"""
    headers = {"Authorization": f"Bearer {auth_token}"}

    def _delete(tender_id: int):
        url = f"{BASE_URL}/api/tenders/{tender_id}"
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            print(f"🧹 Тендер {tender_id} успішно видалено")
        else:
            print(f"⚠️ Не вдалося видалити тендер {tender_id}: {response.status_code} {response.text}")

    return _delete
