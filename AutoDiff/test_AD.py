#test_AD.py
#Nov 4, 2018

#This test suite is associated with file 'AD.py', 
#which implements forward-mode automatic differentiation.

#import unit testing packages pytest and numpy testing
import pytest
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal
#import AD
from AutoDiff import AD

#AD_create allows for simultaneous assignment 
#of AD instances
def test_AD_create():
    a, b, c = AD.AD_create([1, 2, 3])
    assert a.val == [1], a.der == [[1,0,0]]
    assert b.val == [2], b.der == [[0,1,0]]
    assert c.val == [3], c.der == [[0,0,1]]

#AD_stack takes in multiple AD instances
#in the form of numpy arrays, returns 
#values as a vector and derivatives as a matrix
def test_AD_stack():
    a, b, c = AD.AD_create([1, 2, 3])
    c = AD.AD_stack([a, b, c])
    assert_array_equal(c.val, np.array([1,2,3]))
    assert_array_equal(c.der, np.array([[1,0,0],[0,1,0],[0,0,1]]))

#Test whether constructor of AutoDiff class 
#returns proper values, derivatives, and errors
def test_AutoDiff_constuctor_init():
    a = 5.0
    b = AD.AutoDiff(a)
    assert_array_equal(b.val, np.array([5.0]))
    assert_array_equal(b.der, np.array([[1]]))
    #inputs ought not to be type other than integer, list or numpy array
    with pytest.raises(TypeError):
        AD.AutoDiff('hello','friend')
    #check if dimension of derivative input matches that of value input
    #check if dimension of derivative is higher than 2
    with pytest.raises(ValueError):
        AD.AutoDiff([1,2], [[1,0,0],[0,1,0]])
        AD.AutoDiff([1,2,3],[[1,2,3],[1,2]])
        AD.AutoDiff([1,2,3],[[1,2,3],[1,2],[1,3],[2,3]])
        
#Test whether addition works between AD instances, 
#and between AD instance and number, regardless of order
def test_AutoDiff_add():
    x, y = AD.AD_create([5.0, 7.0])
    z = 3.0
    sum1 = x + y #AD+AD
    sum2 = x + z #AD+number
    sum3 = z + y #test __radd__: number+AD
    assert sum1.val == [12.0]
    assert_array_equal(sum1.der, np.array([[1, 1]]))
    assert sum2.val == [8.0]
    assert_array_equal(sum2.der, np.array([[1, 0]]))
    assert sum3.val == [10.0]
    assert_array_equal(sum3.der, np.array([[0, 1]]))
    with pytest.raises(TypeError):
        x + 'hello'
        'friend' + y

#Test whether subtraction works between AD instances,
#and between AD instance and number, regardless of order
def test_AutoDiff_sub():
    x, y = AD.AD_create([5.0, 7.0])
    z = 3.0
    m = 10.0
    sub1 = y - x #AD-AD
    sub2 = x - z #AD-number
    sub3 = m - x #test __rsub__: number-AD
    assert sub1.val == [2.0]
    assert_array_equal(sub1.der, np.array([[-1, 1]]))
    assert sub2.val == [2.0]
    assert_array_equal(sub2.der, np.array([[1, 0]]))
    assert sub3.val == [5.0]
    assert_array_equal(sub3.der, np.array([[-1, 0]]))
    with pytest.raises(TypeError):
        x - 'hello'
        'friend' - y

#Test whether multiplication works between AD instances,
#and between AD instance and number, regardless of order
def test_AutoDiff_mul():
    x, y = AD.AD_create([5.0, 7.0])
    z = 3.0
    mul1 = x * y #AD*AD
    mul2 = x * z #AD*number
    mul3 = z * y #test __rmul__: number*AD
    assert mul1.val == [35.0]
    assert_array_equal(mul1.der, np.array([[7.0, 5.0]]))
    assert mul2.val == [15.0]
    assert_array_equal(mul2.der, np.array([[3.0, 0]]))
    assert mul3.val == [21.0]
    assert_array_equal(mul3.der, np.array([[0 , 3.0]]))
    with pytest.raises(TypeError):
        x * 'hello'
        'friend' * y
    
#Test whether division works between AD instances,
#and between AD instance and number, regardless of order
def test_AutoDiff_div():
    x, y = AD.AD_create([4.0, 8.0])
    z = 2.0
    div1 = y / x #AD/AD
    div2 = x / z #AD/number
    div3 = z / y #test __rtruediv__: number/AD
    assert div1.val == [2.0]
    assert_array_equal(div1.der, np.array([[-0.5, 0.25]]))
    assert div2.val == [2.0]
    assert_array_equal(div2.der, np.array([[0.5, 0]]))
    assert div3.val == [0.25]
    assert_array_equal(div3.der, np.array([[0, -0.03125]]))
    with pytest.raises(TypeError):
        x / 'hello'
        'friend' / y
    
#Test whether differetiation with power works when
#AD instance is the base, and when AD instance is 
#the exponent
def test_AutoDiff_pow():
    x, y = AD.AD_create([2.0, 3.0])
    a, b = AD.AD_create(np.array([1.0, 2.0]))
    z = 5.0
    power1 = (x*y) ** z #AD**number
    power2 = z ** (a*b) #test __rpow__: number**AD
    assert power1.val == [7776.0]
    assert_array_equal(power1.der, np.array([[19440., 12960.]]))
    assert power2.val == [25.0]
    assert_array_almost_equal(power2.der, np.array([[80.47189562, 40.23594781]]))
    with pytest.raises(TypeError):
        x ** 'hello'
        'friend' ** y

#Test whether taking the negative of AD instance works
def test_AutoDiff_neg():
    x, y = AD.AD_create([2.0, 8.0])
    neg1 = -x
    neg2 = -(x/y)
    assert neg1.val == [-2.0]
    assert_array_equal(neg1.der, np.array([[-1, 0]]))
    assert neg2.val == [-0.25]
    assert_array_equal(neg2.der, np.array([[-0.125, 0.03125]]))

#Test whether taking the sine of AD instance returns the correct value
def test_AutoDiff_sin():
    x = AD.AutoDiff(1.0, [1, 0])
    y = x.sin()
    assert_array_almost_equal(y.val, np.array([0.84147098]), decimal = 6)
    assert_array_almost_equal(y.der, np.array([[0.54030231, 0.]]), decimal = 6)

#Test whether taking the cosine of AD instance returns the correct value
def test_AutoDiff_cos():
    a, b = AD.AD_create([2.0, 8.0])
    c = (a*b).cos()
    assert_array_almost_equal(c.val, np.array([-0.95765948]), decimal = 6)
    assert_array_almost_equal(c.der, np.array([[2.30322653, 0.57580663]]), decimal = 6)

#Test whether taking the natural logarithm of AD instance returns the correct value
def test_AutoDiff_log():
    a, b = AD.AD_create([2.0, 8.0])
    c = (a*b).log()
    assert_array_almost_equal(c.val, np.array([2.77258872]), decimal = 6)
    assert_array_equal(c.der, np.array([[0.5, 0.125]]))