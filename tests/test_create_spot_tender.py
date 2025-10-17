import re
import time
from playwright.sync_api import Page, expect


def test_create_spot_tender(login: Page):
    page = login

    # Перехід на створення СПОТ
    page.get_by_role("link", name="SPOT").first.click()
    expect(page.get_by_role("heading", name="SPOT")).to_be_visible()

    page.get_by_role("button").first.click()
    expect(page.get_by_role("combobox", name="Запит пропозицій")).to_be_visible()

    # Вибір типу СПОТ
    page.locator("#mat-select-value-1").click()
    expect(page.get_by_role("option", name="Простий тендер")).to_be_visible()
    page.get_by_role("option", name="SPOT").click()
    expect(page.get_by_role("combobox", name="SPOT")).to_be_visible()
    page.get_by_role("button", name="Продовжити").click()

    # Перевірка переходу на форму
    expect(page.get_by_role("link", name="logo logo")).to_be_visible()

    # Заповнення полів
    tender_name = f"СПОТ автотест {int(time.time())}"
    page.get_by_role("textbox", name="Назва *").fill(tender_name)
    page.get_by_role("textbox", name="Номер закупівлі *").fill("23")
    page.locator("quill-editor div").nth(2).fill("Опис закупівлі")

    # 🔸 Тимчасово пропускаємо завантаження файлів
    # page.get_by_text("Знайти файли").click()
    # page.locator("input[type='file']").set_input_files(["12.jpg", "13.jpg"])

    # Вибір CPV
    page.get_by_role("textbox", name="Класифікатор CPV *").click()
    expect(page.get_by_role("treeitem", name="  03000000-1")).to_be_visible()
    page.locator("span > .icon-tick").first.click()
    page.get_by_role("button", name="Готово").click()

    # Додавання позиції
    page.get_by_role("textbox", name="Введіть").fill("Матеріал")
    page.locator("#field-35").fill("10")
    page.get_by_text("Виберіть").click()
    page.locator("#mat-option-16").click()
    page.locator("#field-37").fill("10000")

    # Збереження чернетки
    page.get_by_role("button", name="Зберегти чернетку").click()

    # Очікування переходу на сторінку деталей
    expect(page).to_have_url(re.compile(r"/tender-details/info"))
    expect(page.get_by_text("Деталі закупівлі")).to_be_visible(timeout=15000)