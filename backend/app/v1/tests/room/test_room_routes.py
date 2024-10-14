import pytest

from app.v1.users.services import user_service


class TestCreatePrivatePublicRoomRoute:
    """
    Test class for create public or private room route
    """

    @pytest.mark.asyncio
    async def test_create_private_room_success(self,
                                               client,
                                               mock_johnson_user_dict,
                                               mock_user_id,
                                               test_get_session,
                                               test_setup):
        """
        Test create private room success.
        """
        mock_johnson_user_dict["id"] = mock_user_id

        _ = await user_service.create(mock_johnson_user_dict, test_get_session)

        response = client.post(
            url="/api/v1/rooms/create",
            json={
                "room_name": "new-room",
                "room_type": "private",
                "messages_deletable": True
            },
            headers={
                "Authorization": f"Bearer fake"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Room Created Successfully"
        assert isinstance(data["data"]["room"], dict)
        assert isinstance(data["data"]["room_members"], list)

    @pytest.mark.asyncio
    async def test_create_private_room_idempotency(self,
                                               client,
                                               mock_johnson_user_dict,
                                               mock_user_id,
                                               test_get_session,
                                               test_setup):
        """
        Test create private room idempotency.
        """
        mock_johnson_user_dict["id"] = mock_user_id

        _ = await user_service.create(mock_johnson_user_dict, test_get_session)

        response = client.post(
            url="/api/v1/rooms/create",
            json={
                "room_name": "new-room",
                "room_type": "private",
                "messages_deletable": True
            },
            headers={
                "Authorization": f"Bearer fake"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Room Created Successfully"
        assert isinstance(data["data"]["room"], dict)
        assert isinstance(data["data"]["room_members"], list)

        response2 = client.post(
            url="/api/v1/rooms/create",
            json={
                "room_name": "new-room",
                "room_type": "private",
                "messages_deletable": True
            },
            headers={
                "Authorization": f"Bearer fake"
            }
        )

        assert response2.status_code == 201
        data = response2.json()
        assert data["message"] == "Room already exists"
        assert isinstance(data["data"]["room"], dict)
        assert isinstance(data["data"]["room_members"], list)

    @pytest.mark.asyncio
    async def test_create_public_room_success(self,
                                               client,
                                               mock_johnson_user_dict,
                                               mock_user_id,
                                               test_get_session,
                                               test_setup):
        """
        Test create public room success.
        """
        mock_johnson_user_dict["id"] = mock_user_id

        _ = await user_service.create(mock_johnson_user_dict, test_get_session)

        response = client.post(
            url="/api/v1/rooms/create",
            json={
                "room_name": "new-room",
                "room_type": "public",
                "messages_deletable": True
            },
            headers={
                "Authorization": f"Bearer fake"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Room Created Successfully"
        assert isinstance(data["data"]["room"], dict)
        assert isinstance(data["data"]["room_members"], list)

    @pytest.mark.asyncio
    async def test_public_room_name_validation_errors(self,
                                               client,
                                               mock_johnson_user_dict,
                                               mock_user_id,
                                               test_get_session,
                                               test_setup):
        """
        Test create public room_name validation_errors.
        """
        mock_johnson_user_dict["id"] = mock_user_id

        _ = await user_service.create(mock_johnson_user_dict, test_get_session)

        response = client.post(
            url="/api/v1/rooms/create",
            json={
                "room_name": "new room",
                "room_type": "public",
                "messages_deletable": True
            },
            headers={
                "Authorization": f"Bearer fake"
            }
        )

        assert response.status_code == 422
        data = response.json()

        assert data["message"] == 'Validation Error.'
        assert data["data"]["msg"] == 'Value error, Only special characters #-_ are allowed in room_name'

    @pytest.mark.asyncio
    async def test_public_room_type_validation_errors(self,
                                               client,
                                               mock_johnson_user_dict,
                                               mock_user_id,
                                               test_get_session,
                                               test_setup):
        """
        Test create public room_type validation_errors.
        """
        mock_johnson_user_dict["id"] = mock_user_id

        _ = await user_service.create(mock_johnson_user_dict, test_get_session)

        response = client.post(
            url="/api/v1/rooms/create",
            json={
                "room_name": "new-room",
                "room_type": "direct",
                "messages_deletable": True
            },
            headers={
                "Authorization": f"Bearer fake"
            }
        )

        assert response.status_code == 422
        data = response.json()

        assert data["message"] == 'Validation Error.'
        assert data["data"]["msg"] == 'Value error, room_type must be either public or private'

    @pytest.mark.asyncio
    async def test_missing_room_type_errors(self,
                                               client,
                                               mock_johnson_user_dict,
                                               mock_user_id,
                                               test_get_session,
                                               test_setup):
        """
        Test missing room_type validation_errors.
        """
        mock_johnson_user_dict["id"] = mock_user_id

        _ = await user_service.create(mock_johnson_user_dict, test_get_session)

        response = client.post(
            url="/api/v1/rooms/create",
            json={
                "room_name": "new-room",
                "messages_deletable": True
            },
            headers={
                "Authorization": f"Bearer fake"
            }
        )

        assert response.status_code == 422
        data = response.json()

        assert data["message"] == 'Validation Error.'
        assert data["data"]["msg"] == 'Value error, room_type must be either public or private'

    @pytest.mark.asyncio
    async def test_missing_room_name_errors(self,
                                               client,
                                               mock_johnson_user_dict,
                                               mock_user_id,
                                               test_get_session,
                                               test_setup):
        """
        Test missing room_name validation_errors.
        """
        mock_johnson_user_dict["id"] = mock_user_id

        _ = await user_service.create(mock_johnson_user_dict, test_get_session)

        response = client.post(
            url="/api/v1/rooms/create",
            json={
                "room_type": "private",
                "room_name": "",
                "messages_deletable": True
            },
            headers={
                "Authorization": f"Bearer fake"
            }
        )

        assert response.status_code == 422
        data = response.json()

        assert data["message"] == 'Validation Error.'
        assert data["data"]["msg"] == 'Value error, room_name cannot bu null'

    @pytest.mark.asyncio
    async def test_missing_messages_deletable_errors(self,
                                               client,
                                               mock_johnson_user_dict,
                                               mock_user_id,
                                               test_get_session,
                                               test_setup):
        """
        Test missing messages_deletable validation_errors.
        """
        mock_johnson_user_dict["id"] = mock_user_id

        _ = await user_service.create(mock_johnson_user_dict, test_get_session)

        response = client.post(
            url="/api/v1/rooms/create",
            json={
                "room_type": "public",
                "room_name": "new-room"
            },
            headers={
                "Authorization": f"Bearer fake"
            }
        )

        assert response.status_code == 422
        data = response.json()

        assert data["message"] == 'Validation Error.'
        assert data["data"]["msg"] == 'Value error, messages_deletable must be either true of false'


class TestCreateDirectMessageRoomRoute:
    """
    Test class for create direct-message room route
    """

    @pytest.mark.asyncio
    async def test_create_direct_message_room_success(self,
                                               client,
                                               mock_johnson_user_dict,
                                               mock_jayson_user_dict,
                                               mock_user_id,
                                               test_get_session,
                                               test_setup):
        """
        Test create direct messsage room success.
        """
        jayson_response = client.post(
            url="/api/v1/auth/register",
            json=mock_jayson_user_dict
        )

        assert jayson_response.status_code == 201
        jayson_id = jayson_response.json()["data"]["user"]["id"]

        mock_johnson_user_dict["id"] = mock_user_id

        johnson_user = await user_service.create(
            mock_johnson_user_dict,
            test_get_session
        )

        response = client.post(
            url="/api/v1/rooms/create/dm",
            json={
                "receiver_id": jayson_id,
            },
            headers={
                "Authorization": "Bearer none"
            }
        )

        assert response.status_code == 201

        data = response.json()

        assert data["status_code"] == 201
        assert data["message"] == "Room Created Successfully"
        assert isinstance(data["data"]["room"], dict)
        assert isinstance(data["data"]["room_members"], list)

    @pytest.mark.asyncio
    async def test_create_direct_message_room_idempotency(self,
                                               client,
                                               mock_johnson_user_dict,
                                               mock_jayson_user_dict,
                                               mock_user_id,
                                               test_get_session,
                                               test_setup):
        """
        Test create direct messsage room idempotency success.
        """
        jayson_response = client.post(
            url="/api/v1/auth/register",
            json=mock_jayson_user_dict
        )

        assert jayson_response.status_code == 201
        jayson_id = jayson_response.json()["data"]["user"]["id"]

        mock_johnson_user_dict["id"] = mock_user_id

        _ = await user_service.create(
            mock_johnson_user_dict,
            test_get_session
        )

        response = client.post(
            url="/api/v1/rooms/create/dm",
            json={
                "receiver_id": jayson_id,
            },
            headers={
                "Authorization": "Bearer none"
            }
        )

        assert response.status_code == 201

        data = response.json()

        assert data["status_code"] == 201
        assert data["message"] == "Room Created Successfully"
        assert isinstance(data["data"]["room"], dict)
        assert isinstance(data["data"]["room_members"], list)

        response2 = client.post(
            url="/api/v1/rooms/create/dm",
            json={
                "receiver_id": jayson_id,
            },
            headers={
                "Authorization": "Bearer none"
            }
        )

        assert response2.status_code == 201

        data = response2.json()

        assert data["status_code"] == 201
        assert data["message"] == "Room already exists"
        assert isinstance(data["data"]["room"], dict)
        assert isinstance(data["data"]["room_members"], list)

    @pytest.mark.asyncio
    async def test_raise_UserNotFoundError(self,
                                               client,
                                               mock_johnson_user_dict,
                                               mock_user_id,
                                               test_get_session,
                                               test_setup):
        """
        Test User not found error..
        """
        mock_johnson_user_dict["id"] = mock_user_id

        johnson_user = await user_service.create(
            mock_johnson_user_dict,
            test_get_session
        )

        response = client.post(
            url="/api/v1/rooms/create/dm",
            json={
                "receiver_id": johnson_user.id,
            },
            headers={
                "Authorization": "Bearer none"
            }
        )

        assert response.status_code == 400

        data = response.json()

        assert data["status_code"] == 400
        assert data["message"] == f"User {johnson_user.id} and User {johnson_user.id} cannot be the same"

    @pytest.mark.asyncio
    async def test_raise_UserNotFoundError2(self,
                                               client,
                                               mock_johnson_user_dict,
                                               mock_user_id,
                                               test_get_session,
                                               test_setup):
        """
        Test User not found error2..
        """
        mock_johnson_user_dict["id"] = mock_user_id

        _ = await user_service.create(
            mock_johnson_user_dict,
            test_get_session
        )

        response = client.post(
            url="/api/v1/rooms/create/dm",
            json={
                "receiver_id": "fake_id",
            },
            headers={
                "Authorization": "Bearer none"
            }
        )

        assert response.status_code == 400

        data = response.json()

        assert data["status_code"] == 400
        assert data["message"] == "User fake_id does not exists"

    @pytest.mark.asyncio
    async def test_create_dm_validation_error(self,
                                               client,
                                               mock_johnson_user_dict,
                                               mock_user_id,
                                               test_get_session,
                                               test_setup):
        """
        Test create dm validation error..
        """
        mock_johnson_user_dict["id"] = mock_user_id

        _ = await user_service.create(
            mock_johnson_user_dict,
            test_get_session
        )

        response = client.post(
            url="/api/v1/rooms/create/dm",
            json={
                "receiver_id": "",
            },
            headers={
                "Authorization": "Bearer none"
            }
        )

        assert response.status_code == 422

        data = response.json()

        assert data["status_code"] == 422
        assert data["message"] == "Validation Error."
        assert data["data"]["msg"] == "Value error, receiver_id cannot be null"
        