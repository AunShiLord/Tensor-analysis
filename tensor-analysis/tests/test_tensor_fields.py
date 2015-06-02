# -*- coding: utf-8 -*-

from sympy.matrices import Matrix
from sympy.tensor.arraypy import Arraypy, TensorArray, list2arraypy, list2tensor
from sympy.tensor.tensor_fields import df, grad, curl, diverg, lie_xy, dw, \
    lie_w
from sympy import symbols, cos, sin


def test_df_varlist():
    x1, x2, x3 = symbols('x1 x2 x3')
    f = x1**2 * x2 + sin(x2 * x3 - x2)
    var_list = [x1, x2, x3]

    assert df(f, var_list) == [
        2 * x1 * x2, x1**2 + (x3 - 1) * cos(x2 * x3 - x2), x2 *
        cos(x2 * x3 - x2)]
    assert isinstance(df(f, var_list), list)
    assert df(f, var_list, 'l') == [
        2 * x1 * x2, x1**2 + (x3 - 1) * cos(x2 * x3 - x2), x2 *
        cos(x2 * x3 - x2)]
    assert isinstance(df(f, var_list, 'l'), list)

    assert df(f, var_list, 'a') == list2arraypy(
        [2 * x1 * x2, x1**2 + (x3 - 1) * cos(x2 * x3 - x2), x2 *
         cos(x2 * x3 - x2)])
    assert isinstance(df(f, var_list, 'a'), Arraypy)

    assert df(f, var_list, 't') == list2tensor(
        [2 * x1 * x2, x1**2 + (x3 - 1) * cos(x2 * x3 - x2), x2 *
         cos(x2 * x3 - x2)])
    assert isinstance(df(f, var_list, 't'), TensorArray)
    assert df(f, var_list, 't').type_pq == (0, 1)


def test_df_var_tnsr0():
    x1, x2, x3 = symbols('x1 x2 x3')
    f = x1**2 * x2 + sin(x2 * x3 - x2)
    var_tnsr0 = TensorArray(Arraypy(3), (1))
    var_tnsr0[0] = x1
    var_tnsr0[1] = x2
    var_tnsr0[2] = x3

    assert df(f, var_tnsr0) == [
        2 * x1 * x2, x1**2 + (x3 - 1) * cos(x2 * x3 - x2), x2 *
        cos(x2 * x3 - x2)]
    assert isinstance(df(f, var_tnsr0), list)

    assert df(f, var_tnsr0, 'l') == [
        2 * x1 * x2, x1**2 + (x3 - 1) * cos(x2 * x3 - x2), x2 *
        cos(x2 * x3 - x2)]
    assert isinstance(df(f, var_tnsr0, 'l'), list)

    assert df(f, var_tnsr0, 'a') == list2arraypy(
        [2 * x1 * x2, x1**2 + (x3 - 1) * cos(x2 * x3 - x2), x2 *
         cos(x2 * x3 - x2)])
    assert isinstance(df(f, var_tnsr0, 'a'), Arraypy)

    assert df(f, var_tnsr0, 't') == list2tensor(
        [2 * x1 * x2, x1**2 + (x3 - 1) * cos(x2 * x3 - x2), x2 *
         cos(x2 * x3 - x2)])
    assert isinstance(df(f, var_tnsr0, 't'), TensorArray)
    assert df(f, var_tnsr0, 't').type_pq == (0, 1)


def test_df_var_tnsr1():
    x1, x2, x3 = symbols('x1 x2 x3')
    f = x1**2 * x2 + sin(x2 * x3 - x2)

    var_tnsr1 = Arraypy([1, 3, 1]).to_tensor(1)
    var_tnsr1[1] = x1
    var_tnsr1[2] = x2
    var_tnsr1[3] = x3

    res_ar1 = Arraypy([1, 3, 1])
    res_ar1[1] = 2 * x1 * x2
    res_ar1[2] = x1**2 + (x3 - 1) * cos(x2 * x3 - x2)
    res_ar1[3] = x2 * cos(x2 * x3 - x2)
    res_ten1 = res_ar1.to_tensor(-1)

    assert df(f, var_tnsr1) == [
        2 * x1 * x2, x1**2 + (x3 - 1) * cos(x2 * x3 - x2), x2 *
        cos(x2 * x3 - x2)]
    assert isinstance(df(f, var_tnsr1), list)

    assert df(f, var_tnsr1, 'l') == [
        2 * x1 * x2, x1**2 + (x3 - 1) * cos(x2 * x3 - x2), x2 *
        cos(x2 * x3 - x2)]
    assert isinstance(df(f, var_tnsr1, 'l'), list)

    assert df(f, var_tnsr1, 'a') == res_ar1
    assert isinstance(df(f, var_tnsr1, 'a'), Arraypy)

    assert df(f, var_tnsr1, 't') == res_ten1
    assert isinstance(df(f, var_tnsr1, 't'), TensorArray)
    assert df(f, var_tnsr1, 't').type_pq == (0, 1)


