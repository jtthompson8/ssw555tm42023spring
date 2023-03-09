import unittest
import json
from unittest.mock import Mock, patch
from unittest.mock import MagicMock

from Data import getData

class MockResponse:
    def __init__(self, data):
        self.data = data
    def json(self):
            return self.data
    


class TestData(unittest.TestCase):

    @patch('Data.requests.get')
    def testData(self, mockedReq):

        mockedReq.return_value = MockResponse(['Repo: CI-Lab Number of commits: 30', 'Repo: Complexity Number of commits: 30', 'Repo: CS-546-lab8 Number of commits: 3', 'Repo: CS_546_Final_Project Number of commits: 30', 'Repo: designPatternPractice Number of commits: 3', 'Repo: GitTest Number of commits: 3', 'Repo: HW1-Git-Github Number of commits: 3', 'Repo: HW3-345 Number of commits: 30', 'Repo: lab8 Number of commits: 3', 'Repo: Node.js-Application-Lab---SSW-345 Number of commits: 2', 'Repo: react-exercise Number of commits: 30', 'Repo: Reflection-SSW345 Number of commits: 10', 'Repo: test-HW4-345 Number of commits: 2', 'Repo: test-HW4-3454 Number of commits: 2', 'Repo: test-HW4-34555 Number of commits: 2', 'Repo: test-HW4-SSW-345 Number of commits: 2', 'Repo: tst Number of commits: 2'])
        res = getData("chuang57")
        self.assertTrue('Repo: Repo: CI-Lab Number of commits: 30' in res)
        self.assertTrue('Repo: Repo: Complexity Number of commits: 30' in res)



if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()

