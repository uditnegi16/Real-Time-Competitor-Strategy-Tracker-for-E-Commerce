# Import necessary libraries
import json
import time
from datetime import datetime
import pandas as pd
import requests
import plotly.express as px  
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller
from transformers import pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA
from selenium.webdriver.chrome.service import Service


# "Apple iPhone 15 plus (128 GB) - Green":"https://www.amazon.in/Apple-iPhone-15-128-GB/dp/B0CHX6NQMD/ref=sr_1_1_sspa?crid=R1L0YPL2S29X&dib=eyJ2IjoiMSJ9.K566O76AQlK71Xxvu5cZV6_Hh6PF3BvOLMRBFifnIHFjNEjzrchmYVdosmxa1iogCPotME2BHnNsaBwUPDA2-mllBijAs7DW8RhIBLy4p9-0H0cHBLm-DzpOvciArbilkz60vobgyha8ic1eC0P42HzmYEw2QEWf0WVbsaGqIsuzl2ehH7OMUCRl5-NFUKjsOq_LK1mKqs_xuQSCawgxHqQz0FQIkrw9jZUPC_edpSs.BrpZORYmy3n8cv644G8deXyR46aI8g1nFhOltas9NK0&dib_tag=se&keywords=apple+iphone+12+122+gb+green&nsdOptOutParam=true&qid=1739185717&sprefix=apple+iphone+12+122+gb+green+%2Caps%2C238&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1",
# "Apple iPhone 15 Plus (128 GB) - Green":"https://www.amazon.in/Apple-iPhone-15-Plus-128/dp/B0CHWZCY43/ref=sr_1_7?crid=265DLKKT3883C&dib=eyJ2IjoiMSJ9.jauChL7kXSWomYIKIMCPMqWDoB5h-9C6cHAj-CJcKnh6YYmEpHxp1ek5oho5l2JwOWGb7xQ_PL6ibNxvQvBwauY4LjNmXf5x-SnPd0MW_6b7Pcn4kBn0Z38ia8bJCLnXlWWSdI7qj8xt5P-SaCwk0IaQXjc-TAELb-6-XS8gqV7MnzsqvZSSr_zDE9gHTV9m4d0393IiBo5-yMoLhT9Yj4pCBh4ckxqmhElb9uoCozc.nwjDCGaTpnVi4lEuAs3LE16EVUC0buN4QasJtEo4D20&dib_tag=se&keywords=apple+iphone+15+128+gb+green&nsdOptOutParam=true&qid=1739185833&sprefix=apple+iphone+15+128+gb+green%2Caps%2C253&sr=8-7",
# "Apple iPhone 15 Plus (128 GB) - Blue":"https://www.amazon.in/Apple-iPhone-15-Plus-128/dp/B0CHX6X2WW/ref=sr_1_11_sspa?crid=265DLKKT3883C&dib=eyJ2IjoiMSJ9.jauChL7kXSWomYIKIMCPMqWDoB5h-9C6cHAj-CJcKnh6YYmEpHxp1ek5oho5l2JwOWGb7xQ_PL6ibNxvQvBwauY4LjNmXf5x-SnPd0MW_6b7Pcn4kBn0Z38ia8bJCLnXlWWSdI7qj8xt5P-SaCwk0IaQXjc-TAELb-6-XS8gqV7MnzsqvZSSr_zDE9gHTV9m4d0393IiBo5-yMoLhT9Yj4pCBh4ckxqmhElb9uoCozc.nwjDCGaTpnVi4lEuAs3LE16EVUC0buN4QasJtEo4D20&dib_tag=se&keywords=apple%2Biphone%2B15%2B128%2Bgb%2Bgreen&nsdOptOutParam=true&qid=1739185833&sprefix=apple%2Biphone%2B15%2B128%2Bgb%2Bgreen%2Caps%2C253&sr=8-11-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9tdGY&th=1",
# "Apple iPhone 15 Plus (128 GB) - Black":"https://www.amazon.in/Apple-iPhone-15-Plus-128/dp/B0CHXCR9CX/ref=sr_1_15?crid=265DLKKT3883C&dib=eyJ2IjoiMSJ9.jauChL7kXSWomYIKIMCPMqWDoB5h-9C6cHAj-CJcKnh6YYmEpHxp1ek5oho5l2JwOWGb7xQ_PL6ibNxvQvBwauY4LjNmXf5x-SnPd0MW_6b7Pcn4kBn0Z38ia8bJCLnXlWWSdI7qj8xt5P-SaCwk0IaQXjc-TAELb-6-XS8gqV7MnzsqvZSSr_zDE9gHTV9m4d0393IiBo5-yMoLhT9Yj4pCBh4ckxqmhElb9uoCozc.nwjDCGaTpnVi4lEuAs3LE16EVUC0buN4QasJtEo4D20&dib_tag=se&keywords=apple%2Biphone%2B15%2B128%2Bgb%2Bgreen&nsdOptOutParam=true&qid=1739185833&sprefix=apple%2Biphone%2B15%2B128%2Bgb%2Bgreen%2Caps%2C253&sr=8-15&th=1",
# "Apple iPhone 15 Plus (128 GB) - Pink":"https://www.amazon.in/Apple-iPhone-15-Plus-128/dp/B0CHWYXK1R/ref=sr_1_16?crid=265DLKKT3883C&dib=eyJ2IjoiMSJ9.jauChL7kXSWomYIKIMCPMqWDoB5h-9C6cHAj-CJcKnh6YYmEpHxp1ek5oho5l2JwOWGb7xQ_PL6ibNxvQvBwauY4LjNmXf5x-SnPd0MW_6b7Pcn4kBn0Z38ia8bJCLnXlWWSdI7qj8xt5P-SaCwk0IaQXjc-TAELb-6-XS8gqV7MnzsqvZSSr_zDE9gHTV9m4d0393IiBo5-yMoLhT9Yj4pCBh4ckxqmhElb9uoCozc.nwjDCGaTpnVi4lEuAs3LE16EVUC0buN4QasJtEo4D20&dib_tag=se&keywords=apple+iphone+15+128+gb+green&nsdOptOutParam=true&qid=1739185833&sprefix=apple+iphone+15+128+gb+green%2Caps%2C253&sr=8-16"
# "ZEBRONICS THUNDER Bluetooth 5.3 Wireless over Ear Headphones with 60H Backup (Black)":"https://www.amazon.in/ZEBRONICS-Bluetooth-Headphones-assistant-Comfortable/dp/B07L8KNP5F/ref=sr_1_2?crid=1W40G5GRB60WE&dib=eyJ2IjoiMSJ9.0DASzxIE9pACZHbHX81_Jf1FjTpQyWa45-bqicf3mZ4TMWosRZQ9p_cEGpkRH6oLsU5tBTUrYq6eTLSldqlNIlTSmwdzX9wOVEhjjwCQUN7-seiopr4I0_V1_jXlzcC3I8SIrbfg0bJwHjtldileTNN1ESpxrXeVXY1dBm7twB6bt9AkfvPe1IOEC_TY2YchiiaRXmaar0c_3g-SHrcQeZtl1Za3EJH6ZyDaBMTRglxkl78jhYaJ7kfgDf5UiNytJBvVfX4H4ST1QaDoHBD38HfAQ56j6HjN8QsvsWv7XQCPaeZOTt1aZpJlaOg-LJFeKbniBt3k-kIg5WIsD6bYoUQvXmrIX8QlJbQtwaiP7g4.ZP4N7cUoMb50y-y1MZKGI3YlZ21qGpKtuygASlyZ1Ek&dib_tag=se&keywords=headphones&qid=1739188659&refinements=p_123%3A396324&rnid=91049095031&s=electronics&sprefix=headphone%2B%2Caps%2C263&sr=1-2&th=1",
# "ZEBRONICS Thunder Bluetooth 5.3 Wireless Over Ear Headphones with 60H Backup (Sea Green)":"https://www.amazon.in/ZEBRONICS-Zeb-Thunder-Connectivity-Sea-Green/dp/B09B5CPV71/ref=sr_1_1?crid=1W40G5GRB60WE&dib=eyJ2IjoiMSJ9.0DASzxIE9pACZHbHX81_Jf1FjTpQyWa45-bqicf3mZ4TMWosRZQ9p_cEGpkRH6oLsU5tBTUrYq6eTLSldqlNIlTSmwdzX9wOVEhjjwCQUN7-seiopr4I0_V1_jXlzcC3I8SIrbfg0bJwHjtldileTNN1ESpxrXeVXY1dBm7twB6bt9AkfvPe1IOEC_TY2YchiiaRXmaar0c_3g-SHrcQeZtl1Za3EJH6ZyDaBMTRglxkl78jhYaJ7kfgDf5UiNytJBvVfX4H4ST1QaDoHBD38HfAQ56j6HjN8QsvsWv7XQCPaeZOTt1aZpJlaOg-LJFeKbniBt3k-kIg5WIsD6bYoUQvXmrIX8QlJbQtwaiP7g4.ZP4N7cUoMb50y-y1MZKGI3YlZ21qGpKtuygASlyZ1Ek&dib_tag=se&keywords=headphones&qid=1739188659&refinements=p_123%3A396324&rnid=91049095031&s=electronics&sprefix=headphone%2B%2Caps%2C263&sr=1-1&th=1",
# "ZEBRONICS Thunder Bluetooth 5.3 Wireless Over Ear Headphones with 60H Backup (Teal Green)":"https://www.amazon.in/ZEBRONICS-Zeb-Thunder-Bluetooth-Teal-Green/dp/B09B5BS6G4/ref=sr_1_4?crid=1Q9Y5CJ3Z2XT3&dib=eyJ2IjoiMSJ9.1AX7wDxY6c1qXJ5gFVFXYOVb6LTEOmUNiVllp1t6aHS9j3cgUfQJ7XcxPpU3vkhFEy7eAEdFjK5gluBIEZWuujnEBaobvTNzyouUwBXaSNs1eZ2uGK1MT6cnUlcolxj7ZR-I8cLecjyFvZF8K1FBcxIqfItdb8Kjq4pTITjUZGlw97ck5iSsggbrJCmU3FiVl8znpHevI6tjycLL7zij9gvdwx8WPeAvuUWgiMPQk0jY3v1JeCW55-sbXP_fJ5-7sIAJ-57YWTnH86W_x3pSneNKs2krw8LYlLmIf72GljKDlKX_73QvtPNYgcg40R4KFUgYFr_fHWU4oUR8Vdfw0Cdpih-6layxGOn4hlIMouc.O48DybnV2ME8jdPP9K7Q-Z9-jzZyi4rHSP8ADatuV24&dib_tag=se&keywords=ZEBRONICS%2BThunder%2BBluetooth%2B5.3%2BWireless%2BOver%2BEar%2BHeadphones%2Bwith%2B60H%2BBackup%2C%2BGaming%2BMode%2C%2BDual%2BPairing%2C%2BEnc%2C%2BAux%2C%2BMicro%2BSd%2C%2BVoice%2BAssistant%2C%2BComfortable%2BEarcups%2C%2BCall%2BFunction&nsdOptOutParam=true&qid=1739188725&s=electronics&sprefix=zebronics%2Bthunder%2Bbluetooth%2B5.3%2Bwireless%2Bover%2Bear%2Bheadphones%2Bwith%2B60h%2Bbackup%2C%2Bgaming%2Bmode%2C%2Bdual%2Bpairing%2C%2Benc%2C%2Baux%2C%2Bmicro%2Bsd%2C%2Bvoice%2Bassistant%2C%2Bcomfortable%2Bearcups%2C%2Bcall%2Bfunction%2Celectronics%2C246&sr=1-4&th=1",
# "ZEBRONICS Thunder Bluetooth 5.3 Wireless Over Ear Headphones with 60H Backup (Red)":"https://www.amazon.in/ZEBRONICS-Bluetooth-Headphones-Assistant-Comfortable/dp/B07L8LTS3J/ref=sr_1_5?crid=1Q9Y5CJ3Z2XT3&dib=eyJ2IjoiMSJ9.1AX7wDxY6c1qXJ5gFVFXYOVb6LTEOmUNiVllp1t6aHS9j3cgUfQJ7XcxPpU3vkhFEy7eAEdFjK5gluBIEZWuujnEBaobvTNzyouUwBXaSNs1eZ2uGK1MT6cnUlcolxj7ZR-I8cLecjyFvZF8K1FBcxIqfItdb8Kjq4pTITjUZGlw97ck5iSsggbrJCmU3FiVl8znpHevI6tjycLL7zij9gvdwx8WPeAvuUWgiMPQk0jY3v1JeCW55-sbXP_fJ5-7sIAJ-57YWTnH86W_x3pSneNKs2krw8LYlLmIf72GljKDlKX_73QvtPNYgcg40R4KFUgYFr_fHWU4oUR8Vdfw0Cdpih-6layxGOn4hlIMouc.O48DybnV2ME8jdPP9K7Q-Z9-jzZyi4rHSP8ADatuV24&dib_tag=se&keywords=ZEBRONICS%2BThunder%2BBluetooth%2B5.3%2BWireless%2BOver%2BEar%2BHeadphones%2Bwith%2B60H%2BBackup%2C%2BGaming%2BMode%2C%2BDual%2BPairing%2C%2BEnc%2C%2BAux%2C%2BMicro%2BSd%2C%2BVoice%2BAssistant%2C%2BComfortable%2BEarcups%2C%2BCall%2BFunction&nsdOptOutParam=true&qid=1739188725&s=electronics&sprefix=zebronics%2Bthunder%2Bbluetooth%2B5.3%2Bwireless%2Bover%2Bear%2Bheadphones%2Bwith%2B60h%2Bbackup%2C%2Bgaming%2Bmode%2C%2Bdual%2Bpairing%2C%2Benc%2C%2Baux%2C%2Bmicro%2Bsd%2C%2Bvoice%2Bassistant%2C%2Bcomfortable%2Bearcups%2C%2Bcall%2Bfunction%2Celectronics%2C246&sr=1-5&th=1",
# "ZEBRONICS Thunder Over Ear Bluetooth 5.3 Wireless Headphones with 60H Backup (Blue)":"https://www.amazon.in/ZEBRONICS-Bluetooth-Headphones-Assistant-Comfortable/dp/B07L8JTZ4H/ref=sr_1_6?crid=1Q9Y5CJ3Z2XT3&dib=eyJ2IjoiMSJ9.1AX7wDxY6c1qXJ5gFVFXYOVb6LTEOmUNiVllp1t6aHS9j3cgUfQJ7XcxPpU3vkhFEy7eAEdFjK5gluBIEZWuujnEBaobvTNzyouUwBXaSNs1eZ2uGK1MT6cnUlcolxj7ZR-I8cLecjyFvZF8K1FBcxIqfItdb8Kjq4pTITjUZGlw97ck5iSsggbrJCmU3FiVl8znpHevI6tjycLL7zij9gvdwx8WPeAvuUWgiMPQk0jY3v1JeCW55-sbXP_fJ5-7sIAJ-57YWTnH86W_x3pSneNKs2krw8LYlLmIf72GljKDlKX_73QvtPNYgcg40R4KFUgYFr_fHWU4oUR8Vdfw0Cdpih-6layxGOn4hlIMouc.O48DybnV2ME8jdPP9K7Q-Z9-jzZyi4rHSP8ADatuV24&dib_tag=se&keywords=ZEBRONICS%2BThunder%2BBluetooth%2B5.3%2BWireless%2BOver%2BEar%2BHeadphones%2Bwith%2B60H%2BBackup%2C%2BGaming%2BMode%2C%2BDual%2BPairing%2C%2BEnc%2C%2BAux%2C%2BMicro%2BSd%2C%2BVoice%2BAssistant%2C%2BComfortable%2BEarcups%2C%2BCall%2BFunction&nsdOptOutParam=true&qid=1739188725&s=electronics&sprefix=zebronics%2Bthunder%2Bbluetooth%2B5.3%2Bwireless%2Bover%2Bear%2Bheadphones%2Bwith%2B60h%2Bbackup%2C%2Bgaming%2Bmode%2C%2Bdual%2Bpairing%2C%2Benc%2C%2Baux%2C%2Bmicro%2Bsd%2C%2Bvoice%2Bassistant%2C%2Bcomfortable%2Bearcups%2C%2Bcall%2Bfunction%2Celectronics%2C246&sr=1-6&th=1"   
# "House of Quirk 1200ML Stainless Steel Tumbler (Green)":"https://www.amazon.in/OCEANEVO-Stainless-Tumbler-Insulated-Leakproof/dp/B0D631YTDT/ref=sr_1_3_sspa?crid=1AGBTKODWN1UX&dib=eyJ2IjoiMSJ9.nrXSdJgz9wxScAo78fS0NHW4KP6taMtjOR8C-G4c9iK-PLEfPeWWJlAC7-9u-JQDgegMjPpACMSphH0p9BvASCftoT4ep0b7RaKjKpHsZW_bWRphKvk21U4O6mOU_LlMUudGnIuFSX6fzh0O9NzVD_7SvG9ZIbg1C4VPrmGmpILNXGT0kvIQ78xrgxp9OqfVrvxbweZ51VL4BoGGexoVhmZIqZXsiQdwpHHIRX_aLQs38H5VhIVCuR-aP4YZ0k4ARVFbAgmFCIxBgsbZDFvopSvRI-3zMg0qpB65DKcCppw.KuH7YLPcTwwSPPwlNo09F89-sI2M5v27oW6sh6svVY8&dib_tag=se&keywords=House%2Bof%2BQuirk%2B1200ML%2BStainless%2BSteel%2BTumbler%2BHot%2Band%2BCold%2Bwith%2BHandle%2Band%2BLid%2B2%2BStraw%2C%2BDouble%2BInsulated%2BCup%2BLeak%2BProof%2BMug%2BCupholder%2Bfor%2BGym%2C%2BTravelling%2B(Oatmeal)&nsdOptOutParam=true&qid=1739190831&sprefix=house%2Bof%2Bquirk%2B1200ml%2Bstainless%2Bsteel%2Btumbler%2Bhot%2Band%2Bcold%2Bwith%2Bhandle%2Band%2Blid%2B2%2Bstraw%2C%2Bdouble%2Binsulated%2Bcup%2Bleak%2Bproof%2Bmug%2Bcupholder%2Bfor%2Bgym%2C%2Btravelling%2Boatmeal%2B%2Caps%2C251&sr=8-3-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&smid=A32IMOCB6C4QUT&th=1",
# "House of Quirk 1200ML Stainless Steel Tumbler (Pink)":"https://www.amazon.in/Rioware%C2%AE-Stainless-Insulated-Cupholder-Travelling/dp/B0D98VXYBJ/ref=sr_1_4_sspa?crid=1AGBTKODWN1UX&dib=eyJ2IjoiMSJ9.nrXSdJgz9wxScAo78fS0NHW4KP6taMtjOR8C-G4c9iK-PLEfPeWWJlAC7-9u-JQDgegMjPpACMSphH0p9BvASCftoT4ep0b7RaKjKpHsZW_bWRphKvk21U4O6mOU_LlMUudGnIuFSX6fzh0O9NzVD_7SvG9ZIbg1C4VPrmGmpILNXGT0kvIQ78xrgxp9OqfVrvxbweZ51VL4BoGGexoVhmZIqZXsiQdwpHHIRX_aLQs38H5VhIVCuR-aP4YZ0k4ARVFbAgmFCIxBgsbZDFvopSvRI-3zMg0qpB65DKcCppw.KuH7YLPcTwwSPPwlNo09F89-sI2M5v27oW6sh6svVY8&dib_tag=se&keywords=House%2Bof%2BQuirk%2B1200ML%2BStainless%2BSteel%2BTumbler%2BHot%2Band%2BCold%2Bwith%2BHandle%2Band%2BLid%2B2%2BStraw%2C%2BDouble%2BInsulated%2BCup%2BLeak%2BProof%2BMug%2BCupholder%2Bfor%2BGym%2C%2BTravelling%2B(Oatmeal)&nsdOptOutParam=true&qid=1739190831&sprefix=house%2Bof%2Bquirk%2B1200ml%2Bstainless%2Bsteel%2Btumbler%2Bhot%2Band%2Bcold%2Bwith%2Bhandle%2Band%2Blid%2B2%2Bstraw%2C%2Bdouble%2Binsulated%2Bcup%2Bleak%2Bproof%2Bmug%2Bcupholder%2Bfor%2Bgym%2C%2Btravelling%2Boatmeal%2B%2Caps%2C251&sr=8-4-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1",
# "House of Quirk 1200ML Stainless Steel Tumbler (Oatmeal)":"https://www.amazon.in/OCEANEVO-Stainless-Tumbler-Insulated-Leakproof/dp/B0D631YTDT/ref=sr_1_3_sspa?crid=1AGBTKODWN1UX&dib=eyJ2IjoiMSJ9.nrXSdJgz9wxScAo78fS0NHW4KP6taMtjOR8C-G4c9iK-PLEfPeWWJlAC7-9u-JQDgegMjPpACMSphH0p9BvASCftoT4ep0b7RaKjKpHsZW_bWRphKvk21U4O6mOU_LlMUudGnIuFSX6fzh0O9NzVD_7SvG9ZIbg1C4VPrmGmpILNXGT0kvIQ78xrgxp9OqfVrvxbweZ51VL4BoGGexoVhmZIqZXsiQdwpHHIRX_aLQs38H5VhIVCuR-aP4YZ0k4ARVFbAgmFCIxBgsbZDFvopSvRI-3zMg0qpB65DKcCppw.KuH7YLPcTwwSPPwlNo09F89-sI2M5v27oW6sh6svVY8&dib_tag=se&keywords=House%2Bof%2BQuirk%2B1200ML%2BStainless%2BSteel%2BTumbler%2BHot%2Band%2BCold%2Bwith%2BHandle%2Band%2BLid%2B2%2BStraw%2C%2BDouble%2BInsulated%2BCup%2BLeak%2BProof%2BMug%2BCupholder%2Bfor%2BGym%2C%2BTravelling%2B(Oatmeal)&nsdOptOutParam=true&qid=1739190831&sprefix=house%2Bof%2Bquirk%2B1200ml%2Bstainless%2Bsteel%2Btumbler%2Bhot%2Band%2Bcold%2Bwith%2Bhandle%2Band%2Blid%2B2%2Bstraw%2C%2Bdouble%2Binsulated%2Bcup%2Bleak%2Bproof%2Bmug%2Bcupholder%2Bfor%2Bgym%2C%2Btravelling%2Boatmeal%2B%2Caps%2C251&sr=8-3-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&smid=A32IMOCB6C4QUT&th=1",
# "House of Quirk 1200ML Stainless Steel Tumbler(Rose Quartz)":"https://www.amazon.in/Leczonio-lid-Insulated-Stainless-Cupholder/dp/B0DBZ5K866/ref=sr_1_2_sspa?crid=1AGBTKODWN1UX&dib=eyJ2IjoiMSJ9.nrXSdJgz9wxScAo78fS0NHW4KP6taMtjOR8C-G4c9iK-PLEfPeWWJlAC7-9u-JQDgegMjPpACMSphH0p9BvASCftoT4ep0b7RaKjKpHsZW_bWRphKvk21U4O6mOU_LlMUudGnIuFSX6fzh0O9NzVD_7SvG9ZIbg1C4VPrmGmpILNXGT0kvIQ78xrgxp9OqfVrvxbweZ51VL4BoGGexoVhmZIqZXsiQdwpHHIRX_aLQs38H5VhIVCuR-aP4YZ0k4ARVFbAgmFCIxBgsbZDFvopSvRI-3zMg0qpB65DKcCppw.KuH7YLPcTwwSPPwlNo09F89-sI2M5v27oW6sh6svVY8&dib_tag=se&keywords=House%2Bof%2BQuirk%2B1200ML%2BStainless%2BSteel%2BTumbler%2BHot%2Band%2BCold%2Bwith%2BHandle%2Band%2BLid%2B2%2BStraw%2C%2BDouble%2BInsulated%2BCup%2BLeak%2BProof%2BMug%2BCupholder%2Bfor%2BGym%2C%2BTravelling%2B(Oatmeal)&nsdOptOutParam=true&qid=1739190831&sprefix=house%2Bof%2Bquirk%2B1200ml%2Bstainless%2Bsteel%2Btumbler%2Bhot%2Band%2Bcold%2Bwith%2Bhandle%2Band%2Blid%2B2%2Bstraw%2C%2Bdouble%2Binsulated%2Bcup%2Bleak%2Bproof%2Bmug%2Bcupholder%2Bfor%2Bgym%2C%2Btravelling%2Boatmeal%2B%2Caps%2C251&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1",
# "House of Quirk 1200ML Stainless Steel Tumbler (Oatmeal)":"https://www.amazon.in/House-Quirk-Stainless-Insulated-Travelling/dp/B0CQCCLSV8/ref=sr_1_5?crid=1AGBTKODWN1UX&dib=eyJ2IjoiMSJ9.nrXSdJgz9wxScAo78fS0NHW4KP6taMtjOR8C-G4c9iK-PLEfPeWWJlAC7-9u-JQDgegMjPpACMSphH0p9BvASCftoT4ep0b7RaKjKpHsZW_bWRphKvk21U4O6mOU_LlMUudGnIuFSX6fzh0O9NzVD_7SvG9ZIbg1C4VPrmGmpILNXGT0kvIQ78xrgxp9OqfVrvxbweZ51VL4BoGGexoVhmZIqZXsiQdwpHHIRX_aLQs38H5VhIVCuR-aP4YZ0k4ARVFbAgmFCIxBgsbZDFvopeIru8YbLImu9DHhyFQjz0aV4M_F_6MRu0iSmMDNRfNNP-95A20FVnW2w3HLi62y46QYwQIlUVb2mBoodIJCSqdD0E6F7MJHyrGmoBGOYS6fu89WIFrXKkIOA71nWKhtWK4rp2i65wQCIlZxac8c2UL00OI9lqQqrjslSR9clXGO.M_K-tcxngE5f-8W2RIoMfulkd3k1pPGdTs0bgdFlU_8&dib_tag=se&keywords=House%2Bof%2BQuirk%2B1200ML%2BStainless%2BSteel%2BTumbler%2BHot%2Band%2BCold%2Bwith%2BHandle%2Band%2BLid%2B2%2BStraw%2C%2BDouble%2BInsulated%2BCup%2BLeak%2BProof%2BMug%2BCupholder%2Bfor%2BGym%2C%2BTravelling%2B(Oatmeal)&nsdOptOutParam=true&qid=1739190831&sprefix=house%2Bof%2Bquirk%2B1200ml%2Bstainless%2Bsteel%2Btumbler%2Bhot%2Band%2Bcold%2Bwith%2Bhandle%2Band%2Blid%2B2%2Bstraw%2C%2Bdouble%2Binsulated%2Bcup%2Bleak%2Bproof%2Bmug%2Bcupholder%2Bfor%2Bgym%2C%2Btravelling%2Boatmeal%2B%2Caps%2C251&sr=8-5&th=1"
       

