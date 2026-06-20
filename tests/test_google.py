import unittest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
import urllib.error
from multi_downloader.google import Google

class TestGoogle(unittest.TestCase):
    def setUp(self):
        self.query = "test"
        self.limit = 1
        self.output_dir = Path("test_output")
        self.adult = "off"
        self.timeout = 10
        self.google = Google(self.query, self.limit, self.output_dir, self.adult, self.timeout)

    def test_get_filter(self):
        self.assertEqual(self.google.get_filter("line"), "+filterui:photo-linedrawing")
        self.assertEqual(self.google.get_filter("photo"), "+filterui:photo-photo")
        self.assertEqual(self.google.get_filter("invalid"), "")

    @patch('multi_downloader.google.urllib.request.urlopen')
    @patch('multi_downloader.google.filetype.guess')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_image_success(self, mock_file, mock_guess, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b"fake_data"
        mock_urlopen.return_value = mock_response
        
        mock_kind = MagicMock()
        mock_kind.mime = "image/jpeg"
        mock_guess.return_value = mock_kind
        
        self.google.save_image("http://example.com/img.jpg", "path/to/save")
        
        mock_urlopen.assert_called_once()
        mock_file.assert_called_with("path/to/save", "wb")

    @patch('multi_downloader.google.urllib.request.urlopen')
    def test_find_all_images_on_page(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b'<html><body><img src="http://example.com/1.jpg"><img src="/2.jpg"></body></html>'
        mock_urlopen.return_value = mock_response
        
        import multi_downloader
        print("MODULE LOADED FROM:", multi_downloader.__file__)
        images = self.google._find_all_images_on_page("http://example.com")
        print("MOCK RETURNED IMAGES:", images)
        self.assertIn("http://example.com/1.jpg", images)
        self.assertIn("http://example.com/2.jpg", images)

    @patch('multi_downloader.google.Google.save_image')
    def test_download_image(self, mock_save):
        self.google.download_image("http://example.com/img.jpg", "goog")
        self.assertEqual(self.google.download_count, 1)
        mock_save.assert_called_once()

    @patch('multi_downloader.google.urllib.request.urlopen')
    @patch('multi_downloader.google.Google.download_image')
    def test_run(self, mock_download, mock_urlopen):
        # Mock Google search result page
        mock_response = MagicMock()
        mock_response.read.return_value = b'<html><body><img src="http://example.com/thumb.jpg"><a href="http://example.com/page1"></a></body></html>'
        mock_urlopen.return_value = mock_response
        
        def mock_download_func(*args, **kwargs):
            self.google.download_count += 1
            
        mock_download.side_effect = mock_download_func
        
        # Mock _find_all_images_on_page to return a list
        with patch.object(Google, '_find_all_images_on_page', return_value=["http://example.com/full.jpg"]):
            self.google.run()
        
        # It should call download_image for thumb and full
        self.assertTrue(mock_download.called)

if __name__ == '__main__':
    unittest.main()
