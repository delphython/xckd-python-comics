# Publish comics on VKontakte

Publish comics on VKontakte is a console utility that downloads comics images from the [xkcd webcomics](https://xkcd.com/) site. And send it to the VKontakte group.

## Prerequisites

Python3 should be already installed. Use `pip` to install dependencies:
```bash
pip install -r requirements.txt
```

## Installation

1. Create the VKontakte group [here](https://vk.com/groups?tab=admin).
2. Create the VKontakte application [here](https://vk.com/apps?act=manage).
3. Get client_id of the created VKontakte application. Go back to the page with your applications. Click on the "Edit" button. The id will appear in the address bar. From this link: https://vk.com/editapp?id=678295892 it can be seen that client_id=678295892.
4. You have to set a VK_API_KEY environment variable before use script:
    * Create a .env file in the project directory.
    * To get the VKontakte API key, use this [instruction](https://vk.com/dev/implicit_flow_user).
    You should use this URL to get the VKontakte API key:
    https://oauth.vk.com/authorize?client_id=1234567&display=page&&scope=photos,groups,wall,offline&response_type=token&v=5.131&state=123456
    where client_id you can get from item 3 of this instruction. You will get a VK_API_KEY in the address bar, signed as access_token. Copy it to .env file:
    ```
    export VK_API_KEY="cd111111a8dde5abb20d65a2222b50eebdf3333333f03022e25007baea82860a444444444c086eb4cd8c"
    ```
5. You have to set VK_GROUP_ID environment variable before use script:
To get VKontakte group id use this [instruction](https://regvk.com/id/). Copy your VKontakte group id to the .env file:
```
export VK_GROUP_ID="123456789"
```

## Usage

Run python script:
```sh
python main.py
```

## Meta

Vitaly Klyukin — [@delphython](https://t.me/delphython) — [delphython@gmail.com](mailto:delphython@gmail.com)

[https://github.com/delphython](https://github.com/delphython/)