links={"realme 12 Pro 5G (Submarine Blue, 8GB RAM 256 GB Storage)":"https://www.amazon.in/realme-12-5G-Submarine-Storage/dp/B0CTHXNT9W/ref=sr_1_1?crid=2V6YG7XUURBZ3&dib=eyJ2IjoiMSJ9.8VKsCk3uy1UUAaj-veQNvcLMHMRP_a9iRw-2kIB4i4IykY-aPoUjQHYU07-8_gUeYnS698A10gCVmj0PPbeTX6dlNm7xZatDgH3_ZQ5CczXCtNwgYyWf5Z3DDHAFH4zZyU0g_hAmrF5QjNKJbLEt4j83LxVRhhOlLSO1MykY0SrthzRqthvLEqbsABNu6265uSy-j2tPVTZ4E6Kk1XzG86LAqUqpZw6Gs2uPbCKji2o.lFYERbkPYgIw6enGMJLa5VN1kbZacv16I1t4TVUESm4&dib_tag=se&keywords=realme+12+pro+8+gb+256+gb&nsdOptOutParam=true&qid=1739193382&sprefix=realme+12+pro+8+gb+256+gb%2Caps%2C257&sr=8-1",}
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import re

def extract_price(price_text):
    """Extracts and converts price from a string with currency symbols or commas."""
    price_text = re.sub(r"[^\d]", "", price_text)  # Remove ₹, commas, and other symbols
    return int(price_text) if price_text else 0

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Automatically install the chromedriver version that matches the chromium version
    chromedriver_autoinstaller.install()

    # Create the webdriver with the options and use the default path
    driver = webdriver.Chrome(options=chrome_options)
    return driver

    