def test_diverg_var_x_list():
    x1, x2, x3 = symbols('x1 x2 x3')

    X = [x1 * x2**3, x2 - cos(x3), x3**3 - x1]
    var = [x1, x2, x3]
    g = Matrix([[2, 1, 0], [1, 3, 0], [0, 0, 1]])

    ten = Arraypy([2, 3, 0]).to_tensor((-1, -1))
    ten[0, 0] = 2
    ten[0, 1] = 1
    ten[0, 2] = 0
    ten[1, 0] = 1
    ten[1, 1] = 3
    ten[1, 2] = 0
    ten[2, 0] = 0
    ten[2, 1] = 0
    ten[2, 2] = 1

    ten1 = Arraypy([2, 3, 1]).to_tensor((-1, -1))
    ten1[1, 1] = 2
    ten1[1, 2] = 1
    ten1[1, 3] = 0
    ten1[2, 1] = 1
    ten1[2, 2] = 3
    ten1[2, 3] = 0
    ten1[3, 1] = 0
    ten1[3, 2] = 0
    ten1[3, 3] = 1

    assert diverg(X, var) == x2**3 + 3 * x3**2 + 1
    assert diverg(X, var, g) == x2**3 + 3 * x3**2 + 1
    assert diverg(X, var, ten) == x2**3 + 3 * x3**2 + 1
    assert diverg(X, var, ten1) == x2**3 + 3 * x3**2 + 1


def test_grad_varlist():
    x1, x2, x3 = symbols('x1 x2 x3')

    f = x1**2 * x2 + sin(x2 * x3 - x2)
    var1 = [x1, x2, x3]

    res_ar1 = Arraypy([1, 3, 0])
    res_ar1[0] = 2 * x1 * x2
    res_ar1[1] = x1**2 + (x3 - 1) * cos(x2 * x3 - x2)
    res_ar1[2] = x2 * cos(x2 * x3 - x2)
    res_ten1 = res_ar1.to_tensor(1)

    res_ar = Arraypy([1, 3, 0])
    res_ar[0] = -x1**2 / 5 + 6 * x1 * x2 / 5 - (x3 - 1) * cos(x2 * x3 - x2) / 5
    res_ar[1] = 2 * x1**2 / 5 - 2 * x1 * x2 / \
        5 + cos(x2 * x3 - x2) * 2 * (x3 - 1) / 5
    res_ar[2] = x2 * cos(x2 * x3 - x2)
    res_ten = res_ar.to_tensor(1)

    g = Matrix([[2, 1, 0], [1, 3, 0], [0, 0, 1]])

    assert grad(f, var1, output_type='l') == [
        2 * x1 * x2, x1**2 + (x3 - 1) * cos(x2 * x3 - x2), x2 *
        cos(x2 * x3 - x2)]
    assert isinstance(grad(f, var1, output_type='l'), list)

    assert grad(f, var1) == [
        2 * x1 * x2, x1**2 + (x3 - 1) * cos(x2 * x3 - x2), x2 *
        cos(x2 * x3 - x2)]
    assert isinstance(grad(f, var1), list)

    assert grad(f, var1, output_type='a') == res_ar1
    assert isinstance(grad(f, var1, output_type='t'), Arraypy)

    assert grad(f, var1, output_type='t') == res_ten1
    assert isinstance(grad(f, var1, output_type='t'), TensorArray)
    assert grad(f, var1, output_type='t').type_pq == (1, 0)

    assert str(
        grad(
            f,
            var1,
            g,
            output_type='l')) == '[-x1**2/5 + 6*x1*x2/5 - (x3 - 1)*cos(x2*x3 - x2)/5, 2*x1**2/5 - 2*x1*x2/5 + 2*(x3 - 1)*cos(x2*x3 - x2)/5, x2*cos(x2*x3 - x2)]'
    assert isinstance(grad(f, var1, g, output_type='l'), list)

    assert grad(f, var1, g, output_type='a') == res_ar
    assert isinstance(grad(f, var1, g, output_type='a'), Arraypy)

    assert grad(f, var1, g, output_type='t') == res_ten
    assert isinstance(grad(f, var1, g, output_type='t'), TensorArray)
    assert grad(f, var1, g, output_type='t').type_pq == (1, 0)


