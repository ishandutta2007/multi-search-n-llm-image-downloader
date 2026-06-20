import unittest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
import urllib.error
from multi_downloader.bing import Bing

class TestBing(unittest.TestCase):
    def setUp(self):
        self.query = "test"
        self.limit = 2
        self.output_dir = Path("test_output")
        self.adult = "off"
        self.timeout = 10
        self.bing = Bing(self.query, self.limit, self.output_dir, self.adult, self.timeout)

    def test_get_filter(self):
        self.assertEqual(self.bing.get_filter("line"), "+filterui:photo-linedrawing")
        self.assertEqual(self.bing.get_filter("photo"), "+filterui:photo-photo")
        self.assertEqual(self.bing.get_filter("invalid"), "")

    @patch('multi_downloader.bing.urllib.request.urlopen')
    @patch('multi_downloader.bing.filetype.guess')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_image_success(self, mock_file, mock_guess, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b"fake_data"
        mock_urlopen.return_value = mock_response
        
        mock_kind = MagicMock()
        mock_kind.mime = "image/jpeg"
        mock_guess.return_value = mock_kind
        
        self.bing.save_image("http://example.com/img.jpg", "path/to/save")
        
        mock_urlopen.assert_called_once()
        mock_file.assert_called_with("path/to/save", "wb")

    @patch('multi_downloader.bing.urllib.request.urlopen')
    def test_save_image_http_error(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError("url", 404, "Not Found", {}, None)
        
        with patch('logging.error') as mock_log:
            self.bing.save_image("http://example.com/img.jpg", "path/to/save")
            mock_log.assert_called()

    @patch('multi_downloader.bing.Bing.save_image')
    def test_download_image(self, mock_save):
        self.bing.download_image("http://example.com/img.jpg")
        self.assertEqual(self.bing.download_count, 1)
        mock_save.assert_called_once()

    @patch('multi_downloader.bing.urllib.request.urlopen')
    @patch('multi_downloader.bing.Bing.download_image')
    def test_run(self, mock_download, mock_urlopen):
        # Mock HTML response from Bing containing one image URL
        mock_response = MagicMock()
        mock_response.read.return_value = b'murl&quot;:&quot;http://example.com/img1.jpg&quot;'
        mock_urlopen.return_value = mock_response
        
        # We only want to run one loop for testing
        # We can control this by setting limit and download_count
        self.bing.limit = 1
        
        def mock_download_func(*args, **kwargs):
            self.bing.download_count += 1
            
        mock_download.side_effect = mock_download_func
        
        self.bing.run()
        
        mock_download.assert_called_with("http://example.com/img1.jpg")

if __name__ == '__main__':
    unittest.main()
