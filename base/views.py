from django.shortcuts import render
from .models import Shoe, Márka, bestseller
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import datetime
import random

def home(request):

    márkák = ['Nike', 'New Balance', 'Adidas', 'Air Jordan', 'Yeezy']

    for marka in márkák:
        Márka.objects.get_or_create(
            name = marka
            )
    népszerű_cipők = ['Nike Dunk', 'Air Jordan', 'Adidas Campus', 'Air Force', 'Yeezy', 'New Blanace 550']
    for shoe in népszerű_cipők:
        bestseller.objects.get_or_create(
            name = shoe
            )
            
    base_url_1 = "https://www.truetosole.hu/collections/sneaker?page={}&grid_list=grid-view"
    result = requests.get(base_url_1).text
    doc = BeautifulSoup(result, "html.parser")
    nav = doc.select_one("nav.pagination--container")
    szamolas = 0
    szam = int(nav.select("li")[-2].select_one("a").string)
    with requests.Session() as s:
        for b in range(1, 1): 
            url = base_url_1.format(b)
            result_ = s.get(url).text
            doc_ = BeautifulSoup(result_, "html.parser")
            ul_ = doc_.select_one("ul.productgrid--items.products-per-row-4")
            if ul_ is None:  
                break
            li_ = ul_.find_all("li")  
            for i in li_:
                img = i.select_one("img.productitem--image-primary")
                src = img['src']
                név = i.find('h2', class_="productitem--title")
                név = név.a
                név = név.text.strip
                asd = i.select_one("div.price__current")
                árak  = asd.find("span", class_="mw-price")
                ár = árak.string
                ár = ár.replace("FT", "")
                link = i.find('a', attrs={'data-product-page-link': True}) 
                link = link["href"]
                link = f"https://www.truetosole.hu{link}"
                rendezes = re.sub(r'[^\d\s]', '', ár)
                rendezes = rendezes.replace(" ", "")
                rendezes = int(rendezes)
                
                Shoe.objects.get_or_create(
                    name = név,
                    price = ár,
                    image = src,
                    rendszerezes = rendezes,
                    cég = "TrueToSole",
                    link = link
                )
                szamolas += 1

    base_url = "https://balazskicks.com/collections/sneakerek?page={}"

    for a in range(1, 1):
        url = base_url.format(a)
        result = requests.get(url).text
        doc = BeautifulSoup(result, "html.parser")
        divs = doc.find_all('div', class_='product-card__info')
        if not divs:
            break
        nevek = []
        fotok = []
        árak = []
        linkek = []
        for cucc in divs:
            név = cucc.find('span', class_='product-card__title')
            név = név.a
            név = név.string
            ár = cucc.find('span', class_='tlab-currency-format')
            ár = ár.string
            ár = ár.split('.')
            ár = ár[0].replace(",", " ")
            rendezes = ár.replace(" ", "")
            árak.append(ár)
            nevek.append(név)
        foto_divs = doc.find_all('div', class_='product-card__figure')
        for kepstuff in foto_divs:
            a = kepstuff.a
            img = a.img
            src = img['src']
            link = a['href']
            fotok.append(src)
            linkek.append(link)
        cipők = list(zip(nevek, árak, fotok, linkek))
        for cipő_dolgok in cipők:
            rendezes = cipő_dolgok[1]
            rendezes = rendezes.replace(" ", "")
            jo_link = cipő_dolgok[3]
            jo_link = f"https://balazskicks.com{jo_link}"
            Shoe.objects.get_or_create(
                        name = cipő_dolgok[0],
                        price = cipő_dolgok[1],
                        image = cipő_dolgok[2],
                        rendszerezes = rendezes,
                        cég = "balázskicks",
                        link = jo_link,
                    )
    márka_sneak = ['nike', 'air-jordan', 'adidas', 'new-balance-1']
    nevek = []
    fotok = []
    linkek = []
    árak = []
    for w in márka_sneak:
        for y in range(1, 1):
            url = f"https://sneakcenter.com/collections/{w}?page={y}"
            result = requests.get(url).text
            doc = BeautifulSoup(result, "html.parser")
            árak_span = doc.find_all('p', class_='product-item__price')
            if not árak_span:
                break
            for i in árak_span:
                try:
                    ár = i.find('span', class_='sale')
                    ár = ár.span
                    ár = ár.string
                except:
                    ár = i.find('span', class_='money')
                    ár = ár.string
                ár = ár.split('.')[0].replace(",", " ")
                árak.append(ár)
            név_h4 = doc.find_all('h4', class_='ff-body product-item__product-title fs-product-card-title')
            for x in név_h4:
                a = x.a                    
                név = a.string
                if "(W)" or "(GS)" in név:
                    név = név.replace("(W)", "")
                    név = név.replace("(GS)", "")
                nevek.append(név)
            kep_as = doc.find_all('a', class_='product-item__image-link')
            for kep_div in kep_as:
                    link = kep_div['href']
                    link = f"https://sneakcenter.com/{link}"
                    div = kep_div.div
                    img = div.img
                    src = img['src']
                    fotok.append(src)
                    linkek.append(link)

    cipők = list(zip(nevek, árak, fotok, linkek))  
    for cipő_dolgok in cipők:
        rendezes = cipő_dolgok[1].replace(" ", "")
        Shoe.objects.get_or_create(
                            name = cipő_dolgok[0],
                            price = cipő_dolgok[1],
                            image = cipő_dolgok[2],
                            rendszerezes = rendezes,
                            cég = "sneakercenter",
                            link = cipő_dolgok[3],
                        )
    base_url_2 = "https://onsize.eu/collections/sneakerek?page={}"

    nevek = []
    árak = []
    fotók = []
    fotók_2 = []
    linkek = []

    for i in range(1, 1):
        url = base_url_2.format(i)
        result = requests.get(url).text
        doc = BeautifulSoup(result, "html.parser")
        divs = doc.find_all('product-card')
        for product in divs:
            név = product.find('span', class_='product-card__title')
            if not név:
                break
            név = név.a
            név = név.string
            
            ár = product.find('sale-price')
            ár = ár.find_all('span')
            ár = ár[1]
            ár = ár.string
            ár = ár.replace("Ft", "")
            ár = ár.replace(" ", "")
            ár = int(ár)
            ár = '{:,}'.format(ár)
            ár = ár.replace(",", " ")
            kép = product.find('div', class_="product-card__figure")
            kép = kép.a
            link = kép['href']
            link = f"https://onsize.eu{link}"
            imgk = kép.find_all('img')
            if len(imgk) == 1:
                    pass
            else:
                    kép = imgk[1]
                    kép_2 = imgk[0]
                    kép_2 = kép_2['src']
                    kép = kép['src']
                    fotók.append(kép)
                    linkek.append(link)
                    árak.append(ár)
                    nevek.append(név)
                    fotók_2.append(kép_2)
    cipők = list(zip(nevek, árak, fotók, fotók_2, linkek))
    for cipő_dolgok in cipők:
        rendezes = cipő_dolgok[1].replace(" ", "")
        Shoe.objects.get_or_create(
                            name = cipő_dolgok[0],
                            price = cipő_dolgok[1],
                            image = cipő_dolgok[2],
                            image_2 = cipő_dolgok[3],
                            rendszerezes = rendezes,
                            cég = "OnSize",
                            link = cipő_dolgok[4],
                        )
    
    base_url_3 = "https://www.rdrop.hu/collections/all?page={}"


    for i in range(1, 1):
        

        url = base_url_3.format(i)
        result = requests.get(url).text
        doc = BeautifulSoup(result, "html.parser")
        lis = doc.find_all('li', class_='grid__item')
        if not lis:
            break
        for q in lis:
            név = q.find('h3', class_='card__heading h5')
            név = név.a
            href = név['href']
            href = f"https://www.rdrop.hu/{href}"
            név = név.string
            név = név.lstrip()
            if "(ENFANT)" or "(NOIR)" in név:
                név = név.replace("(ENFANT)", "")
                név = név.replace("(NOIR)", "")
            név = név.title()
            ár = q.find('span', class_="price-item price-item--sale price-item--last")
            ár = ár.string
            ár = ár.split('Ft')
            ár = ár[0]
            ár = ár.replace('.', ' ')
            ár = ár.replace(' ', '')
            ár = int(ár)
            ár = '{:,}'.format(ár)
            ár = ár.replace(",", " ")
            rendezes = ár.replace(" ", "")
            
            kép = q.find('div', class_="media media--transparent media--hover-effect")
            kép = kép.img
            kép = kép['src']
            Shoe.objects.get_or_create(
                            name = név,
                            price = ár,
                            image = kép,
                            rendszerezes = rendezes,
                            cég = "Rdrop",
                            link = href,
                        )

    # service = Service(executable_path="chromedriver.exe")
    # driver = webdriver.Chrome(service=service)
    # link = "https://www.footshop.hu/hu/4600-ferfi-sneakerek/page-{}"
    # for szam in range(0, 0):
    #     if szam != 1:
    #         url = link.format(szam)
    #         driver.get(url)
    #         source = driver.page_source
    #         soup = BeautifulSoup(source, 'html.parser')
    #         try:
    #             cookie = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "cbButton.cbButtonPrimary")))
    #             cookie.click()
    #         except:
    #             pass

    #         nevek = []
    #         árak = []
    #         linkek = []
    #         fotók = []
    #         try: 
    #             cipő_nevek = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Product_name_1Go7D")))
    #         except TimeoutException:
    #             break
    #         for cipő in cipő_nevek:
    #             név = cipő.text
    #             nevek.append(név)
    #         cipő_árak = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[class*='ProductPrice_price_J4pAM']")))
    #         for i in cipő_árak:
    #             ár = i.text
    #             if "\n" in ár:
    #                 ár = ár.split("\n")[0]
    #             else:
    #                 pass
    #             árak.append(ár)
    #         links =  WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"Product_inner_1kysz")))
    #         for q in links:
    #             link_ = q.find_element(By.TAG_NAME, "a")
    #             link_ = link_.get_attribute("href")
    #             linkek.append(link_)
    #         kép_divs = soup.find_all('div', class_='Products_product_1JtLQ')

    #         for div in kép_divs:
    #             img = div.find('meta', itemprop="image")
    #             src = img['content']
    #             fotók.append(src)
    #             print(src)
    #         cipők = list(zip(nevek, árak, linkek, fotók))
    #         for cipő_dolgok in cipők:
    #             ár = cipő_dolgok[1]
    #             ár = str(ár)
    #             ár = ár.replace("Ft", "")
    #             rendezes = ár.replace(" ", "")
    #             rendezes = int(rendezes)
    #             Shoe.objects.get_or_create(
    #                     name = cipő_dolgok[0],
    #                     price = ár,
    #                     image = cipő_dolgok[3],
    #                     rendszerezes = rendezes,
    #                     cég = "footshop",
    #                     link = cipő_dolgok[2],
    #                 )
            
    # driver.quit() 

    # service = Service(executable_path="chromedriver.exe")
    # driver = webdriver.Chrome(service=service)


    # link = "https://sizeer.hu/ferfi/cipo?page={}"



    # for szam in range(1, 1):
        
    #         url = link.format(szam)
    #         driver.get(url)
            
    #         # try:
    #         #     cookie = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
    #         #     cookie.click()
    #         # except:
    #         #     pass
    #         nevek = []
    #         árak = []
    #         fotók = []
    #         linkek = []
    #         start_ido = datetime.datetime.now()  


    #         for i in range(1000000):

    #             WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.PAGE_DOWN)

    #             jelenidő = datetime.datetime.now()
    #             elteltidő = jelenidő - start_ido

    #             if elteltidő.total_seconds() >= 3:  
    #                 break
    #         source = driver.page_source
    #         soup = BeautifulSoup(source, 'html.parser')
    #         try: 
    #             cipő_nevek = WebDriverWait(driver, 100).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "b-itemList_nameLink")))
    #         except TimeoutException:
    #             break
                
            
    #         ár_divs = soup.find_all('div', class_='b-itemList_prices js-offer-price is-omnibus')
            
    #         for z in ár_divs:
    #             p_k = z.find_all('p')
    #             if len(p_k) == 2:
    #                 ár = p_k[1]
    #             else: 
    #                 ár = p_k[0]
    #             ár = ár.string
    #             ár = ár.replace("FT", "")
    #             ár = ár.replace(" ", "")
                # ár = int(ár)
                # ár = '{:,}'.format(ár)
                # ár = ár.replace(",", " ")
    #             árak.append(ár)

    #         for cipő in cipő_nevek:
    #             név = cipő.text
    #             név_link = cipő.get_attribute("href")
    #             linkek.append(név_link)
    #             nevek.append(név)
            
    #         kep_divs = soup.find_all('a', class_='b-itemList_photoLink')
    #         for x in kep_divs:
    #             kép = x.img
    #             kép = kép['src']
    #             kép = f"https://sizeer.hu{kép}"
    #             fotók.append(kép)

    #         cipők = list(zip(nevek, árak, fotók, linkek))
            
    #         for cipő_dolgok in cipők:
    #             rendezes = cipő_dolgok[1]
    #             rendezes = rendezes.replace(" ", "")
    #             Shoe.objects.get_or_create(
    #                         name = cipő_dolgok[0],
    #                         price = cipő_dolgok[1],
    #                         image = cipő_dolgok[2],
    #                         rendszerezes = rendezes,
    #                         cég = "sizeer",
    #                         link = cipő_dolgok[3],
    #                     )


    # driver.quit() 
    # service = Service(executable_path="chromedriver.exe")
    # driver = webdriver.Chrome(service=service)

    # url = "https://www.footlocker.hu/en/category/men/shoes/sneakers.html?currentPage=0"
    # szam = 0
    # driver.get(url)
    # while szam != 23:

    #     nevek = []
    #     árak = []
    #     fotók = []
    #     linkek = []
        
    #     try:
    #         cookie = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-reject-all-handler")))
    #         cookie.click()
    #     except:
    #         pass
    #     try: 
    #         next_gomb = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Next")))
    #     except TimeoutException:
    #         break
    #     source = driver.page_source
    #     soup = BeautifulSoup(source, 'html.parser')
    #     cipő_nevek = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ProductName-primary")))
    #     cipő_árak = soup.find_all('span', "ProductPrice")    
    #     cipő_fotók = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ProductCard-image")))
    #     cipő_linkek = soup.find_all('a', "ProductCard-link ProductCard-content")

    #     for név, lehetseges_ár, fotó, link in zip(cipő_nevek, cipő_árak, cipő_fotók, cipő_linkek):
    #         ár = lehetseges_ár.text
    #         ár = ár.split(",")
    #         ár = ár[0]
    #         ár = ár.replace("Ft", "")
    #         ár = ár.replace(" ", "")
    #         try:
    #             ár = int(ár)
    #             ár = '{:,}'.format(ár)
    #             ár = ár.replace(",", " ")
    #         except:
    #             ár = lehetseges_ár.find('span', "ProductPrice-final")
    #             ár = ár.string
    #             ár = ár.split(",")
    #             ár = ár[0]
    #             ár = ár.replace("Ft", "")
    #             ár = ár.replace(" ", "")
    #             ár = int(ár)
    #             ár = '{:,}'.format(ár)
    #             ár = ár.replace(",", " ")
    #         név = név.text
    #         img_element = fotó.find_element(By.TAG_NAME, "img")
    #         fotó = img_element.get_attribute("src")
    #         link = link['href']
    #         link = f"https://www.footlocker.hu{link}"
    #         nevek.append(név)
    #         árak.append(ár)
    #         fotók.append(fotó)
    #         linkek.append(link)
    
    #     cipők = list(zip(nevek, árak, fotók, linkek))
    #     for cipő_dolgok in cipők:
    #         rendezes = cipő_dolgok[1].replace(" ", "")
    #         Shoe.objects.get_or_create(
    #                         name = cipő_dolgok[0],
    #                         price = cipő_dolgok[1],
    #                         image = cipő_dolgok[2],
    #                         rendszerezes = rendezes,
    #                         cég = "Foot Locker",
    #                         link = cipő_dolgok[3],
    #                     )
    #     if szam != 9:
    #         next_gomb.click()
    #     else:
    #         break
    #     szam = szam + 1

    # driver.quit()
    cipők = {'NIKE DUNK': [], 'AIR JORDAN': [], 'NEW BALANCE 550': [], 'AIR FORCE': [], 'ADIDAS CAMPUS': [], 'ADIDAS YEEZY': []}
    márkák = Márka.objects.all()
    shoes = Shoe.objects.all()
    shoes = shoes.exclude(name__icontains="(TD & PS)")
    shoes = shoes.exclude(name__icontains="(Infants)")
    shoes = list(shoes)
    random.shuffle(shoes)
    if len(shoes) > 50:
        shoes = shoes[:50]
        print("fasz")
    for cipő in shoes:
        cipő_név = cipő.name.lower()
        if 'dunk' in cipő_név:
            cipők['NIKE DUNK'].append(cipő)
        elif 'jordan' in cipő_név:
            cipők['AIR JORDAN'].append(cipő)
        elif '550' in cipő_név:
            cipők['NEW BALANCE 550'].append(cipő)
        elif 'air force' in cipő_név:
            cipők['AIR FORCE'].append(cipő)
        elif 'campus' in cipő_név:
            cipők['ADIDAS CAMPUS'].append(cipő)
        elif 'yeezy' in cipő_név:
            cipők['ADIDAS YEEZY'].append(cipő)
    
    q = request.GET.get('q', '')

    if q == '':
        q = None
        length = '2'
    
    else:
        if "Campus" in q:
            q = q.split(" ")
            q = f"{q[-3]} {q[-2]} {q[-1]}"
            campus = "1"
        else:
            q = q.split(" ")
            q = f"{q[-2]} {q[-1]}"
            campus = "2"
        shoes__ = Shoe.objects.all()
        shoes__ = shoes__.exclude(name__icontains="(TD & PS)")
        shoes__ = shoes__.exclude(name__icontains="(Infants)")
        cipők=[]
        for shoe_ in shoes__:
            try:
                név_filter =  shoe_.name
                név_filter = név_filter.replace("'", "")
                név_filter = név_filter.strip()
                név_filter = név_filter.split(" ")
                if campus == "1":
                    név_filter = f"{név_filter[-3]} {név_filter[-2]} {név_filter[-1]}"
                elif campus == "2":
                    név_filter = f"{név_filter[-2]} {név_filter[-1]}"    
                if q.lower() in név_filter.lower():
                    cipők.append(shoe_)
            except: pass
        random.shuffle(cipők)
        length=len(cipők)
        print(cipők)
    
    
    best_shoes = {'Nike': ["Air Force 1", "Air Max 1", "Dunk High", "Dunk Low"], 'Air Jordan': ["Air Jordan 1 High", "Air Jordan 1 Mid", "Air Jordan 1 Low", "Air Jordan 3", "Air Jordan 4"],
                    'Adidas': ["Adidas Campus", "Adidas Gazelle", "Adidas Samba"], 'Yeezy': ["Yeezy Boost 350", "Yeezy Slide", "Yeezy Foam"]}

    context = {'shoes': cipők,  'szamolas': szamolas, 'márkák': márkák, 'best_shoes': best_shoes, 'q': q, 'length': length}

    return render(request, 'home.html', context)