def test_grad_gtnsr():
    x1, x2, x3 = symbols('x1 x2 x3')
    f = x1**2 * x2 + sin(x2 * x3 - x2)
    var1 = [x1, x2, x3]

    k1 = Arraypy([1, 3, 0]).to_tensor(1)
    k1[0] = x1
    k1[1] = x2
    k1[2] = x3

    # g задано tensor, индекс с 1 и var-list
    a = Arraypy([2, 3, 1])
    b = a.to_tensor((-1, -1))
    b[1, 1] = 2
    b[1, 2] = 1
    b[1, 3] = 0
    b[2, 1] = 1
    b[2, 2] = 3
    b[2, 3] = 0
    b[3, 1] = 0
    b[3, 2] = 0
    b[3, 3] = 1

    res_ar = Arraypy([1, 3, 1])
    res_ar[1] = -x1**2 / 5 + 6 * x1 * x2 / 5 - (x3 - 1) * cos(x2 * x3 - x2) / 5
    res_ar[2] = 2 * x1**2 / 5 - 2 * x1 * x2 / \
        5 + cos(x2 * x3 - x2) * 2 * (x3 - 1) / 5
    res_ar[3] = x2 * cos(x2 * x3 - x2)
    res_ten = res_ar.to_tensor(1)

    res_ar1 = Arraypy([1, 3, 0])
    res_ar1[0] = 2 * x1 * x2
    res_ar1[1] = x1**2 + (x3 - 1) * cos(x2 * x3 - x2)
    res_ar1[2] = x2 * cos(x2 * x3 - x2)

    assert str(
        grad(
            f,
            var1,
            b,
            'l')) == '[-x1**2/5 + 6*x1*x2/5 - (x3 - 1)*cos(x2*x3 - x2)/5, 2*x1**2/5 - 2*x1*x2/5 + 2*(x3 - 1)*cos(x2*x3 - x2)/5, x2*cos(x2*x3 - x2)]'
    assert isinstance(grad(f, var1, b, 'l'), list)

    assert grad(f, var1, b, 'a') == res_ar
    assert isinstance(grad(f, var1, b, 'a'), Arraypy)
    assert grad(f, k1, output_type='a') == res_ar1
    assert isinstance(grad(f, k1, output_type='a'), Arraypy)

    assert grad(f, var1, b, 't') == res_ten
    assert isinstance(grad(f, var1, b, 't'), TensorArray)
    assert grad(f, var1, b, 't').type_pq == (1, 0)
    assert grad(f, var1, b) == res_ten
    assert isinstance(grad(f, var1, b, 't'), TensorArray)
    assert grad(f, var1, b, 't').type_pq == (1, 0)


def test_grad_gm_vl():
    x1, x2, x3 = symbols('x1 x2 x3')
    f = x1**2 * x2 + sin(x2 * x3 - x2)
    var1 = [x1, x2, x3]
    g = Matrix([[2, 1, 0], [1, 3, 0], [0, 0, 1]])

    k0 = Arraypy([1, 3, 1]).to_tensor(1)
    k0[1] = x1
    k0[2] = x2
    k0[3] = x3

    res_ar = Arraypy([1, 3, 0])
    res_ar[0] = -x1**2 / 5 + 6 * x1 * x2 / 5 - (x3 - 1) * cos(x2 * x3 - x2) / 5
    res_ar[1] = 2 * x1**2 / 5 - 2 * x1 * x2 / \
        5 + cos(x2 * x3 - x2) * 2 * (x3 - 1) / 5
    res_ar[2] = x2 * cos(x2 * x3 - x2)
    res_ten = res_ar.to_tensor(1)

    assert str(
        grad(
            f,
            k0,
            g,
            'l')) == '[-x1**2/5 + 6*x1*x2/5 - (x3 - 1)*cos(x2*x3 - x2)/5, 2*x1**2/5 - 2*x1*x2/5 + 2*(x3 - 1)*cos(x2*x3 - x2)/5, x2*cos(x2*x3 - x2)]'
    assert isinstance(grad(f, k0, g, 'l'), list)

    assert grad(f, k0, g, 'a') == res_ar
    assert isinstance(grad(f, k0, g, 'a'), Arraypy)

    assert grad(f, k0, g, 't') == res_ten
    assert isinstance(grad(f, k0, g, 't'), TensorArray)
    assert grad(f, k0, g, 't').type_pq == (1, 0)


