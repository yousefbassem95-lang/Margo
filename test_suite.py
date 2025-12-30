import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import io
import margo
import sqli_scanner
import traffic_edu
import access_auditor
import crypto_utils
from colorama import Fore, Style

class TestMargoModules(unittest.TestCase):

    @patch('builtins.print')
    def test_access_auditor(self, mock_print):
        # Test Calculate Entropy
        entropy = access_auditor.calculate_entropy("Password123!")
        self.assertTrue(entropy > 0)
        
        # Test Crack Time
        time_str = access_auditor.estimate_crack_time(50)
        self.assertIsInstance(time_str, str)
        
        # Test Audit Interaction
        with patch('builtins.input', return_value="StrongPassword123!"):
            access_auditor.audit_password()
            # Verify it printed something about "STATUS"
            # We just check if print was called
            self.assertTrue(mock_print.called)

    @patch('builtins.print')
    @patch('requests.get')
    def test_sqli_scanner(self, mock_get, mock_print):
        # Mock a safe response
        safe_response = MagicMock()
        safe_response.text = "<html>Safe Content</html>"
        safe_response.status_code = 200
        
        # Mock a vulnerable response
        vuln_response = MagicMock()
        vuln_response.text = "Warning: mysql_fetch_array() expects parameter"
        
        mock_get.side_effect = [safe_response, safe_response, vuln_response]
        
        sqli_scanner.check_sqli_vulnerability("http://test.com")
        self.assertTrue(mock_print.called)

    @patch('builtins.print')
    def test_traffic_edu(self, mock_print):
        # Just run it, it's a print-only module
        traffic_edu.explain_traffic_stress()
        self.assertTrue(mock_print.called)

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['1', 'test_phrase']) 
    def test_crypto_utils_text(self, mock_input, mock_print):
        # Test Text Hashing
        crypto_utils.generate_hash()
        self.assertTrue(mock_print.called)

    @patch('builtins.print')
    @patch('subprocess.run')
    @patch('builtins.input', side_effect=['127.0.0.1', '1', '100'])
    def test_margo_port_scan(self, mock_input, mock_subprocess, mock_print):
        # Test Port Scan triggering subprocess
        # Mock check_cpp_scanner to return True so we don't try to compile
        with patch('margo.check_cpp_scanner', return_value=True):
            margo.run_port_scan()
            mock_subprocess.assert_called_with(["./scanner", "127.0.0.1", "1", "100"])

if __name__ == '__main__':
    unittest.main()
