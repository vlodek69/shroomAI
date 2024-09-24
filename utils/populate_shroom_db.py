import os

import dill
import redis
from dotenv import load_dotenv

from utils.mushroom_wiki_scraper import ShroomScraper

load_dotenv()

# Configure Redis
redis_client = redis.StrictRedis.from_url(os.getenv("REDIS_URL"))

BASE_URL = "https://en.wikipedia.org"

# Data to populate
# CLASS_NAMES is taken from training dataset 'class_names = train_dataset.class_names' in Jupiter notebook
CLASS_NAMES = [
    "Agaricus augustus",
    "Agaricus xanthodermus",
    "Blusher",
    "Amanita augusta",
    "Amanita brunnescens",
    "Amanita calyptroderma",
    "Amanita flavoconia",
    "Amanita muscaria",
    "Amanita persicina",
    "Amanita phalloides",
    "Amanita velosa",
    "Armillaria mellea",
    "Armillaria tabescens",
    "Artomyces pyxidatus",
    "Bolbitius titubans",
    "Boletus pallidus",
    "Boletus rex-veris",
    "Cantharellus californicus",
    "Cantharellus cinnabarinus",
    "Cerioporus squamosus",
    "Chlorophyllum brunneum",
    "Chlorophyllum molybdites",
    "Clitocybe nuda",
    "Coprinellus micaceus",
    "Coprinopsis lagopus",
    "Coprinus comatus",
    "Crucibulum laeve",
    "Cryptoporus volvatus",
    "Daedaleopsis confragosa",
    "Entoloma abortivum",
    "Flammulina velutipes",
    "Fomitopsis mounceae",
    "Galerina marginata",
    "Ganoderma applanatum",
    "Ganoderma curtisii",
    "Ganoderma oregonense",
    "Ganoderma tsugae",
    "Gliophorus psittacinus",
    "Gloeophyllum sepiarium",
    "Grifola frondosa",
    "Gymnopilus luteofolius",
    "Hericium coralloides",
    "Hericium erinaceus",
    "Hygrophoropsis aurantiaca",
    "Hypholoma fasciculare",
    "Hypholoma lateritium",
    "Hypomyces lactifluorum",
    "Ischnoderma resinosum",
    "Laccaria ochropurpurea",
    "Laetiporus sulphureus",
    "Leratiomyces ceres",
    "Leucoagaricus americanus",
    "Leucoagaricus leucothites",
    "Lycogala epidendrum",
    "Lycoperdon perlatum",
    "Lycoperdon pyriforme",
    "Mycena haematopus",
    "Mycena leaiana",
    "Omphalotus illudens",
    "Omphalotus olivascens",
    "Panaeolus papilionaceus",
    "Panellus stipticus",
    "Phaeolus schweinitzii",
    "Phlebia tremellosa",
    "Phyllotopsis nidulans",
    "Pleurotus ostreatus",
    "Pleurotus pulmonarius",
    "Psathyrella candolleana",
    "Pseudohydnum gelatinosum",
    "Psilocybe azurescens",
    "Psilocybe caerulescens",
    "Psilocybe cubensis",
    "Psilocybe cyanescens",
    "Psilocybe ovoideocystidiata",
    "Psilocybe pelliculosa",
    "Retiboletus ornatipes",
    "Sarcomyxa serotina",
    "Schizophyllum commune",
    "Stereum hirsutum",
    "Stereum ostrea",
    "Stropharia ambigua",
    "Suillus americanus",
    "Suillus luteus",
    "Suillus spraguei",
    "Tapinella atrotomentosa",
    "Trametes betulina",
    "Trametes gibbosa",
    "Trametes versicolor",
    "Trichaptum biforme",
    "Tricholoma murrillianum",
    "Tricholomopsis rutilans",
    "Tylopilus felleus",
    "Tylopilus rubrobrunneus",
    "Volvopluteus gloiocephalus",
]
# Wikipedia requires a header with contact information to access the images via bot
HEADERS = {
    "User-Agent": "MushroomAI script for one-time data extraction (currently stored localy), lordgadyka71@gmail.com - personal email"
}


def populate_redis(scraper: ShroomScraper) -> None:
    print("\033[33mStarting...\033[0m")
    total_mushrooms = len(CLASS_NAMES)
    for key, value in enumerate(CLASS_NAMES):
        try:
            shroom = scraper.get_mushroom_data(value)
        except Exception as e:
            print(f"Error when getting {value}: {e}")
            raise
        dilled_shroom = dill.dumps(shroom)
        redis_client.set(str(key), dilled_shroom)
        print(f"{key + 1}/{total_mushrooms} {value} \033[32mSUCCESS\033[0m")
    print("\033[32mData populated successfully.\033[0m")


if __name__ == "__main__":
    scraper = ShroomScraper(BASE_URL, HEADERS)
    redis_client.flushdb()
    populate_redis(scraper)
