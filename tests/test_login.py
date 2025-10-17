from playwright.sync_api import Page, expect
import re


def test_login(page: Page):
    page.goto("https://stg.e-tender.ua/v2/auth/home/all-tenders")

    page.get_by_role("link", name="Вхід").click()
    expect(page.get_by_role("link", name="Увійти")).to_be_visible()

    page.get_by_role("textbox", name="Email").fill("99v.dikhtiar@e-tender.ua")
    page.get_by_role("textbox", name="Пароль").fill("VBF/j9U~{_pAdx")
    page.get_by_role("button", name="Увійти").click()

    expect(page.get_by_role(
        "row",
        name=re.compile("Назва Ініціатор Закупівельник Статус Прийом пропозицій до")
    )).to_be_visible()