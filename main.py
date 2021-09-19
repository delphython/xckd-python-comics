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


def get_random_comic_number(url):
    response = requests.get(url)
    response.raise_for_status()

    comic_metadata = response.json()
    last_comic_number = comic_metadata["num"]

    return random.randint(1, last_comic_number)


def get_image_metadata(url, params=None):
    response = requests.get(url, params)
    response.raise_for_status()

    return response.json()


def download_image(url, filename, image_dir, params=None):
    response = requests.get(url, params)
    response.raise_for_status()

    image_path = os.path.join(image_dir, filename)

    with open(image_path, "wb") as file:
        file.write(response.content)


def get_vk_upload_server_metadata(vk_group_id, token, token_version):
    vk_api_url = "https://api.vk.com/method/photos.getWallUploadServer"

    params = {
      "access_token": token,
      "v": token_version,
      "group_id": vk_group_id,
    }

    response = requests.post(vk_api_url, params=params)
    response.raise_for_status()

    return response.json()["response"]


def upload_image_to_vk(upload_url, image_path, vk_group_id,
                       token, token_version):

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


def save_image_to_vk(uploaded_server, uploaded_image, uploaded_hash,
                     vk_group_id, token, token_version):
    vk_save_image_url = "https://api.vk.com/method/photos.saveWallPhoto"

    params = {
        "access_token": token,
        "v": token_version,
        "server": uploaded_server,
        "photo": uploaded_image,
        "hash": uploaded_hash,
        "group_id": vk_group_id,
    }

    response = requests.post(vk_save_image_url, params=params)
    response.raise_for_status()

    return response.json()["response"][0]


def publish_image_to_vk(save_response_metadata, image_comment, vk_group_id,
                        token, token_version):
    vk_publish_image_url = "https://api.vk.com/method/wall.post"
    post_from_group = 1

    vk_owner_id = save_response_metadata["owner_id"]
    uploaded_image_id = save_response_metadata["id"]
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

    vk_group_id = os.environ["VK_GROUP_ID"]
    vk_token = os.environ["VK_API_KEY"]

    random_comic = get_random_comic_number(comic_url)
    random_comic_url = f"https://xkcd.com/{random_comic}/info.0.json"

    image_metadata = get_image_metadata(random_comic_url)
    image_url = image_metadata["img"]
    image_comment = image_metadata["alt"]
    image_file_name = get_file_name(image_url)
    image_dir = os.getcwd()
    image_path = os.path.join(image_dir, image_file_name)

    download_image(image_url, image_file_name, image_dir)

    try:
        vk_upload_server_metadata = get_vk_upload_server_metadata(
            vk_group_id, vk_token,
            token_version
        )
        upload_url = vk_upload_server_metadata["upload_url"]

        vk_upload_response_metadata = upload_image_to_vk(
            upload_url,
            image_path,
            vk_group_id,
            vk_token,
            token_version
        )
        uploaded_server = vk_upload_response_metadata["server"]
        uploaded_image = vk_upload_response_metadata["photo"]
        uploaded_hash = vk_upload_response_metadata["hash"]

        vk_save_response_metadata = save_image_to_vk(
            uploaded_server,
            uploaded_image,
            uploaded_hash,
            vk_group_id,
            vk_token,
            token_version
        )

        publish_image_to_vk(
            vk_save_response_metadata,
            image_comment,
            vk_group_id,
            vk_token,
            token_version
        )

        os.remove(image_path)
    finally:
        os.remove(image_path)


if __name__ == "__main__":
    main()
