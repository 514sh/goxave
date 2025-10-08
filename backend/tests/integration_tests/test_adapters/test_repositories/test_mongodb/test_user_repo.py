def test_add_new_user(user_repository, user):
    user_repository.add(user)
    added_user = user_repository.get(user)

    assert added_user.email == user.email


def test_user_doesnt_exist(user_repository, user):
    added_user = user_repository.get(user)
    assert added_user is None
