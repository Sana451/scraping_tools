import requests


url = "https://mall.industry.siemens.com/mall/en/DE/Catalog/Product/?mlfb=1FL6094-1AC61-0AG1&SiepCountryCode=DE&quantity=1"


cookies = {
    'idp_login_query_param': 'display=sup flender-off azure-social-common-off facebook-off github-off gitlab-off google-off linkedin-off twitter-off windows-off',
    'ASP.NET_SessionId': 'uoywivyvghmhwpgpelhhgtjc',
    '_evga_7af4': '{%22uuid%22:%22e24dd0c9a4249f41%22}',
    'AMCV_EFB35E09512D2A530A490D4D%40AdobeOrg': '1585540135%7CMCMID%7C50982330891546286979162646595350957120%7CvVersion%7C4.4.0',
    's_cc': 'true',
    '_sfid_baec': '{%22anonymousId%22:%22e24dd0c9a4249f41%22%2C%22consents%22:[]}',
    'ste_vi': 'vi_fv%3A1731400006438%7Cvi%3A43bc88326533d1fde17e9b27754878c6',
    'SSO_Y': 'Y',
    '_shibsession_64656661756c74496e6475737472794d616c6c': '_1fe295c1b9b3fd0dfb1e3f66a3748461',
    'RegionUrl': '/b1',
    'mall-us': '7EED88D6A83DF30E781110430AE72919|EUR|',
    'mall-tn': '7EED88D6A83DF30E781110430AE72919|CatalogTree',
    'SiePortalSwitchView': 'Internet',
    'SiePortalIS': 'toggles%3D%5B%7B%22name%22%3A%22ISTrackingUserBehavior%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISTrackingWebssoId%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignCarouselRecommendations%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignSupportMaterialRecommendations%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignPromotionExpandable%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISCampaignProductSearchRecommendation%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignIBaseRecommendation%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignChatbotRecommendation%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISTemporaryImplementationToggle%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISCampaignMySiePortalRecommendation%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignSupportPageRecommendation%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignForumRecommendation%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISCampaignSpiceConfiguratorRecommendation%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISOneHomePlatformPromotion%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISRecommendationEventsAndStoriesEnabled%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISRecommendationNewsTabEnabled%22%2C%22enabled%22%3Afalse%7D%5D',
    'SiePortal': 'navigation',
    's_cc': 'true',
    'sieportal.chatbotSync': '%7B%22en%22%3A%7B%22startChat%22%3A0%2C%22closeChat%22%3A0%7D%7D',
    'SieportalGbWebssoID': 'F0EEF4AE-3B57-4306-96CB-B36764D0F721',
    'ADRUM': 's=1731401587096&r=https%3A%2F%2Fsieportal.siemens.com%2Fen-de%2Fhomehttps%3A',
    'SSO_WhatEver': 'AGeoQ9WZwwV/OH3mxve3TBB76MKNRZvmQNO07HN79liz5Fm4+n8Eg1NZ78edomqWQ5xXQFxuiLNoN/bmCClIMkdv3y9u9avfcB3YALtekzM+5kOdAw1vW4nmVvROeepmdBhkaFt7OaFTN7HTreQ6vNUwrMF5OKcDgEDqVy3IDAb77k1QW4IRPa3UpThrtRCdGqWYcx8dSwYdSC7aFONRiEtSCkqbO7m00VntVS9os1gBppxT09L+QqBYDfplXBCPjTofkgzsvT6VHE78P4sUeIc/yFgwyE+lWwvWr+0YS2cbEUoYHzWU3fGR33tT851dEXYqtt5b5OGgL9JPZc55l2v6TRXwA89QmPqURznzowPvrryYqozS1iYI3tB+UXeeW1Gd4sN8Qg/XHJXZB8kfOTSV/Av+/c6lqWT9KTT2TeV6BMQ5lT53UUyYD4ERxYfehGNXVgZzpHw/yvuqZJ02OWZw/A7FDYMi',
    'mall-ci': '7EED88D6A83DF30E781110430AE72919|1',
    'bm_mi': 'D0EA6F1B66254F867DE28038F560FCB2~YAAQHroXAsrnlxeTAQAAYebzHxnEpi6JSoEddG4XluGSnxIyZsIOv/6sWOQi8qxSVUsWQ89lXz9M4kRLd8+RqlrDNJQylk6uBQkrTdaIqHJQ0wigUnOWViqwW2W6rWgi8Q/bQ/4Mre3viXebIhZgbv92WBaYSXwN1GHPxoN/CyBaY/NCLFzGMsOh3v/7W8tHNkg7KHJB0iBaguCA+2GRT5AHxOtrcwHTbTkKBYIUG2zuqE7VfQLb2k/OThvyjV9DCN3wgd61Pbtkavzr9n3xw/NnHWW/j6LJTlh41UT3Yt2fCFJIj9mZwpFYz4QO5m+cYrx2VKgVO9wVIgDNv7uQf1yvQEM1M6QRwId0lBDUliA=~1',
    'ak_bmsc': 'D654DA068A1ACADC6E917AE0B8896597~000000000000000000000000000000~YAAQHLoXAgACtheTAQAAr+3zHxmDXh37swPj7DVgI1InaYmLBRa6TUcZi8JoSsENEXUN85ELo86hGCRjPFfkHGPPMwm9CmcjUv6UiqIz3LNqkD2YhfbFnoRfR1Smg71EEWzjUotqu0+GLWMKC+btZjHcl4t9kKLTEevDw8nssg9BAXGV21rc66nASsXodYLt2snEARsN2OWgYGPK6+bpeGkzrqLnoeMURxtdv7RjOORMjq3K1Um0gTCEORe4oH5pt1aD8+atbTjK3xQHnP2GmCWjhYkCdBRVVrPP6qAG4kg72OEPKtdOE1B+e3loKAYl3f1wmVnq5BFRGCcNJMcEUUkSblLxZgxND+qzlkTArQyRoPIOJ0Q6Hz3nBbROPkKZ7/JKY246RHQA2ALHN8FXB6z5PO0rHZV+v5QHlCKk6Bc28IV7fNuCqPY4viSVu/L5zHl5folOyKZgJU4F8Cpbe8l8V0g0NZ/I4UMPj0ob907oIXpjpJNfGZWuh7us4yO8XnnM32/1sYE=',
    'MallCookiePermitions': 'fnct:1,perf:1,targ:1',
    'ste_p': 'fv%3A1731400006438%7Cvs%3A1731407484508%7Clv%3A1731407967307',
    'ste_s': 'stc%3Aundefined%7Clang%3Aen%7Cdbid%3Aisp%7Cdbind%3Aundefined%7Cdbsubind%3Aundefined',
    '.ASPXAUTH': '662BFBD92E660A153F81F4D13D164FD2FC01F082FA93021836065FFD6F7CFB978977385E5DA3FC921E3B36B22BF2815A1665F707B648E90502762BC8FD4F5429EA3B4C7F7B9CDB2C617135D2DB613BE8B6E494A91D944F64B028B23919DA7FC9882FCD7EC3B9E2B00CD8BDC2EBD97D11AE5F3593',
    'mall-sd': 'ae31d74d-06df-4c5e-ba8b-f2132c8cd0c1',
    'bm_sv': '9341807F030A2595B7A7B8505CE750A3~YAAQHLoXAmkJtheTAQAArkT1HxkxXwzW88lgpzewNqwbcMUZ1vqG+6pcarLke8HZjPF5YgTVBD1SZ9eUtkf7mQfSMJRUKYxIUhVXAwC13AHLle5tScnMjjcokKhYvUzvgurdvO8OhfhlGaFVazDtIKE8/INXYdMgLcWvaElUc9nIWtjyixQRbNWJpc8dMPgW7auuyHsVOIA6vxDfBD7ukFGmUBPJ+GVuLD+2JlsJJyc6KDBow8gh2AlnzGjx+2U08JBbUMHcpg/EP3M=~1',
    'ste_cds': 'ppn%3Axm%253Ade%253Aen%252Fproductsviewlayer%7Ccdiv%3An%252Fa',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'idp_login_query_param=display=sup flender-off azure-social-common-off facebook-off github-off gitlab-off google-off linkedin-off twitter-off windows-off; ASP.NET_SessionId=uoywivyvghmhwpgpelhhgtjc; _evga_7af4={%22uuid%22:%22e24dd0c9a4249f41%22}; AMCV_EFB35E09512D2A530A490D4D%40AdobeOrg=1585540135%7CMCMID%7C50982330891546286979162646595350957120%7CvVersion%7C4.4.0; s_cc=true; _sfid_baec={%22anonymousId%22:%22e24dd0c9a4249f41%22%2C%22consents%22:[]}; ste_vi=vi_fv%3A1731400006438%7Cvi%3A43bc88326533d1fde17e9b27754878c6; SSO_Y=Y; _shibsession_64656661756c74496e6475737472794d616c6c=_1fe295c1b9b3fd0dfb1e3f66a3748461; RegionUrl=/b1; mall-us=7EED88D6A83DF30E781110430AE72919|EUR|; mall-tn=7EED88D6A83DF30E781110430AE72919|CatalogTree; SiePortalSwitchView=Internet; SiePortalIS=toggles%3D%5B%7B%22name%22%3A%22ISTrackingUserBehavior%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISTrackingWebssoId%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignCarouselRecommendations%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignSupportMaterialRecommendations%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignPromotionExpandable%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISCampaignProductSearchRecommendation%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignIBaseRecommendation%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignChatbotRecommendation%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISTemporaryImplementationToggle%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISCampaignMySiePortalRecommendation%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignSupportPageRecommendation%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignForumRecommendation%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISCampaignSpiceConfiguratorRecommendation%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISOneHomePlatformPromotion%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISRecommendationEventsAndStoriesEnabled%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISRecommendationNewsTabEnabled%22%2C%22enabled%22%3Afalse%7D%5D; SiePortal=navigation; s_cc=true; sieportal.chatbotSync=%7B%22en%22%3A%7B%22startChat%22%3A0%2C%22closeChat%22%3A0%7D%7D; SieportalGbWebssoID=F0EEF4AE-3B57-4306-96CB-B36764D0F721; ADRUM=s=1731401587096&r=https%3A%2F%2Fsieportal.siemens.com%2Fen-de%2Fhomehttps%3A; SSO_WhatEver=AGeoQ9WZwwV/OH3mxve3TBB76MKNRZvmQNO07HN79liz5Fm4+n8Eg1NZ78edomqWQ5xXQFxuiLNoN/bmCClIMkdv3y9u9avfcB3YALtekzM+5kOdAw1vW4nmVvROeepmdBhkaFt7OaFTN7HTreQ6vNUwrMF5OKcDgEDqVy3IDAb77k1QW4IRPa3UpThrtRCdGqWYcx8dSwYdSC7aFONRiEtSCkqbO7m00VntVS9os1gBppxT09L+QqBYDfplXBCPjTofkgzsvT6VHE78P4sUeIc/yFgwyE+lWwvWr+0YS2cbEUoYHzWU3fGR33tT851dEXYqtt5b5OGgL9JPZc55l2v6TRXwA89QmPqURznzowPvrryYqozS1iYI3tB+UXeeW1Gd4sN8Qg/XHJXZB8kfOTSV/Av+/c6lqWT9KTT2TeV6BMQ5lT53UUyYD4ERxYfehGNXVgZzpHw/yvuqZJ02OWZw/A7FDYMi; mall-ci=7EED88D6A83DF30E781110430AE72919|1; bm_mi=D0EA6F1B66254F867DE28038F560FCB2~YAAQHroXAsrnlxeTAQAAYebzHxnEpi6JSoEddG4XluGSnxIyZsIOv/6sWOQi8qxSVUsWQ89lXz9M4kRLd8+RqlrDNJQylk6uBQkrTdaIqHJQ0wigUnOWViqwW2W6rWgi8Q/bQ/4Mre3viXebIhZgbv92WBaYSXwN1GHPxoN/CyBaY/NCLFzGMsOh3v/7W8tHNkg7KHJB0iBaguCA+2GRT5AHxOtrcwHTbTkKBYIUG2zuqE7VfQLb2k/OThvyjV9DCN3wgd61Pbtkavzr9n3xw/NnHWW/j6LJTlh41UT3Yt2fCFJIj9mZwpFYz4QO5m+cYrx2VKgVO9wVIgDNv7uQf1yvQEM1M6QRwId0lBDUliA=~1; ak_bmsc=D654DA068A1ACADC6E917AE0B8896597~000000000000000000000000000000~YAAQHLoXAgACtheTAQAAr+3zHxmDXh37swPj7DVgI1InaYmLBRa6TUcZi8JoSsENEXUN85ELo86hGCRjPFfkHGPPMwm9CmcjUv6UiqIz3LNqkD2YhfbFnoRfR1Smg71EEWzjUotqu0+GLWMKC+btZjHcl4t9kKLTEevDw8nssg9BAXGV21rc66nASsXodYLt2snEARsN2OWgYGPK6+bpeGkzrqLnoeMURxtdv7RjOORMjq3K1Um0gTCEORe4oH5pt1aD8+atbTjK3xQHnP2GmCWjhYkCdBRVVrPP6qAG4kg72OEPKtdOE1B+e3loKAYl3f1wmVnq5BFRGCcNJMcEUUkSblLxZgxND+qzlkTArQyRoPIOJ0Q6Hz3nBbROPkKZ7/JKY246RHQA2ALHN8FXB6z5PO0rHZV+v5QHlCKk6Bc28IV7fNuCqPY4viSVu/L5zHl5folOyKZgJU4F8Cpbe8l8V0g0NZ/I4UMPj0ob907oIXpjpJNfGZWuh7us4yO8XnnM32/1sYE=; MallCookiePermitions=fnct:1,perf:1,targ:1; ste_p=fv%3A1731400006438%7Cvs%3A1731407484508%7Clv%3A1731407967307; ste_s=stc%3Aundefined%7Clang%3Aen%7Cdbid%3Aisp%7Cdbind%3Aundefined%7Cdbsubind%3Aundefined; .ASPXAUTH=662BFBD92E660A153F81F4D13D164FD2FC01F082FA93021836065FFD6F7CFB978977385E5DA3FC921E3B36B22BF2815A1665F707B648E90502762BC8FD4F5429EA3B4C7F7B9CDB2C617135D2DB613BE8B6E494A91D944F64B028B23919DA7FC9882FCD7EC3B9E2B00CD8BDC2EBD97D11AE5F3593; mall-sd=ae31d74d-06df-4c5e-ba8b-f2132c8cd0c1; bm_sv=9341807F030A2595B7A7B8505CE750A3~YAAQHLoXAmkJtheTAQAArkT1HxkxXwzW88lgpzewNqwbcMUZ1vqG+6pcarLke8HZjPF5YgTVBD1SZ9eUtkf7mQfSMJRUKYxIUhVXAwC13AHLle5tScnMjjcokKhYvUzvgurdvO8OhfhlGaFVazDtIKE8/INXYdMgLcWvaElUc9nIWtjyixQRbNWJpc8dMPgW7auuyHsVOIA6vxDfBD7ukFGmUBPJ+GVuLD+2JlsJJyc6KDBow8gh2AlnzGjx+2U08JBbUMHcpg/EP3M=~1; ste_cds=ppn%3Axm%253Ade%253Aen%252Fproductsviewlayer%7Ccdiv%3An%252Fa',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':
        'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}



resp = requests.get(
    url,
    proxies={
        'http': 'http://vk0dUcb:Us5jxS8o88@23.27.3.254:59100',
        'https': 'http://vk0dUcb:Us5jxS8o88@138.36.92.202:59100',
        # "http": "http://54.152.3.36:80",
        # "https": "http://54.152.3.36:80",
    },
    timeout=10
)

print(resp.status_code)
print(resp.content)
