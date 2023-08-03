from datahub import data as dt


def test_get_wesim_api(client, mocker, wesim_input_data):
    """Test get_wesim returns a dictionary with appropriate DataFrames."""
    with mocker.patch("datahub.wesim.read_wesim", return_value=wesim_input_data):
        response = client.get("/wesim")

    assert response.json()["data"] == dt.wesim_data
