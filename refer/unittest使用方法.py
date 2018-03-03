import unittest


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        # Do something to initiate the test environment here.
        pass

    def tearDown(self):
        # Do something to clear the test environment here.
        pass

    def test_upper(self):
        self.assertTrue(True)

    def test_isupper(self):
        self.assertTrue(False)


if __name__ == '__main__':
    # 构造测试集
    tests = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)

    suite = unittest.TestSuite([tests])
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)


    # class TextTestResult(result.TestResult): 继承 result.TestResult
    unittest.runner.TextTestResult
    """
        self.failfast = False
        self.failures = []
        self.errors = []
        self.testsRun = 0
        self.skipped = []
        self.expectedFailures = []
        self.unexpectedSuccesses = []
        self.shouldStop = False
        self.buffer = False
        self.tb_locals = False
        self._stdout_buffer = None
        self._stderr_buffer = None
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        self._mirrorOutput = False
    """

    # print(type(test_result)) # <class 'unittest.runner.TextTestResult'>
    # print("result:",test_result) # <unittest.runner.TextTestResult run=2 errors=0 failures=1>
    print("sum:",test_result.testsRun)
    print("fail:",len(test_result.failures),type(test_result.failures))
    print("skip:",len(test_result.skipped),type(test_result.skipped))

    print("-"*50)
    for case, reason in test_result.failures:
        print("caseId:",case.id()," reason:",reason)
        print("xx"*50)