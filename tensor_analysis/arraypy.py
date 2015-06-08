# -*- coding: utf-8 -*-

from sympy import Symbol
from sympy.matrices import Matrix, MatrixSymbol
from copy import copy
from sympy import sympify

"""
Module "arraypy" describes tensor and it's bases - Multidimentional arrays.
Module consists of Arraypy class, TensorArray class and converting functions:
list2arraypy, matrix2arraypy, list2tensor, matrix2tensor.
"""


class Arraypy(object):

    """
    N-dimentional array.

    Parameters
    ==========

    self._dims - tuple, array dimension.
    self._rank - Length of self._dims, rank of array.
    self._sparse - boolean variable. True means that array is sparse.
    self._name - custom _name of the element or default value of the element
    self._start_index - first, starting index.
    self._end_index - last, maximum index.
    self._loop_size - Counts number of elements in array.
    self._output - dictionary. Dictionary key is an element index.
    Dictionary value - is array value.
    self._current_index - current index (used in iterator)
    self._iterator_index_count - count of indices (in iterator)

    index - list, represent current index in calculating process.
    [0,0,0]; [0,0,1]; [0,0,2] etc (for 3-dim array).

    """

    def __init__(self, *arg):
        """
        Class constructor
        Creates n-dimensional array.

        Input:
        *arg - custom list of arguments. It could be:
        -Array dimension
        -Name of the Symbol element
        -Default element
        -Sparse
        -Custom range of dimensions

        """

        # main variables declaration
        self._name = '0'
        self._sparse = True
        self._dims = [1]
        self._start_index = [0]
        self._end_index = [1]

        j = 0
        # --recognition of constructor arguments--
        for i in arg:
            # for arguments of type: a = Arraypy( (3,3) )
            if isinstance(i, (tuple)):
                self._dims = i
                self._start_index = [0 for j in range(len(self._dims))]
                self._end_index = [j for j in self._dims]

            # for arguments of type: a = Arraypy( 3 )
            if isinstance(i, int):
                self._dims[0] = i
                self._start_index = [0]
                self._end_index = [i]

            # for string arguments
            if isinstance(i, str):
                i = i.strip()
                # a = Arraypy ('sparse')
                if i == 'sparse':
                    self._sparse = True

                # a = Arraypy ('0..3, 1..4')
                elif len(i.split('..')) != 1:
                    self._dims = i

                    # splitting the string by commas ','. Length of resulted
                    # list will be the rank of array.
                    # '0..3, 1..4'  -> ['0..3' , '1..4']
                    temp = self._dims.split(',')

                    self._rank = len(temp)
                    self._dims = []

                    k = 0
                    for temp_str in temp:
                        # splitting every k-th string by '..'. Resulted digits
                        # will be a start index and end index.
                        # Difference between end index and start index
                        # will be dimension
                        # ['0..3'] -> [['0'], ['3']]
                        temp[k] = temp_str.split('..')
                        if len(temp[k]) != 2:
                            raise SyntaxError('Wrong argument syntax')

                        # cleaning from spaces. If resulted string is digit,
                        # then converting it to integer.
                        # [['0'], ['3']] -> [[0], [3]]
                        for j in range(2):
                            temp[k][j] = temp[k][j].strip()
                            if temp[k][j].isdigit() is False:
                                raise TypeError('Wrong type')
                            temp[k][j] = int(temp[k][j])

                        self._dims.append(temp[k][1] - temp[k][0] + 1)
                        k += 1

                    self._dims = tuple(self._dims)

                    self._start_index = [temp[k][0] for k in range(self._rank)]
                    self._end_index = [
                        temp[k][1] + 1
                        for k in range(self._rank)]

                # a = Arraypy('Py')
                else:
                    self._name = i

            # for list arguments
            if isinstance(i, (list)):

                # a = Arraypy( [2, 4, 1] )
                # first list element - rank
                # second list element - length of every dimension
                # third list element - start index
                if isinstance(i[0], int):
                    if len(i) != 3:
                        raise TypeError('This argument must be lenght of 3')
                    for j in i:
                        if not isinstance(j, int):
                            raise TypeError(
                                'All list elements must be the same type (tuple or int)')
                    if i[0] < 1 or i[1] < 1:
                        raise ValueError(
                            '_rank and length of each dimensions must be greater than 0')
                    self._rank = i[0]
                    self._dims = tuple([i[1] for j in range(i[0])])
                    self._start_index = tuple([i[2] for j in range(i[0])])
                    self._end_index = tuple([i[2] + i[1] for j in range(i[0])])

                # a = Arraypy( [(0, 3), (1, 4)] )
                elif isinstance(i[0], tuple):
                    self._dims = []
                    self._start_index = []
                    self._end_index = []
                    for j in i:
                        if not isinstance(j, tuple):
                            raise TypeError(
                                'All list elements must be the same type (tuple or int)')
                        if len(j) != 2:
                            raise TypeError('Every tuple must be size of 2')
                        if j[0] > j[1]:
                            raise ValueError(
                                'Right border must be greater than left border')
                        self._start_index.append(j[0])
                        self._end_index.append(j[1] + 1)
                        self._dims.append(j[1] - j[0] + 1)
                    self._start_index = tuple(self._start_index)
                    self._end_index = tuple(self._end_index)
        # rank - length of tuple with dimensions
        self._rank = len(self._dims)

        self._output = {}

        # check if self._name is not digit (except '0')
        if self._name[0].isdigit():
            if self._name.isdigit() and self._name == '0':
                self._name = int(self._name)
            else:
                raise ValueError('Element name cant start from digits')

        # index - is an index of current array element
        index = [self._start_index[i] for i in range(self._rank)]

        # counting number of elements in array(equals to number of loops),
        # which is product of every self._dims element
        self._loop_size = self._dims[0]
        for i in range(1, self._rank):
            self._loop_size *= self._dims[i]

        # --setting elements value to dictionary self._output--
        if not (self._sparse and self._name == 0):
            for i in range(self._loop_size):
                if isinstance(self._name, str):
                    self._output[tuple(index)] = Symbol(
                        self._name + str(list(index)))
                else:
                    self._output[tuple(index)] = self._name
                index = self.next_index(index)

        self._dims = tuple(self._dims)
        self._start_index = tuple(self._start_index)
        self._end_index = tuple(self._end_index)

    def __add__(self, other):
        """Overload operator '+'. Returns new Arraypy instance, per elemental
        sum of two Arraypy instances. Both arrays must have the same shape and
        start index.

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy, list2arraypy
        >>> a = list2arraypy([1 for i in range (4)], (2,2))
        >>> b = list2arraypy([4 for i in range (4)], (2,2))
        >>> c = a + b
        >>> print (c)
        5 5
        5 5

        """

        if other == 0:
            return self
        if not isinstance(other, Arraypy):
            raise TypeError('Both operands must be Arraypy type')
        if self._dims != other._dims:
            raise ValueError('Both operands must be same shape')
        if self._start_index != other._start_index or self._end_index != other._end_index:
            raise ValueError(
                'Both operands must have the same start index and end index')

        # forming list of tuples for Arraypy constructor of type
        # a = Arraypy( [(a, b), (c, d), ... , (y, z)] )
        arg = [(self.start_index[i], self.end_index[i])
               for i in range(self._rank)]
        res = Arraypy(arg)

        index = tuple(copy(self._start_index))

        # per elemental sum
        for i in range(self._loop_size):
            res[index] = self.__getitem__(index) + other[index]
            index = self.next_index(index)

        return res

    def __sub__(self, other):
        """
        Overloads operator '-'. Returns new Arraypy instance, per elemental
        difference of two Arraypy instances. Both arrays must have the same
        shape and start index.

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy, list2arraypy
        >>> a = list2arraypy([1 for i in range (4)], (2,2))
        >>> b = list2arraypy([4 for i in range (4)], (2,2))
        >>> c = a - b
        >>> print (c)
        -3 -3
        -3 -3
        """
        if other == 0:
            return self
        if not isinstance(other, Arraypy):
            raise TypeError('Both operands must be Arraypy type')
        if self._dims != other._dims:
            raise ValueError('Both operands must be same shape')
        if self._start_index != other._start_index or self._end_index != other._end_index:
            raise ValueError(
                'Both operands must have the same start index and end index')

        # forming list of tuples for Arraypy constructor of type
        # a = Arraypy( [(a, b), (c, d), ... , (y, z)] )
        arg = [(self.start_index[i], self.end_index[i])
               for i in range(self._rank)]
        res = Arraypy(arg)

        index = tuple(copy(self._start_index))

        # per elemental difference
        for i in range(self._loop_size):
            res[index] = self.__getitem__(index) - other[index]
            index = self.next_index(index)

        return res

    def __mul__(self, other):
        """
        Overloads *.
        n-dimensional arrays can be multiplyed on atom types (int, float, Symbol)

        Examples
        ========

        """
        # forming list of tuples for Arraypy constructor of type
        # a = Arraypy( [(a, b), (c, d), ... , (y, z)] )
        arg = [(self.start_index[i], self.end_index[i])
               for i in range(self._rank)]
        res = Arraypy(arg)

        idx = self.start_index
        for i in range(len(self)):
            res[idx] = self[idx] * other
            idx = self.next_index(idx)

        return res

    def __truediv__(self, other):
        """
        Overloads /.
        n-dimensional arrays can be divided on atom types (int, float, Symbol)

        Examples
        ========

        """
        # forming list of tuples for Arraypy constructor of type
        # a = Arraypy( [(a, b), (c, d), ... , (y, z)] )
        arg = [(self.start_index[i], self.end_index[i])
               for i in range(self._rank)]
        res = Arraypy(arg)

        idx = self.start_index
        for i in range(len(self)):
            res[idx] = self[idx] / other
            idx = self.next_index(idx)

        return res

    # imethods. += -= *= /=
    def __iadd__(self, other):
            return self + other
    def __isub__(self, other):
            return self - other
    def __imul__(self, other):
            return self * other
    def __itruediv__(self, other):
        return self / other

    __radd__ = __add__
    __rmul__ = __mul__
    __rsub__ = __sub__
    __rtruediv__ = __truediv__

    def __eq__(self, other):
        """
        Overloads '=='.
        Arraypy instances can be compared to each other.
        Instances equal if they have same shape, indexes and data.

        Examples
        ========

        >>> from sympy import Arraypy
        >>> a = Arraypy((2, 3))
        >>> b = Arraypy((2, 3))
        >>> a == b
        True
        >>> c = a.reshape((3,2))
        >>> c == b
        False
        >>> a[0,0] = 1
        >>> b[0,0] = 2
        >>> a == b
        False
        """
        if not isinstance(other, Arraypy):
            return False
            #raise TypeError('Compared instances must be Arraypy type')
        if (self.shape != other.shape or self.start_index !=
                other.start_index or self.end_index != other.end_index):
            return False
        idx = self.start_index
        for i in range(len(self)):
            if (self[idx] != other[idx]):
                return False
            idx = self.next_index(idx)

        return True

    def __getitem__(self, index):
        """Allows to get items from arraypy.

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy, list2arraypy
        >>> a = list2arraypy(list(range(4)), (2,2))
        >>> print (a)
        0 1
        2 3
        >>> print(a[0,0])
        0
        >>> print(a.__getitem__((1,1)))
        3

        """
        if isinstance(index, int):
            index = (index,)
        if len(index) != self._rank:
            raise ValueError('Wrong number of array axes')

        # check if input index can exist in current indexing
        for i in range(self._rank):
            if index[i] >= self._end_index[
                    i] or index[i] < self._start_index[i]:
                raise ValueError('Value ' + str(i) + ' out of border')

        # returning element. If array is sparse and index not in dictionary
        # then return '0'
        try:
            if self._sparse:
                if index in self._output:
                    return self._output[index]
                else:
                    return 0
            else:
                return self._output[index]
        except NameError:
            print('Something BAD happend!')

    def __setitem__(self, index, value):
        """Allows to set items to Arraypy.

        Examples
        ========

        from sympy.tensor.arraypy import Arraypy
        a = Arraypy((2,2))
        a[0,0] = 1
        a.__setitem__((1,1),1)
        print (a)
        1 0
        0 1

        """
        if isinstance(index, int):
            index = (index,)

        if len(index) != self._rank:
            raise ValueError('Wrong number of array axes')

        # check if input index can exist in current indexing
        for i in range(self._rank):
            if index[i] >= self._end_index[
                    i] or index[i] < self._start_index[i]:
                raise ValueError('Value ' + str(i) + ' out of border')
            
        # temporary fix. Arraypy sympify is not correct
        if not isinstance(value, Arraypy):
            value = sympify(value)

        # setting element. If array is sparse, index in dictionary and value is
        # 0 then poping it from dictionary
        # If array is sparse, index NOT in dictionary and value is 0 then do
        # nothing
        try:
            # temporary fix. To allow Arraypy to be an element of Arraypy
            if not isinstance(value, Arraypy):
                if self._sparse and value == 0 and index in self._output:
                    self._output.pop(index)
                elif value == 0 and index not in self._output:
                    exit
                else:
                    self._output[index] = value
            else:
                self._output[index] = value
        except NameError:
            print('Something BAD happend!')

    def __len__(self):
        """Overload common function len(). Returns number of elements in array.

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy
        >>> a = Arraypy( (3,3) )
        >>> len(a)
        9
        >>> a.__len__()
        9

        """
        return self._loop_size

    def __str__(self):
        """Returns string, allows to use standart functions print() and str().

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy
        >>> a = Arraypy ( (2, 2), 'Py' )
        >>> print (a)
        Py[0, 0] Py[0, 1]
        Py[1, 0] Py[1, 1]

        """
        out_str = ''
        index = list(copy(self._start_index))

        # forming output string
        for i in range(self._loop_size):
            if self._sparse and not (tuple(index) in self._output):
                out_str += '0' + '  '
            else:
                out_str += str(self._output[tuple(index)]) + '  '

            # code below are equal to method .next_index with few additions.
            j = self._rank - 1
            index[j] += 1
            if (index[j] == self._end_index[j]) and (j != 0):

                # if dimension is changes, then adding '\n'
                out_str += '\n'
                while (index[j] == self._end_index[j]) and j > 0:
                    index[j] = self._start_index[j]
                    j -= 1
                    index[j] += 1

        return out_str

    def __copy__(self):
        """Overload commom python function "copy". Makes right copy of Arraypy
        instance.

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy, copy
        >>> a = Arraypy((2,2))
        >>> b = copy(a)
        >>> c = a

        """

        # creating new instance of Arraypy. All parameters are coping from
        # current array
        res = Arraypy(self._dims)
        res._name = self._name
        res._sparse = self._sparse
        res._start_index = copy(self._start_index)
        res._end_index = copy(self._end_index)
        res._output = copy(self._output)

        return res

    def __iter__(self):
        """Arraypy iterator."""
        self._next_iter_index = self._start_index
        self._current_index = self._start_index
        self._iterator_index_number = 0

        return self

    def __next__(self):
        """Next elemenet in Arraypy in iteration process.

        Allows to use Arraypy instance in for loop.

        """
        if (self._iterator_index_number == self._loop_size):
            raise StopIteration
        else:
            self._iterator_index_number += 1
            self._current_index = self._next_iter_index
            self._next_iter_index = self.next_index(self._current_index)
            return self[self._current_index]

    def next_index(self, index):
        """Returns tuple that represents next index of Arraypy instance.

        Input argument - current index.
        This method allows user to organize loop over whole array.


        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy
        >>> a = Arraypy((2,2,2))
        >>> idx = (0, 0, 0)
        >>> for i in range(0, len(a)):
        ...     print (idx)
        ...     a[idx] = i*10
        ...     idx = a.next_index(idx)
        ...
        (0, 0, 0)
        (0, 0, 1)
        (0, 1, 0)
        (0, 1, 1)
        (1, 0, 0)
        (1, 0, 1)
        (1, 1, 0)
        (1, 1, 1)

        ========

        If input index will be last possible index, then result will be the
        first index(equal to ._start_index)
        >>> idx = (1,1,1)
        >>> idx = a.next_index(idx)
        >>> print (idx)
        (0, 0, 0)

        """
        # check if input index can exist in current indexing
        index = list(index)
        for i in range(0, self._rank):
            if index[i] >= self._end_index[
                    i] or index[i] < self._start_index[i]:
                raise IndexError('Wrong index')

        j = self._rank - 1
        # increasing index by 1. (0, 0, 0) -> (0, 0, 1)
        index[j] += 1

        # in index exceeds top border, then index changes this way
        # ( self._start_index = (0, 0, 0) и self._end_index = (2, 2, 2) ):
        # (0, 0, 1) -> (0, 0, 2) -> (0, 1, 0)
        # (0, 1, 0) -> (0, 1, 1)
        # (0, 1, 1) -> (0, 1, 2) - > (0, 2, 0) -> (1, 0, 0)
        # and so on...
        if (index[j] == self._end_index[j]) and (j != 0):
            while (index[j] == self._end_index[j]) and j > 0:
                index[j] = self._start_index[j]
                j -= 1
                index[j] += 1

        # if index == (2, 0, 0), then index sets to self._start_index -> (0, 0,
        # 0)
        if index[0] >= self._end_index[0]:
            index = copy(self._start_index)

        index = tuple(index)
        return index

    def reshape(self, new_shape):
        """Returns Arraypy instance with new shape. Elements number must be
        suitable to new shape. The only argument of method sets new shape.

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy
        >>> a = Arraypy( '1..2, 1..3', 'Py' )
        >>> a.shape
        (2, 3)
        >>> a.start_index
        (1, 1)
        >>> print (a)
        Py[1, 1] Py[1, 2] Py[1, 3]
        Py[2, 1] Py[2, 2] Py[2, 3]
        >>> b = a.reshape((3,2))
        >>> b.shape
        (3, 2)
        >>> b.start_index
        (0, 0)
        >>> print (b)
        Py[1, 1] Py[1, 2]
        Py[1, 3] Py[2, 1]
        Py[2, 2] Py[2, 3]

        """
        if (isinstance(new_shape, int)):
            new_shape = (new_shape,)

        prod = 1
        for i in new_shape:
            prod *= i

        # if product of shape elements equals to number of elements in array
        # then
        if (prod == self.__len__()):
            new_base = Arraypy(new_shape)
            idx1 = self._start_index
            idx2 = new_base._start_index

            for i in range(self.__len__()):
                new_base[idx2] = self._output[idx1]
                idx2 = new_base.next_index(idx2)
                idx1 = self.next_index(idx1)

        else:
            raise ValueError(
                'Number of elements of New shaped array must be equal to number of elements in Old shape')
        return new_base

    @property
    def shape(self):
        """Returs array shape (dimension).

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy
        >>> a = Arraypy((3,3))
        >>> a.shape
        (3, 3)

        """
        return self._dims

    @property
    def start_index(self):
        """Returns the first index.

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy
        >>> a = Arraypy ( [(0, 2), (1, 3)] )
        >>> a.start_index
        (0, 1)

        """
        return self._start_index

    @property
    def end_index(self):
        """Returns the last possible index.

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy
        >>> a = Arraypy ( [(0, 2), (1, 3)] )
        >>> a.end_index
        (2, 3)

        """
        res = tuple([self._end_index[i] - 1 for i in range(self._rank)])
        return res

    @property
    def iter_index(self):
        """Return current index in iteration process.

        Use it only in loops over Arraypy/TensorArray.

        """
        return self._current_index

    @property
    def rank(self):
        """Returns rank of arrray.

        Examples
        ========

        from sympy.tensor.arraypy import Arraypy
        a = Arraypy ( (3,4,5,6,3) )
        a.rank
        5

        """
        return self._rank

    @property
    def index_list(self):
        """Returns list of all possible indicies.
        The indices are sorted in ascending: from very first to very last.
        Another way to organize loops over Arraypy or TensorArray.

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy
        >>> a = Arraypy((2,2))
        >>> print(a.index_list)
        [(0, 0), (0, 1), (1, 0), (1, 1)]
        >>> for i in a.index_list:
        ...     a[i] = 5
        >>> print(a)
        5  5
        5  5

        """
        result_list = []
        idx = self.start_index
        for i in range(len(self)):
            result_list.append(idx)
            idx = self.next_index(idx)

        return result_list

    def to_matrix(self):
        """
        Converts Arraypy to Matrix. Can convert only 2-dim array, else will raise error.

        Examples
        ========

        from sympy.tensor.arraypy import Arraypy, list2arraypy
        a = list2arraypy( [1 for i in range(9)], (3,3))
        b = a.to_matrix()
        print(b)
        [1, 1, 1]
        [1, 1, 1]
        [1, 1, 1]
        type(b)
        <class 'sympy.matrices.matrices.MutableMatrix'>
        """
        if self._rank != 2:
            raise ValueError('Dimensions must be of size of 2')

        # creating matrix of needed shape: self._dims[0] on self._dims[1]
        x = MatrixSymbol(0, self._dims[0], self._dims[1])
        res_matrix = Matrix(x)
        # res_matrix = Matrix(self.shape[0], self.shape[1], [0 for i in range
        # self.shape[0]*self.shape[1]])

        # filling matrix with Arraypy elements
        idx = self._start_index
        idx = tuple(idx)
        for i in range(len(res_matrix)):
            res_matrix[i] = self.__getitem__(idx)
            idx = self.next_index(idx)

        return res_matrix

    def to_tensor(self, ind_char):
        """Convert Arraypy to TensorArray. TensorArray uses Arraypy as base. The only
        parametrer is used to set valency of TensorArray. Valency tuple length must
        be equal to shape tuple legth.

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy, list2arraypy
        >>> a = list2arraypy(list(range(9)), (3,3))
        >>> b = a.to_tensor((-1,1))
        >>> type(b)
        <class 'sympy.tensor.arraypy.TensorArray'>

        """
        return TensorArray(self, ind_char)

    def to_list(self):
        """
        Conveting Arraypy to one-dim list

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy
        >>> a = Arraypy ( (2,2) )
        >>> a = Arraypy ( (2,2), 'Py' )
        >>> print (a)
        Py[0, 0] Py[0, 1]
        Py[1, 0] Py[1, 1]

        >>> b = a.to_list()
        >>> print (b)
        [Py[0, 0], Py[0, 1], Py[1, 0], Py[1, 1]]
        """
        res = []
        idx = self._start_index
        for i in range(self.__len__()):
            res.append(self.__getitem__(idx))
            idx = self.next_index(idx)

        return res