def room(request, pk):
    
    shoe = Shoe.objects.get(id=pk) 

    context = {'shoe': shoe}

    return render(request, 'room.html', context)

def sneakerek(request): 
        shoes = Shoe.objects.all()
        shoes = shoes.exclude(name__icontains="(TD & PS)")
        shoes = shoes.exclude(name__icontains="(Infants)")
        best_shoes = {'Nike': ["Air Force 1", "Air Max 1", "Dunk High", "Dunk Low"], 'Air Jordan': ["Air Jordan 1 High", "Air Jordan 1 Mid", "Air Jordan 1 Low", "Air Jordan 3", "Air Jordan 4"],
                    'Adidas': ["Adidas Campus", "Adidas Gazelle", "Adidas Samba"], 'Yeezy': ["Yeezy Boost 350", "Yeezy Slide", "Yeezy Foam"]}

        query = request.GET.get('q', '') 
        rendezes = request.GET.get('r', '')
        if query == "NIKE DUNK" :
            query = 'dunk'
        elif query == "AIR FORCE":
            query = 'force'
        elif query == "ADIDAS CAMPUS":
            query = 'campus'
        elif query == 'ADIDAS YEEZY':
            query = 'yeezy'
        elif query == 'NEW BALANCE 550':
            query = '550'
        elif query == 'AIR JORDAN':
            query = 'jordan'
        
            
        shoes = shoes.filter(name__icontains=query) | shoes.filter(cég__icontains=query)
        if rendezes == "legalacsonyabb":
            shoes = shoes.order_by('rendszerezes')
        elif rendezes == "legmagasabb":
            shoes = shoes.order_by('-rendszerezes')
        else:
            shoes = list(shoes)
            random.shuffle(shoes)
        shoes = list(shoes)
        márkák = Márka.objects.all()

        context = {'shoes': shoes, 'márkák':márkák, 'best_shoes':best_shoes}

        return render(request, 'sneakerek.html', context)

