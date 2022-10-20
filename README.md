# Feishu Bot Python SDK

## Installation

```shell script
pip install PYfeishuBot
```

## Tips for using Lark

You may change the default endpoint to using Lark.

```python
import feishuBot
bot = feishuBot.Bot("app_id", "app_secret", "verification_token","encrypt_key",feishu_url="https://open.feishu.cn")
```

## Webhook Setup

1. Setup the verification token and encryption key in Feishu/Lark Event Subscribe Settings;
2. The Server needs a public IP address for setup, then use this command to expose the local server.
3. Using the script below to listen a port, if you want to use https webhook, please configure the reserved proxy yourself.

    ```python
    import feishuBot
    bot = feishuBot.Bot("app_id", "app_secret", "verification_token","encrypt_key")
    bot.runserver("0.0.0.0",80,is_sign = True,is_encrypt = True)
    # The configuration setting should match your webook setting in feishu/lark.
    ```

4. Then setup the url in webhook in Feishu/Lark Event Subscribe.

## Example Usage

```python
import feishuBot
bot = feishuBot.Bot(app_id, app_secret, verification_token,encrypt_key)
# Register the listen event function
@bot.register_handler("im.message.receive_v1",message_type="text")
def auto_reply(message):
    text = utils.get_message_text(message)
    bot.send_message(message["sender"]["sender_id"]["open_id"],text)
# this function would send the text you sent back to you.

bot.runserver("0.0.0.0",80,is_encrypt=True,is_sign=True)
# this function would start the webhook listener
# IMPORTANT! The settings should be the same when you setup webhook in Feishu/Lark.
```

## Documention

Todo