class TensorArray(Arraypy):

    """TensorArray based on Arraypy.

    Parameters
    ==========

    self.base - Arraypy base.
    self._ind_char - index character

    +all Arraypy variables
    self._dims - tuple, array dimension. Refers to self.base._dims
    self._rank - Length of self._dims.
    self._sparse - boolean variable. True means that array is sparse.
    self._name - custom _name of the element or default value of the element
    self._start_index - first, starting index. Refers to self.base._start_index
    self._end_index - last, maximum index. Refers to self.base._end_index
    self._loop_size - Counts number of elements in array.
    self._output - dictionary. Dictionary key is an element index. Dictionary
    value - is array value. Refers to self.base._output

    """

    def __init__(self, array, ind_char):
        """
        Class TensorArray constructor.
        Input:
        -array - Arraypy array
        -_ind_char - tuple type, index character (valency). For example (-1,1,1)
        """
        if isinstance(ind_char, int):
            ind_char = (ind_char,)

        if isinstance(ind_char, list):
            ind_char = tuple(ind_char)

        if not isinstance(ind_char, (list, tuple)):
            raise TypeError('Wrong type. ind_char must be list or tuple.')

        for i in ind_char:
            if i != 1 and i != -1:
                raise ValueError('Valency (ind_char) must be 1 or -1')

        if len(ind_char) != array._rank:
            raise ValueError(
                'Length of Valency (ind_char) must be equal to length of Dimension of array')

        if isinstance(array, TensorArray):
            raise TypeError('Wrong type. Fisrt argument must be array')
        elif isinstance(array, Arraypy):
            # overwriting parameters
            self.base = copy(array)
            self._output = self.base._output

            self._name = self.base._name
            self._sparse = self.base._sparse
            self._dims = self.base._dims
            self._rank = self.base._rank
            self._start_index = self.base._start_index
            self._end_index = self.base._end_index
            self._loop_size = self.base._loop_size

        self._ind_char = ind_char

    def __add__(self, other):
        """Overloads operator "+". But unlike Arraypy, it works only with
        tensors with the same index character.

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy, TensorArray, list2tensor
        >>> a = list2tensor ([3 for i in range(9)], (3,3), (1,-1))
        >>> b = list2tensor ([2 for i in range(9)], (3,3), (1,-1))
        >>> c = a + b
        >>> print (c)
        5 5 5
        5 5 5
        5 5 5

        """

        if self._ind_char != other._ind_char:
            raise ValueError('Both tensors must be the same ind_char')

        res_base = self.base + other.base

        res_tensor = TensorArray(res_base, self._ind_char)

        return res_tensor

    def __sub__(self, other):
        """
        Overloads operator "-". But unlike Arraypy, it works only with tensors
        with the same index character.

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy, TensorArray, list2tensor
        >>> a = list2tensor ([3 for i in range(9)], (3,3), (1,-1))
        >>> b = list2tensor ([2 for i in range(9)], (3,3), (1,-1))
        >>> c = a - b
        >>> print (c)
        1 1 1
        1 1 1
        1 1 1
        """
        if self._ind_char != other._ind_char:
            raise ValueError('Both tensors must be the same ind_char')

        res_base = self.base - other.base

        res_tensor = TensorArray(res_base, self._ind_char)

        return res_tensor

    def __eq__(self, other):
        """
        Overloads '=='.
        TensorArray instances can be compared to each other.
        Instances equal if they have same shape, indexes and data.

        Examples
        ========

        >>> from sympy import Arraypy, TensorArray, list2tensor
        >>> a = list2tensor ([i for i in range(9)], (3, 3), (1, -1))
        >>> b = list2tensor ([i for i in range(9)], (3, 3), (1, 1))
        >>> c = list2tensor ([0 for i in range(9)], (3, 3), (1, -1))
        >>> d = list2tensor ([i for i in range(9)], 9, -1)
        >>> e = list2tensor ([i for i in range(9)], (3, 3), (1, -1))
        >>> a == b
        False
        >>> a == c
        False
        >>> a == d
        False
        >>> a == e
        True
        """
        if not isinstance(other, TensorArray):
            raise TypeError('Compared instances must be TensorArray type')
        if (not(self._ind_char == other._ind_char)
                or not(self.base == other.base)):
            return False

        return True

    def __copy__(self):
        """Overload commom python function "copy". Makes right copy of Arraypy
        object.

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy, TensorArray, copy
        >>> a = TensorArray(Arraypy((2,2)), (1,1))
        >>> b = copy(a)
        >>> c = a

        """

        return TensorArray(copy(self.base), copy(self._ind_char))

    @property
    def type_pq(self):
        """Returns tuple, that represents valency of the TensorArray in (P,Q)
        format, where P is upper (contrvarian) index and Q is lower
        (covariant).

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy, TensorArray
        >>> a = Arraypy ((3,3,3,3,3)).to_tensor((1, 1, -1, 1, -1))
        >>> a.type_pq
        (3, 2)

        """
        p = 0
        q = 0
        for i in self._ind_char:
            if i == 1:
                p += 1
            else:
                q += 1
        return (p, q)

    @property
    def ind_char(self):
        """Returns tuple, index caracter.

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy, TensorArray, list2tensor
        >>> a = list2tensor ([3 for i in range(9)], (3,3), (1,-1))
        >>> a.ind_char
        (1, -1)

        """
        return self._ind_char

    def contract(self, idx1, idx2):
        """Method returns new TensorArray instance, contract of current tensor.

        Result tensor rank will be current rank – 2 and valency will be
        (p - 1, q - 1).
        Takes 2 parameters: first and second index number.
        Index numbers counts from “1”.

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy, TensorArray, list2tensor, list2arraypy
        >>> a = list2tensor(list(range(27)), (3,3,3), (1, -1, 1))
        >>> b = a.contract(1,2)
        >>> print (b)
        36 39 42
        >>> b.ind_char
        (1,)
        >>> b.rank
        1
        >>> b.shape
        (3,)

        >>> d = list2arraypy(list(range(9)), (3,3))
        >>> d = d.to_tensor((1,-1))
        >>> print (d)
        0 1 2
        3 4 5
        6 7 8

        >>> e = d.contract(1,2)
        >>> print (e)
        12

        """
        if idx1 > self._rank or idx2 > self._rank or idx1 == idx2:
            raise ValueError('Wrong index')
        if idx1 < 1 or idx2 < 0:
            raise ValueError('Index starts from 1')

        idx1 -= 1
        idx2 -= 1

        if self._ind_char[idx1] == self._ind_char[idx2]:
            raise ValueError('Indexes must have diferent valency (ind_char)')
        for i in self._dims:
            if self._dims[0] != i:
                raise TypeError('Can''t do that in dimension like this')

        # making idx1 greater then idx2
        if idx1 < idx2:
            temp = idx1
            idx1 = idx2
            idx2 = temp

        # creating result tensor.
        # result tensor valency will be (p-1, q-1)
        arg = [(self.start_index[i], self.end_index[i])
               for i in range(self.rank) if i != idx1 and i != idx2]
        if arg == []:
            arg = 1

        new_ind_char = [self.ind_char[i]
                        for i in range(self.rank) if i != idx1 and i != idx2]
        if new_ind_char == []:
            new_ind_char = 1

        result_tensor = TensorArray(Arraypy(arg), new_ind_char)

        for i in result_tensor.index_list:
            temp_index = list(i)
            if (len(result_tensor) == 1):
                temp_index = [self.start_index[idx2], self.start_index[idx1]]
            else:
                temp_index.insert(idx2, self.start_index[idx2])
                temp_index.insert(idx1, self.start_index[idx1])

            for j in range(0, self.shape[idx1]):
                result_tensor[i] += self[tuple(temp_index)]
                temp_index[idx1] += 1
                temp_index[idx2] += 1

        return result_tensor

    def reshape(self, new_shape, ind_char):
        """reshape method are overloaded and now requires 2 arguments.

        -Shape of new tensor base
        -Index character of new tensor.

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy, TensorArray, list2tensor
        >>> a = list2tensor(list(range(6)), (3,2), (1, -1))
        >>> print (a)
        0 1
        2 3
        4 5

        >>> b = a.reshape(6, 1)
        >>> print (b)
        0 1 2 3 4 5
        >>> b.shape
        (6,)
        >>> b.ind_char
        (1,)

        >>> c = a.reshape((2,3), (-1,-1))
        >>> print (c)
        0 1 2
        3 4 5
        >>> c.shape
        (2, 3)
        >>> c.ind_char
        (-1, -1)

        """
        if isinstance(ind_char, tuple):
            if len(ind_char) != len(new_shape):
                raise ValueError(
                    'ind_char tuple length must be equal to new shape length')
            for i in ind_char:
                if i != 1 and i != -1:
                    raise ValueError('!!!ind_char elements must be 1 or -1')
        # reshaping Arraypy and creating tensor with new base
        new_base = self.base.reshape(new_shape)
        new_tensor = TensorArray(new_base, ind_char)

        return new_tensor

    def to_arraypy(self):
        """
        Returns Arraypy - base of the current TensorArray object.

        Examples
        ========

        >>> from sympy.tensor.arraypy import Arraypy, TensorArray, list2tensor
        >>> a = list2tensor (list(range(9)), (3, 3), (1, -1))
        >>> b = a.to_arraypy()
        >>> type(b)
        <class 'sympy.tensor.arraypy.Arraypy'>
        >>> print (b)
        0 1 2
        3 4 5
        6 7 8
        """
        return copy(self.base)

    def to_tensor(self, ind_char):
        """Converting TensorArray to TensorArray is not required, so this method is not
        implemented."""
        raise NotImplementedError()