def test_lie_xy():
    x1, x2, x3, t, l, a = symbols('x1 x2 x3 t l a')

    X = [x1 * x2**3, x2 - cos(x3), x3**3 - x1]
    Y = [x1**3 * x2**3, x2 * x3 - sin(x1 * x3), x3**3 - x1**2]
    arg = [x1, x2, x3]

    res_ar = Arraypy([1, 3, 0])
    res_ar[0] = 2 * x1**3 * x2**6 + 3 * x1**3 * x2**2 * \
        (x2 - cos(x3)) - 3 * x1 * x2**2 * (x2 * x3 - sin(x1 * x3))
    res_ar[1] = -x1 * x2**3 * x3 * cos(x1 * x3) - x2 * x3 + x3 * (x2 - cos(
        x3)) + (-x1 + x3**3) * (-x1 * cos(x1 * x3) + x2) - (-x1**2 + x3**3) * \
        sin(x3) + sin(x1 * x3)
    res_ar[2] = x1**3 * x2**3 - 2 * x1**2 * x2**3 + 3 * \
        x3**2 * (-x1 + x3**3) - 3 * x3**2 * (-x1**2 + x3**3)
    res_ten = res_ar.to_tensor(1)

    assert lie_xy(X, Y, arg, 'l') == [2 *
                                      x1**3 *
                                      x2**6 +
                                      3 *
                                      x1**3 *
                                      x2**2 *
                                      (x2 -
                                       cos(x3)) -
                                      3 *
                                      x1 *
                                      x2**2 *
                                      (x2 *
                                          x3 -
                                          sin(x1 *
                                              x3)), -
                                      x1 *
                                      x2**3 *
                                      x3 *
                                      cos(x1 *
                                          x3) -
                                      x2 *
                                      x3 +
                                      x3 *
                                      (x2 -
                                          cos(x3)) +
                                      (-
                                          x1 +
                                          x3**3) *
                                      (-
                                          x1 *
                                          cos(x1 *
                                              x3) +
                                          x2) -
                                      (-
                                          x1**2 +
                                          x3**3) *
                                      sin(x3) +
                                      sin(x1 *
                                          x3), x1**3 *
                                      x2**3 -
                                      2 *
                                      x1**2 *
                                      x2**3 +
                                      3 *
                                      x3**2 *
                                      (-
                                          x1 +
                                          x3**3) -
                                      3 *
                                      x3**2 *
                                      (-
                                          x1**2 +
                                          x3**3)]
    assert isinstance(lie_xy(X, Y, arg, 'l'), list)

    assert lie_xy(X, Y, arg, 'a') == res_ar
    assert isinstance(lie_xy(X, Y, arg, 'a'), Arraypy)

    assert lie_xy(X, Y, arg, 't') == res_ten
    assert isinstance(lie_xy(X, Y, arg, 't'), TensorArray)
    assert lie_xy(X, Y, arg, 't').type_pq == (1, 0)


def test_curl():
    x1, x2, x3 = symbols('x1 x2 x3')
    X = [x1 * x2**3, x2 - cos(x3), x3**3 - x1]
    arg = [x1, x2, x3]

    j = Arraypy(3)
    k0 = TensorArray(j, (1))
    k0[0] = x1 * x2**3
    k0[1] = x2 - cos(x3)
    k0[2] = x3**3 - x1

    k1 = Arraypy([1, 3, 1]).to_tensor(1)
    k1[1] = x1 * x2**3
    k1[2] = x2 - cos(x3)
    k1[3] = x3**3 - x1

    v0 = TensorArray(j, (1))
    v0[0] = x1
    v0[1] = x2
    v0[2] = x3

    v1 = Arraypy([1, 3, 1]).to_tensor(1)
    v1[1] = x1
    v1[2] = x2
    v1[3] = x3

    s0 = TensorArray(j, (1))
    s0[0] = -sin(x3)
    s0[1] = 1
    s0[2] = -3 * x1 * x2**2

    s1 = Arraypy([1, 3, 1]).to_tensor(1)
    s1[1] = -sin(x3)
    s1[2] = 1
    s1[3] = -3 * x1 * x2**2

    assert curl(X, arg) == [-sin(x3), 1, -3 * x1 * x2**2]
    assert isinstance(curl(X, arg), list)

    assert curl(X, arg, 'a') == list2arraypy([-sin(x3), 1, -3 * x1 * x2**2])
    assert isinstance(curl(X, arg, 'a'), Arraypy)

    assert curl(X, arg, 't') == s0
    assert isinstance(curl(X, arg, 't'), TensorArray)
    assert curl(X, arg, 't').type_pq == (1, 0)

    assert curl(k0, arg) == s0
    assert isinstance(curl(k0, arg), TensorArray)
    assert curl(X, arg, 't').type_pq == (1, 0)

    assert curl(k0, arg, 'a') == list2arraypy([-sin(x3), 1, -3 * x1 * x2**2])
    assert isinstance(curl(k0, arg, 'a'), Arraypy)

    assert curl(k0, arg, 't') == s0
    assert isinstance(curl(k0, arg, 't'), TensorArray)
    assert curl(X, arg, 't').type_pq == (1, 0)

    assert curl(k1, v1, 't') == s1
    assert isinstance(curl(k1, v1, 't'), TensorArray)
    assert curl(k1, v1, 't').type_pq == (1, 0)


