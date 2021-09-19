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
3. You have to set VK_API_KEY environment variable before use script:
    * Create .env file in project directory.
    * To generate VKontakte API key, use this [instruction](https://vk.com/dev/implicit_flow_user). Copy your VKontakte API key to .env file:
    ```
    export VK_API_KEY="cd111111a8dde5abb20d65a2222b50eebdf3333333f03022e25007baea82860a444444444c086eb4cd8c"
    ```
4. You have to set VK_GROUP_ID environment variable before use script:
To get VKontakte group id use this [instruction](https://regvk.com/id/). Copy your VKontakte group id to .env file:
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