def matrix2arraypy(matrix):
    """matrix2arraypy converts Matrix instance to Arraypy. Matrix class alredy
    has wide list of usfull methods and functions, which is used in tensor
    package.

    Examples
    ========

    >>> from sympy.tensor.arraypy import Arraypy, TensorArray, matrix2arraypy
    >>> from sympy import Matrix
    >>> a = Matrix(((1,2),(3,4)))
    >>> print (a)
    Matrix([[1, 2], [3, 4]])
    >>> b = matrix2arraypy(a)
    >>> type(b)
    <class 'sympy.tensor.arraypy.Arraypy'>
    >>> print (b)
    1 2
    3 4

    """
    if not isinstance(matrix, Matrix):
        raise TypeError('Input attr must be Matrix type')
    else:
        n = matrix.shape
        massiv = Arraypy(n)

        idx = massiv._start_index
        for i in range(len(matrix)):
            massiv[idx] = matrix[i]
            idx = massiv.next_index(idx)

        return massiv


def matrix2tensor(matrix, ind_char=(-1, -1)):
    """
    Convert Matrix to TensorArray.
    Function take 2 arguments. First is a Matrix. The second is a tuple that
    represents index character. By default it is (-1,-1).

    Examples
    ========

    >>> from sympy.tensor.arraypy import Arraypy, TensorArray, matrix2tensor
    >>> from sympy import Matrix
    >>> a = Matrix(((1,2),(3,4)))
    >>> print (a)
    Matrix([[1, 2], [3, 4]])
    >>> b = matrix2tensor(a, (1,-1))
    >>> type(b)
    <class 'sympy.tensor.arraypy.TensorArray'>
    >>> print (b)
    1 2
    3 4
    """
    if not isinstance(matrix, Matrix):
        raise TypeError('Input attr must be Matrix type')
    else:
        n = matrix.shape
        massiv = TensorArray(Arraypy(n), ind_char)

        idx = massiv._start_index
        for i in range(len(matrix)):
            massiv[idx] = matrix[i]
            idx = massiv.next_index(idx)

        return massiv


