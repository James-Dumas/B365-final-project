import requests, re, json, os, time
from bs4 import BeautifulSoup

SEARCH_URL = "https://www.ebay.com/sch/i.html?_fsrp=1&LH_Auction=1&rt=nc&_from=R40&_nkw=smartphone&_sacat=0&LH_ItemCondition=1000%7C1500%7C2030%7C2020&LH_Sold=1&_ipg=200"
BIDS_URL = "https://www.ebay.com/bfl/viewbids/"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "max-age=0",
    "DNT": "1",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

COOKIES_FILE = "ebay.com_cookies.txt"

def parseCookieFile(cookiefile):
    """Parse a cookies.txt file and return a dictionary of key value pairs compatible with requests."""

    cookies = {}
    with open(cookiefile, "r") as f:
        for line in f:
            line = line.strip()
            if line and not re.match(r"^\#", line):
                fields = line.split("\t")
                cookies[fields[5]] = fields[6]

    return cookies

pattern_nonnumeric = re.compile(r"[^\d\.]")

session = requests.Session()

print("Retrieving list of closed auctions...")
req = session.get(SEARCH_URL, headers=HEADERS, cookies=parseCookieFile(COOKIES_FILE), timeout=30)
print("Parsing HTML...")
soup = BeautifulSoup(req.content, "html.parser")
item_list = soup.find("ul", {"class": "srp-results srp-list clearfix"})
print("Retrieving bid information...")
data = []
for item in item_list.find_all("li", {"class": "s-item"}):
    # generate the url to the bid history page from item id
    listing_url = item.find("a", {"class": "s-item__link"})["href"]
    listing_id = listing_url.split("?")[0].split("/")[-1]
    listing_bids_url = BIDS_URL + listing_id
    print(listing_bids_url)
    req = session.get(listing_bids_url, headers=HEADERS, timeout=10)
    # write to temp html file for debugging
    with open("temp.html", "wb") as f:
        f.write(req.text.encode("utf-8", errors="ignore"))

    soup = BeautifulSoup(req.content, "html.parser")

    bid_data = {}
    info_box_items = soup.find_all("li", {"class": "ui-inline-map-upgrade-wrapper ui-inline-map-padding"})

    # get the number of bidders
    for item in info_box_items[1].div.span.span.contents:
        success = False
        try:
            bid_data["bidders"] = int(item)
            success = True
        except ValueError:
            pass
        
        if success:
            break

    # get the auction duration
    for item in info_box_items[4].div.span.span.contents:
        if "day" in item:
            bid_data["duration"] = int(item.split()[0])
            break

    bid_data["start_price"] = None
    bid_data["start_time"] = None

    # go through the table of all bids
    bid_data["bids"] = []
    bids_table = soup.find("table", {"class": "app-bid-history__table"}).find("tbody")
    if bids_table.find("img", {"alt": "Buy It Now"}):
        # skip this listing if it ended with a buy it now
        continue

    for tr in bids_table.find_all("tr"):
        bid = {}
        td = tr.td
        bidder = td.span.span.string
        td = td.find_next_sibling("td")
        bid["price"] = float(re.sub(pattern_nonnumeric, "", td.span.span.string))
        td = td.find_next_sibling("td")
        bid["time"] = td.span.span.string
        if bidder == "Starting price":
            # set starting price and time instead of adding a bid entry
            bid_data["start_price"] = bid["price"]
            bid_data["start_time"] = bid["time"]
        else:
            bid_data["bids"].insert(0, bid)
    
    data.append(bid_data)
    time.sleep(1)

os.remove("temp.html")

# write the data to a json file
if not os.path.exists("data/scraped"):
    os.makedirs("data/scraped")

data_file = f"data/scraped/out_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"
print(f"Writing data to {data_file}")
with open(data_file, "w") as f:
    json.dump(data, f)

print("Done!")