def scrape_product_data(link):
    driver = get_driver()
    driver.set_window_size(1920, 1080)
    driver.get(link)
    product_data = {
        "product_name": "",  # Add product_name to the dictionary
        "selling price": 0,
        "original price": 0,
        "discount": 0,
        "rating": 0,
        "review": [],
        "product_url": link,
        "date": datetime.now().strftime("%Y-%m-%d"),
    }
    retry = 0
    while retry < 3:
        try:
            driver.save_screenshot("screenshot.png")
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "a-offscreen")))
            break
        except Exception as e:
            print(f"Retrying... Error: {e}")
            retry += 1
            driver.get(link)
            time.sleep(5)

    try:
        price_elem = driver.find_element(
            By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[2]'
        )
        product_data["selling price"] = int("".join(price_elem.text.strip().split(",")))
    except Exception as e:
        print(f"Error extracting selling price: {e}")

    try:
        original_price = driver.find_element(
        By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[2]/span/span[1]/span[2]/span/span[2]'
        ).text
        product_data["original price"] = extract_price(original_price)
    except Exception as e:
        print(f"Error extracting original price: {e}")


    try:
        discount = driver.find_element(
            By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]'
        )
        full_rating_text = discount.get_attribute("innerHTML").strip()
        if " out of 5 stars" in full_rating_text.lower():
            product_data["rating"] = full_rating_text.lower().split(" out of")[0].strip()
        else:
            product_data["discount"] = full_rating_text
    except Exception as e:
        print(f"Error extracting discount: {e}")

    try:
        rating_elem = driver.find_element(By.XPATH, '//*[@id="acrPopover"]/span[1]/a/span')
        product_data["rating"] = rating_elem.text.strip()
        print("Extracted Rating:", product_data["rating"])
    except Exception as e:
        print(f"Error extracting rating: {e}")
    try:
        # Wait for the review element to appear
        review_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='product-summary']/p/span"))
        )
        product_data["review"].append(review_elem.text.strip())
        print("Extracted Review:", review_elem.text.strip())
    except Exception as e:
        print(f"Error extracting AI-generated review: {e}")


    driver.quit()
    return product_data

