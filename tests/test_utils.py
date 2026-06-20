import unittest
from multi_downloader.utils import gen_valid_dir_name_for_keywords, gen_keywords_list_from_str, AppConfig

class TestUtils(unittest.TestCase):
    def test_gen_valid_dir_name_for_keywords(self):
        self.assertEqual(gen_valid_dir_name_for_keywords("hello world"), "hello_world")
        self.assertEqual(gen_valid_dir_name_for_keywords("hello:world"), "hello-world")
        self.assertEqual(gen_valid_dir_name_for_keywords("hello/world"), "helloworld")
        self.assertEqual(gen_valid_dir_name_for_keywords("query with - _ ."), "query_with_-___.")
    
    def test_gen_keywords_list_from_str(self):
        self.assertEqual(gen_keywords_list_from_str("a,b,c"), ["a", "b", "c"])
        self.assertEqual(gen_keywords_list_from_str("a;b;c", sep=";"), ["a", "b", "c"])
        self.assertEqual(gen_keywords_list_from_str("single"), ["single"])

    def test_app_config_initialization(self):
        config = AppConfig()
        self.assertEqual(config.engine, "Google")
        self.assertEqual(config.driver, "chrome_headless")
        self.assertEqual(config.num_threads, 50)

    def test_app_config_to_command_paras(self):
        config = AppConfig()
        config.keywords = "test query"
        config.engine = "Bing"
        config.max_number = 10
        config.num_threads = 5
        config.output_dir = "./test_output"
        
        paras = config.to_command_paras()
        
        self.assertIn("-e Bing", paras)
        self.assertIn("-n 10", paras)
        self.assertIn("-j 5", paras)
        self.assertIn('"test query"', paras)
        # Check generated directory name in output path
        self.assertIn('./test_output/test_query"', paras)

    def test_app_config_to_command_paras_flags(self):
        config = AppConfig()
        config.keywords = "test"
        config.face_only = True
        config.safe_mode = True
        
        paras = config.to_command_paras()
        self.assertIn("-F", paras)
        self.assertIn("-S", paras)

    def test_app_config_to_command_paras_proxy(self):
        config = AppConfig()
        config.keywords = "test"
        
        config.proxy_type = "http"
        config.proxy = "127.0.0.1:8080"
        paras = config.to_command_paras()
        self.assertIn('-ph "127.0.0.1:8080"', paras)
        
        config.proxy_type = "socks5"
        config.proxy = "127.0.0.1:1080"
        paras = config.to_command_paras()
        self.assertIn('-ps "127.0.0.1:1080"', paras)

if __name__ == '__main__':
    unittest.main()
