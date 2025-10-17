from playwright.sync_api import Page, expect
import time


def test_create_group(login: Page):
    page = login

    # Перехід до сторінки "Групи"
    page.get_by_role("link", name="Групи").click()
    page.get_by_role("button", name="Створити").click()
    expect(page.get_by_role("heading", name="Нова група")).to_be_visible()

    # Створення унікальної назви
    timestamp = int(time.time())  # Поточний Unix час, наприклад 1728659032
    group_name = f"Нова група {timestamp}"

    page.get_by_role("textbox", name="Назва групи").fill(group_name)
    page.locator("#modal-form span").first.click()
    page.get_by_role("button", name="Створити").click()

    # Очікування завантаження списку після створення
    expect(page.get_by_text(group_name)).to_be_visible(timeout=10000)

    # Перехід на головну
    page.get_by_role("link", name="logo").click()
    expect(page.get_by_role("link", name="Всі закупівлі")).to_be_visible()