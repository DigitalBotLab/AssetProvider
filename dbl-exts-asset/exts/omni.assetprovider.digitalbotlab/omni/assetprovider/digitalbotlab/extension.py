import importlib

import carb
import carb.settings
import carb.tokens
import omni.ui as ui

import omni.ext

from omni.services.browser.asset import get_instance as get_asset_services

from .model import DBLAssetProvider
from .constants import SETTING_STORE_ENABLE 

import aiohttp
import asyncio

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

        self._window = ui.Window("DBL Asset Debug", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                #ui.Label("Prim Path:", width = 100)
                ui.Button("Debug", height = 20, clicked_fn = self.debug)
                ui.Button("Debug", height = 20, clicked_fn = self.debug_token)



    def on_shutdown(self):
        print("[omni.assetprovider.digitalbotlab] omni assetprovider digitalbotlab shutdown")
        self._asset_service.unregister_store(self._asset_provider)
        carb.settings.get_settings().set(SETTING_STORE_ENABLE, False)
        self._asset_provider = None
        self._asset_service = None

    def debug(self):
        
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