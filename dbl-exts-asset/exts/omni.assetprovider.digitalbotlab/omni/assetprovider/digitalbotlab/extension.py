import importlib

import carb
import carb.settings
import carb.tokens
import omni.ui as ui

import omni.ext

from omni.services.browser.asset import get_instance as get_asset_services

from .model import DBLAssetProvider
from .constants import SETTING_STORE_ENABLE, IN_RELEASE, DBL_ASSETPROVIDER_INTRO

import aiohttp
import asyncio
import pathlib

EXTENSION_FOLDER_PATH = pathlib.Path(
    omni.kit.app.get_app().get_extension_manager().get_extension_path_by_module(__name__)
)

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class OmniAssetproviderDigitalbotlabExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[omni.assetprovider.digitalbotlab] omni assetprovider digitalbotlab startup") 
        self._asset_provider = DBLAssetProvider()
        self._asset_service = get_asset_services()
        self._asset_service.register_store(self._asset_provider)
        carb.settings.get_settings().set(SETTING_STORE_ENABLE, True)
        print("what", carb.settings.get_settings().get(SETTING_STORE_ENABLE))  

        self._window = ui.Window("Digital Bot Lab: AssetProvider", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                ui.ImageWithProvider(
                        f"{EXTENSION_FOLDER_PATH}/data/logo.png",
                        width=30,
                        height=30,
                    )
                ui.Label("Introduction:", height = 20)
                #intro_field = ui.StringField(multiline = True, readonly = True)
                model = ui.SimpleStringModel(DBL_ASSETPROVIDER_INTRO)
                field = ui.StringField(model, multiline=True, readonly=True, height=200) 
                # intro_field.model.set_value()
                with ui.VStack(visible= not IN_RELEASE):
                    ui.Button("debug_authenticate", height = 20, clicked_fn = self.debug_authenticate)
                    ui.Button("debug_token", height = 20, clicked_fn = self.debug_token)
                    ui.Button("Debug", height = 20, clicked_fn = self.debug)

                



    def on_shutdown(self):
        print("[omni.assetprovider.digitalbotlab] omni assetprovider digitalbotlab shutdown")
        self._asset_service.unregister_store(self._asset_provider)
        carb.settings.get_settings().set(SETTING_STORE_ENABLE, False)
        self._asset_provider = None
        self._asset_service = None

    def debug_authenticate(self):
        
        async def authenticate():
            params = {"email": "10@qq.com", "password": "97654321abc"}
            
            async with aiohttp.ClientSession() as session:
                async with session.post("http://localhost:8000/api/auth/signin", json=params) as response:
                    self._auth_params = await response.json()
                    print("auth_params", self._auth_params)
                    self.token = self._auth_params["token"]

        asyncio.ensure_future(authenticate())
    
    def debug_token(self):

        async def verify_token():
            params = {"token": self.token, "asset": "test"}
            async with aiohttp.ClientSession() as session:
                async with session.post("http://localhost:8000/api/omniverse/download", json=params) as response:
                    response = await response.json()
                    print("response", response)
        
        asyncio.ensure_future(verify_token())

    def debug(self):
        print("debug")
        
        STORE_URL = "http://localhost:8000/api/omniverse/assets"
        params = {}
        params["page"] = 1

        async def search():
            # Uncomment once valid Store URL has been provided
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{STORE_URL}", params=params) as resp:
                    result = await resp.read()
                    result = await resp.json()
                    items = result
                    print("items", items)
        
        asyncio.ensure_future(search())