def test_lie_w():

    x1, x2, x3 = symbols('x1, x2, x3')

    X = [x1 * x2**3, x2 - cos(x3), x3**3 - x1]

    arr = Arraypy((3, 3))
    y = TensorArray(arr, (-1, -1))
    y1 = TensorArray(arr, (-1, -1))

    y[0, 1] = x3
    y[0, 2] = -x2
    y[1, 0] = -x3
    y[1, 2] = x1
    y[2, 0] = x2
    y[2, 1] = -x1

    y1[0, 1] = x2**3 * x3 + x3**3 + x3
    y1[0, 2] = -x2**4 - 3 * x2 * x3**2 - x2 + x3 * sin(x3) + cos(x3)
    y1[1, 0] = -x2**3 * x3 - x3**3 - x3
    y1[1, 2] = -2 * x1 * x2**3 + 3 * x1 * x3**2 + x1
    y1[2, 0] = x2**4 + 3 * x2 * x3**2 + x2 - x3 * sin(x3) - cos(x3)
    y1[2, 1] = 2 * x1 * x2**3 - 3 * x1 * x3**2 - x1

    assert lie_w(y, X, [x1, x2, x3]) == y1
    assert isinstance(lie_w(y, X, [x1, x2, x3]), TensorArray)
    assert lie_w(y, X, [x1, x2, x3]).type_pq == (0, 2)

    omega = TensorArray(arr, (-1, -1))
    omega[0, 1] = x2
    omega[1, 0] = -x2
    omega[0, 2] = -x1
    omega[2, 0] = x1

    ten = TensorArray(arr, (-1, -1))
    ten[0, 1] = x2**4 + 2 * x2 - cos(x3)
    ten[0, 2] = -2 * x1 * x2**3 - 3 * x1 * x3**2 + x2 * sin(x3)
    ten[1, 0] = -x2**4 - 2 * x2 + cos(x3)
    ten[1, 2] = -3 * x1**2 * x2**2
    ten[2, 0] = 2 * x1 * x2**3 + 3 * x1 * x3**2 - x2 * sin(x3)
    ten[2, 1] = 3 * x1**2 * x2**2

    assert lie_w(omega, X, [x1, x2, x3]) == ten
    assert isinstance(lie_w(omega, X, [x1, x2, x3]), TensorArray)
    assert lie_w(omega, X, [x1, x2, x3]).type_pq == (0, 2)


def test_dw():
    x1, x2, x3 = symbols('x1 x2 x3')

    y = TensorArray(Arraypy((3, 3)), (-1, -1))
    y1 = TensorArray(Arraypy((3, 3, 3)), (-1, -1, -1))

    y[0, 1] = x3
    y[0, 2] = -x2
    y[1, 0] = -x3
    y[1, 2] = x1
    y[2, 0] = x2
    y[2, 1] = -x1

    y1[0, 1, 2] = 3
    y1[0, 2, 1] = -3
    y1[1, 0, 2] = -3
    y1[1, 2, 0] = 3
    y1[2, 0, 1] = 3
    y1[2, 1, 0] = -3

    assert dw(y, [x1, x2, x3]) == y1
    assert isinstance(dw(y, [x1, x2, x3]), TensorArray)
    assert dw(y, [x1, x2, x3]).type_pq == (0, 3)
