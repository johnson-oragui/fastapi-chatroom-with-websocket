import pytest

from app.v1.profile.services import profile_service
from app.v1.users.services import user_service

class TestProfileService:
    """
    Test class for profile service.
    """
    @pytest.mark.asyncio
    async def test_create(self,
                          mock_johnson_user_dict,
                          test_get_session,
                          test_setup):
        """
        Test profile_service.create
        """
        new_user = await user_service.create(mock_johnson_user_dict, test_get_session)
        profile_user = await profile_service.create(
            {"user_id": new_user.id}
            , test_get_session
        )

        assert new_user.id == profile_user.user_id
        assert profile_user.bio == None

    @pytest.mark.asyncio
    async def test_delete_all(self,
                          mock_johnson_user_dict,
                          mock_jayson_user_dict,
                          test_get_session,
                          test_setup):
        """
        Test profile_service.delete_all.
        """
        new_users = await user_service.create_all(
            [
                mock_johnson_user_dict,
                mock_jayson_user_dict,
            ],
            test_get_session
        )
        profile_users = await profile_service.create_all(
            [
                {"user_id": new_users[0].id},
                {"user_id": new_users[1].id}
            ]
            , test_get_session
        )

        assert len(profile_users) == 2

        await profile_service.delete_all(
            where={
                "bio": None
            },
            session=test_get_session
        )

        deleted_profile = await profile_service.fetch_all(
            {},
            session=test_get_session
        )

        assert deleted_profile == []


    @pytest.mark.asyncio
    async def test_fetch(self,
                          mock_johnson_user_dict,
                          test_get_session,
                          test_setup):
        """
        Test profile_service.fetch
        """
        new_user = await user_service.create(mock_johnson_user_dict, test_get_session)
        profile_user = await profile_service.create(
            {"user_id": new_user.id}
            , test_get_session
        )

        profile = await profile_service.fetch({"id": profile_user.id}, test_get_session)

        assert profile.id == profile_user.id
        assert profile_user.user_id == profile.user_id

    @pytest.mark.asyncio
    async def test_fetch_all(self,
                          mock_johnson_user_dict,
                          mock_jayson_user_dict,
                          test_get_session,
                          test_setup):
        """
        Test profile_service.fetch_all.
        """
        new_user = await user_service.create(mock_johnson_user_dict, test_get_session)
        profile_user = await profile_service.create(
            {"user_id": new_user.id}
            , test_get_session
        )

        new_user2 = await user_service.create(mock_jayson_user_dict, test_get_session)
        profile_user2 = await profile_service.create(
            {"user_id": new_user2.id}
            , test_get_session
        )

        profile = await profile_service.fetch_all({}, test_get_session)

        assert profile == [profile_user, profile_user2]

    @pytest.mark.asyncio
    async def test_update(self,
                          mock_johnson_user_dict,
                          test_get_session,
                          test_setup):
        """
        Test profile_service.update.
        """
        new_user = await user_service.create(mock_johnson_user_dict, test_get_session)
        profile_user = await profile_service.create(
            {"user_id": new_user.id}
            , test_get_session
        )

        updated_profile = await profile_service.update(
            [{"id": profile_user.id}, {"bio": "i am king"}],
            test_get_session
        )

        assert profile_user.bio == "i am king"
        assert updated_profile.bio == profile_user.bio

    @pytest.mark.asyncio
    async def test_delete(self,
                          mock_johnson_user_dict,
                          test_get_session,
                          test_setup):
        """
        Test profile_service.delete.
        """
        new_user = await user_service.create(mock_johnson_user_dict, test_get_session)
        profile_user = await profile_service.create(
            {"user_id": new_user.id}
            , test_get_session
        )

        assert profile_user is not None

        await profile_service.delete(
            {"id": profile_user.id},
            test_get_session
        )

        deleted_profile = await profile_service.delete(
            {"user_id": new_user.id},
            test_get_session
        )

        assert deleted_profile is None