def list2arraypy(list_arr, shape=0):
    """Convert list to Arraypy.

    Examples
    ========

    >>> from sympy.tensor.arraypy import Arraypy, list2arraypy
    >>> a = list2arraypy(list(range(3*3)), (3,3))
    >>> print (a)
    0 1 2
    3 4 5
    6 7 8

    """
    if not isinstance(list_arr, list):
        raise TypeError('First attr must be list type')
    # checking shape type
    if shape == 0:
        shape = len(list_arr)
    elif isinstance(shape, (tuple, list)):
        mult = 1
        for i in shape:
            mult *= i
        if mult != len(list_arr):
            raise ValueError(
                'Length of input list must be equal to product of shape elements')
    elif isinstance(shape, int):
        if shape != len(list_arr):
            raise ValueError(
                'Length of input list must be equal to product of shape elements')
    else:
        raise TypeError('Second attr must be tuple, list or int')

    # creating new Arraypy and filling it with list elements
    result = Arraypy(shape)
    idx = result._start_index
    for i in range(len(list_arr)):
        result[idx] = list_arr[i]
        idx = result.next_index(idx)
    return result


def list2tensor(list_arr, shape=0, ind_char=0):
    """Convert list to TensorArray. It takes 3 arguments.

    -a list, which elements will be elements of the tensor base.
    -a tuple, shape of the new tensor (by default it is 0, which will mean that
    result tensor will be vector)
    -a tuple with index character (by default it feels with -1)

    Examples
    ========

    >>> from sympy.tensor.arraypy import Arraypy, TensorArray, list2tensor
    >>> a = list2tensor([i*2 for i in range(9)], (3,3), (-1,1))
    >>> type(a)
    <class 'sympy.tensor.arraypy.TensorArray'>
    >>> print (a)
    0 2 4
    6 8 10
    12 14 16

    """
    if not isinstance(list_arr, list):
        raise TypeError('Fisrt attr must be list type')
    # checking shape type
    if shape == 0:
        shape = len(list_arr)
    elif isinstance(shape, (tuple, list)):
        mult = 1
        for i in shape:
            mult *= i
        if mult != len(list_arr):
            raise ValueError(
                'Length of input list must be equal to product of shape elements')
    elif isinstance(shape, int):
        if shape != len(list_arr):
            raise ValueError(
                'Length of input list must be equal to product of shape elements')
    else:
        raise TypeError('Second attr must be tuple, list or int')

    if ind_char == 0:
        if isinstance(shape, tuple):
            ind_char = tuple([-1 for i in range(len(shape))])
        elif isinstance(shape, int):
            ind_char = -1

    # creating new tensor and filling it with list elements
    result = TensorArray(Arraypy(shape), ind_char)
    idx = result._start_index
    for i in range(len(list_arr)):
        result[idx] = list_arr[i]
        idx = result.next_index(idx)
    return result
