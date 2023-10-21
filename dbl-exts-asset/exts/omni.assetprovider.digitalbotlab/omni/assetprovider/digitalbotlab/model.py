# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

from typing import Dict, List, Optional, Union, Tuple

import aiohttp

from omni.services.browser.asset import BaseAssetStore, AssetModel, SearchCriteria, ProviderModel
from .constants import SETTING_STORE_ENABLE
from pathlib import Path

CURRENT_PATH = Path(__file__).parent
DATA_PATH = CURRENT_PATH.parent.parent.parent.joinpath("data")

# The name of your company
PROVIDER_ID = "Digital Bot Lab"
# The URL location of your API
STORE_URL = "https://evermotion.org/control/querry.php"


class DBLAssetProvider(BaseAssetStore):
    """
        Asset provider implementation.
    """

    def __init__(self, ov_app="Kit", ov_version="na") -> None:
        super().__init__(PROVIDER_ID)
        self._ov_app = ov_app
        self._ov_version = ov_version

    async def _search(self, search_criteria: SearchCriteria) -> Tuple[List[AssetModel], bool]:
        """ Searches the asset store.

            This function needs to be implemented as part of an implementation of the BaseAssetStore.
            This function is called by the public `search` function that will wrap this function in a timeout.
        """
        params = {}

        # Setting for filter search criteria
        if search_criteria.filter.categories:
            # No category search, also use keywords instead
            categories = search_criteria.filter.categories
            for category in categories:
                if category.startswith("/"):
                    category = category[1:]
                category_keywords = category.split("/")
                params["filter[categories]"] = ",".join(category_keywords).lower()

        # Setting for keywords search criteria
        if search_criteria.keywords:
            params["keywords"] = ",".join(search_criteria.keywords)


        # Setting for page number search criteria
        if search_criteria.page.number:
            params["page"] = search_criteria.page.number

        # Setting for max number of items per page
        if search_criteria.page.size:
            params["page_size"] = search_criteria.page.size


        items = []

        print("[model] params", params)

        # Uncomment once valid Store URL has been provided
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{STORE_URL}", params=params) as resp:
                result = await resp.read()
                result = await resp.json()
                items = result

        print("[model] items", items)

        assets: List[AssetModel] = []

        # Create AssetModel based off of JSON data
        for item in items:
            assets.append(
                AssetModel(
                  identifier=item.get("identifier", ""),
                  name=item.get("name", ""),
                  published_at=item.get("pub_at", ""),
                  categories=item.get("categories", []),
                  tags=item.get("tags", []),
                  vendor=PROVIDER_ID,
                  product_url=item.get("url", ""),
                  download_url=item.get("download_url", ""),
                  price=item.get("price", 0),
                  thumbnail=item.get("thumbnail", ""),
                )
            )

        # Are there more assets that we can load?
        more = True
        if search_criteria.page.size and len(assets) < search_criteria.page.size:
            more = False

        return (assets, more)

    def provider(self) -> ProviderModel:
        """Return provider info"""
        return ProviderModel(
            name=PROVIDER_ID, icon=f"{DATA_PATH}/logo.png", enable_setting=SETTING_STORE_ENABLE
        )
