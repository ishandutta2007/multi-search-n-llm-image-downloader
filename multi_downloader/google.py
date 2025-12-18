from bs4 import BeautifulSoup

import urllib.request
import urllib
import posixpath
import re
import logging
from tqdm import tqdm
import filetype
import pprint as pp
import traceback
from colorama import Fore
from colorama import init as colorama_init
from colorama import Style

colorama_init()

ignore_domains = (
    "www.google.com",
    "support.google.com",
    "www.youtube.com",
    "https://en.wikipedia.org/wiki/Special:CentralAutoLogin/setCookies",
    "https://en.wikipedia.org/wiki/Special:CentralAutoLogin/start",
)
ignore_exts = (".cms", ".svg", ".gif")

"""

Python api to download image form Google.
Origina Author: Guru Prasad (g.gaurav541@gmail.com)
Improved Author: Krishnatejaswi S (shentharkrishnatejaswi@gmail.com) 

"""


class Google:
    """_summary_
    A class to download images from Google.

    _description_
    This class is used to download images from Google. It uses the Google Image Search API to get the links of the images and then downloads the images from the links. The class can be used to download images based on a query, with a limit on the number of images to be downloaded. The images can be filtered based on the type of image (photo, clipart, line drawing, animated gif, transparent) and the adult content can be filtered as well. The images are saved in the specified output directory. The class also has the option to be verbose, which will print the progress of the download.

    _parameters_

    query : str
        The query to be used to search for images.
    limit : int
        The number of images to be downloaded.
    output_dir : str
        The directory where the images are to be saved.
    adult : str
        The adult content filter. Can be "off" or "on".
    timeout : int
        The time in seconds to wait for the request to Google to be completed.
    filter : str
        The type of image to be filtered. Can be "line", "photo", "clipart", "gif", "transparent".
    verbose : bool
        Whether to print the progress of the download.

    _methods_

    get_filter(shorthand)
        Returns the filter string based on the shorthand.
        ============
        shorthand : str
            The shorthand for the filter. Can be "line", "photo", "clipart", "gif", "transparent".
        ============
        return : str
            The filter string based on the shorthand.

    save_image(link, file_path)
        Saves the image from the link to the file path.
        ============
        link : str
            The link of the image to be saved.
        file_path : str
            The file path where the image is to be saved.
        ============
        return : None

    download_image(link)
        Downloads the image from the link.
        ============
        link : str
            The link of the image to be downloaded.
        ============
        return : None
    run()
        Runs the download of the images.
        ============
        return : None

    """

    def __init__(
        self,
        query,
        limit,
        output_dir,
        adult,
        timeout,
        filter="",
        verbose=True,
        badsites=[],
        name="Image",
    ):
        self.download_count = 0
        self.query = query
        self.output_dir = output_dir
        self.adult = adult
        self.filter = filter
        self.verbose = verbose
        self.seen = set()
        self.urls = []
        self.badsites = badsites
        self.image_name = name
        self.download_callback = None

        if self.badsites:
            logging.info(
                "Download links will not include: %s", ", ".join(self.badsites)
            )

        assert type(limit) == int, "limit must be integer"
        self.limit = limit
        assert type(timeout) == int, "timeout must be integer"
        self.timeout = timeout

        self.page_counter = 0
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.11 (KHTML, like Gecko) "
            "Chrome/23.0.1271.64 Safari/537.11",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
            "Accept-Encoding": "none",
            "Accept-Language": "en-US,en;q=0.8",
            "Connection": "keep-alive",
        }

    def get_filter(self, shorthand):
        if shorthand == "line" or shorthand == "linedrawing":
            return "+filterui:photo-linedrawing"
        elif shorthand == "photo":
            return "+filterui:photo-photo"
        elif shorthand == "clipart":
            return "+filterui:photo-clipart"
        elif shorthand == "gif" or shorthand == "animatedgif":
            return "+filterui:photo-animatedgif"
        elif shorthand == "transparent":
            return "+filterui:photo-transparent"
        else:
            return ""

    def _find_largest_image_on_page(self, page_url):
        try:
            request = urllib.request.Request(page_url, None, self.headers)
            response = urllib.request.urlopen(request, timeout=self.timeout)
            html = response.read().decode("utf8")
            soup = BeautifulSoup(html, "html.parser")

            largest_image_url = None
            largest_area = 0

            for img_tag in soup.find_all("img"):
                img_src = img_tag.get("src")
                if (
                    not img_src
                    or not img_src.startswith("http")
                    or img_src.startswith("data:")
                ):
                    continue

                width = img_tag.get("width")
                height = img_tag.get("height")

                try:
                    width = int(width) if width else 0
                    height = int(height) if height else 0
                except ValueError:
                    width = 0
                    height = 0

                current_area = width * height

                if current_area > largest_area:
                    largest_area = current_area
                    largest_image_url = img_src
                elif (
                    largest_image_url is None
                    and current_area == 0
                    and "large" in img_src.lower()
                ):
                    largest_image_url = img_src
                elif (
                    largest_image_url is None
                    and current_area == 0
                    and "original" in img_src.lower()
                ):
                    largest_image_url = img_src
                elif (
                    largest_image_url is None
                    and current_area == 0
                    and "full" in img_src.lower()
                ):
                    largest_image_url = img_src

            return largest_image_url

        except urllib.error.HTTPError as e:
            print(f"{Fore.RED} HTTPError while fetching page {page_url} : {e}{Style.RESET_ALL}")
            traceback.print_stack()
            return None
        except urllib.error.URLError as e:
            print(f"{Fore.RED} URLError while fetching page {page_url} : {e}{Style.RESET_ALL}")
            traceback.print_stack()
            return None
        except Exception as e:
            print(f"{Fore.RED} Error finding largest image on page {page_url} : {e}{Style.RESET_ALL}")
            traceback.print_stack()
            return None

    def save_image(self, link, file_path) -> None:
        try:
            request = urllib.request.Request(link, None, self.headers)
            image = urllib.request.urlopen(request, timeout=self.timeout).read()
            kind = filetype.guess(image)
            if kind is None or not kind.mime.startswith("image/"):
                print(f"Invalid image, not saving {link}")
                raise ValueError(f"{Fore.RED} Invalid image, not saving {link}{Style.RESET_ALL}")
            with open(str(file_path), "wb") as f:
                f.write(image)

        except urllib.error.HTTPError as e:
            self.sources -= 1
            print(f"{Fore.RED} HTTPError while saving image {link}: {e}{Style.RESET_ALL}")
            traceback.print_stack()

        except urllib.error.URLError as e:
            self.sources -= 1
            print(f"{Fore.RED} URLError while saving image {link}: {e}{Style.RESET_ALL}")
            traceback.print_stack()

    def download_image(self, link):
        self.download_count += 1
        # Get the image link
        try:
            path = urllib.parse.urlsplit(link).path
            filename = posixpath.basename(path).split("?")[0]
            file_type = filename.split(".")[-1]
            if file_type.lower() not in [
                "jpe",
                "jpeg",
                "jfif",
                "exif",
                "tiff",
                "gif",
                "bmp",
                "png",
                "webp",
                "jpg",
            ]:
                file_type = "jpg"

            if self.verbose:
                print(
                    "[%] Downloading Image #{} from {}".format(
                        self.download_count, link
                    )
                )

            self.save_image(
                link,
                self.output_dir.joinpath(
                    f"{self.image_name}_{self.download_count}.{file_type}"
                ),
            )
            if self.verbose:
                print("[%] File Downloaded !\n")

            # Update progress bar
            if self.download_callback:
                self.download_callback(self.download_count)

        except Exception as e:
            self.download_count -= 1
            print(f"{Fore.RED} Issue getting: {link}\nError: {e}{Style.RESET_ALL}")
            traceback.print_stack()

    def run(self):
        while self.download_count < self.limit:
            if self.verbose:
                logging.info("\n\n[!]Indexing page: %d\n", self.page_counter + 1)
            # Parse the page source and download pics
            try:
                # &sca_esv=75f9aadc3d86adc0
                # &sxsrf=AE3TifN9cKTMY7aIPOftxQcy3Fu68bjg5w:1759831749189&source=hp
                # &ei=xebkaN7LCMSWseMP9K-i2A4
                # &iflsig=AOw8s4IAAAAAaOT01UQuD-658A5Rqe6Jcxe5Li_aTWe_
                # &ved=0ahUKEwiewpaS7JGQAxVES2wGHfSXCOsQ4dUDCBc
                # &uact=5
                # &oq=cofinex+logo
                # &gs_lp=EgNpbWciDGNvZmluZXggbG9nbzIHECMYJxjJAkjuT1AAWIpAcAF4AJABAJgBwwGgAcMBqgEDMC4xuAEDyAEA-AEC-AEBigILZ3dzLXdpei1pbWeYAgKgAtUBqAIKwgIKECMYJxjJAhjqApgDD5IHAzEuMaAH7AGyBwMwLjG4B8UBwgcHMC4xLjAuMcgHDQ

                request_url = (
                    "https://www.google.com/search?q="
                    + urllib.parse.quote_plus(self.query)
                    + "&hl=en"
                    + "&sclient=img"
                    + "&udm=2"
                    # + '&fbs=AIIjpHxU7SXXniUZfeShr2fp4giZ1Y6MJ25_tmWITc7uy4KIeqDdErwP5rACeJAty2zADJgYJpo1blvMpITBRgbnARM6y8KwxzRsF24u6g33NutBQod-bHaq-BaxULyF1bB2Uqyl-vUCNqEkT_YgKWrg4nlgIgtJDN8PYh5ozrABlRQ5aXJDZxAIbMOAM9soz4Ir11tZ76Bv-Q6kZAI729A6TsfHvehHyw'
                    + "&tbs=isz:l"
                    + "&sa=X"
                    + "&biw=1990"
                    + "&bih=980"
                    + "&dpr=0.8"
                    # + '&first=' + str(self.page_counter)
                    # + '&count=' + str(self.limit)
                    # + '&adlt=' + self.adult
                    # + '&qft=' + ('' if self.filter is None else self.get_filter(self.filter))
                )
                request = urllib.request.Request(
                    request_url, None, headers=self.headers
                )
                response = urllib.request.urlopen(request)
                html = response.read().decode("utf8")
                if html == "":
                    logging.info("[%] No more images are available")
                    break
                soup = BeautifulSoup(html, "html.parser")
                referrer_urls = []
                anchors = soup.find_all("a")
                # pp.pprint(anchors)
                for aidx, anc in enumerate(anchors):
                    try:
                        urls = re.findall(r"(https?://\S+)", anc["href"])
                        if len(urls) == 0:
                            continue
                        referrer_url = urls[0].split("&")[
                            0
                        ]  # anc['href']#anc.get('href')
                        if referrer_url is None:
                            continue
                        referrer_url = referrer_url.strip()
                        if any(d in referrer_url for d in ignore_domains):
                            continue
                        if any(referrer_url.endswith(e) for e in ignore_exts):
                            continue
                        if referrer_url in referrer_urls:
                            continue
                        print(f"[{self.query}][{aidx + 1}] ===>>> {referrer_url}")
                        referrer_urls.append(referrer_url)
                    except Exception as e:
                        print(f"{Fore.RED} Error iterating anchors: {e}{Style.RESET_ALL}")
                        traceback.print_stack()
                links = referrer_urls
                max_image_possible = len(links)
                print(
                    f"[{self.query}]No of websites to be scraped = {max_image_possible}"
                )
                if self.verbose:
                    logging.info(
                        "[%%] Indexed %d Referrer URLs on Page %d.",
                        len(referrer_urls),
                        self.page_counter + 1,
                    )
                    logging.info("\n===============================================\n")
                for ridx, referrer_url in enumerate(referrer_urls):
                    try:
                        isbadsite = False
                        for badsite in self.badsites:
                            isbadsite = badsite in referrer_url
                            if isbadsite:
                                if self.verbose:
                                    logging.info(
                                        "[!] Link included in badsites %s %s",
                                        badsite,
                                        referrer_url,
                                    )
                                    break
                        if isbadsite:
                            continue

                        if self.download_count < self.limit:
                            image_url = self._find_largest_image_on_page(referrer_url)
                            if image_url is None:
                                max_image_possible -= 1
                                continue
                            if any(d in image_url for d in ignore_domains):
                                max_image_possible -= 1
                                continue
                            if image_url and any(
                                image_url.endswith(e) for e in ignore_exts
                            ):
                                max_image_possible -= 1
                                continue
                            print(f"{Fore.BLUE} {image_url} {Style.RESET_ALL}")
                            if image_url and image_url not in self.seen:
                                self.seen.add(image_url)
                                self.download_image(image_url)
                                print(
                                    f"\n[{self.query}][{ridx + 1}/{len(referrer_urls)}]Images {self.download_count}(downloaded) of {max_image_possible}(max possible), sent limit={self.limit} :{image_url}"
                                )
                            elif not image_url:
                                logging.info(
                                    "No suitable image found on page: %s", referrer_url
                                )
                                print(
                                    f"\n[{self.query}][{ridx + 1}/{len(referrer_urls)}]Images {self.download_count}(downloaded) of {max_image_possible}(max possible), sent limit={self.limit}"
                                )
                    except Exception as e:
                        print(f"{Fore.RED} Error iterating largest image {e} {Style.RESET_ALL}")
                        traceback.print_stack()

                self.page_counter += 1
            except urllib.error.HTTPError as e:
                print(f"{Fore.RED} HTTPError while making request to Google: {e}{Style.RESET_ALL}")
                traceback.print_stack()
                if "429" in str(e):
                    raise e
            except urllib.error.URLError as e:
                print(f"{Fore.RED} URLError while making request to Google: {e}{Style.RESET_ALL}")

        logging.info("\n\n[%%] Done. Downloaded %d images.", self.download_count)
