import sys
import unittest

from github.issues import main

class ListCommandTests(unittest.TestCase):

    def setUp(self):
        self.repo = 'jsmits/github-cli-public-test'
        self.prog = 'ghi'
        
    def test_0(self):
        sys.argv = [self.prog, 'list', '-r', self.repo]
        output = main()
        self.assertEqual(None, output)
        
    def test_1(self):
        sys.argv = [self.prog, 'list', '-r', self.repo, '-v']
        output = main()
        self.assertEqual(None, output)
        
    def test_2(self):
        sys.argv = [self.prog, '-r', self.repo]
        output = main()
        self.assertEqual(None, output)
        
    def test_3(self):
        sys.argv = [self.prog, '-r', self.repo]
        output = main()
        self.assertEqual(None, output)
        
    def test_4(self):
        sys.argv = [self.prog, '-r', self.repo, '-v']
        output = main()
        self.assertEqual(None, output)
        
    def test_5(self):
        sys.argv = [self.prog, '-r', self.repo, '-w']
        self.assertRaises(SystemExit, main)

    def test_wrong_cmd_0(self):
        sys.argv = [self.prog, 'lis', '-r', 'repo']
        output = main()
        self.assertEqual("error: command 'lis' not implemented", output)
        
    def test_wrong_cmd_1(self):
        sys.argv = [self.prog, 'l', '-r', 'repo']
        output = main()
        self.assertEqual("error: command 'l' not implemented", output)

    def test_6(self):
        sys.argv = [self.prog, 'list', '-r', self.repo, '-s', 'open']
        output = main()
        self.assertEqual(None, output)
        
    def test_7(self):
        sys.argv = [self.prog, 'list', '-r', self.repo, '-s', 'o']
        output = main()
        self.assertEqual(None, output)
        
    def test_8(self):
        sys.argv = [self.prog, 'list', '-r', self.repo, '-s', 'closed']
        output = main()
        self.assertEqual(None, output)
        
    def test_9(self):
        sys.argv = [self.prog, 'list', '-r', self.repo, '-s', 'c']
        output = main()
        self.assertEqual(None, output)
        
    def test_10(self):
        sys.argv = [self.prog, 'list', '-r', self.repo, '-s', 'all']
        output = main()
        self.assertEqual(None, output)
        
    def test_11(self):
        sys.argv = [self.prog, 'list', '-r', self.repo, '-s', 'a']
        output = main()
        self.assertEqual(None, output)
        
    def test_12(self):
        sys.argv = [self.prog, '-r', self.repo, '-s', 'a']
        output = main()
        self.assertEqual(None, output)
        
    def test_13(self):
        sys.argv = [self.prog, '-r', self.repo, '-s', 'a', '-v']
        output = main()
        self.assertEqual(None, output)
        
    def test_wrong_state_0(self):
        """`close` is not a state: `c` or `closed` are"""
        sys.argv = [self.prog, 'list', '-r', self.repo, '-s', 'close']
        self.assertRaises(SystemExit, main)
    
class ShowCommandTests(unittest.TestCase):
    
    def setUp(self):
        self.repo = 'jsmits/github-cli-public-test'
        self.prog = 'ghi'
        
    def test_0(self):
        sys.argv = [self.prog, 'show', '1', '-r', self.repo]
        output = main()
        self.assertEqual(None, output)
        
    def test_1(self):
        sys.argv = [self.prog, '1', '-r', self.repo]
        output = main()
        self.assertEqual(None, output)
        
    def test_2(self):
        sys.argv = [self.prog, '1', '-r', self.repo, '-w']
        self.assertRaises(SystemExit, main)
        
    def test_error_0(self):
        """try to show a non-existing issue"""
        sys.argv = [self.prog, '17288182', '-r', self.repo]
        output = main()
        self.assertEqual("error: issue not found", output)
    
