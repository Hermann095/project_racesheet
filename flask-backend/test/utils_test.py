from simulation.utils import isNan, isInvalid, FLOAT_MAX, secToTimeStr, nationCodeToFlag

#isNan
def test_nan():
    assert isNan(1.0) == False

def test_nan2():
    assert isNan(float("nan")) == True

def test_nan3():
    assert isNan(FLOAT_MAX) == False

def test_nan4():
    assert isNan(123) == False

def test_nan5():
    assert isNan(float("inf")) == False

#isInvalid
def test_valid():
    assert isInvalid(1.0) == False

def test_valid2():
    assert isInvalid(float("nan")) == True

def test_valid3():
    assert isInvalid(FLOAT_MAX) == False

def test_valid4():
    assert isInvalid(123) == False

def test_valid5():
    assert isInvalid(float("inf")) == True

#secToTimeStr
def test_secToTimeStr():
    assert secToTimeStr(FLOAT_MAX) == "No Time"

def test_secToTimeStr2():
    assert secToTimeStr(float("nan")) == "No Time"

def test_secToTimeStr3():
    assert secToTimeStr(90.0) == "1:30.000"

def test_secToTimeStr4():
    assert secToTimeStr(81.123) == "1:21.123"

def test_secToTimeStr5():
    assert secToTimeStr(59.456) == "59.456"

def test_secToTimeStr6():
    assert secToTimeStr(0) == "0.000"

def test_secToTimeStr7():
    assert secToTimeStr(3602.998) == "1:00:02.998"

def test_secToTimeStr8():
    assert secToTimeStr(3672.998) == "1:01:12.998"

def test_secToTimeStr9():
    assert secToTimeStr(float("inf")) == "No Time"

def test_secToTimeStr10():
    assert secToTimeStr(float("-inf")) == "No Time"


#nationCodeToFlag
def test_nationCodeToFlag():
    assert nationCodeToFlag("") == None

def test_nationCodeToFlag2():
    assert nationCodeToFlag("AAAA") == None

def test_nationCodeToFlag3():
    assert nationCodeToFlag("AUT") == "at.png"


