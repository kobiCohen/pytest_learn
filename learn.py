from pytest import fixture
import mock_server
import os

@fixture(scope="function")
def serv():
    global serv
    os.system("sudo su \n sudopass \n")
    mock_server.start_server()
    os.system("rm a.txt")
    os.system("echo aa >> a.txt")
    yield serv
    mock_server.stop_server()


def test_create_user(serv):
    # creating user in  a certain group, create a file for the grp, and delete the file - should succeed
    mock_server.create_user("usrname", "pass", "grp")
    os.system("chgrp grp file.txt")
    os.system("chmod 770 ./a.txt")
    os.system("su - ""username ","pass")
    assert os.system("rm a.txt") == 0


def test_create_user_negative(serv):
    # create a user in a certain grp, create a file that another grp could change and try to delete it - negative
    mock_server.create_user("usrname", "pass", "grp")
    os.system("chgrp grp2 file.txt")
    os.system("chmod 770 ./a.txt")
    os.system("su - ""username ","pass")
    assert os.system("rm a.txt") != 0



def test_create_user_and_change_grp(serv):
    # create a user in a certain grp, create a file that another grp could change, and changing user grp to that grp
    # and try to delete the file, should succeed
    mock_server.create_user("usrname", "pass", "grp")
    mock_server.change_grp("usrname", "grp2")
    os.system("chgrp grp2 file.txt")
    os.system("chmod 770 ./a.txt")
    os.system("su - ""username ","pass")
    assert os.system("rm a.txt") == 0


def test_create_user_and_change_grp_negative(serv):
    # create a user in a certain grp, create a file that this grp could change, and changing user grp  and try to
    # delete the file, should fail
    mock_server.create_user("usrname", "pass", "grp")
    mock_server.change_grp("usrname", "grp2")
    os.system("chgrp grp file.txt")
    os.system("chmod 770 ./a.txt")
    os.system("su - ""username ","pass")
    assert os.system("rm a.txt") != 0

