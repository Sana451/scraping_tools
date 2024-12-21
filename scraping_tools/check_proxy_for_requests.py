import requests

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
    'mall-ci': '7EED88D6A83DF30E781110430AE72919|1',
    'SSO_WhatEver': 'L7bkjrMvSvfXZ4XDil5NdJsHkbxQaq1okqBafxJhLEzuA4toNdJAAhQyXK9lJnho29wNThm93aMjhgyVVcsHhk/cM4v02CgQPJV4gwHhVSA0rZcKdng9gchpubb/rxCnovn1zOa2dbQLJ7FriIGdI1ojH1g/K7t5N3oVtZovm+p7HvYQcLtNRKACntVOUqooBzTO22yWBIMX1ycRM5XXdl/DNXoVeEaI0en4Ca4ylKcP/2nXWUPjb+otiOuqDmjq+uC2htXfRhWJb8LfpgnWI3eVIo9Zmqz8HVlAwtmibaTnlSaExBjygLyiWwCzhFPG4PuFHFdihNtYDN0Nh/p6lZUObhn255FjUkkgVpqpOgWdn904kmVlbgheBFjZZ+5clVR8YhztPkDkBT18+KrBEJ9UhwQhpUkqmnDr/Ni+4+91fsBlI+6eaxz67cR/OzYxsgWYYwFg8tPSoc3uTBpqUxTWpT05QfzM',
    'bm_mi': 'EBFA24545E6173FD68F8F27FE7F4CFC4~YAAQHroXAu33oReTAQAAeFOFIBmq6vAwNuFi3f3y8kNDS8BoanMRzCMFHIzLFtg+fMe/xLpFfBJZi2UgWO+9hqNgwgroshcHSlwkK54yqDWTjgJKYcJf28/4G6YJpRAJhn9xYuD3ZRNeOfmxNzdvTqRtVkHNht5AkHDDwtzPH1xH8oWU3IuJCV/S1CYfvZJr0nvkVOMdhK3K9lJer858QCvZbfBr4HyjPxxsibNT7+O3jeBdgLBx+I7uEx0Wvow2i4BAZW+8qd2/TdtHARdbgsiq5rFevhZTn/so7sy3qQefUm342D2TjITnr2T4pZNLEZvRqW3HRLxGGMXsC73WYx3f62YyeSsiGKKuqZqgu2IVmaSVrezw~1',
    'bm_sv': 'C6AA328CF4AFF30083A65AA5B41C0375~YAAQHLoXAkkPvxeTAQAAe2OFIBl6/QqqNLew9vOjVDCc2YVy9mj6UeNSHm9z+cKF6Wa60icv6Gf77Rm58YKhF+6GjdsjN+KS/TfCFuYX2oTUjSAnNYJo3j43RvAtFUU4ltNWITFMKiz/ocPMokuN5Og/mRW+uSwFj3+T8vKPn2xKgYC0xvsC8U4dNqk0uDXUpVo3WEf/3L0eR6shVEzxe+9HaMZbFfUDUc1LaqATfc8JzXAb50BcUcs+fQN3V/bEezYVjdkC8ITfCiQ=~1',
    'ak_bmsc': 'F1F5F3E7EAB5035CB70A21EAEC29763E~000000000000000000000000000000~YAAQHroXAqvwoheTAQAASBKVIBmkk2JsxFImVI2bDM2r18tghFua/i6shKeFqnuSeKXfjYjWxnNyCfA3hdExIchV+j+NQ7tCzVNkk1Y9DHWHrnlzCn3WZovxTibG3ANJpIS366k69as2DJzlAX+0HVr8i8jDGmUrBqEA8O7uBUh6DeX+gv97zBzwgD2c5MAIEARwMim6GAjk8X04er3oAz7IeM2kueRBIyuwOGZ/G9Tfoo24Pzc4jXFx/AdiZ/A8ul73zFxJDzK7TTr4wQaFR6F6cKyWA5WvvGl2RixJkURR6xVILmkCPFM5USqv6VvTC0g13fni4Y3lco8hHc6sEahQb3BD2NXEmrvBaWPKYRGb4g/G6PQGdEE/JyX1/a0oNkc10FrIOzDWlKIQmJfWi7ekEoD/YQHJKKwiwesj48FTOKhI+1ylHawqyt2N0XS+fQS3UPIcsvCSVqYMQBi83FeKwZuaeLskTAg4E0XYUw4gcIDDyYSmoTnKlWe9qXkA+KDO+PKidhpr+N6438rSAkVA',
    '.ASPXAUTH': 'FAA70CC34039BA15FB21D480EF2B4C59A35F56A83D4A8EAF5288343D82160E24CC2C46A06ACB13EEBBFCE8A6A541DD4D66D29F6310C3DEBA5119FE263FCDBC0CA1945C587D4824B6A4822C342B4DA09DFB191A88269F21DEF45902F5F76F16428AE8622654F102B887FE909018E85834C3133314',
    'ste_p': 'fv%3A1731400006438%7Cvs%3A1731416555824%7Clv%3A1731419357304',
    'ste_s': 'stc%3Aundefined%7Clang%3Aen%7Cdbid%3Aisp%7Cdbind%3Aundefined%7Cdbsubind%3Aundefined',
    'mall-sd': '938d926c-d4c1-49ca-9200-e57042868b63',
    'MallCookiePermitions': 'fnct:0,perf:0,targ:0',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8',
    # 'Cookie': 'idp_login_query_param=display=sup flender-off azure-social-common-off facebook-off github-off gitlab-off google-off linkedin-off twitter-off windows-off; ASP.NET_SessionId=uoywivyvghmhwpgpelhhgtjc; _evga_7af4={%22uuid%22:%22e24dd0c9a4249f41%22}; AMCV_EFB35E09512D2A530A490D4D%40AdobeOrg=1585540135%7CMCMID%7C50982330891546286979162646595350957120%7CvVersion%7C4.4.0; s_cc=true; _sfid_baec={%22anonymousId%22:%22e24dd0c9a4249f41%22%2C%22consents%22:[]}; ste_vi=vi_fv%3A1731400006438%7Cvi%3A43bc88326533d1fde17e9b27754878c6; SSO_Y=Y; _shibsession_64656661756c74496e6475737472794d616c6c=_1fe295c1b9b3fd0dfb1e3f66a3748461; RegionUrl=/b1; mall-us=7EED88D6A83DF30E781110430AE72919|EUR|; mall-tn=7EED88D6A83DF30E781110430AE72919|CatalogTree; SiePortalSwitchView=Internet; SiePortalIS=toggles%3D%5B%7B%22name%22%3A%22ISTrackingUserBehavior%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISTrackingWebssoId%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignCarouselRecommendations%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignSupportMaterialRecommendations%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignPromotionExpandable%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISCampaignProductSearchRecommendation%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignIBaseRecommendation%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignChatbotRecommendation%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISTemporaryImplementationToggle%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISCampaignMySiePortalRecommendation%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignSupportPageRecommendation%22%2C%22enabled%22%3Atrue%7D%2C%7B%22name%22%3A%22ISCampaignForumRecommendation%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISCampaignSpiceConfiguratorRecommendation%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISOneHomePlatformPromotion%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISRecommendationEventsAndStoriesEnabled%22%2C%22enabled%22%3Afalse%7D%2C%7B%22name%22%3A%22ISRecommendationNewsTabEnabled%22%2C%22enabled%22%3Afalse%7D%5D; SiePortal=navigation; s_cc=true; sieportal.chatbotSync=%7B%22en%22%3A%7B%22startChat%22%3A0%2C%22closeChat%22%3A0%7D%7D; SieportalGbWebssoID=F0EEF4AE-3B57-4306-96CB-B36764D0F721; ADRUM=s=1731401587096&r=https%3A%2F%2Fsieportal.siemens.com%2Fen-de%2Fhomehttps%3A; mall-ci=7EED88D6A83DF30E781110430AE72919|1; SSO_WhatEver=L7bkjrMvSvfXZ4XDil5NdJsHkbxQaq1okqBafxJhLEzuA4toNdJAAhQyXK9lJnho29wNThm93aMjhgyVVcsHhk/cM4v02CgQPJV4gwHhVSA0rZcKdng9gchpubb/rxCnovn1zOa2dbQLJ7FriIGdI1ojH1g/K7t5N3oVtZovm+p7HvYQcLtNRKACntVOUqooBzTO22yWBIMX1ycRM5XXdl/DNXoVeEaI0en4Ca4ylKcP/2nXWUPjb+otiOuqDmjq+uC2htXfRhWJb8LfpgnWI3eVIo9Zmqz8HVlAwtmibaTnlSaExBjygLyiWwCzhFPG4PuFHFdihNtYDN0Nh/p6lZUObhn255FjUkkgVpqpOgWdn904kmVlbgheBFjZZ+5clVR8YhztPkDkBT18+KrBEJ9UhwQhpUkqmnDr/Ni+4+91fsBlI+6eaxz67cR/OzYxsgWYYwFg8tPSoc3uTBpqUxTWpT05QfzM; bm_mi=EBFA24545E6173FD68F8F27FE7F4CFC4~YAAQHroXAu33oReTAQAAeFOFIBmq6vAwNuFi3f3y8kNDS8BoanMRzCMFHIzLFtg+fMe/xLpFfBJZi2UgWO+9hqNgwgroshcHSlwkK54yqDWTjgJKYcJf28/4G6YJpRAJhn9xYuD3ZRNeOfmxNzdvTqRtVkHNht5AkHDDwtzPH1xH8oWU3IuJCV/S1CYfvZJr0nvkVOMdhK3K9lJer858QCvZbfBr4HyjPxxsibNT7+O3jeBdgLBx+I7uEx0Wvow2i4BAZW+8qd2/TdtHARdbgsiq5rFevhZTn/so7sy3qQefUm342D2TjITnr2T4pZNLEZvRqW3HRLxGGMXsC73WYx3f62YyeSsiGKKuqZqgu2IVmaSVrezw~1; bm_sv=C6AA328CF4AFF30083A65AA5B41C0375~YAAQHLoXAkkPvxeTAQAAe2OFIBl6/QqqNLew9vOjVDCc2YVy9mj6UeNSHm9z+cKF6Wa60icv6Gf77Rm58YKhF+6GjdsjN+KS/TfCFuYX2oTUjSAnNYJo3j43RvAtFUU4ltNWITFMKiz/ocPMokuN5Og/mRW+uSwFj3+T8vKPn2xKgYC0xvsC8U4dNqk0uDXUpVo3WEf/3L0eR6shVEzxe+9HaMZbFfUDUc1LaqATfc8JzXAb50BcUcs+fQN3V/bEezYVjdkC8ITfCiQ=~1; ak_bmsc=F1F5F3E7EAB5035CB70A21EAEC29763E~000000000000000000000000000000~YAAQHroXAqvwoheTAQAASBKVIBmkk2JsxFImVI2bDM2r18tghFua/i6shKeFqnuSeKXfjYjWxnNyCfA3hdExIchV+j+NQ7tCzVNkk1Y9DHWHrnlzCn3WZovxTibG3ANJpIS366k69as2DJzlAX+0HVr8i8jDGmUrBqEA8O7uBUh6DeX+gv97zBzwgD2c5MAIEARwMim6GAjk8X04er3oAz7IeM2kueRBIyuwOGZ/G9Tfoo24Pzc4jXFx/AdiZ/A8ul73zFxJDzK7TTr4wQaFR6F6cKyWA5WvvGl2RixJkURR6xVILmkCPFM5USqv6VvTC0g13fni4Y3lco8hHc6sEahQb3BD2NXEmrvBaWPKYRGb4g/G6PQGdEE/JyX1/a0oNkc10FrIOzDWlKIQmJfWi7ekEoD/YQHJKKwiwesj48FTOKhI+1ylHawqyt2N0XS+fQS3UPIcsvCSVqYMQBi83FeKwZuaeLskTAg4E0XYUw4gcIDDyYSmoTnKlWe9qXkA+KDO+PKidhpr+N6438rSAkVA; .ASPXAUTH=FAA70CC34039BA15FB21D480EF2B4C59A35F56A83D4A8EAF5288343D82160E24CC2C46A06ACB13EEBBFCE8A6A541DD4D66D29F6310C3DEBA5119FE263FCDBC0CA1945C587D4824B6A4822C342B4DA09DFB191A88269F21DEF45902F5F76F16428AE8622654F102B887FE909018E85834C3133314; ste_p=fv%3A1731400006438%7Cvs%3A1731416555824%7Clv%3A1731419357304; ste_s=stc%3Aundefined%7Clang%3Aen%7Cdbid%3Aisp%7Cdbind%3Aundefined%7Cdbsubind%3Aundefined; mall-sd=938d926c-d4c1-49ca-9200-e57042868b63; MallCookiePermitions=fnct:0,perf:0,targ:0',
    'Origin': 'https://mall.industry.siemens.com',
    'Referer': 'https://mall.industry.siemens.com/mall/en/DE/Catalog/Product/?mlfb=1FK7080-5AF71-1UA0&SiepCountryCode=DE&quantity=1',
    'RequestVerificationToken': '7VVAFlPkMlcQA9n1_tc4XoXtaOl9xi6NNczS_3ZcN_V7gvjP1J9-SZw8puCZOjTXmK6sfAFbxWWNdI9NCpoNROwVPME1:NpXAqRYZe3_-0E9ls3SgSyh1wW1p9FyhH5NXlncqbKY6sMGInYmV1Fad5VasPIqLoTQ1MXaB99YIJpyR670jzG3L1K0b0jel4J0BAInSamtRy2rQoKTZ48zLBBZsicRZgzFbvg2',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

url = "https://mall.industry.siemens.com/mall/en/DE/Catalog/Product/?mlfb=5SP3263-3&SiepCountryCode=DE&quantity=1"


with open("/proxy.txt", "r", encoding="utf-8") as f:
    proxy_list = f.readlines()


for proxy in proxy_list:
    proxies = {"http": f"http://{proxy.strip()}", "https": f"http://{proxy.strip()}"}

    try:
        print(proxies)
        response = requests.get(
            url,
            cookies=cookies,
            headers=headers,
            proxies=proxies,
            timeout=5
        )
        if response.status_code != 403:
            print(proxies, "GOOD")
    except Exception:
        print(proxies, "is dead")

