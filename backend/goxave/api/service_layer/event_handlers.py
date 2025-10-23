import smtplib
from datetime import datetime
from email.message import EmailMessage
from email.mime.text import MIMEText

import httpx

from goxave.api.domain.events import (
    NotifyErrorAddingNewItem,
    NotifyNewItemAdded,
    NotifyUserOnPriceChange,
)
from goxave.config import EMAIL_ACCOUNT, EMAIL_PASSWORD, SMTP_HOST, SMTP_PORT


def send_email(
    smtp_host: str,
    smtp_port: int,
    to_email: str,
    to_name: str,
    subject: str,
    message: str,
) -> None:
    html_content = f"""
        <html>
            <body>
                <h4>Hello {to_name}!</h4>
                <p>{message}</p>
                <hr style="border: 1px solid #ccc; margin: 20px 0;">
                <footer style="font-family: Arial, sans-serif; font-size: 12px; color: #555;">
                    <p><strong>goSave Team</strong></p>
                    <p>Track prices across your favorite online stores!</p>
                    <p><a href="https://gosave.grog.com.ph" style="color: #1a73e8; text-decoration: none;">Visit goSave</a>
                    <p style="color: #888;">&copy; {datetime.now().year} goSave. All rights reserved.</p>
                </footer>
            </body>
        </html>
        """
    email_msg = EmailMessage()
    email_msg["From"] = EMAIL_ACCOUNT
    email_msg["To"] = to_email
    email_msg["Subject"] = subject
    email_msg.set_content(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL(host=smtp_host, port=smtp_port) as smtp_server:
        smtp_server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        smtp_server.send_message(email_msg)
        print("email sent!")


def notify_via_email_on_new_item_added(event: NotifyNewItemAdded, uow):
    user_name = event.user_name
    email = event.user_email
    product_url = event.product_url
    message = f'You have a new saved product ready to be tracked: <a href="{product_url}">{product_url}</a>'
    subject = "goSave - New Item Ready to be Tracked"
    send_email(
        smtp_host=SMTP_HOST,
        smtp_port=SMTP_PORT,
        to_email=email,
        to_name=user_name,
        message=message,
        subject=subject,
    )


def notify_via_email_on_error_adding_new_item(event: NotifyErrorAddingNewItem, uow):
    user_name = event.user_name
    product_url = event.product_url
    email = event.user_email
    message = f'We are unable to add the following product to your tracked items at this moment. <a href="{product_url}">{product_url}</a>. Please try again!'
    subject = "goSave - Unable to Add Product to your Tracked Items"
    send_email(
        smtp_host=SMTP_HOST,
        smtp_port=SMTP_PORT,
        to_email=email,
        to_name=user_name,
        message=message,
        subject=subject,
    )
    return None


def notify_via_email_on_price_change(event: NotifyUserOnPriceChange, uow) -> None:
    for user in event.my_trackers:
        user_name = user.name
        email = user.email
        product_url = event.product_url
        previous_price = event.previous_price
        current_price = event.current_price
        message = f'There is a price change for <a href="{product_url}">{product_url}</a>. From {previous_price} to {current_price}. Check it out now!"'
        subject = "goSave - Price Change Update"
        send_email(
            smtp_host=SMTP_HOST,
            smtp_port=SMTP_PORT,
            to_email=email,
            to_name=user_name,
            message=message,
            subject=subject,
        )
    return None


def notify_discord_new_item_added(event: NotifyNewItemAdded, uow):
    discord_webhook = event.discord_webhook
    user_name = event.user_name
    product_url = event.product_url
    if not discord_webhook:
        return None
    data = {
        "content": f"Hello {user_name}! You have new saved product ready to be tracked. {product_url}"
    }
    if discord_webhook:
        response = httpx.post(
            discord_webhook, headers={"Content-Type": "application/json"}, json=data
        )
        return response
    return None


def notify_discord_on_error_adding_new_item(event: NotifyErrorAddingNewItem, uow):
    discord_webhook = event.discord_webhook
    user_name = event.user_name
    product_url = event.product_url
    data = {
        "content": f"Hello {user_name}! We are unable to add the following product to your tracked items at this moment. {product_url}. Please try again!"
    }
    if discord_webhook:
        response = httpx.post(
            discord_webhook, headers={"Content-Type": "application/json"}, json=data
        )
        return response
    return None

    pass


def notify_discord_on_price_change(event: NotifyUserOnPriceChange, uow):
    for user in event.my_trackers:
        discord_webhook = user.discord_webhook
        product_url = event.product_url
        previous_price = event.previous_price
        current_price = event.current_price
        data = {
            "content": f"Hello {user.name}, There's a price change for {product_url}. From {previous_price} to {current_price}. Check it out now!"
        }
        httpx.post(
            discord_webhook, headers={"Content-Type": "application/json"}, json=data
        )
    return None
