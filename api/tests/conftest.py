# Copyright (C) 2021, Mindee.

# This program is licensed under the Apache License version 2.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0.txt> for full license details.

import pytest
import requests
from httpx import AsyncClient

from app.main import app


@pytest.fixture(scope="session")
def mock_recognition_image(tmpdir_factory):
    url = 'https://user-images.githubusercontent.com/76527547/117133599-c073fa00-ada4-11eb-831b-412de4d28341.jpeg'
    return requests.get(url).content


@pytest.fixture(scope="function")
async def test_app_asyncio():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac  # testing happens here
