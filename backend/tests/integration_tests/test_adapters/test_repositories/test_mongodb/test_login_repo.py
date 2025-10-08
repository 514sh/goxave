def test_new_login(login_repository, login):
    login_repository.add(login)
    added_login = login_repository.get(login)

    assert added_login.session_id == login.session_id


def test_login_doesnt_exist(login_repository, login):
    added_login = login_repository.get(login)
    assert added_login is None