class CloseCommandTests(unittest.TestCase):
    
    def setUp(self):
        self.repo = 'jsmits/github-cli-public-test'
        self.prog = 'ghi'
        
    def test_0(self):
        """close issue 1"""
        sys.argv = [self.prog, 'close', '1', '-r', self.repo]
        output = main()
        self.assertEqual(None, output)
        
    def test_1(self):
        """reopen issue 1"""
        sys.argv = [self.prog, 'open', '1', '-r', self.repo]
        output = main()
        self.assertEqual(None, output)
        
    def test_2(self):
        """close issue 1 with abbreviation: c"""
        sys.argv = [self.prog, 'c', '1', '-r', self.repo]
        output = main()
        self.assertEqual(None, output)
        
    def test_3(self):
        """and reopen issue 1 with abbreviation: o"""
        sys.argv = [self.prog, 'o', '1', '-r', self.repo]
        output = main()
        self.assertEqual(None, output)
        
class LabelCommandTests(unittest.TestCase):
    
    def setUp(self):
        self.repo = 'jsmits/github-cli-public-test'
        self.prog = 'ghi'
        
    def test_0(self):
        """add label 'testing' to issue 1"""
        sys.argv = [self.prog, 'label', 'add', 'testing', '1', '-r', self.repo]
        output = main()
        self.assertEqual(None, output)
        
    def test_1(self):
        """remove label 'testing' from issue 1"""
        sys.argv = [self.prog, 'label', 'remove', 'testing', '1', '-r', self.repo]
        output = main()
        self.assertEqual(None, output)
        
    def test_2(self):
        """add label 'testing' to issue 1 with abbreviation: al"""
        sys.argv = [self.prog, 'al', 'testing', '1', '-r', self.repo]
        output = main()
        self.assertEqual(None, output)
        
    def test_3(self):
        """remove label 'testing' from issue 1 with abbreviation: rl"""
        sys.argv = [self.prog, 'rl', 'testing', '1', '-r', self.repo]
        output = main()
        self.assertEqual(None, output)
    
    def test_error_0(self):
        """missing issue nr"""
        sys.argv = [self.prog, 'label', 'add', 'testing', '-r', self.repo]
        output = main()
        self.assertEqual("error: number required\nexample: ghi label add testing 1", output)
        
class SearchCommandTests(unittest.TestCase):
    
    def setUp(self):
        self.repo = 'jsmits/github-cli-public-test'
        self.prog = 'ghi'
        
    def test_0(self):
        sys.argv = [self.prog, 'search', 'test', '-r', self.repo]
        output = main()
        self.assertEqual(None, output)
        
    def test_1(self):
        sys.argv = [self.prog, 's', 'test', '-r', self.repo]
        output = main()
        self.assertEqual(None, output)
        
    def test_2(self):
        sys.argv = [self.prog, 'search', 'test', '-r', self.repo, '-s', 'open']
        output = main()
        self.assertEqual(None, output)
        
    def test_3(self):
        sys.argv = [self.prog, 'search', 'test', '-r', self.repo, '-s', 'o']
        output = main()
        self.assertEqual(None, output)
        
    def test_4(self):
        sys.argv = [self.prog, 's', 'test', '-r', self.repo, '-s', 'o']
        output = main()
        self.assertEqual(None, output)
        
    def test_5(self):
        sys.argv = [self.prog, 'search', 'test', '-r', self.repo, '-s', 'closed']
        output = main()
        self.assertEqual(None, output)
        
    def test_6(self):
        sys.argv = [self.prog, 'search', 'test', '-r', self.repo, '-s', 'c']
        output = main()
        self.assertEqual(None, output)
        
    def test_7(self):
        sys.argv = [self.prog, 's', 'test', '-r', self.repo, '-s', 'c']
        output = main()
        self.assertEqual(None, output)
        
    def test_wrong_0(self):
        sys.argv = [self.prog, 'search', '-r', self.repo]
        self.assertRaises(SystemExit, main)
        
class HelpCommandTests(unittest.TestCase):
    
    def setUp(self):
        self.repo = 'jsmits/github-cli-public-test'
        self.prog = 'ghi'
        
    def test_0(self):
        sys.argv = [self.prog, '--help']
        self.assertRaises(SystemExit, main)
        
    def test_1(self):
        sys.argv = [self.prog, '-h']
        self.assertRaises(SystemExit, main)
        
if __name__ == '__main__':
    unittest.main()