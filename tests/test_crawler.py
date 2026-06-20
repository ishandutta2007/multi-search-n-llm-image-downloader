import unittest
from unittest.mock import patch, MagicMock
from multi_downloader.crawler import google_gen_query_url, bing_gen_query_url, crawl_image_urls

class TestCrawler(unittest.TestCase):
    def test_google_gen_query_url(self):
        url = google_gen_query_url("cats", face_only=True, safe_mode=True, image_type="photo", color="red")
        self.assertIn("q=cats", url)
        self.assertIn("safe=on", url)
        self.assertIn("itp:photo", url)
        self.assertIn("itp:face", url)
        self.assertIn("isc:red", url)

    def test_bing_gen_query_url(self):
        url = bing_gen_query_url("dogs", face_only=True, image_type="clipart", color="blue")
        self.assertIn("q=dogs", url)
        self.assertIn("filterui:face-face", url)
        self.assertIn("filterui:photo-clipart", url)
        self.assertIn("filterui:color2-FGcls_BLUE", url)

    @patch('multi_downloader.crawler.webdriver.Chrome')
    @patch('multi_downloader.crawler.shutil.which')
    def test_crawl_image_urls_google(self, mock_which, mock_chrome):
        mock_which.return_value = "/path/to/chromedriver"
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        # Mock finding image elements
        mock_elem = MagicMock()
        mock_elem.get_attribute.return_value = '<div class="islib"><a href="imgurl=http://example.com/img.jpg&amp;imgrefurl=..."></a></div>'
        mock_driver.find_elements.side_effect = [
            [mock_elem] * 5, # thumb_elements (google_image_url_from_webpage)
            [mock_elem] * 5  # image_elements (google_image_url_from_webpage)
        ]
        
        urls = crawl_image_urls("test", engine="Google", max_number=2, browser="chrome_headless")
        
        self.assertEqual(len(urls), 2)
        self.assertEqual(urls[0], "http://example.com/img.jpg")

    @patch('multi_downloader.crawler.requests.get')
    def test_crawl_image_urls_bing_api(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = 'murl&quot;:&quot;http://example.com/api_img.jpg&quot;'
        mock_get.return_value = mock_response
        
        urls = crawl_image_urls("test", engine="Bing", max_number=1, browser="api")
        
        self.assertEqual(len(urls), 1)
        self.assertEqual(urls[0], "http://example.com/api_img.jpg")

if __name__ == '__main__':
    unittest.main()
