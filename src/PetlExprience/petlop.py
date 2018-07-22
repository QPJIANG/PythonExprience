#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
etl csv
code from petl doc



A table container (also referred to here as a table) is any object which satisfies the following:

1. implements the __iter__ method
2. __iter__ returns a table iterator (see below)
3. all table iterators returned by __iter__ are independent, i.e., consuming items from one iterator will not affect any other iterators

A table iterator is an iterator which satisfies the following:

4. each item returned by the iterator is a sequence (e.g., tuple or list)
5. the first item returned by the iterator is a header row comprising a sequence of header values
6. each subsequent item returned by the iterator is a data row comprising a sequence of data values
7. a header value is typically a string (str) but may be an object of any type as long as it implements __str__ and is pickleable
8. a data value is any pickleable object
So,  a list of lists is a valid table container'

table 需要是一个可迭代对象
"""
import petl as etl
import numpy as np

def saveToCsv():
    """
    write data to csv file
    """
    example_data = """foo,bar,baz
a,1,3.4
b,2,7.4
c,6,2.2
d,9,8.1
"""
    with open('example.csv', 'w') as f:
        f.write(example_data)
    pass


def loadDataFromCsv():
    """
    read csv to table
    :return: table
    """
    _table = etl.fromcsv('example.csv')
    return _table


def convertData():
    """
    1. load data from csv
    2. field op

    3. Functional and object-oriented programming styles
    """
    table = loadDataFromCsv()
    table2 = etl.convert(table, 'foo', 'upper')
    table3 = etl.convert(table2, 'bar', int)
    table4 = etl.convert(table3, 'baz', float)
    table5 = etl.addfield(table4, 'quux', lambda row: row.bar * row.baz)
    print(etl.look(table5))

    tablex = (
        etl.fromcsv('example.csv')
            .convert('foo', 'upper')
            .convert('bar', int)
            .convert('baz', float)
            .addfield('quux', lambda row: row.bar * row.baz)
    )
    print(tablex)
    print(etl.look(tablex))



def wrapData():
    """
     2d array to table
    """
    l = [['foo', 'bar'], ['a', 1], ['b', 2], ['c', 2]]
    table = etl.wrap(l)
    print(table.look())


def customTableView():
    """
        custom table  iterator
    """
    class ArrayView(etl.Table):
        def __init__(self, a):
            # assume that a is a numpy array
            self.a = a

        def __iter__(self):
            # yield the header row
            header = tuple(self.a.dtype.names)
            yield header
            # yield the data rows
            for row in self.a:
                yield tuple(row)
    a = np.array([('apples', 1, 2.5), ('oranges', 3, 4.4), ('pears', 7, 0.1)], dtype='U8, i4,f4')
    t1 = ArrayView(a)
    print(t1)
    # 选择列
    t2 = t1.cut('f0', 'f2').convert('f0', 'upper').addfield('f3', lambda row: row.f2 * 2)
    print(t2)


def captureData():
    """
    >>> table1
    +-------+
    | lines |
    +=======+
    | 'a,1' |
    +-------+
    | 'b,2' |
    +-------+
    | 'c,2' |
    +-------+

    >>> # post-process, e.g., with capture()
    ... table2 = table1.capture('lines', '(.*),(.*)$', ['foo', 'bar'])
    >>> table2
    +-----+-----+
    | foo | bar |
    +=====+=====+
    | 'a' | '1' |
    +-----+-----+
    | 'b' | '2' |
    +-----+-----+
    | 'c' | '2' |
    +-----+-----+
    """
    pass


def dataWriteLoad():
    """
    petl.io.base.fromcolumns(cols, header=None, missing=None)

    petl.io.csv.fromcsv(source=None, encoding=None, errors='strict', header=None, **csvargs)
    petl.io.csv.tocsv(table, source=None, encoding=None, errors='strict', write_header=True, **csvargs)
    ... table1 = [['foo', 'bar'],
    ...           ['a', 1],
    ...           ['b', 2],
    ...           ['c', 2]]
    >>> with open('example.csv', 'w') as f:
    ...     writer = csv.writer(f)   # csv.writer()
    ...     writer.writerows(table1)

    petl.io.csv.appendcsv(table, source=None, encoding=None, errors='strict', write_header=False, **csvargs)
    petl.io.csv.teecsv(table, source=None, encoding=None, errors='strict', write_header=True, **csvargs)

    petl.io.csv.fromtsv(source=None, encoding=None, errors='strict', header=None, **csvargs)
    petl.io.csv.totsv(table, source=None, encoding=None, errors='strict', write_header=True, **csvargs)
    petl.io.csv.appendtsv(table, source=None, encoding=None, errors='strict', write_header=False, **csvargs)
    petl.io.csv.teetsv(table, source=None, encoding=None, errors='strict', write_header=True, **csvargs)

    petl.io.pickle.frompickle(source=None)
    >>> import pickle
    >>> # set up a file to demonstrate with
    ... with open('example.p', 'wb') as f:
    ...     pickle.dump(['foo', 'bar'], f)
    ...     pickle.dump(['a', 1], f)
    ...     pickle.dump(['b', 2], f)
    ...     pickle.dump(['c', 2.5], f)

    petl.io.pickle.topickle(table, source=None, protocol=-1, write_header=True)
    petl.io.pickle.appendpickle(table, source=None, protocol=-1, write_header=False)
    petl.io.pickle.teepickle(table, source=None, protocol=-1, write_header=True)

    -------------------------------------------------------------------------------
    function : from* ,to* append*,tee*

    Python objects: fromcolumns
    Delimited files(csv,tsv): csv.writer()
    Pickle files: pickle.dump
    Text files
    XML files
    HTML files
    JSON files: fromdicts,tojsonarrays
    Databases ( pip install sqlalchemy)
    Excel .xls files ( pip install xlrd xlwt-future, pip install openpyxl)
    Arrays (NumPy) (pip install numpy)
    DataFrames (pandas)  ( pip install pandas)
    HDF5 files (PyTables)
    Bcolz ctables  (pip install bcolz)
    Text indexes (Whoosh)  (pip install whoosh)
    """
    pass


def transformData():
    """
    petl.transform.basics.head(table, n=5)   : top n
    petl.transform.basics.tail(table, n=5)   : tail n
    petl.transform.basics.rowslice(table, *sliceargs):  选取指定行
    petl.transform.basics.cut(table, *args, **kwargs):  选取指定列
    petl.transform.basics.cutout(table, *args, **kwargs):  选取指定列之外的列
    petl.transform.basics.movefield(table, field, index)
    petl.transform.basics.cat(*tables, **kwargs)： 列数不相等的数据补齐，表连接（考虑表头）
    petl.transform.basics.stack(*tables, **kwargs)： 列数不相等的数据补齐，表连接（不考虑表头）
    petl.transform.basics.skipcomments(table, prefix)：  Skip any row where the first value is a string and starts with prefix
    petl.transform.basics.addfield(table, field, value=None, index=None, missing=None)： 添加列
            table2 = etl.addfield(table1, 'baz', 42)
            table2 = etl.addfield(table1, 'baz', lambda rec: rec['bar'] * 2)
    petl.transform.basics.addcolumn(table, field, col, index=None, missing=None) ： 创建新的一列并填入相应的数据
    petl.transform.basics.addrownumbers(table, start=1, step=1, field='row')： 添加序号列
    petl.transform.basics.addfieldusingcontext(table, field, query)： 添加列
                etl.addfieldusingcontext(table1, 'baz', upstream)
                upstream(prv, cur, nxt)：  上一行，当前行，下一行
    petl.transform.basics.annex(*tables, **kwargs)： Join two or more tables by row order.（petl.transform.joins.join()）
    petl.transform.headers.rename(table, *args, **kwargs)： 列重命名
    petl.transform.headers.setheader(table, header)：  替换表头
    petl.transform.headers.extendheader(table, fields) ：  补充缺省列表头
    petl.transform.headers.pushheader(table, header, *args)：  数据表没有表头，设置表头

    petl.transform.headers.prefixheader(table, prefix)：
    petl.transform.headers.suffixheader(table, suffix)：
    petl.transform.headers.sortheader(table, reverse=False, missing=None)
    petl.transform.headers.skip(table, n)  ： 转换为table 前丢弃前n行数据
    petl.transform.conversions.convert(table, *args, **kwargs)：
            将制定列的数据类型转换为指定类型：
                table2 = etl.convert(table1, 'bar', float)
                table4 = etl.convert(table1, 'foo', 'lower')
                table8 = etl.convert(table1, ('foo', 'bar', 'baz'), str)
            对指定列做数据运算
                table3 = etl.convert(table1, 'baz', lambda v: v*2)
                table5 = etl.convert(table1, 'foo', 'replace', 'A', 'AA') # 替换
                table7 = etl.convert(table1, 'foo', {'A': 'Z', 'B': 'Y'}) # 替换
            table9 = etl.convert(table1, {'foo': 'lower',
                                        'bar': float,
                                        'baz': lambda v: v * 2})
            table10 = etl.convert(table1, ['lower', float, lambda v: v*2]) # 操作列为操作index,依次对应
            table11 = etl.convert(table1, 'baz', lambda v: v * 2,
                                where=lambda r: r.foo == 'B') # 符合条件的列进行操作
            table12 = etl.convert(table1, 'baz',
                        lambda v, row: v * float(row.bar),
                        pass_row=True)：  # pass_row 为true,lambda表达式有两个参数
        petl.transform.conversions.convertall(table, *args, **kwargs)
            # Convenience function to convert all fields in the table using a common function or mapping
        petl.transform.conversions.convertnumbers(table, strict=False, **kwargs)
            # 将所有可以转化为数字的的值都转换为数字
        petl.transform.conversions.replace(table, field, a, b, **kwargs)
            # Convenience function to replace all occurrences of a with b under the given field
        petl.transform.conversions.replaceall(table, a, b, **kwargs)
            # Convenience function to replace all instances of a with b under all fields
        petl.transform.conversions.format(table, field, fmt, **kwargs)
            #Convenience function to format all values in the given field using the fmt format string
        petl.transform.conversions.formatall(table, fmt, **kwargs)
        petl.transform.conversions.interpolate(table, field, fmt, **kwargs)
        petl.transform.conversions.interpolateall(table, fmt, **kwargs)
        petl.transform.conversions.update(table, field, value, **kwargs)

        petl.transform.selects.select(table, *args, **kwargs)
             table2 = etl.select(table1,lambda rec: rec.foo == 'a' and rec.baz > 88.1)
             table3 = etl.select(table1, "{foo} == 'a' and {baz} > 88.1")  # {列名}
             table4 = etl.select(table1, 'foo', lambda v: v == 'a')
             # 未使用{}时，指定了列名 lambda 参数为值，未指定列名，lambda参数为行。
        petl.transform.selects.selectop(table, field, value, op, complement=False)： top
        petl.transform.selects.selecteq(table, field, value, complement=False): eq
        petl.transform.selects.selectne(table, field, value, complement=False): not equal
        petl.transform.selects.selectlt(table, field, value, complement=False): less than
        petl.transform.selects.selectle(table, field, value, complement=False): less than or equal
        petl.transform.selects.selectgt(table, field, value, complement=False): greater
        petl.transform.selects.selectge(table, field, value, complement=False): greater than or equal
        petl.transform.selects.selectrangeopen(table, field, minv, maxv, complement=False): between open
        petl.transform.selects.selectrangeopenleft(table, field, minv, maxv, complement=False): between open left
        petl.transform.selects.selectrangeopenright(table, field, minv, maxv, complement=False): between open right
        petl.transform.selects.selectrangeclosed(table, field, minv, maxv, complement=False): between close
        petl.transform.selects.selectcontains(table, field, value, complement=False): contain
        petl.transform.selects.selectin(table, field, value, complement=False): ( field is a member )
        petl.transform.selects.selectnotin(table, field, value, complement=False) : (field is a member )
        petl.transform.selects.selectis(table, field, value, complement=False)
        petl.transform.selects.selectisnot(table, field, value, complement=False)
        petl.transform.selects.selectisinstance(table, field, value, complement=False): field is an instance of the given type
        petl.transform.selects.selecttrue(table, field, complement=False) : field evaluates True
        petl.transform.selects.selectfalse(table, field, complement=False) : field evaluates False.
        petl.transform.selects.selectnone(table, field, complement=False) :  field is None.
        petl.transform.selects.selectnotnone(table, field, complement=False):field is not None.
        petl.transform.selects.selectusingcontext(table, query):Select rows based on data in the current row and/or previous and next
                def query(prv, cur, nxt):
                    return  True/False
                table2 = etl.selectusingcontext(table1, query)
        petl.transform.selects.rowlenselect(table, n, complement=False): Select rows of length n.
        petl.transform.selects.facet(table, key):
            # Return a dictionary mapping field values to tables
        petl.transform.selects.biselect(table, *args, **kwargs):
            # Return two tables, the first containing selected rows, the second containing remaining rows.

        petl.transform.regex.search(table, *args, **kwargs)
            # Perform a regular expression search, returning rows that match a given pattern, either anywhere in the row or within a specific field
             table2 = etl.search(table1, '.g.')
             table3 = etl.search(table1, 'foo', '.g.')

        petl.transform.regex.searchcomplement(table, *args, **kwargs)
            # Perform a regular expression search, returning rows that do not match a given pattern, either anywhere in the row or within a specific field
        petl.transform.regex.sub(table, field, pattern, repl, count=0, flags=0)
        petl.transform.regex.split(table, field, pattern, newfields=None, include_original=False, maxsplit=0, flags=0)
        petl.transform.regex.capture(table, field, pattern, newfields=None, include_original=False, flags=0, fill=None)

    """
    pass
if __name__ == "__main__":
    # saveToCsv()
    # convertData()
    # wrapData()

    # customTableView()
    captureData()
    pass
