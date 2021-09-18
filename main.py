import os
import random
from urllib.parse import urlparse, unquote

import requests
from dotenv import load_dotenv


def get_file_name(url):
    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)
    *arg, file_name = os.path.split(path)

    return file_name


def get_random_comic(url):
    response = requests.get(url)
    response.raise_for_status()

    comic_info = response.json()
    last_comic_number = comic_info["num"]

    random_comic_number = random.randint(1, last_comic_number)

    return f"https://xkcd.com/{random_comic_number}/info.0.json"


def get_image_info(url, params=None):
    response = requests.get(url, params)
    response.raise_for_status()

    return response.json()


def download_image(url, filename, image_dir, params=None):
    response = requests.get(url, params)
    response.raise_for_status()

    image_path = os.path.join(image_dir, filename)

    with open(image_path, "wb") as file:
        file.write(response.content)


def get_vk_upload_server_info(vk_group_id, token, token_version):
    vk_api_url = "https://api.vk.com/method/photos.getWallUploadServer"

    params = {
      "access_token": token,
      "v": token_version,
      "group_id": vk_group_id,
    }

    response = requests.post(vk_api_url, params=params)
    response.raise_for_status()

    return response.json()["response"]


def upload_image_to_vk(vk_upload_server_info, image_path, vk_group_id, token,
                       token_version):
    upload_url = vk_upload_server_info["upload_url"]

    with open(image_path, 'rb') as image_file:
        files = {
            'photo': image_file,
        }
        params = {
            "access_token": token,
            "v": token_version,
            "group_id": vk_group_id,
        }
        response = requests.post(upload_url, files=files, params=params)
        response.raise_for_status()

    return response.json()


def save_image_to_vk(upload_response_info, vk_group_id, token, token_version):
    vk_save_image_url = "https://api.vk.com/method/photos.saveWallPhoto"

    server_to_upload = upload_response_info["server"]
    image_info_to_upload = upload_response_info["photo"]
    hash_to_upload = upload_response_info["hash"]

    params = {
        "access_token": token,
        "v": token_version,
        "server": server_to_upload,
        "photo": image_info_to_upload,
        "hash": hash_to_upload,
        "group_id": vk_group_id,
    }

    response = requests.post(vk_save_image_url, params=params)
    response.raise_for_status()

    return response.json()["response"][0]


def publish_image_to_vk(save_response_info, image_comment, vk_group_id, token,
                        token_version):
    vk_publish_image_url = "https://api.vk.com/method/wall.post"
    post_from_group = 1

    vk_owner_id = save_response_info["owner_id"]
    uploaded_image_id = save_response_info["id"]
    media_content = f"photo{vk_owner_id}_{uploaded_image_id}"

    params = {
        "access_token": token,
        "v": token_version,
        "attachments": media_content,
        "owner_id": f"-{vk_group_id}",
        "from_group": post_from_group,
        "message": image_comment,
    }

    response = requests.post(vk_publish_image_url, params=params)
    response.raise_for_status()


def main():
    load_dotenv()

    comic_url = "https://xkcd.com/info.0.json"
    token_version = "5.131"
    vk_group_id = 207191194

    vk_token = os.environ["VK_API_KEY"]

    image_info = get_image_info(get_random_comic(comic_url))
    image_url = image_info["img"]
    image_comment = image_info["alt"]
    image_file_name = get_file_name(image_url)
    image_dir = os.getcwd()
    image_path = os.path.join(image_dir, image_file_name)

    download_image(image_url, image_file_name, image_dir)

    vk_upload_server_info = get_vk_upload_server_info(
        vk_group_id, vk_token,
        token_version
    )
    vk_upload_response_info = upload_image_to_vk(
        vk_upload_server_info,
        image_path,
        vk_group_id,
        vk_token,
        token_version
    )
    vk_save_response_info = save_image_to_vk(
        vk_upload_response_info,
        vk_group_id,
        vk_token,
        token_version
    )

    publish_image_to_vk(
        vk_save_response_info,
        image_comment,
        vk_group_id,
        vk_token,
        token_version
    )

    os.remove(image_path)


if __name__ == "__main__":
    main()
