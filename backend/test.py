from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import asyncio

async def main():
  html_content = ""
  product_dict = {
    "url": "https://www.lazada.com.ph/products/beelink-eq14-mini-pc-intel-lake-n150-up-to-36ghz-ddr4-3200mhz-pcie-30-m2-ssd-windows-11-pro-dual-25g-lan-wifi6-bt52-desktop-for-office-1-year-warranty-i4596802114.html"
  }   
  product_dict["url"] = "https://www.lazada.com.ph/products/jbl-partybox-520-portable-battery-powered-party-speaker-with-powerful-and-loud-sound-i5183269064-s30724343190.html?spm=a2o4l.pdp_revamp.recommend_2.1.36873897jQKIkL&mp=1&cid=101100036374424&mp=1&impsrc=&ad_src=1400_522:0.142857,1400_8906:0.125&pid_pvid=eaf8c43c87163c587394fc621906aa7f&sub_product_id=F&pvtime=1755182157&member_id=151220698&mp=1&cpc=174&originalCpc=152&highest_price=152&adFlag=3&pdp_item=4221569797&pa=sponsored_bottom&did=41af66ad-dee6-44da-9318-ea0ad9c62b3f&adid=0&bucketId=0,481452&sellerId=25&itemId=5183269064&ncid=101100036374424&adgroup_id=4320248338&creative_id=10933170419&brand_id=127188081&category_id=10100399&pvid=41af66ad-dee6-44da-9318-ea0ad9c62b3f&abid=21398470,0,21439302,13208392,19483692,16681078,21440074,21432414,21374428,21386330,21379288,13630928,13147232,21391084,12559252,481452,21421290,366889,21431914,12900842,21387124,12575244,21384432,8460342,21375870,21429628,12091908,21425146,21438970,21419526,21120642,21421572,12668418,21394574,12656138,12449264,21376146,21428378,21434136,12345564,21426214,12950436,21435430,12192856,21384356,21382958,240363,12616746,19944028,21426730,21397544,14620714,12729396,12793016,123,21423802,13198516,13057466,21425336&nick=&pos=-1&regional_key=300300001045&impsrc=&crowd_id=&one_id=&"
  async with async_playwright() as p:
      # browser = await p.chromium.launch(headless=False, slow_mo=50)
      browser = await p.chromium.launch()
      page = await browser.new_page()
      wait_until = "load"
      await page.goto(product_dict["url"], wait_until=wait_until, timeout=60000)
      html_content = await page.content()
      await browser.close()

  soup = BeautifulSoup(html_content, "html5lib")
  current_price = None
  product_name = ""
  image_link = ""
  price_tag = soup.find_all(class_="pdp-price_size_xl")
  item_name_tag = soup.find_all(class_= "pdp-mod-product-badge-title")
  preview_image = soup.find_all(class_="gallery-preview-panel__image")
  # print(type(price[0]))
  # discounted_price = price.find_all(id="pdpd-price_size_xl")
  for tag in price_tag:
      current_price = tag.string

  for tag in item_name_tag:
      tag_str = tag.string.replace("  ", "")
      tag_str = tag_str.replace("\n", " ")
      product_name = tag_str

  for tag in preview_image:
      image_link = tag.attrs["src"]

  response =  {
      "url": product_dict["url"],
      "name": product_name,
      "image_link": image_link,
      "details": [
          {
              "price": current_price,
              "timestamp": "",
          }
      ]
  }
  print(response)
  return response

if __name__ == "__main__":
  asyncio.run(main())