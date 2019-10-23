import unittest
from gitphplint.src import string_processing

class StringProcessingTest(unittest.TestCase):

    def test_line_numbers(self): 
        code = r"""<?php
               
       namespace App\Controller\UserController;

       use App\Entity\User

       class UserController extends Controller
       {
       }
        """
        
        data = tuple(string_processing.add_line_numbers(code)) 
        
        self.assertEqual(repr(''.join(data)), r"'\x1b[1;30;40m0\x1b[0;37;40m <?php\x1b[1;30;40m1\x1b[0;37;40m                \x1b[1;30;40m2\x1b[0;37;40m        namespace App\\Controller\\UserController;\x1b[1;30;40m3\x1b[0;37;40m \x1b[1;30;40m4\x1b[0;37;40m        use App\\Entity\\User\x1b[1;30;40m5\x1b[0;37;40m \x1b[1;30;40m6\x1b[0;37;40m        class UserController extends Controller\x1b[1;30;40m7\x1b[0;37;40m        {\x1b[1;30;40m8\x1b[0;37;40m        }\x1b[1;30;40m9\x1b[0;37;40m         '")
      
    
    def test_remove_lines(self):
        code = r"""
            Test
            
            Another test
            @@test
        
        """
        
        data = string_processing.remove_lines_from_string(code, 2)
        
        self.assertEqual(repr(data), "'            \\n            Another test\\n        \\n        '")
        self.assertEqual(data.strip(), 'Another test')
        
if __name__ == '__main__':
    unittest.main()
