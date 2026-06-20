import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import shutil
from multi_downloader.helperdownload import download_image, download_images

class TestHelperDownload(unittest.TestCase):
    @patch('multi_downloader.helperdownload.requests.get')
    @patch('multi_downloader.helperdownload.filetype.guess')
    @patch('multi_downloader.helperdownload.shutil.move')
    @patch('multi_downloader.helperdownload.os.remove')
    @patch('builtins.open', new_callable=mock_open)
    def test_download_image_success(self, mock_file, mock_remove, mock_move, mock_guess, mock_get):
        # Setup mocks
        mock_response = MagicMock()
        mock_response.content = b"fake_image_data"
        mock_get.return_value = mock_response
        
        mock_kind = MagicMock()
        mock_kind.extension = "jpg"
        mock_guess.return_value = mock_kind
        
        # Call function
        download_image("http://example.com/img.jpg", "dst", "img_0001")
        
        # Assertions
        mock_get.assert_called_once()
        mock_file.assert_called_with(os.path.join("dst", "img_0001"), "wb")
        mock_file().write.assert_called_once_with(b"fake_image_data")
        mock_guess.assert_called_once()
        mock_move.assert_called_once()
        mock_remove.assert_not_called()

    @patch('multi_downloader.helperdownload.requests.get')
    @patch('multi_downloader.helperdownload.filetype.guess')
    @patch('multi_downloader.helperdownload.os.remove')
    @patch('builtins.open', new_callable=mock_open)
    def test_download_image_invalid_type(self, mock_file, mock_remove, mock_guess, mock_get):
        # Setup mocks
        mock_response = MagicMock()
        mock_response.content = b"not_an_image"
        mock_get.return_value = mock_response
        
        mock_guess.return_value = None # Invalid image
        
        # Call function
        download_image("http://example.com/not_img.txt", "dst", "img_0001")
        
        # Assertions
        mock_remove.assert_called_once()

    @patch('multi_downloader.helperdownload.requests.get')
    def test_download_image_failure(self, mock_get):
        # Setup mock to raise exception
        mock_get.side_effect = Exception("Connection error")
        
        # Call function (it should retry 3 times and then break)
        with patch('builtins.print') as mock_print:
            download_image("http://example.com/fail.jpg", "dst", "img_0001")
            
        self.assertEqual(mock_get.call_count, 3)

    @patch('multi_downloader.helperdownload.concurrent.futures.wait')
    @patch('multi_downloader.helperdownload.concurrent.futures.ThreadPoolExecutor')
    @patch('multi_downloader.helperdownload.os.path.exists')
    @patch('multi_downloader.helperdownload.os.makedirs')
    def test_download_images_concurrency(self, mock_makedirs, mock_exists, mock_executor, mock_wait):
        mock_exists.return_value = False
        
        image_urls = ["url1", "url2", "url3"]
        download_images(image_urls, "dst")
        
        mock_makedirs.assert_called_once_with("dst")
        mock_executor.assert_called_once()

if __name__ == '__main__':
    unittest.main()
