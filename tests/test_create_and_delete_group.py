from playwright.sync_api import Page, expect
import time


def test_create_and_delete_group(login: Page):
    page = login

    # Перейти до сторінки "Групи"
    page.get_by_role("link", name="Групи").click()
    expect(page).to_have_url("https://stg.e-tender.ua/v2/suppliers/my-suppliers-groups")

    # Створити нову групу
    page.get_by_role("button", name="Створити").click()
    expect(page.get_by_role("heading", name="Нова група")).to_be_visible()

    group_name = f"Нова група {int(time.time())}"
    page.get_by_role("textbox", name="Назва групи").fill(group_name)
    page.get_by_role("button", name="Створити").click()

    # Перевірка, що група з'явилася у таблиці
    expect(page.get_by_text(group_name)).to_be_visible(timeout=10000)

    # Видалення створеної групи
    row = page.get_by_role("row", name=group_name)
    row.get_by_role("button").click()  # відкриває контекстне меню

    page.get_by_role("button", name="Видалити").click()
    expect(page.get_by_role("heading", name="Видалити")).to_be_visible()

    page.get_by_role("button", name="Так").click()

    # Перевірка, що групи більше немає
    expect(page.get_by_text(group_name)).not_to_be_visible(timeout=10000)