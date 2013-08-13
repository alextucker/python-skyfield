from skyfield.datalib import DownloadFile, is_days_old
from datetime import datetime, timedelta
import pytest
import httpretty
import os

@httpretty.activate
def test_simple_download():
    httpretty.register_uri(httpretty.GET, 'http://foo.com/data.txt',
                           body='FOOBAR')

    DownloadFile(url='http://foo.com/data.txt', filename='data.txt')
    assert os.path.exists('data.txt')
    assert open('data.txt', 'r').read() == 'FOOBAR'
    os.remove('data.txt')

@httpretty.activate
def test_simple_download_days_old_0():
    httpretty.register_uri(httpretty.GET, 'http://foo.com/data.txt',
                           body='FOOBAR')
    write_file('data.txt', 'BAZ')

    DownloadFile(url='http://foo.com/data.txt', filename='data.txt', days_old=0)
    assert open('data.txt', 'r').read() == 'FOOBAR'
    os.remove('data.txt')

def test_is_days_old_true():
    write_file('data.txt', 'BAZ')
    hours_ago = datetime.today()-timedelta(hours=6)
    unix_ago = int(hours_ago.strftime('%s'))
    os.utime('data.txt', (unix_ago, unix_ago))

    assert is_days_old('data.txt', 1) == False

    os.remove('data.txt')

def test_is_days_old_false():
    write_file('data.txt', 'BAZ')
    hours_ago = datetime.today()-timedelta(hours=48)
    unix_ago = int(hours_ago.strftime('%s'))
    os.utime('data.txt', (unix_ago, unix_ago))

    assert is_days_old('data.txt', 1) == True

    os.remove('data.txt')

@pytest.mark.skipif('True')
@httpretty.activate
def test_simple_download_days_old_1():
    httpretty.register_uri(httpretty.GET, 'http://foo.com/data.txt',
                           body='FOOBAR')

    write_file('data.txt', 'BAZ')
    hours_ago = datetime.today()-timedelta(hours=48)
    unix_ago = int(hours_ago.strftime('%s'))
    os.utime('data.txt', (unix_ago, unix_ago))

    DownloadFile(url='http://foo.com/data.txt', filename='data.txt', days_old=1)
    assert open('data.txt', 'r').read() == 'BAZ'
    os.remove('data.txt')

def write_file(filename, data):
    f = open(filename, 'w')
    f.write(data)

