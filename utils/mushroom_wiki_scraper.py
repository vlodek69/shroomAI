import base64
from dataclasses import dataclass
from io import BytesIO

import bs4
import requests
from PIL import Image


@dataclass
class Mushroom:
    name: str
    description: str
    image: bytes

    def serialize(self) -> dict[str, str]:
        image_base64 = base64.b64encode(self.image).decode("utf-8")

        return {
            "name": self.name,
            "description": self.description,
            "image": f"data:image/png;base64,{image_base64}",
        }


class ShroomScraper:
    def __init__(self, base_url: str, headers: dict[str, str]) -> None:
        self.base_url = base_url
        self.headers = headers

    @staticmethod
    def get_page_soup(url: str) -> bs4.BeautifulSoup:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return bs4.BeautifulSoup(response.content, "html.parser")
        except Exception as e:
            print("Exception during retrieving page soup", e)

    def get_mushroom_data(self, mushroom_name: str) -> Mushroom:
        url = self.base_url + "/wiki/" + mushroom_name.replace(" ", "_")
        soup = self.get_page_soup(url).select_one(
            ".mw-content-ltr.mw-parser-output"
        )

        image = self.get_image(soup)

        description = self.get_description(soup)

        return Mushroom(
            name=mushroom_name, image=image, description=description
        )

    def get_image(self, soup: bs4.BeautifulSoup) -> bytes:
        try:
            image_page_url = soup.select_one(
                ".infobox .mw-file-description"
            ).get("href")
            image_soup = self.get_page_soup(
                self.base_url + image_page_url
            ).select_one(".fullImageLink > a")
            image_url = "https:" + image_soup.get("href")
            image_response = requests.get(image_url, headers=self.headers)
            image_data = image_response.content
            max_size = (512, 512)
            with BytesIO(image_data) as img_stream:
                with Image.open(img_stream) as img:
                    img.thumbnail(max_size, Image.LANCZOS)
                    with BytesIO() as output_stream:
                        img.save(output_stream, format="PNG")

                        return output_stream.getvalue()
        except Exception:
            raise

    def get_description(self, soup: bs4.BeautifulSoup) -> str:
        try:
            description = soup.select_one("table.infobox ~ p").text
        except AttributeError:
            try:
                description = soup.find("p", recursive=False).text
                if description.strip() == "":
                    description = soup.select_one("p ~ p").text
            except Exception:
                raise

        description = self.reformat_descr(description)

        return description

    @staticmethod
    def reformat_descr(text: str) -> str:
        while "[" in text:
            p_open = text.find("[")
            p_close = text.find("]")
            if p_open < p_close:
                text = text[:p_open] + text[(p_close + 1):]
        return text.strip()