for product_name, link in links.items():
    product_data = scrape_product_data(link)
    
    # Update reviews.csv
    try:
        reviews_df = pd.read_csv("reviews.csv")
    except FileNotFoundError:
        reviews_df = pd.DataFrame(columns=["product_name", "review", "rating", "date"])
    
    new_reviews={
        "product_name": product_name,
        "review": product_data["review"],
        "rating": product_data["rating"],
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    
    new_reviews_df = pd.DataFrame(new_reviews)
    reviews_df = pd.concat([reviews_df, new_reviews_df], ignore_index=True)
    reviews_df.to_csv("reviews.csv", index=False)
    
    try:
        competitor_df = pd.read_csv("competitor_data.csv")

        # Drop extra columns if they exist
        competitor_df = competitor_df[['product_name', 'price', 'discount', 'date']]
    except FileNotFoundError:
        competitor_df = pd.DataFrame(columns=["product_name", "price", "discount", "date"])

    # Create new data entry
    new_data = {
        "product_name": product_name,
        "price": product_data["selling price"],
        "discount": product_data["discount"],
        "date": datetime.now().strftime("%Y-%m-%d"),
    }

    #  Convert to DataFrame and ensure column alignment
    new_data_df = pd.DataFrame([new_data], columns=["product_name", "price", "discount", "date"])

    # Append data correctly
    competitor_df = pd.concat([competitor_df, new_data_df], ignore_index=True)

    # Save without extra columns
    competitor_df.to_csv("competitor_data.csv", index=False)

    
# API keys
API_KEY = "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"  # Groq API Key
SLACK_WEBHOOK = "https://hooks.slack.com/services/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"  # Slack webhook URL
# Streamlit app setup
st.set_page_config(layout="wide")
# Create two columns
col1, col2 = st.columns(2)

# Add content to the first column
with col1:
     st.markdown(
        """
        <div style="font-size: 40px; text-align: left; width: 100%;">
            ❄️❄️❄️<strong>E-Commerce Competitor Strategy Dashboard</strong>❄️❄️❄️
        </div>
        """,
        unsafe_allow_html=True,
    )

# Add GIF to the second column
with col2:
    st.markdown(
        """
        <div style="text-align: right;">
            <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbzh4dXpuc2hpY3JlNnR1MDdiMXozMXlreHFoZjl0a2g5anJqNWxtMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/hWe6YajFuxX41eV8I0/giphy.gif" alt="Engaging GIF" width="300">
        </div>
        """,
        unsafe_allow_html=True,
    )

# Utility function to truncate text
def truncate_text(text, max_length=512):
    return text[:max_length]

# Load competitor data
def load_competitor_data():
    """Load competitor data from a CSV file."""
    data = pd.read_csv("competitor_data.csv")
    return data

# Load reviews data
def load_reviews_data():
    """Load reviews data from a CSV file."""
    reviews = pd.read_csv("reviews.csv")
    return reviews

# Analyze customer sentiment
def analyze_sentiment(reviews):
    """Analyze customer sentiment for reviews."""
    sentiment_pipeline = pipeline("sentiment-analysis")
    return sentiment_pipeline(reviews)

# Train predictive model
def train_predictive_model(data):
    """Train a predictive model for competitor pricing strategy."""
    data["Discount"] = data["Discount"].str.replace("%", "").astype(float)
    data["Price"] = data["Price"].astype(float)
    data["Predicted_Discount"] = data["Discount"] + (data["Price"] * 0.05).round(2)

    X = data[["Price", "Discount"]]
    y = data["Predicted_Discount"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    return model

# Forecast discounts using ARIMA
def forecast_discounts_arima(data, future_days=5):
    """
    Forecast future discounts using ARIMA.
    :param data: DataFrame containing historical discount data (with a datetime index).
    :param future_days: Number of days to forecast.
    :return: DataFrame with historical and forecasted discounts.
    """
    data = data.sort_index()
    data["discount"] = pd.to_numeric(data["discount"], errors="coerce")
    data = data.dropna(subset=["discount"])

    discount_series = data["discount"]

    if not isinstance(data.index, pd.DatetimeIndex):
        try:
            data.index = pd.to_datetime(data.index)
        except Exception as e:
            raise ValueError("Index must be datetime or convertible to datetime.") from e

    model = ARIMA(discount_series, order=(5, 1, 0))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=future_days)
    future_dates = pd.date_range(
        start=discount_series.index[-1] + pd.Timedelta(days=1),
        periods=future_days
    )

    forecast_df = pd.DataFrame({"Date": future_dates, "Predicted_Discount": forecast})
    forecast_df.set_index("Date", inplace=True)
    return forecast_df

# Send notifications to Slack
def send_to_slack(data):
    payload = {"text": data}
    response = requests.post(
        SLACK_WEBHOOK,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )
    if response.status_code != 200:
        st.write(f"Failed to send notification to Slack: {response.status_code}")

# Generate strategy recommendations using an LLM
def generate_strategy_recommendation(product_name, competitor_data, sentiment):
    """Generate strategic recommendations using an LLM."""
    date = datetime.now()
    prompt = f"""
    You are a highly skilled business strategist specializing in e-commerce. Based on the following details, suggest actionable strategies:

    *Product Name*: {product_name}
    *Competitor Data* (including current prices, discounts, and predicted discounts):
    {competitor_data}
    *Sentiment Analysis*: {sentiment}
    *Today's Date*: {str(date)}

    # Task:
    - Analyze the competitor data and identify key pricing trends.
    - Leverage sentiment analysis insights to highlight areas where customer satisfaction can be improved.
    - Use the discount predictions to suggest how pricing strategies can be optimized over the next 5 days.
    - Recommend promotional campaigns or marketing strategies that align with customer sentiments and competitive trends.

    Provide your recommendations in a structured format:
    - **Pricing Strategy**
    - **Promotional Campaign Ideas**
    - **Customer Satisfaction Recommendations**
    """

    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama3-8b-8192",
        "temperature": 0,
    }

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps(data),
        headers=headers,
    )
    res = res.json()
    response = res["choices"][0]["message"]["content"]
    return response

