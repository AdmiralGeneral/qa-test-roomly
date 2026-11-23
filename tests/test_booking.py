import pytest
from playwright.sync_api import Page, expect

# Тестовые данные
FUTURE_DATE = "2027-01-15"
VALID_NAME = "Иван Иванов"
VALID_EMAIL = "ivan.ivanov@example.com"


def test_successful_booking(page: Page, base_url: str):
    """
    Позитивный тест: успешное бронирование комнаты при корректном заполнении.
    """
    page.goto(base_url)

    page.select_option("#room", value="small")
    page.fill("#date", FUTURE_DATE)
    page.fill("#start-time", "10:00")
    page.fill("#end-time", "11:00")
    page.fill("#participants", "3")
    page.fill("#name", VALID_NAME)
    page.fill("#email", VALID_EMAIL)

    page.click("button[type='submit']")

    status_message = page.locator("#form-status")
    expect(status_message).to_be_visible()
    expect(status_message).to_contain_text("Малая")
    expect(status_message).to_contain_text(FUTURE_DATE)
    expect(status_message).to_contain_text("10:00")
    expect(status_message).to_contain_text(VALID_NAME)


def test_invalid_email(page: Page, base_url: str):
    """
    Негативный тест: некорректный формат email — форма не должна отправляться.
    """
    page.goto(base_url)

    page.select_option("#room", value="medium")
    
    page.fill("#date", FUTURE_DATE)
    page.fill("#start-time", "12:00")
    page.fill("#end-time", "13:00")
    page.fill("#participants", "5")
    page.fill("#name", VALID_NAME)
    # Вводим некорректную почту
    page.fill("#email", "invalid-email")

    page.click("button[type='submit']")

    status_message = page.locator("#form-status")
    expect(status_message).not_to_contain_text("Средняя")
    expect(status_message).not_to_contain_text(FUTURE_DATE)


@pytest.mark.xfail(
    strict=True,
    reason="BUG-04: Форма позволяет отправить имя, состоящее из цифр и спецсимволов",
    raises=AssertionError,
)
@pytest.mark.xfail(
    strict=True,
    reason="BUG-04: Форма позволяет отправить имя, состоящее из цифр и спецсимволов",
    raises=AssertionError,
)
def test_bug_invalid_name(page: Page, base_url: str):
    """
    Тест на найденный дефект (BUG_#4): проверяем КОРРЕКТНОЕ (ожидаемое) поведение.
    Форма не должна принимать имя, состоящее только из цифр или спецсимволов.
    """
    page.goto(base_url)

    page.select_option("#room", value="small")
    page.fill("#date", FUTURE_DATE)
    page.fill("#start-time", "14:00")
    page.fill("#end-time", "15:00")
    page.fill("#participants", "2")
    
    page.fill("#name", "12345!@#$%")
    page.fill("#email", VALID_EMAIL)

    page.click("button[type='submit']")

    status_message = page.locator("#form-status")
    expect(status_message).not_to_contain_text("успешно")