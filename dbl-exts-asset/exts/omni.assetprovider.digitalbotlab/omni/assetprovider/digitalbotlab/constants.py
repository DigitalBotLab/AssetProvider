IN_RELEASE = True

SETTING_ROOT = "/exts/omni.assetprovider.template/"
SETTING_STORE_ENABLE = SETTING_ROOT + "enable"

STORE_URL = "http://api.digitalbotlab.com/api/omniverse/assets" if IN_RELEASE else "http://localhost:8000/api/omniverse/assets"
THUMBNAIL_URL = "http://api.digitalbotlab.com/image/" if IN_RELEASE else "http://localhost:8000/image/"



DBL_ASSETPROVIDER_INTRO = "\n The Digital Bot Lab's Insiderobo Connector is \n a cutting-edge solution designed to seamlessly \n connect our extensive digital robot collection \n with the powerful NVIDIA Omniverse platform. \n\n Learn more about us: https://digitalbotlab.com/ \n Learn more about Omniverse: https://www.nvidia.com/en-us/omniverse/ \n Learn more about Insiderobo Connector: https://digitalbotlab.com/omniverse/asset-provider \n \n Contact us: info@digitalbotlab.com"