# Streamlit UI

st.sidebar.header("❄️Select a Product❄️")

def get_product_list():
    try:
        competitor_df = pd.read_csv("competitor_data.csv")
        return competitor_df["product_name"].drop_duplicates().tolist()
    except FileNotFoundError:
        return []

products = get_product_list()

selected_product = st.sidebar.selectbox("Choose a product to analyze:", products)

competitor_data = load_competitor_data()
reviews_data = load_reviews_data()

product_data = competitor_data[competitor_data["product_name"] == selected_product]
product_reviews = reviews_data[reviews_data["product_name"] == selected_product]

st.header(f"Competitor Analysis for {selected_product}")
st.subheader("Competitor Data")
st.table(product_data.tail(5))

if not product_reviews.empty:
    product_reviews.loc[:, "review"] = product_reviews["review"].apply(lambda x: truncate_text(x, 1024))

    reviews = product_reviews["review"].tolist()
    sentiments = analyze_sentiment(reviews)

    st.subheader("Customer Sentiment Analysis")
    sentiment_df = pd.DataFrame(sentiments)
    fig = px.bar(sentiment_df, x="label", title="Sentiment Analysis Results")
    st.plotly_chart(fig)
else:
    st.write("No reviews available for this product.")

product_data["date"] = pd.to_datetime(product_data["date"], errors="coerce")
# product_data = product_data.dropna(subset=["Date"])
product_data.index= pd.date_range(start=product_data.index.min(), periods=len(product_data), freq="D")
product_data["discount"] = pd.to_numeric(product_data["discount"], errors="coerce")
product_data = product_data.dropna(subset=["discount"])

# Forecasting Model
product_data_with_predictions = forecast_discounts_arima(product_data)

st.subheader("Competitor Current and Predicted Discounts")
st.table(product_data_with_predictions[["Predicted_Discount"]].tail(10))


recommendations = generate_strategy_recommendation(
    selected_product,
    product_data_with_predictions,
    sentiments if not product_reviews.empty else "No reviews available",
)
st.subheader("Strategic Recommendations")
st.write(recommendations)

send_to_slack(recommendations)
