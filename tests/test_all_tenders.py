from playwright.sync_api import Page, expect


def test_open_all_tenders(login: Page):
    page = login
    page.get_by_role("link", name="Всі закупівлі").click()
    expect(page).to_have_url("https://stg.e-tender.ua/v2/all-tenders")