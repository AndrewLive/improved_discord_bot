class referenceTest():
    def __init__(self, dict):
        self.refDict = dict
        return
    
    def pop(self, key):
        value = self.refDict.pop(key)
        return value

if __name__ == '__main__':
    testDict = {}
    testDict[0] = 'a'
    testDict[1] = 'b'
    testDict[2] = 'c'
    refTest = referenceTest(testDict)
    testDict[3] = 'd'
    testDict[4] = 'e'

    print(testDict)
    print(refTest.refDict)

    testDict.pop(2)

    print(testDict)
    print(refTest.refDict)

    refTest.pop(3)

    print(testDict)
    print(refTest.refDict)

    refTest.refDict[99] = 'z'
    print(testDict)
    print(refTest.refDict)
